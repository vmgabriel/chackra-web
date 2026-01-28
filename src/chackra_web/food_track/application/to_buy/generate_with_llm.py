import pydantic
import json

from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.notifications import base as shared_notifications
from chackra_web.shared.domain.model.llm import base as shared_llm

from chackra_web.shared.domain.model.user import (
    additional_user_id as shared_additional_user_id,
    user_id as shared_user_id
)
from chackra_web.shared.domain.model.food_track import to_buy as shared_to_buy_id, inventory_id as shared_inventory_id
from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.food_track.domain.models import (
    inventory as model_inventory,
    to_buy as model_to_buy,
    repositories as inventory_repositories
)
from chackra_web.user.domain.models import (
    additional_user as domain_additional_user,
    repositories as user_repositories,
)

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies

from chackra_web.user.application.additional_information import get_by_user_id as application_get_by_user_id


SYSTEM_MESSAGE = """
Eres un nutricionista clínico especializado en personas de {birth} años {lifestyle} en {country}, con enfoque en {profession}.
Esta persona es de genero {gender}
Su Actual altura es de {height} cm y pesa {weight} kg.

Tiene las siguientes dificultades medicas:
{medical_conditions}

Tus recomendaciones deben:
- Priorizar alimentos accesibles en supermercados y tiendas de barrio en ciudades de {country}.
- Puedes agregar productos carnicos sin problema (Salmon, Carne, Trucha, etc.).
- Considerar horarios irregulares, alto consumo de café y posible estrés mental.
- Promover saciedad, estabilidad glucémica y salud digestiva.
- Usar unidades métricas comunes en Colombia (gramos, kilogramos, unidades, tazas).
- Evitar suplementos costosos o de difícil acceso.
- La comunicacion es siempre con LIST o JSON dependiendo de el output requerido.
- Evita repetir elementos ya presentes en la alacena.
- No añadas nada antes ni después del JSON.
- No expliques tu razonamiento. Solo devuelve el JSON.
- Los campos en el json deben estar en ingles y las respuestas en español ex. 
    elements: [
        object(
            "name": ...,
            "quantity": ...,
            "description": ...,"
        ),
        ...
    ]
"""


HUMAN_MESSAGE = """
Basado en mi alacena actual, genera una lista de compras optimizada para dos semanas, pensada para un {profession} {lifestyle} en {country}.

Alacena actual:
{inventory_items}.

Esta persona es alergica a, asi que es obligatorio evitar productos con este o relacionados a este:
{allergenic_products}

**Instrucciones específicas:**
1. Analiza si la alacena tiene déficits nutricionales comunes en personas {lifestyle} (fibra, omega-3, magnesio, vitamina D, etc.).
2. Genera una lista plana (sin categorías) de **8 a 12 productos nuevos** que complementen lo existente.
3. Cada ítem debe incluir:
   - Nombre del producto debe estar en el json con el nombre 'name' (priorizando marcas o formatos comunes en Colombia, ej. "panela en bloque", "frijol cargamanto"), mandalo como str.
   - Cantidad suficiente para 2 semanas (especifica en gramos, kg o unidades) debe estar en el json con el nombre 'quantity', mandalo como str.
   - Breve descripción (1 oración) con beneficio clave relacionado con sedentarismo, enfoque mental o metabolismo, debe estar en el json con el nombre 'description', mandalo como str.
4. Prioriza alimentos frescos, integrales y de bajo índice glucémico disponibles en mercados locales o cadenas.
5. No repitas ingredientes ya presentes en la alacena.

Entrega la respuesta en español, con tono profesional pero cercano, sin usar viñetas ni markdown.
"""

NOTIFICATION_MESSAGE = """
chackra lista de compras, te recomienda:
{to_buy_list_items}
"""

class GenerateToBuyInput(pydantic.BaseModel):
     message: str


class GenerateToBuyInputMessage(shared_llm.InputMessage[GenerateToBuyInput]):
    content: GenerateToBuyInput

    def __str__(self) -> str:
        return self.content.message


class GeneratedToBuyItem(pydantic.BaseModel):
    name: str
    quantity: str
    description: str

    def __str__(self) -> str:
        return f"- {self.name}: ({self.quantity}) - {self.description}"


class GeneratedToBuyResponse(pydantic.BaseModel):
    elements: list[GeneratedToBuyItem]

    def __str__(self) -> str:
        message = ""
        for element in self.elements:
            message += str(element) + "\n"
        return message


class GenerateToBuyOutputMessage(shared_llm.OutputResponse[GeneratedToBuyResponse]):
    response: GeneratedToBuyResponse

    def __str__(self) -> str:
        return str(self.response)


class GenerateWithLLMCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    to_buy_items_repository: inventory_repositories.ToBuyItemListRepository[
        model_to_buy.FoodTrackToBuyItem,
        shared_to_buy_id.FoodTrackItemToBuyId,
    ]
    inventory_repository:  inventory_repositories.InventoryRepository[
        model_inventory.InventoryItem,
        shared_inventory_id.InventoryID
    ]
    additional_user_repository: user_repositories.AdditionalUserRepository[
        domain_additional_user.UserAdditionalInformation,
        shared_additional_user_id.AdditionalUserId,
    ]
    configuration: shared_configuration.Configuration
    notification: shared_notifications.NotificationPort
    llm_adapter: shared_llm.GenericLLMPort[GenerateToBuyInputMessage, GenerateToBuyOutputMessage]

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.dependencies = dependencies
        self.uow = dependencies.uow
        self.logger = dependencies.logger
        self.to_buy_items_repository = dependencies.repository_store.build(
            inventory_repositories.ToBuyItemListRepository[
                model_to_buy.FoodTrackToBuyItem,
                shared_to_buy_id.FoodTrackItemToBuyId,
            ]
        )
        self.inventory_repository = dependencies.repository_store.build(
            inventory_repositories.InventoryRepository[
                model_inventory.InventoryItem,
                shared_inventory_id.InventoryID
            ]
        )
        self.additional_user_repository = dependencies.repository_store.build(
            user_repositories.AdditionalUserRepository[
                domain_additional_user.UserAdditionalInformation,
                shared_additional_user_id.AdditionalUserId,
            ]
        )
        self.notification = dependencies.notification_adapter
        self.llm_adapter = dependencies.llm_adapter
        self.configuration = dependencies.configuration
        self.paginator_builder = dependencies.paginator_builder
        self.to_specification_builder = dependencies.to_specification_builder

    def execute(self, user_id: shared_user_id.UserId) -> None:
        if not user_id:
            self.logger.warning("User ID not found")
            return

        current_specification = self.to_specification_builder.to_specification(key="is_sold_out__ne", value=True)

        pagination = self.paginator_builder.get_pagination()(
            page=1,
            page_size=1000,
            filters=current_specification
        )
        list_content = self.inventory_repository.matching(pagination)
        names_products = [getattr(product, "name", "") for product in list_content.entities]

        self.logger.info(f"Names Products - {names_products}")

        current_additional_information = application_get_by_user_id.AdditionalInformationGetByUserByIdCommand(
            dependencies=self.dependencies
        ).execute(
            user_id=user_id,
        )
        if not current_additional_information:
            self.logger.warning("Additional Information not found")
            return

        system_prompt = GenerateToBuyInputMessage(
            role=shared_llm.MessageRole.SYSTEM,
            content=GenerateToBuyInput(
                message=SYSTEM_MESSAGE.format(
                    birth=str(current_additional_information.birth_year()),
                    lifestyle=str(current_additional_information.lifestyle),
                    country=str(current_additional_information.country),
                    profession=str(current_additional_information.profession),
                    gender=str(current_additional_information.genre),
                    height=str(current_additional_information.height),
                    weight=str(current_additional_information.weight),
                    medical_conditions=current_additional_information.health_difficulties,
                )
            ),
        )
        human_prompt = GenerateToBuyInputMessage(
            role=shared_llm.MessageRole.USER,
            content=GenerateToBuyInput(
                message=HUMAN_MESSAGE.format(
                    profession=str(current_additional_information.profession),
                    lifestyle=str(current_additional_information.lifestyle),
                    country=str(current_additional_information.country),
                    inventory_items=",".join(names_products),
                    allergenic_products=str(current_additional_information.allergenic_products),
                )
            ),
        )
        output_response = self.llm_adapter.invoke(
            messages=[system_prompt, human_prompt],
            response_model=GeneratedToBuyResponse,
        )

        if output_response.response and not output_response.errors:
            message = NOTIFICATION_MESSAGE.format(to_buy_list_items=str(output_response.response))
            self.notification.send_message(
                recipient_id=self.configuration.current_channel_id,
                message=message,
            )

        self.logger.info(f"Output Response - {json.dumps(output_response.model_dump(), indent=2)}")

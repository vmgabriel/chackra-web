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
    user as domain_user,
    additional_user as domain_additional_user,
    repositories as user_repositories,
)

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies

from chackra_web.user.application import get_by_id as application_get_by_id
from chackra_web.user.application.additional_information import get_by_user_id as application_get_by_user_id


SYSTEM_MESSAGE = """
Eres un nutricionista clínico especializado personas en {country}, con enfoque de ayuda de mantener el equilibrio de salud y mantener energia.

Tus respuestas deben cumplir estrictamente lo siguiente:
- Responde **EXCLUSIVAMENTE** con un objeto JSON válido.
- **No añadas** texto antes, después ni dentro del JSON (ni explicaciones, ni saludos, ni markdown).>
- El JSON debe contener un único campo: `"meals"`, que es una lista ({foods}).
- Cada comida debe incluir:
  - `"name"`: tipo de comida, ej: "Desayuno".
  - `"calories"`: número entero estimado de calorías. **Total diario entre 1,800 y 2,000 kcal**.
  - `"description"`: instrucciones claras de preparación (1–2 oraciones), usando solo ingredientes de la alacena. **Sigue estas reglas estrictas**:
    • No combines legumbres secas sin cocer (frijol, garbanzo, arveja seca) — solo usa versiones cocidas.
    • En la cena, evita carbohidratos como arroz, quinoa, papa o plátano; prioriza proteína + verduras.
    • Usa cantidades realistas: ej. "1/2 aguacate", "2 huevos", "100 g de pollo", "1 cda aceite".
  - `"ingredients"`: lista de ingredientes usados , esto es un objeto.
        - `"name"`: nombre del ingrediente en minuscula
        - `"quantity"`: la medida que se requiera ej: (2 unidades, 1/2 unidad, 100g, 100ml)

ejemplo:
object(
    `"meals"`: [
        object(
            `"name"`: `"Desayuno"`,
            `"calories"`: 1800,
            `"description"`: `"Preparo de desayuno con arroz y pollo"`,
            `"ingredients"`: [
                object(`"name"`: `"arroz"`, `"quantity"`: `"1/2 unidad"`),
            ]
        )
    ]
)

Prioriza:
- Comidas prácticas (máx. 30 min de preparación).
- Saciedad mediante proteína y fibra.
- Estabilidad glucémica: cero azúcar añadido.
- Ingredientes accesibles en {country}.
- Preparaciones: {oven}, sartén, olla, licuadora o ensamblaje frío.

¡Recuerda! Solo JSON. Nada más.
"""

HUMAN_MESSAGE = """
Genera un plan de comidas para un día completo ({foods}) basado **exclusivamente** en los siguientes datos:

**Perfil:**
- Genero {genre}, {year_old} años, {lenght} cm, {weight} kg.
- Objetivo: perder peso de forma sostenible y aumentar energía diaria.
- Estilo de vida: {lifestyle}
- Productos alergicos:
    {allergenic_products}
    
- Dificultades de salud:
    {difficulties}

**Alacena disponible (usa SOLO estos ingredientes):**
{ingredients}

**Requisitos por comida:**
1. Usa solo ingredientes de la alacena.
2. Indica calorías estimadas (entero).
3. Da instrucciones de preparación sencillas.
4. Sé específico con cantidades (ej. "1 taza de arroz", "2 unidades de huevos", "30 gr de aguacate", "80 ml de leche de almendras").
5. Asegura equilibrio nutricional (proteína, fibra, grasas saludables).
"""


NOTIFICATION_MESSAGE = """
Menu Diario segun tu Nutricionista - ({full_name}) 
{recommendations}
"""


RECOMMENDATION_ITEM_STR = """
{name} ({calories} cal)
{description}
Ingredientes: 
{ingredients}
"""


RECOMMENDATION_INGREDIENT_ITEM_STR = "  - {name} ({quantity})"


class RecommendationInput(pydantic.BaseModel):
    message: str


class RecommendationMessage(shared_llm.InputMessage[RecommendationInput]):
    content: RecommendationInput

    def __str__(self) -> str:
        return self.content.message


class RecommendationIngredientItem(pydantic.BaseModel):
    name: str
    quantity: str

    def __str__(self) -> str:
        return RECOMMENDATION_INGREDIENT_ITEM_STR.format(
            name=self.name,
            quantity=self.quantity
        )


class RecommendationItem(pydantic.BaseModel):
    name: str
    calories: int
    description: str
    ingredients: list[RecommendationIngredientItem] = pydantic.Field(default_factory=list)

    def __str__(self) -> str:
        return RECOMMENDATION_ITEM_STR.format(
            name=self.name,
            description=self.description,
            calories=self.calories,
            ingredients="\n".join(str(ingredient) for ingredient in self.ingredients)
        )


class RecommendationResponse(pydantic.BaseModel):
    meals: list[RecommendationItem]

    def __str__(self) -> str:
        message = ""
        for element in self.meals:
            message += str(element) + "\n"
        return message


class RecommendationMessageResponse(shared_llm.OutputResponse[RecommendationResponse]):
    response: RecommendationResponse

    def __str__(self) -> str:
        return str(self.response)


class RecommendationMenuLLMCommand:
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
    user_repository: user_repositories.UserBaseRepository[
        domain_user.User,
        shared_user_id.UserId,
    ]
    configuration: shared_configuration.Configuration
    notification: shared_notifications.NotificationPort
    llm_adapter: shared_llm.GenericLLMPort[RecommendationMessage, RecommendationMessageResponse]

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
        self.user_repository = dependencies.repository_store.build(
            user_repositories.UserBaseRepository[
                domain_user.User,
                shared_user_id.UserId,
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

        current_user = application_get_by_id.GetByIdUserCommand(self.dependencies).execute(
            get_by_id_user_dto=application_get_by_id.GetByIDUserDTO(user_id=user_id.value)
        )
        if not current_user:
            self.logger.warning("User not found")
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

        system_prompt = RecommendationMessage(
            role=shared_llm.MessageRole.SYSTEM,
            content=RecommendationInput(
                message=SYSTEM_MESSAGE.format(
                    country=str(current_additional_information.country),
                    oven="Tengo Horno" if current_additional_information.with_oven else "No tengo Horno",
                    foods=",".join(current_additional_information.foods),
                )
            ),
        )
        human_prompt = RecommendationMessage(
            role=shared_llm.MessageRole.USER,
            content=RecommendationInput(
                message=HUMAN_MESSAGE.format(
                    foods=",".join(current_additional_information.foods),
                    country=str(current_additional_information.country),
                    genre=str(current_additional_information.genre),
                    year_old=str(current_additional_information.birth_year()),
                    lifestyle=str(current_additional_information.lifestyle),
                    allergenic_products=str(current_additional_information.allergenic_products),
                    difficulties=str(current_additional_information.health_difficulties),
                    ingredients=",".join(names_products),
                    lenght=str(current_additional_information.height),
                    weight=str(current_additional_information.weight),
                )
            ),
        )
        output_response = self.llm_adapter.invoke(
            messages=[system_prompt, human_prompt],
            response_model=RecommendationResponse,
        )

        if output_response.response and not output_response.errors:
            message = NOTIFICATION_MESSAGE.format(
                full_name=current_user.full_name,
                recommendations=str(output_response.response),
            )
            self.notification.send_message(
                recipient_id=self.configuration.current_channel_id,
                message=message,
            )

        self.logger.info(f"Output Response - {json.dumps(output_response.model_dump(), indent=2)}")

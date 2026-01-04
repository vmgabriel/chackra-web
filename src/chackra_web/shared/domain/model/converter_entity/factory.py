import dataclasses

from chackra_web.shared.domain.model.converter_entity import converter as converter_entity


@dataclasses.dataclass
class ConverterHandler:
    converter: converter_entity.AbstractConverter
    name: str


class ConverterFactory:
    converters: dict[str, converter_entity.AbstractConverter]

    def __init__(self) -> None:
        self.converters = {}

    def inject(self, name: str, converter: converter_entity.AbstractConverter) -> None:
        if name in self.converters:
            raise ValueError(f"Converter {name} already registered")
        self.converters[name] = converter

    def build(self, name: str) -> converter_entity.AbstractConverter:
        if name not in self.converters:
            raise ValueError(f"Converter {name} not registered")
        return self.converters[name]


CURRENT_CONVERTER_FACTORY = ConverterFactory()

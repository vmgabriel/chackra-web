import pydantic

from chackra_web.shared.domain.model.converter_entity import factory as converter_factory


def to_html(entity: pydantic.BaseModel, field_name: str, converter: str = "default"):
    if isinstance(entity, dict):
        ...
    elif getattr(entity, field_name) is None:
        return ""
    try:
        current_converter = converter_factory.CURRENT_CONVERTER_FACTORY.build(converter)
        value = None
        if isinstance(entity, dict):
            value = entity.get(field_name)
        else:
            value = getattr(entity, field_name)
        return current_converter.render_field(field_name=field_name, value=value)
    except ValueError:
        print("invalid converter")
        return ""

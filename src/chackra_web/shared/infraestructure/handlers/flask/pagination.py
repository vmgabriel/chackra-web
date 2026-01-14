from flask import url_for
import pydantic


def dynamic_url(
        endpoint_name,
        entity: pydantic.BaseModel | dict[str, str],
        attributes: dict[str, str] | None = None,
        **kwargs
):
    """
    Permite usar url_for con un endpoint pasado como string.
    """
    default_attributes = {"id": "id"} if isinstance(entity, pydantic.BaseModel) else {}
    attributes = attributes or default_attributes
    try:
        values = {}
        for attribute_name, attributes_path in attributes.items():
            if isinstance(entity, pydantic.BaseModel):
                values[attribute_name] = str(getattr(entity, attributes_path, ""))
            if isinstance(entity, dict):
                values[attribute_name] = entity.get(attribute_name, "")
        values.update(kwargs)
        return url_for(endpoint_name, **values)
    except Exception:
        return "#"
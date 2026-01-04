from flask import url_for


def dynamic_url(endpoint_name, **kwargs):
    """
    Permite usar url_for con un endpoint pasado como string.
    """
    try:
        return url_for(endpoint_name, **kwargs)
    except Exception:
        return "#"
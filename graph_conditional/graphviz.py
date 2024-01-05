"""Tools related to graphviz."""


def attr_string(attrs: dict) -> str:
    """Convert an attribute dictionary to the respective dot-file attribute string."""
    return ';'.join(
        '{}={}'.format(attr, attr_value) for attr, attr_value in attrs.items()
    )



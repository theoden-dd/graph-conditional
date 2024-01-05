"""Tools related to graphviz."""


def attr_string(attr_dict: dict) -> str:
    """Convert an attribute dictionary to the respective dot-file attribute string."""
    return ';'.join(
        '{}={}'.format(attr, attr_value) for attr, attr_value in attr_dict.items()
    )



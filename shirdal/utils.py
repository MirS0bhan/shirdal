from typing import Union, Callable, List


def get_methods(obj) -> List[str]:
    """
    Retrieve all methods of an object excluding built-in special methods.

    Args:
    obj: The object whose methods are to be listed.

    Returns:
    list: A list of method names as strings.
    """
    # Get all attributes of the object
    attributes = dir(obj)

    # Filter out callable attributes (methods) and special methods
    return [
        attr for attr in attributes
        if callable(getattr(obj, attr)) and not attr.startswith('__')
    ]


def get_name(item: Union[object, Callable]) -> str:
    match item.__class__.__name__:
        case 'type' | 'function':
            return item.__name__
        case _:
            return item.__class__.__name__

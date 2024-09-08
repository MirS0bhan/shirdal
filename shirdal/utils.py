from typing import Union, Callable, List, get_type_hints


def get_methods(obj) -> List[Callable]:
    """
    Retrieve all methods of an object excluding built-in special methods.

    Args:
    obj: The object whose methods are to be listed.

    Returns:
    list: A list of method.
    """
    # Get all attributes of the object
    attributes = dir(obj)

    # Filter out callable attributes (methods) and special methods
    return [
        getattr(obj, attr) for attr in attributes
        if callable(getattr(obj, attr)) and not attr.startswith('__')
    ]


def get_name(item: Union[object, Callable]) -> str:
    match item.__class__.__name__:
        case 'type' | 'function':
            return item.__name__
        case _:
            return item.__class__.__name__


def get_type_list(func: Callable):
    return list(get_type_hints(func).values())

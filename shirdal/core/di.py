from typing import  TypeVar, Callable, Any, Union

from .container import Container
from shirdal.utils import get_name

T = TypeVar('T', bound=Callable[..., Any])


class Scope(Container):
    pass


class DependencyInjection:
    def __init__(self) -> None:
        self.scope = Scope()

    def inject(self, func: T) -> T:
        """
        Decorator to automatically resolve dependencies for a function.
        """
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = get_name(func)
            if func_name in self.scope:
                return self.scope.resolve(func_name)(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper

    def depend(self, dependency: Union[object, Callable[..., Any]]) -> None:
        """
        Register a dependency in the current scope.
        """
        self.scope.register(dependency)

    def depenject(self, func: T) -> Callable[..., Any]:
        """
        Inject dependencies and then execute the function.
        """
        @self.inject
        def wrapped_func(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)
        return wrapped_func

    def resolve(self, name: str) -> Any:
        """
        Resolve a dependency by name.
        """
        return self.scope.resolve(name)
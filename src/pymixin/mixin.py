from typing import Any, Callable
from functools import wraps
import registry


def mixin(mixin_cls: str) -> Callable[..., Any]:
    def decorator(cls):
        print(mixin_cls)
        registry.MIXIN_REGISTRY.update({mixin_cls: cls.__name__})
        cls.__is_mixin_class__ = True
        cls.__mixin_defined_on__ = cls
        return cls

    return decorator


def inject(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def decorator(self, *args, **kwargs):
        if not self:
            raise RuntimeError(f"{func.__name__} is not an instance method")

        cls = self.__class__

        if getattr(cls, "__is_mixin_class__", False) and getattr(cls, "__mixin_defined_on__", None) is cls:
            print(cls.__name__, func.__name__)
        else:
            raise Exception(f"MixinApplyError: {cls.__name__}.{func.__name__} is not declared on a @mixin class")
        return func(self, *args, **kwargs)

    return decorator


if __name__ == "__main__":
    @mixin(mixin_cls="TestClass")
    class TestMixin:
        @inject
        def test_func(self):
            pass


    class TC2(TestMixin):
        @inject
        def test_func(self):
            pass


    print(registry.MIXIN_REGISTRY)
    tc = TestMixin()
    # tc2 = TC2()
    tc.test_func()
    # tc2.test_func()

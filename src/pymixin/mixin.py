import ast
import inspect
import textwrap
from typing import Any, Callable

import registry


def mixin(target, priority=0, condition=None) -> Callable[..., Any]:
    def decorator(_cls):
        def __init_subclass__(_cls, **kwargs):
            raise TypeError(f"Mixin class {_cls.__name__} cannot be subclassed")

        def __new__(_cls, *args, **kwargs):
            raise TypeError(f"Mixin class {_cls.__name__} cannot be instantiated")

        _cls.__init_subclass__ = classmethod(__init_subclass__)
        _cls.__new__ = classmethod(__new__)

        module, class_name = target.rsplit('.', 1)
        for name, func in _cls.__dict__.items():
            if hasattr(func, "_mixin_injection"):
                operation = func._mixin_injection
                operation["method"] = operation.get("method", name)
                operation["priority"] = priority
                operation["condition"] = condition
                registry.register_mixin(module, class_name, operation)
        return _cls

    return decorator


def inject(method, at="HEAD", priority=0, condition=None) -> Callable[..., Any]:
    def wrapper(_func):
        source = inspect.getsource(_func)
        dedent = textwrap.dedent(source)
        tree = ast.parse(dedent)
        code_content = ""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                code_content = "\n".join(ast.unparse(stmt) for stmt in node.body)
                break
        print(code_content)
        operation = {"type": "inject", "method": method, "at": at, "code": code_content, "priority": priority,
                  "condition": condition}
        _func._mixin_injection = recode
        return _func

    return wrapper


if __name__ == "__main__":
    @mixin(target="test.TestClass")
    class TestMixinClass:
        @inject(method="TestMethod", at="TestAt", condition="TestCondition")
        def test_func(self):
            test_str = "TEST"

            def logic():
                print(test_str)

            logic()


    print(registry.MIXIN_REGISTRY)
    print(TestMixinClass.test_func._mixin_injection)

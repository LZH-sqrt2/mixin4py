import ast
import importlib.abc
import sys

_AUTO_APPLY_ENABLED = True
_HOOK_INSTALLED = False


class InjectionTransformer(ast.NodeTransformer):
    def __init__(self, class_name, records, global_namespace):
        self.class_name = class_name
        self.records = records
        self.global_namespace = global_namespace
        self.current_class = None


class MixinHook:
    def __init__(self):
        self.mixin_loader = self.MixinLoader()
        self.mixin_finder = self.MixinFinder()

    class MixinLoader(importlib.abc.Loader):
        def __init__(self):
            pass
            # self.namespace = namespace
            # self._origin_loader = namespace.loader

        def exec_module(self):
            pass

    class MixinFinder(importlib.abc.Loader):
        def __init__(self):
            pass


def disable_auto_apply():
    global _AUTO_APPLY_ENABLED
    _AUTO_APPLY_ENABLED = False


def apply_mixins():
    frame = sys._getframe()
    global_namespace = frame.f_globals


if __name__ == "__main__":
    print(sys._getframe().f_globals)

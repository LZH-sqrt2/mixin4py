import ast
import importlib.abc
import sys

_AUTO_APPLY_ENABLED = True
_HOOK_INSTALLED = False


class InjectionTransformer(ast.NodeTransformer):
    def __init__(self, class_name, operations, global_namespace):
        self.class_name = class_name
        self.operations = operations
        self.global_namespace = global_namespace
        self.current_class = None

    def visit_ClassDef(self, node):
        if node.name == self.class_name:
            self.current_class = node.name
            self._apply_class_level_modifications(node)
            self.generic_visit(node)
            self.current_class = None
        return node

    def visit_FunctionDef(self, node):
        if self.current_class == self.class_name:
            for opt in self.operations:
                if opt.get("method") == node.name:
                    self._apply_function_modification(node, opt)
        self.generic_visit(node)
        return node

    def _apply_class_level_modifications(self, node):
        pass

    def _apply_function_modification(self, node, operation):
        pass

"""
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
"""

def disable_auto_apply():
    global _AUTO_APPLY_ENABLED
    _AUTO_APPLY_ENABLED = False


def apply_mixins():
    frame = sys._getframe()
    global_namespace = frame.f_globals


if __name__ == "__main__":
    print(sys._getframe().f_globals)

import ast
import sys

_APPLIED = False
_AUTO_APPLY_ENABLED = True


class InjectionTransformer(ast.NodeTransformer):
    def __init__(self, class_name, records, global_namespace):
        self.class_name = class_name
        self.records = records
        self.global_namespace = global_namespace
        self.current_class = None


def disable_auto_apply():
    global _AUTO_APPLY_ENABLED
    _AUTO_APPLY_ENABLED = False


def apply_mixins():
    global _APPLIED
    if _APPLIED:
        return
    _APPLIED = True

    frame = sys._getframe()
    global_namespace = frame.f_globals


if __name__ == "__main__":
    print(sys._getframe().f_globals)

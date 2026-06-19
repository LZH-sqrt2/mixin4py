from typing import Optional, List, Dict, Tuple


class MixinRegistry:
    def __init__(self):
        self.__data: Dict[Tuple[str, str], List[dict]] = {}
        self.__id_counter = 0

    def add(self, module: str, class_name: str, entry: dict) -> None:
        key = (module, class_name)
        if key not in self.__data:
            self.__data[key] = []
        entry["id"] = self.__id_counter
        self.__id_counter += 1
        self.__data[key].append(entry)

    def get(self, module: str, class_name: str, default=None) -> Optional[List[dict]]:
        return self.__data.get((module, class_name), default)

    def get_all(self) -> Dict[Tuple[str, str], List[dict]]:
        return {k: v.copy() for k, v in self.__data.items()}

    def __getitem__(self, key: Tuple[str, str]) -> List[dict]:
        return self.__data.get(key, [])

    def __setitem__(self, key: Tuple[str, str], value: List[dict]):
        raise AttributeError("Registry does not allow direct assignment")


_MIXIN_REGISTRY = MixinRegistry()


def register_mixin(module, class_name, entry):
    _MIXIN_REGISTRY.add(module, class_name, entry)


def get_mixins(module, class_name):
    return _MIXIN_REGISTRY.get(module, class_name)


def get_mixin():
    return _MIXIN_REGISTRY.get_all()

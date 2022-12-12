from typing import Any


def does_path_exist_in_query(path: str, info: Any) -> bool:
    def does_path_exist_in_selection(_path: str, selection_set: Any) -> bool:
        if "." not in _path:
            return _path in (field.name.value for field in selection_set.selections)
        left, right = _path.split(".", 1)
        for field in selection_set.selections:
            if field.name.value == left:
                return does_path_exist_in_selection(right, field.selection_set)
        return False

    return does_path_exist_in_selection(path, info.field_asts[0].selection_set)

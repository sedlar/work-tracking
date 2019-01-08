def get_enum_length(enum) -> int:
    return max([len(item.value) for item in enum])

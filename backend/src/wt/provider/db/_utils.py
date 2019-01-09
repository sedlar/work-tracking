from sqlalchemy.dialects.postgresql import insert


def get_enum_length(enum) -> int:
    return max([len(item.value) for item in enum])


def insert_or_update(table, insert_data, update_data, index_elements):
    query = insert(table).values(*[insert_data])
    return query.on_conflict_do_update(
        index_elements=index_elements,
        set_=update_data
    )

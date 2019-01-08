def remove_nones(response: dict) -> dict:
    final_response = {}
    for key, value in response.items():
        if isinstance(value, dict):
            final_response[key] = remove_nones(value)
        elif value is not None:
            final_response[key] = value
    return final_response

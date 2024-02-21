import json

def check_field(json_str, field):
    try:
        data = json.loads(json_str)
        if field in data:
            return True
        else:
            return False
    except json.JSONDecodeError:
        return False


def check_node_not_none(dictionary, node):
    if isinstance(dictionary, dict):
        if node in dictionary:
            if dictionary[node] is not None:
                return True
            else:
                return False
        else:
            for key in dictionary:
                if check_node_not_none(dictionary[key], node):
                    return True
    return False

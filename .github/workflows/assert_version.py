import json
import re
with open('schema.json', 'r') as f:
    schema = json.load(f)
pattern = r'v\d+.\d+.\d+'
homepage = schema['homepage']
version = schema['version']


def check(obj, parents=''):
    """
    This functions recursively parses all fields in the schema looking for
    version names that would not be the same as the one mentionned
    in the 'version' field
    """
    errors = []
    # if field is a string, we check for a potential version
    if isinstance(obj, str):
        if homepage in obj:
            tmp = re.search(pattern, obj)
            if tmp and tmp[0] != version:
                errors += [(parents, tmp[0])]
    # if field is a list, we check every item
    elif isinstance(obj, list):
        for idx, k in enumerate(obj):
            errors += check(k, parents=parents + f'[{str(idx)}]')
    # if field is a dict, we check every value
    elif isinstance(obj, dict):
        for k in obj:
            errors += check(
                obj[k], parents=parents + '.' + k
                if parents else k
            )
    return errors


errors = check(schema)
if errors:
    message = (
        "Errors are mismatched within the schema, "
        f"expected version {version} but:"
    )
    for e in errors:
        message += f'\n- {e[0]} has version {e[1]}'
    raise Exception(message)

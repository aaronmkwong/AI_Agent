# render.py

import json


def format_json_output(expression: str, result: float, indent: int = 2) -> str:
    # if result is a float but has no fractional part, store it as int for cleaner JSON
    if isinstance(result, float) and result.is_integer():
        result_to_dump = int(result)
    else:
        # otherwise keep the original (could be float or other numeric)
        result_to_dump = result

    # build a simple JSON-serializable dict
    output_data = {
        "expression": expression,
        "result": result_to_dump,
    }
    # pretty-print JSON with configurable indentation
    return json.dumps(output_data, indent=indent)

from typing import TypedDict, Dict, Any

def typeof(initial_data: Dict[str, Any]):
    return TypedDict('DynamicData', {k: type(v) for k, v in initial_data.items()})

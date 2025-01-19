import json
import os
import numpy as np

defaultCanvas = {"high": [], "medium": []}


def dict_to_array(data: list[dict[str, int]]) -> list[list[int, int]]:
    # damn =  [[point["x"], point["y"]] for point in data]
    array = []
    for point in data:
        if "x" in point and "y" in point:
            if point["x"] is not None and point["y"] is not None:
                array.append([point["x"], point["y"]])
    return array


def load_canvas():
    print("> Loading canvas file")
    if os.path.exists("canvas.json"):
        with open("canvas.json", "r") as file:
            canvas = json.load(file)  # type: dict[str, list[dict[str, int]]]

            requiredKeys = defaultCanvas.keys()

            data = {}  # type: dict[str, np.ndarray]
            for key in requiredKeys:
                data[key] = np.array(
                    dict_to_array(canvas[key]),
                    # if (key in canvas)
                    # else defaultCanvas[key],
                    dtype=np.int32,
                )

            return data
    else:
        print("> Canvas file not found")
        data = {}  # type: dict[str, np.ndarray]
        for key in defaultCanvas:
            data[key] = np.array([defaultCanvas[key]], dtype=np.int32)

        return data


if __name__ == "__main__":
    canvasData = load_canvas()
    print(canvasData)

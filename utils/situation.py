from utils.storage import SaveToBucket
from visual.image import GetBase64
from model.vector import GetNow, SaveSituation
from model.vision import VisionModel


def RunSaveSituation(frame, label):
    time = GetNow()
    base64, bytes, _ = GetBase64(frame)

    text = VisionModel(base64)
    print(">", text)

    id = SaveSituation(text, time, {"label": label})

    SaveToBucket(bytes, id)

from model.vector import GetNow, ParseIds, SaveSituation, SearchSituation
from model.vision import VisionModel
from utils.database import SaveSituationDB, SearchSituationDB
from utils.storage import CreatePublicURLs, GetURL, SaveToBucket
from visual.image import GetBase64


def RunSaveSituation(frame, label):
    time = GetNow()
    base64, bytes, _ = GetBase64(frame)

    text = VisionModel(base64)
    print(">", text)

    id = SaveSituation(text, time, {"label": label})

    SaveToBucket(bytes, id)

    print(
        SaveSituationDB(
            id.__str__(), text, GetURL(id), time, {"label": label} if label else None
        )
    )


def RunSearchSituation(q: str):
    ids = SearchSituation(q)

    if len(ids) == 0:
        return None

    (ids, idKeys) = ParseIds(ids)

    print(idKeys)

    data = SearchSituationDB(idKeys)

    print(data)

    if len(data) == 0:
        return None

    return CreatePublicURLs(idKeys)

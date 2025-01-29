from model.text import TextModel
from model.vector import GetNow, ParseIds, SaveSituation, SearchSituation
from model.vision import VisionModel
from utils.database import SaveSituationDB, SearchSituationDB
from utils.storage import CreatePublicURLs, GetURL, SaveToBucket
from visual.image import GetBase64


def RunSaveSituation(frame, label):
    time = GetNow()
    base64, bytes, _ = GetBase64(frame)

    text = VisionModel(base64)
    text = TextModel(
        system="You are monitoring CCTV, you need to rewrite the given description to much simpler and in fewer no of words. Write less about background and focus on main subjects (persons, cars, etc), its appearence (color, dress, structure) and activity (also try to guess what its gonna do next). Write in a single sentence, not points",
        user=f"CCTV Description: {text}",
    )

    print(">", text)

    id = SaveSituation(text, time, {"label": label})

    SaveToBucket(bytes, id)

    SaveSituationDB(
        id.__str__(), text, GetURL(id), time, {"label": label} if label else None
    )


def RunSearchSituation(q: str):
    ids = SearchSituation(q)

    if len(ids) == 0:
        return None

    (ids, idKeys) = ParseIds(ids)

    data = SearchSituationDB(idKeys)

    return data

    # if len(data) == 0:
    #     return None

    # return CreatePublicURLs(idKeys)

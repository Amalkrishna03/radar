import re
import uuid
from datetime import datetime

from vecs.adapter import Adapter, ParagraphChunker, TextEmbedding

from utils.source import SupabaseVector

# create a collection with an adapter
imageSituation = SupabaseVector.get_or_create_collection(
    name="imageSituation",
    adapter=Adapter(
        [
            ParagraphChunker(skip_during_query=True),
            TextEmbedding(model="all-MiniLM-L6-v2"),
        ]
    ),
)


def GetNow():
    return datetime.now().timestamp()


def ParseIds(results: list[str]):
    dict = {}
    for result in results:
        id = re.sub(r"_para_\d+$", "", result)
        if id not in dict:
            dict[id] = 0
        dict[id] += 1

    return dict, list(dict.keys())


def SaveSituation(text: str, timestamp: float, extraData: dict = {}):
    data = {"timestamp": timestamp} | extraData
    id = uuid.uuid4()

    # add records to the collection using text as the media type
    imageSituation.upsert(
        records=[
            (
                id,
                text,
                data,
            )
        ]
    )

    return id


def SearchSituation(text: str):
    results = imageSituation.query(
        text,
        # include_metadata=True,
        limit=10,
    )

    return results


if __name__ == "__main__":
    epoch_time = GetNow()

    SaveSituation("four score and seven years ago", epoch_time)

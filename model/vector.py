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


if __name__ == "__main__":
    epoch_time = GetNow()

    SaveSituation("four score and seven years ago", epoch_time)

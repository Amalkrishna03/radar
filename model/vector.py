import os
from datetime import datetime

import vecs
from vecs.adapter import Adapter, ParagraphChunker, TextEmbedding

# create vector store client
vx = vecs.Client(
    os.getenv("DB_CONNECTION"),
)

# create a collection with an adapter
imageSituation = vx.get_or_create_collection(
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


def SaveSituation(text: str, id: str, timestamp: float):
    # add records to the collection using text as the media type
    imageSituation.upsert(
        records=[
            (
                id,
                text,
                {"timestamp": timestamp},
            )
        ]
    )



if __name__ == "__main__":
    epoch_time = GetNow()

    SaveSituation("four score and seven years ago", "vec0", epoch_time)

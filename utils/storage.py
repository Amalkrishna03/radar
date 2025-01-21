from utils.source import SupabaseClient
from visual.image import ByteToImage


def GetURL(id: str, bucket: str = "anomalies"):
    return f"{id}.png"


def SaveToBucket(buffer: bytes, id: str, bucket: str = "anomalies"):
    response = SupabaseClient.storage.from_(bucket).upload(
        file=buffer,
        path=f"{id}.png",
        file_options={"cache-control": "3600", "upsert": "false"},
    )

    return response


def SearchInBucket(id: str, bucket: str = "anomalies"):
    response = SupabaseClient.storage.from_(bucket).download(GetURL(id))

    return response


def CreatePublicURL(ids: list[str], bucket: str = "anomalies"):
    response = SupabaseClient.storage.from_(bucket).create_signed_urls(
        [GetURL(id) for id in ids], 180
    )

    dictionary = {}

    for res in response:
        dictionary[res["path"]] = res["signedUrl"]

    return dictionary


def DownloadImage(path: str, bucket: str = "anomalies"):
    imageByte = SupabaseClient.storage.from_(bucket).download(path)
    imageFrame = ByteToImage(imageByte)
    return imageFrame


def ListBucket(bucket: str = "anomalies", download: bool = False):
    response = SupabaseClient.storage.from_(bucket).list()

    print(response)

    imageFrames = []
    for imageData in response:
        if download:
            imageFrames.append(DownloadImage(imageData["name"]))

        else:
            imageFrames.append(imageData["name"])

    return imageFrames

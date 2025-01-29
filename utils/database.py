from utils.source import APIResponse, SupabaseClient


def SearchSituationDB(ids: list[str], table: str = "events"):
    response = SupabaseClient.table(table).select("*").order("timestamp", desc=True).in_("id", ids).execute()  # type: APIResponse

    print(response)

    return response.data  # type: list[dict]


def SaveSituationDB(
    id: str,
    text: str,
    url: str,
    timestamp: float,
    extraData: dict = None,
    table: str = "events",
):
    response = (
        SupabaseClient.table(table)
        .upsert(
            {
                "id": id,
                "text": text,
                "url": url,
                "timestamp": timestamp,
                "extradata": extraData if extraData else None,
            }
        )
        .execute()
    )

    # print(response.data)

    return id

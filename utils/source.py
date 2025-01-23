import os
from typing import Literal, Optional

import vecs
from groq import Groq
from pydantic import AnyUrl, BaseModel
from supabase import Client, create_client
from supabase import PostgrestAPIResponse as APIResponse

GroqClient = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

SupabaseVector = vecs.Client(
    os.getenv("DB_CONNECTION"),
)

SupabaseClient: Client = create_client(
    os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")
)


class Config(BaseModel):
    ENV: Literal["production", "development"]
    FRONTEND: AnyUrl = "http://localhost:5173"


config = Config.model_validate({
    "ENV": os.getenv("ENV"), 
    "FRONTEND": os.getenv("FRONTEND")
}).model_dump()
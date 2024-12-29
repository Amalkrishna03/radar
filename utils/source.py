import os

import vecs
from groq import Groq
from supabase import Client, create_client

GroqClient = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

SupabaseVector = vecs.Client(
    os.getenv("DB_CONNECTION"),
)

SupabaseClient: Client = create_client(
    os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")
)
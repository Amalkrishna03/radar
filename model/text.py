from utils.source import GroqClient

model = "llama-3.1-8b-instant"


def TextModel(system: str, user: str):
    completion = GroqClient.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": user,
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    return completion.choices[0].message.content
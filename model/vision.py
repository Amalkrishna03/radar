from utils.source import GroqClient

model = "llama-3.2-11b-vision-preview"


def VisionModel(base64_image: str) -> str:
    completion = GroqClient.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Explain the image with exact color, situation of what happening, and presence of all objects?",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    return completion.choices[0].message.content

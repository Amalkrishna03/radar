import os

import cv2
from groq import Groq

import base64
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)


def VisionModel(image: cv2.typing.MatLike):
    retval, buffer = cv2.imencode('.png', image)
    base64_image = base64.b64encode(buffer).decode("utf-8")
    
    # return base64_image
    
    
    completion = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Explain the image with exact color, situation of what happening, and presence of all objects?"},
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

if __name__ == "__main__":
    
    frame = cv2.imread("./image.png")
    text = VisionModel(frame)

    print(text)
    
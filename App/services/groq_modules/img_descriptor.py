from App.services.groq_modules.groq_client import client

def get_img_description(IMAGE_DATA_URL, prompt=""):
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful ai assistant that helps user with generating detailed descriptions of images. Format of description is dict."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                        "url": IMAGE_DATA_URL
                        }
                    }
                ]
            },
        ],
        temperature=1,
        max_completion_tokens=2028,
        top_p=1,
        stream=False,
        stop=None,
    )

    return completion.choices[0].message
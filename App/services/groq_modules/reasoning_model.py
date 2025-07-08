from App.services.groq_modules.groq_client import client

class REASONING_MODEL():
    def __init__(self, system_prompt=None, max_tokens=4096):
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.model = "deepseek-r1-distill-llama-70b"
    
    def get_response(self, prompt="",  IMAGE_DATA_URL=None, his=None):
        messages = []
        if self.system_prompt is not None:
            messages.append(
                {
                    "role": "system",
                    "content": self.system_prompt
                }
            )
        
        if his is not None:
            messages.extend(his)

        messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        completion = client.chat.completions.create(
            model = self.model,
            messages = messages,
            temperature=0.7,
            max_completion_tokens=self.max_tokens,
            top_p=0.95,
            stream=False,
            stop=None,
        )

        return completion.choices[0].message
import httpx


class OpenAICompatibleProvider:
    def __init__(self,model:str,base_url:str,timeout:int=60,api_key:str|None=None):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self,system_prompt:str,user_prompt:str)->str:
        headers = {}

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        response = httpx.post(
            f"{self.base_url}/v1/chat/completions",
            headers=headers,
            timeout=self.timeout,
            json={
                "model":self.model,
                "messages":[
                    {"role":"system","content":system_prompt},
                    {"role":"user","content":user_prompt},
                ],
            },
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"] or ""
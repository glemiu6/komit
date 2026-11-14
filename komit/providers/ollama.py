from ollama import Client


class OllamaProvider:

    def __init__(self,model:str,base_url:str,timeout:int):
        self.client = Client(base_url=base_url,timeout=timeout)
        self.model = model

    def generate(self,system_prompt:str,user_prompt:str)->str:

        response = self.client.chat(model=self.model,
                                    messages=[
                                        {"role":"system","content":system_prompt},
                                        {"role":"user","content":user_prompt},
                                    ],)
        return response.message.content or ""
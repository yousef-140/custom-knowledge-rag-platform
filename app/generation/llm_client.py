import requests

class OllamaClient:

    def __init__(self,model_name: str = "llama3.2",base_url: str = "http://localhost:11434"):
        self.model_name =model_name
        self.base_url = base_url


    def generate(self,prompt: str ,temperature : float =0.0) ->str :
        url = f"{self.base_url}/api/generate"

        payload ={

            "model": self.model_name,
            "prompt":prompt,
            "stream" : False,
            "option": {
                "temperature": temperature
            }
        }



        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()

        data = response.json()
        return data.get("response", "").strip()
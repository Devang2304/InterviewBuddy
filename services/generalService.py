import os
class generalService: 
    def __init__(self):
        pass

    async def set_api_key(self, api_key):
        try:
            path = os.path.join("config/", "llm_config.py")
            with open(path, "w") as f:
                f.write(f'LLM_CONFIG = {{\n    "api_key": "{api_key}",\n    "base_url":"https://generativelanguage.googleapis.com/v1beta/openai/",\n    "model": "gemini-2.0-flash",\n    "temperature": 0.7,\n    "max_tokens": 4000,\n}}')
                return {
                    "status_code": 200,
                    "message": "API key set successfully"
                }
        except Exception as e:
            print(e)
            return {
                "status_code": 500,
                "message": "Error in setting API key"
            }


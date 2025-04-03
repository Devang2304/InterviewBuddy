from openai import OpenAI
from ..config.llm_config import LLM_CONFIG

class text_generation_service:
    def __init__(self):
        self.llm = OpenAI
        self.llm_config = LLM_CONFIG
        self.client = self.llm(api_key=self.llm_config['api_key'],base_url=self.llm_config['base_url'])
    
    async def generate_questions(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model = self.llm_config['model'],
                messages=[
                    {"role":"user","content":prompt}
                ],
                temperature=self.llm_config['temperature'],
                max_tokens=self.llm_config['max_tokens'],
                response_format={"type": "json_object"}
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return None
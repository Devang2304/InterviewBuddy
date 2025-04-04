from openai import OpenAI
import asyncio
from config.llm_config import LLM_CONFIG

#  USE THIS LINE FOR RUNNING LOCALLY INDIVIDUAL FILES
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from config.llm_config import LLM_CONFIG


class LLM:
    def __init__(self):
        self.llm = OpenAI
        self.llm_config = LLM_CONFIG
        self.client = self.llm(api_key=self.llm_config['api_key'],base_url=self.llm_config['base_url'])
        self.JSON_FORMAT = {
            "education": "",
            "experience": "",
            "skills": "",
            "projects": "",
            "achievements": ""
        }
    
    async def get_response(self, extracted_data):
        try:
            prompt = f"""
            Analyze the following resume data and generate a JSON response with the following format:
            {self.JSON_FORMAT}
            Resume Data:
            {extracted_data}
            """
            response =self.client.chat.completions.create(
                model=self.llm_config['model'],
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=self.llm_config['temperature'],
                max_tokens=self.llm_config['max_tokens'],
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return None
        
# UNCOMMENT THIS IF YOU WANT TO TEST THIS FILE INDIVIDUALLY 

# resume_data = f"""

# """

# if __name__ == "__main__":
#     async def main():
#         llm = LLM()
#         response =await llm.get_response(resume_data)
#         print("Response:",response)
        
#     asyncio.run(main())
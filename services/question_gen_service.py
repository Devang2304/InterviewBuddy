from services.text_generation_service import text_generation_service
from services.resume_analyser import ResumeAnalyser
from typing import Dict,Any
import os
import json

class QuestionGenerationService:
    
    VALID_CATEGORIES = {'education', 'experience', 'skills', 'projects', 'achievements'}
    
    def __init__(self):
        self.resume_analyser = ResumeAnalyser()
        self.text_generation_service = text_generation_service()
    
    async def generate_questions(self) -> None:
        await self.resume_analyser.analyse_resume("C:/Users/devan/Coding_Projects/AI_powered_interviewer/Devang_Vartak_resume.pdf")
        
        # if category not in self.VALID_CATEGORIES:
        #     raise ValueError(f"Invalid category: {category}. Valid categories are: {', '.join(self.VALID_CATEGORIES)}")
        
        try:
            for singleCategory in self.VALID_CATEGORIES:
                getter_method = getattr(self.resume_analyser, f"get_{singleCategory}")
                data = getter_method()
                
                if not data:
                    raise ValueError(f"No data found for category: {singleCategory}")
                
                prompt = f"""
                Generate 5 questions based on the following {singleCategory} data:
                {data}
                """
                questions = await self.text_generation_service.generate_questions(prompt)
                path = "resume_data_json"
                if not os.path.exists(path):
                    os.makedirs(path)
                json_file_path = os.path.join(path, f"{singleCategory}SessionData.json")
                with open(json_file_path, 'w') as f:
                    json.dump({singleCategory: questions}, f, indent=4)
                
        
        except Exception as e:
            print(f"Error: {e}")
            return None
    
        
        

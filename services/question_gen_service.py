from services.text_generation_service import text_generation_service
from services.resume_analyser import ResumeAnalyser
from typing import Dict,Any

class QuestionGenerationService:
    
    VALID_CATEGORIES = {'education', 'experience', 'skills', 'projects', 'achievements'}
    
    def __init__(self):
        self.resume_analyser = ResumeAnalyser()
        self.text_generation_service = text_generation_service()
    
    async def generate_questions(self, category: str) -> Dict[str, Any]:
        await self.resume_analyser.analyse_resume("C:/Users/devan/Coding_Projects/AI_powered_interviewer/Devang_Vartak_resume.pdf")
        
        if category not in self.VALID_CATEGORIES:
            raise ValueError(f"Invalid category: {category}. Valid categories are: {', '.join(self.VALID_CATEGORIES)}")
        
        try:
            getter_method = getattr(self.resume_analyser, f"get_{category}")
            data = getter_method()
            
            if not data:
                raise ValueError(f"No data found for category: {category}")
            
            prompt = f"""
            Generate 5 questions based on the following {category} data:
            {data}
            """
            questions = await self.text_generation_service.generate_questions(prompt)
            
            return questions
        
        except Exception as e:
            print(f"Error: {e}")
            return None
    
        
        

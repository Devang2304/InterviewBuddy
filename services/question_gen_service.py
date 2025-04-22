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
    
    async def generate_questions(self,pdf) -> None:
        await self.resume_analyser.analyse_resume(pdf)
        
        # if category not in self.VALID_CATEGORIES:
        #     raise ValueError(f"Invalid category: {category}. Valid categories are: {', '.join(self.VALID_CATEGORIES)}")
        
        try:
            
            category_prompts = {
                "education": "Generate 5 specific questions about the candidate's educational background, focusing on their degree, major, institution, and timeline. Verify key details from their education history.",
                
                "experience": "Generate 5 in-depth technical questions based on their work experience. Focus on specific projects, technologies used, and achievements. Include questions about architectural decisions, optimizations, and problem-solving approaches.",
                
                "skills": "Generate 5 technical questions to assess proficiency in their listed skills. Include scenario-based questions that test practical application. Focus on both technical depth and breadth of their skillset.",
                
                "projects": "Generate 5 detailed questions about their projects. Focus on technical implementation, challenges faced, and solutions developed. Ask about specific technologies used and architectural decisions made.",
                
                "achievements": "Generate 5 questions about their achievements and impact. Focus on quantifiable results, methodologies used, challenges overcome, and lessons learned."
            }
            
            for singleCategory in self.VALID_CATEGORIES:
                getter_method = getattr(self.resume_analyser, f"get_{singleCategory}")
                data = getter_method()
                
                if not data:
                    raise ValueError(f"No data found for category: {singleCategory}")
                
                
                prompt_template = category_prompts.get(singleCategory)
                prompt = f"{prompt_template}\n\nbased on the following {singleCategory} data:\n{data}"
                
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
    
        
        

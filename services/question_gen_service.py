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
        
    async def get_fiveRandom_questionsFromJson(self,category:str) -> Dict[str, Any]:
        try:
            
            
    
    async def get_question(self,category:str) -> Dict[str, Any]:
        try:
            if category not in self.VALID_CATEGORIES:
                raise ValueError(f"Invalid category: {category}. Valid categories are: {', '.join(self.VALID_CATEGORIES)}")
            path = os.path.join("resume_data_json",f"{category}SessionData.json")
            with open(path, 'r') as file:
                data = json.load(file)
            questions = data[category]
            return questions
        except Exception as e:
            return {"error": str(e)}
            
    
    async def generate_questions(self,pdf) -> None:
        await self.resume_analyser.analyse_resume(pdf)
        
        # if category not in self.VALID_CATEGORIES:
        #     raise ValueError(f"Invalid category: {category}. Valid categories are: {', '.join(self.VALID_CATEGORIES)}")
        
        try:
            
            category_prompts = {
                        "education": """
                        You are a recruiter-bot. For the “education” category, generate exactly 5 concise, standalone questions (no sub-questions or multi-part questions) about the candidate’s educational background (degree, major, institution, timeline). 

                        Output **only** valid JSON in this exact format (no extra keys):

                         [
                            "Question 1?",
                            "Question 2?",
                            "Question 3?",
                            "Question 4?",
                            "Question 5?"
                        ]
                        
                        """,

                        "experience": """
                        You are a recruiter-bot. For the “experience” category, generate exactly 5 concise, standalone technical questions based on the candidate’s work history—focus on one project or technology per question (architecture, optimizations, problem solving).

                        Output **only** valid JSON in this exact format (no extra keys):

                        [
                            "Question 1?",
                            "Question 2?",
                            "Question 3?",
                            "Question 4?",
                            "Question 5?"
                        ]
                        
                        """,

                        "skills": """
                        You are a recruiter-bot. For the “skills” category, generate exactly 5 concise, standalone scenario-based questions that assess practical proficiency in the candidate’s listed skills.

                        Output **only** valid JSON in this exact format (no extra keys):

                        [
                            "Question 1?",
                            "Question 2?",
                            "Question 3?",
                            "Question 4?",
                            "Question 5?"
                        ]
                        
                        """,

                        "projects": """
                        You are a recruiter-bot. For the “projects” category, generate exactly 5 concise, standalone questions about the candidate’s projects—focus on implementation details, challenges, and architecture (one topic per question).

                        Output **only** valid JSON in this exact format (no extra keys):

                        [
                            "Question 1?",
                            "Question 2?",
                            "Question 3?",
                            "Question 4?",
                            "Question 5?"
                        ]
                        """,

                        "achievements": """
                        You are a recruiter-bot. For the “achievements” category, generate exactly 5 concise, standalone questions about the candidate’s achievements—focus on quantifiable impact, methodologies, and lessons learned (one achievement per question).

                        Output **only** valid JSON in this exact format (no extra keys):

                        [
                            "Question 1?",
                            "Question 2?",
                            "Question 3?",
                            "Question 4?",
                            "Question 5?"
                        ]
                        """
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
    
        
        

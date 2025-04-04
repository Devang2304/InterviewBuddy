from utils.text_extractor import text_extractor
from services.Resume_extractor_LLM import LLM
import json


class ResumeAnalyser:
    def __init__(self):
        self.education = None
        self.experience = None
        self.skills = None
        self.projects = None
        self.achievements = None
        
    def set_education(self, content):
        self.education = content
        
    def set_experience(self, content):
        self.experience = content
    
    def set_skills(self, content):
        self.skills = content
    
    def set_projects(self, content):
        self.projects = content
    
    def set_achievements(self, content):
        self.achievements = content
    
    def get_education(self):
        return self.education
    
    def get_experience(self):
        return self.experience
    
    def get_skills(self):
        return self.skills
    
    def get_projects(self):
        return self.projects
    
    def get_achievements(self):
        return self.achievements
    
    
    def get_resumeData(self,pdf):
        extractor = text_extractor()
        data = extractor.extract_text(pdf)
        return data
    
    async def analyse_resume(self,pdf):
        data = self.get_resumeData(pdf)
        llm =LLM()
        response = await llm.get_response(data)
        
        try:
            response_dict = json.loads(response) if isinstance(response, str) else response
            print("LLM Response:", response_dict)
            if all(value is None for value in response_dict.values()):
                print("Warning: All response values are None")
        
            for key in ['education', 'experience', 'skills', 'projects', 'achievements']:
                value = response_dict.get(key)
                print(f"Processing {key}: {value}")
                if value is not None:
                    setter = getattr(self, f'set_{key}')
                    setter(value)
                else:
                    print(f"Warning: {key} is None in the response")
        except json.JSONDecodeError:
            print("Error: Invalid JSON response")
        except Exception as e:
            print(f"Error processing response: {str(e)}")
        
        
        
             
        
        
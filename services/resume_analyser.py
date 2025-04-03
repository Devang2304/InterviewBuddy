from ..utils.text_extractor import text_extractor
from .Resume_extractor_LLM import LLM


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
        self.education = content
    
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
        if(response["education"]):
            self.set_education(response["education"])
        if(response["experience"]):
            self.set_experience(response["experience"])
        if(response["skills"]):
            self.set_skills(response["skills"])
        if(response["projects"]):
            self.set_projects(response["projects"])
        if(response["achievements"]):
            self.set_achievements(response["achievements"])
        
        
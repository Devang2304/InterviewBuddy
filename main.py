from services.resume_analyser import ResumeAnalyser
from services.question_gen_service import QuestionGenerationService
import asyncio





async def runIt():
    # resume_analyser =ResumeAnalyser()
    # await resume_analyser.analyse_resume("C:/Users/devan/Coding_Projects/AI_powered_interviewer/Devang_Vartak_resume.pdf")
    
    question_gen_service = QuestionGenerationService()
    
    questions = await question_gen_service.generate_questions("education")
    print(questions,end="\n")
    questions = await question_gen_service.generate_questions("experience")
    print(questions,end="\n")
    questions = await question_gen_service.generate_questions("skills")
    print(questions,end="\n")
    questions = await question_gen_service.generate_questions("projects")
    print(questions,end="\n")
    questions = await question_gen_service.generate_questions("achievements")
    print(questions,end="\n")
    

if __name__ == "__main__":
    async def main():
        response = await runIt()
        print("Response:", response)
        
    asyncio.run(main())
       
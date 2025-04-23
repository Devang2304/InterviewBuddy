# from services.resume_analyser import ResumeAnalyser
# from services.question_gen_service import QuestionGenerationService
# import asyncio





# async def runIt():
#     # resume_analyser =ResumeAnalyser()
#     # await resume_analyser.analyse_resume("C:/Users/devan/Coding_Projects/AI_powered_interviewer/Devang_Vartak_resume.pdf")
    
#     question_gen_service = QuestionGenerationService()
    
#     questions = await question_gen_service.generate_questions()

# if __name__ == "__main__":
#     async def main():
#         response = await runIt()
#         # print("Response:", response)
        
#     asyncio.run(main())
       
from fastapi import FastAPI, UploadFile, HTTPException, File, Body
from fastapi.middleware.cors import CORSMiddleware
from services.question_gen_service import QuestionGenerationService
from services.followupQGenService import FollowupQGenService
from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-resume")
async def upload_pdf(file: UploadFile):
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        content = await file.read()
        filePath = "./userResume/"+file.filename
        with open(filePath, "wb") as f:
            f.write(content)
        
        return {"filename":file.filename, "message":"File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    finally:
        question_gen_service = QuestionGenerationService()
        await question_gen_service.generate_questions(filePath)
        print("process successful!")

class SectionRequest(BaseModel):
    section: str = None
    question: str = None
    answer: str = None
@app.post("/round1/section")
async def round1(request: SectionRequest):
    try:
        question_gen_service = QuestionGenerationService()
        questions = await question_gen_service.get_question(request.section)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))      

@app.post("/round1/generate-followup-question")
async def generate_followup_question(request: SectionRequest):
    print(request)
    if request.question is None or request.answer is None:
        raise HTTPException(status_code=400, detail="Question and answer are required")
    if request.question == "" or request.answer == "":
        raise HTTPException(status_code=400, detail="Question and answer cannot be empty")
    try:
        followup_gen_service = FollowupQGenService()
        followup_question = await followup_gen_service.generate_followup_question(request.question, request.answer)
        print("followup_question", followup_question)
        if isinstance(followup_question, (str, dict)):
            return {"followup_question": followup_question}
        else:
            # Convert to string if it's not a basic type
            return {"followup_question": str(followup_question)}
    except Exception as e:
        print(f"Error in generate_followup_question: {str(e)}")  
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
async def root():
    return {"message":"Hello World"}


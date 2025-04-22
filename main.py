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
       
from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.middleware.cors import CORSMiddleware
from services.question_gen_service import QuestionGenerationService

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
        

@app.get("/")
async def root():
    return {"message":"Hello World"}


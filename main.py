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
from services.generalService import generalService
from services.voiceTranscribeService import voiceTranscribeService
from pydantic import BaseModel
import os 
import tempfile


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcribe-chunk")
async def transcribe_audio(file: UploadFile):
    try:
        print("file", file)
        if file.content_type !="audio/wav" and file.content_type !="audio/mpeg":
            raise HTTPException(status_code=400, detail="Only WAV and MP3 files are allowed")
        content = await file.read()
        if file.content_type == "audio/mpeg":
            fileSuffix = ".mp3"
        else:
            fileSuffix = ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=fileSuffix) as temp_file:
            temp_path = temp_file.name
            temp_file.write(content)
        
        try:
            translate_service = voiceTranscribeService()
            transcription = translate_service.transcribe(temp_path)

            return {"transcription": transcription}
        finally:
            os.unlink(temp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-resume")
async def upload_pdf(file: UploadFile):
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        content = await file.read()
        filePath = "./userResume/"+file.filename
        with open(filePath, "wb") as f:
            f.write(content)
        
        return {
            "status_code":200,
            "filename":file.filename,
            "message":"File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    finally:
        question_gen_service = QuestionGenerationService()
        await question_gen_service.generate_questions(filePath)
        print("process successful!")

class SectionRequest(BaseModel):
    section: str = None
    csSubject: str = None
    question: str = None
    answer: str = None
    api_key: str = None

@app.post("/set-api-key")
async def set_api_key(request: SectionRequest):
    try:
        general_service = generalService()
        api_key = request.api_key
        if api_key is None:
            raise HTTPException(status_code=400, detail="API key is required")
        if api_key == "":
            raise HTTPException(status_code=400, detail="API key cannot be empty")
        set_api_key = await general_service.set_api_key(api_key)

        if set_api_key["status_code"] == 200:
            return {"message":"API key set successfully"}
        else:
            return {"message":"cannot set API key at the moment, please try again later"}
    except Exception as e:
        print(f"Error in set_api_key: {str(e)}")  
        raise HTTPException(status_code=500, detail=str(e))
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

@app.post("/round2/cs-fundamentals")
async def round2(request: SectionRequest):
    try:
        question_gen_service = QuestionGenerationService()
        questions = await question_gen_service.get_fiveRandom_questionsFromJsonCS(request.csSubject)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/round4/HR")
async def round4():
    try:
        question_gen_service = QuestionGenerationService()
        questions = await question_gen_service.get_random_questionHR("HR")
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    
@app.get("/")
async def root():
    return {"message":"Hello World"}


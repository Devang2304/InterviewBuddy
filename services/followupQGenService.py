from services.text_generation_service import text_generation_service

class FollowupQGenService:
    def __init__(self):
        self.llm = text_generation_service()
    
    async def generate_followup_question(self, question, user_response):
        try:
            prompt = f"Question Asked: {question}\nUser Response: {user_response}\nGenerate a follow-up question that is relevant to the user's response."
            response =await self.llm.generate_questions(prompt)
            return response
        except Exception as e:
            print(f"Error: {e}")
            return None


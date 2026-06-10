from fastapi import FastAPI
import google.generativeai as genai 
import os
from dotenv import load_dotenv
from pydantic import BaseModel 
import json

load_dotenv()


class user_query(BaseModel):
    messages: list[str]

app = FastAPI()

genai.configure(api_key=os.environ['GEMINI_API_KEY'])


@app.post("/classify")
def user_query_classifier(requests: user_query):
    model=genai.GenerativeModel(model_name="gemini-3.5-flash")

    results= []
    for message in requests.messages:
        if not message:
            return {"error": "Message cannot be empty"}
        
        try: 
            
            print(message)
            # client = genai.Client()
        
            response = model.generate_content( contents= f'''You are a virtual customer service for a fintech company. 
                        Your role is to analyse the user's full message and classify it into one of the following catigories:
                        - Billing
                        - Technical Support 
                        - Account Management
                        - General Inquiry
                        PLease show you confidence score as a decimal between 0 and 1 for the category. Your answer can only be one of the categories stated. 
                        Or Return category as 'Unclassified' if confidence score is below 0.20 for all categories.  Here is the user's message '{message}'.
                        Return your response ONLY as a JSON object with two keys: category and confidence. Nothing else.'''
        )
        
            print(response.text)
            
            cleaned = response.text.strip().removeprefix("```json").removesuffix("```").strip()
            result = json.loads(cleaned)
            category = result['category']
            confidence = result['confidence']

            results.append({"category": category, "confidence": confidence})

            
        except Exception as e:
            print(e)
            return {"error": "Cannot classify your request, please speak to a human customer service"}
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

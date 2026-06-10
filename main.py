from fastapi import FastAPI
import google.generativeai as genai 
import os
from dotenv import load_dotenv
from pydantic import BaseModel 
import json

load_dotenv()

class user_query(BaseModel):   # Pydantic model defines the expected format of the incoming request
    messages: list[str]         # message format: list of strings

app = FastAPI()     # fastapi instance

genai.configure(api_key=os.environ['GEMINI_API_KEY'])


@app.post("/classify")     # decorator that registers the function below as a POST endpoint at /classify
def user_query_classifier(requests: user_query):
    model=genai.GenerativeModel(model_name="gemini-3.5-flash")      # google gemini ai model

    results= []     # store answers from model
    for message in requests.messages:   # loop through user's query
        if not message:     # handle empty query
            return {"error": "Message cannot be empty"} 
        
        try: 
            
            # print(message)
            
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
        
            # print(response.text)
            
            cleaned = response.text.strip().removeprefix("```json").removesuffix("```").strip()  # clean version of gemini response in string format
            result = json.loads(cleaned)    # covert response to python object
            category = result['category']   
            confidence = result['confidence']

            results.append({"category": category, "confidence": confidence})    # append response for a message in the correct format

            
        except Exception as e:   # catch any unexpected errors eg Gemini returning unparseable response
            print(e)
            return {"error": "Cannot classify your request, please speak to a human customer service"}
    return results

if __name__ == "__main__":
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8000)     # run fastapi server using host and port

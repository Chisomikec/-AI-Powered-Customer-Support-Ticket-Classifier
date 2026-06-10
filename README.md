# AI-Powered Customer Support Ticket Classifier
 
A FastAPI application that automatically classifies customer support messages into predefined categories using Google's Gemini AI model.
 
## What it does
 
The application accepts a customer support message (or a batch of messages) and classifies each one into one of the following categories:
 
- Billing
- Technical Support
- Account Management
- General Inquiry
  
It returns the predicted category along with a confidence score between 0 and 1. Messages with low confidence are returned as "Unclassified".
 
## Setup Instructions
 
### Prerequisites
 
- Python 3.11 or higher
- A Google Gemini API key (get one free at https://aistudio.google.com)
### Installation
 
1. Clone the repository:
```
git clone https://github.com/Chisomikec/-AI-Powered-Customer-Support-Ticket-Classifier.git
cd -AI-Powered-Customer-Support-Ticket-Classifier
```
 
2. Create and activate a virtual environment:
```
python -m venv venv
venv\Scripts\activate
```
 
3. Install dependencies:
```
pip install -r requirements.txt
```
 
4. Create a `.env` file in the root of the project and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```
 
### Running the application
 
```
python main.py
```
 
The application will start on http://localhost:8000
 
To access the interactive API documentation, open your browser and go to:
 
```
http://localhost:8000/docs
```
 
## How the model works
 
When a message is received, it is sent to Google's Gemini AI model along with a prompt that instructs it to act as a customer support classifier. The prompt specifies the four valid categories and asks Gemini to return a JSON response containing the predicted category and a confidence score.
 
The confidence score is a decimal between 0 and 1 representing how certain the model is about the classification. If the confidence is below 0.20 for all categories, the message is returned as "Unclassified".
 
The response is parsed and returned to the user as a clean JSON object.
 
## Example Requests and Responses
 
### Single message classification
 
POST /classify
 
Request:
```json
{
  "messages": ["I was charged twice for my subscription this month."]
}
```
 
Response:
```json
[
  {
    "category": "Billing",
    "confidence": 0.98
  }
]
```
 
### Batch classification
 
POST /classify
 
Request:
```json
{
  "messages": [
    "I was charged twice for my subscription this month.",
    "The app keeps crashing every time I try to log in.",
    "I want to update my email address.",
    "What are your customer service opening hours?"
  ]
}
```
 
Response:
```json
[
  {
    "category": "Billing",
    "confidence": 0.98
  },
  {
    "category": "Technical Support",
    "confidence": 0.98
  },
  {
    "category": "Account Management",
    "confidence": 0.98
  },
  {
    "category": "General Inquiry",
    "confidence": 0.98
  }
]
```
 
### Invalid or empty input
 
Empty messages return an error:
```json
{
  "error": "Message cannot be empty"
}
```
 
Unrecognised or unclear messages return:
```json
{
  "category": "Unclassified",
  "confidence": 0.10
}
```
 
## Docker
 
A Dockerfile is included in the repository. To build and run the container, ensure Docker and WSL are installed on your machine, then run:
 
```
docker build -t ticket-classifier .
docker run -p 8000:8000 --env-file .env ticket-classifier
```
 
The application will be available at http://localhost:8000

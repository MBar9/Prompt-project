from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Set API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

class ReviewRequest(BaseModel):
    review: str

@app.post("/analyze")
async def analyze_review(data: ReviewRequest):
    prompt = f'''
You are an expert Customer Experience Analyst. A customer has left a review. Please analyze the review and respond with the following information:
1. Category: Classify as [Food Quality, Service, Ambience, Price, Mixed, Other].
2. Sentiment: Positive, Negative, or Neutral.
3. Priority: High, Medium, or Low.
4. Suggested Action: Recommend a suitable internal action.
5. Customer Response: Write a short and empathetic reply to the customer.

Customer Review: "{data.review}"
'''

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=500
    )

    return {"result": response['choices'][0]['message']['content']}

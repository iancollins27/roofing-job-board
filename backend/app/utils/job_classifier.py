import os
from openai import OpenAI
from ..core.config import settings

def classify_job_function(job_title: str) -> str | None:
    """
    Classifies a job title into predefined categories using OpenAI's API.
    Returns None if classification fails.
    """
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        print("OPENAI_API_KEY not found in settings")
        return None

    try:
        # Initialize the client with the API key
        client = OpenAI(api_key=api_key)
        
        print(f"Classifying job title: {job_title}")  # Debug log
        
        # Create the chat completion using the new API syntax
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a job title classifier for the roofing industry. "
                        "Classify the job title into one of these categories: "
                        "SALES, LABOR, PRODUCTION, MANAGEMENT. "
                        "Return only the category name in all caps."
                    )
                },
                {
                    "role": "user",
                    "content": f"Classify this job title: {job_title}"
                }
            ],
            max_tokens=10,
            temperature=0
        )
        
        classification = response.choices[0].message.content.strip()
        print(f"Classification result: {classification}")  # Debug log
        # Convert to lowercase to match the enum values
        classification = classification.lower()
        print(f"Converted to lowercase: {classification}")  # Debug log
        return classification
    
    except Exception as e:
        print(f"Error classifying job title:")
        print(f"Error message: {str(e)}")
        print(f"Error type: {type(e)}")
        return None

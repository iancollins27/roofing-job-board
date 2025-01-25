import os
import openai
from typing import Optional
from ..models.job_model import JobFunction
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def classify_job_function(job_title: str) -> Optional[JobFunction]:
    """
    Use OpenAI to classify a job title into one of our JobFunction categories.
    
    Args:
        job_title (str): The job title to classify
        
    Returns:
        JobFunction: The classified job function or None if classification fails
    """
    try:
        print("\n" + "="*50)  # Separator for better readability
        print(f"Processing Job Title: {job_title}")
        print("="*50)
        
        prompt = f"""Classify the following roofing industry job title into exactly one of these categories:
- SALES: Sales, Business Development, Account Management roles
- LABOR: Hands-on roofing work, installation, repair
- PRODUCTION: Production, project management
- MANAGEMENT: Supervisory, project management, leadership roles

Job Title: {job_title}

Return only one word in uppercase from the above categories (SALES, LABOR, PRODUCTION, or MANAGEMENT)."""

        print(f"OpenAI API Key present: {bool(openai.api_key)}")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a job classification assistant. Respond with exactly one word from the allowed categories."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=20
        )

        # Print the full response for debugging
        print("\nOpenAI Response:")
        print(f"Raw response: {response}")
        print(f"Content: {response.choices[0].message.content}")
        
        classification = response.choices[0].message.content.strip().upper()
        print(f"\nProcessed Classification: {classification}")
        
        if classification in JobFunction.__members__:
            print(f"✓ Successfully classified as: {classification}")
            return JobFunction[classification]
        
        print(f"✗ Error: Classification '{classification}' not in valid options: {list(JobFunction.__members__.keys())}")
        return None
        
    except Exception as e:
        print(f"\n✗ Error classifying job title:")
        print(f"Error message: {str(e)}")
        print(f"Error type: {type(e)}")
        return None 
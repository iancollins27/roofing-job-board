from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Stripe with your secret key
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

router = APIRouter()

class PaymentIntentRequest(BaseModel):
    amount: int  # Amount in cents
    payment_method_id: str

@router.post("/create-intent")
async def create_payment_intent(request: PaymentIntentRequest):
    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=request.amount,
            currency='usd',
            payment_method=request.payment_method_id,
            confirmation_method='manual',
            confirm=True,
            return_url='http://localhost:3000/post-job/success'
        )
        
        return {
            "client_secret": intent.client_secret,
            "status": intent.status,
        }
    except stripe.error.CardError as e:
        # Handle card errors (e.g., declined card)
        raise HTTPException(
            status_code=400,
            detail=f"Card error: {str(e)}"
        )
    except stripe.error.StripeError as e:
        # Handle other Stripe errors
        raise HTTPException(
            status_code=500,
            detail=f"Stripe error: {str(e)}"
        )
    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )

@router.post("/webhook")
async def stripe_webhook(request: dict):
    try:
        event = stripe.Event.construct_from(
            request,
            stripe.api_key
        )

        # Handle the event
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
            print(f"Payment succeeded for amount: {payment_intent.amount}")
            # Here you could update your database or trigger other actions
            
        elif event.type == 'payment_intent.payment_failed':
            payment_intent = event.data.object
            print(f"Payment failed for amount: {payment_intent.amount}")
            # Handle failed payment
            
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Webhook error: {str(e)}"
        ) 
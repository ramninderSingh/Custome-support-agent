# src/router/classifier.py

import os
from dotenv import load_dotenv
from google import genai

from src.router.schema import QueryRoute


load_dotenv()


class QueryRouter:

    def __init__(
        self,
        model_name: str = "gemini-3.5-flash-lite"
    ):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.model_name = model_name

    def classify(self, query: str) -> QueryRoute:

        prompt = f"""
You are an intent router for an enterprise customer support system.

Your task is ONLY to classify the user's request and determine
which backend systems are required.

Available systems:

1. Knowledge Base
   - billing policies
   - refund policies
   - cancellation policies
   - payment failure policies

2. Customer Database
   - customer profile
   - account status

3. Subscription Database
   - subscription plan
   - price
   - renewal date
   - status

4. Transaction Database
   - payments
   - payment status
   - transaction history
   - payment method

5. Ticket System
   - support tickets
   - ticket status
   - ticket history

Possible intents:

- general_question
- billing_question
- duplicate_payment
- payment_failure
- refund_policy
- refund_request
- subscription_information
- subscription_cancellation
- customer_information
- transaction_status
- transaction_history
- ticket_status
- ticket_history
- ticket_creation
- ticket_update
- ticket_escalation
- technical_issue
- unknown

Rules:

- Do NOT answer the user's question.
- Do NOT execute any action.
- Only classify the request.
- Select all backend systems required.
- Set requires_action=true when the user requests an operation.
- Set confidence between 0 and 1.

User query:

{query}
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": QueryRoute,
                "temperature": 0
            }
        )

        return QueryRoute.model_validate_json(response.text)
from datetime import datetime, timedelta
from fastapi import HTTPException
from google.cloud.firestore_v1.base_query import FieldFilter
from typing import Dict
import logging
from src.database.db import  users_data_ref
from src.model.billing_model import PaymentLinkDetails, PlanTier
from src.crud.email_service import EmailService

logger = logging.getLogger(__name__)


class BillingCrud:
    def __init__(self):
        self.users_data_ref = users_data_ref
        self.email_service = EmailService()
    def process_stripe_webhook(self, data: Dict):
        """Process Stripe webhooks for subscription events"""
        try:
            event_type = data.get("type")
            
            if event_type == "checkout.session.completed":
                self._handle_checkout_session(data)
            elif event_type == "payment_intent.succeeded":
                self._handle_payment_intent(data)
            elif event_type == "payment_intent.payment_failed":
                self._handle_payment_failed(data)
            else:
                logger.warning(f"Unhandled webhook event type: {event_type}")
                
        except Exception as e:
            logger.error(f"Error processing stripe webhook: {str(e)}")
            # raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")

    def _handle_checkout_session(self, data: Dict):
        """Handle initial subscription setup with trial"""
        try:
            session = data.get("data", {}).get("object", {})
            user_id = session.get("client_reference_id")
            customer_id = session.get("customer")
            payment_link = session.get("payment_link")
            status = session.get("status")

            if status != "complete":
                raise ValueError("Checkout session is not complete")
            
            if not all([user_id, customer_id, payment_link]):
                raise ValueError("Missing required fields in checkout session")

            # Determine plan tier from payment link
            if payment_link == PaymentLinkDetails.STARTER.value:
                plan_tier = PlanTier.STARTER.value
            elif payment_link == PaymentLinkDetails.PRO.value:
                plan_tier = PlanTier.PRO.value
            elif payment_link == PaymentLinkDetails.PREMIUM.value:
                plan_tier = PlanTier.PREMIUM.value
            else:
                raise ValueError("Invalid payment link")
            

            user_doc = self.users_data_ref.document(user_id).get()
            if not user_doc:
                raise ValueError(f"No user found for {user_id}")
            
            if user_doc.to_dict().get("stripe_customer_id"):
                raise ValueError(f"User {user_id} already has a Stripe customer ID {customer_id}")
    
            # Image limits based on plan tier
            image_limits = {
                PlanTier.STARTER.value: 10,
                PlanTier.PRO.value: 30,
                PlanTier.PREMIUM.value: 100
            }
            
            current_time = datetime.utcnow()
            
            # Update with set/merge instead of update
            self.users_data_ref.document(user_id).set({
                "stripe_customers": {
                    customer_id: {
                        "billing_period_start": current_time.isoformat(),
                        "billing_period_end": (current_time + timedelta(days=30)).isoformat(),
                        "last_payment_date": current_time.isoformat(),
                        "image_limit": image_limits.get(plan_tier, 0),
                        "plan_tier": plan_tier,
                        "created_at": current_time.isoformat()
                    },
                    "stripe_customer_id": customer_id
                },
                "plan_tier": plan_tier
            }, merge=True)

            logger.info(f"Updated user {user_id} with Stripe customer ID {customer_id} and plan {plan_tier}")

        except Exception as e:
            logger.error(f"Error handling checkout session: {str(e)}")
            raise

    def _handle_payment_intent(self, data: Dict):
        """Handle successful payment after trial"""
        try:
            payment_intent = data.get("data", {}).get("object", {})
            customer_id = payment_intent.get("customer")
            
            if not customer_id:
                raise ValueError("Missing customer ID in payment intent")
            
            # Query for user with stripe_customer_id
            user_docs = self.users_data_ref.where(
                filter=FieldFilter("stripe_customer_id", "==", customer_id)
            ).limit(1).get()  # Add limit(1) since we expect only one user
            
            if not user_docs:
                raise ValueError(f"No user found for Stripe customer {customer_id}")

            user_doc = user_docs[0]  # Get first document
            user_id = user_doc.id
            customer_data = user_doc.to_dict().get('stripe_customers', {}).get(customer_id)
            
            if not customer_data:
                raise ValueError(f"No customer data found for {customer_id}")

            # Image limits based on plan tier
            image_limits = {
                PlanTier.STARTER.value: 10,
                PlanTier.PRO.value: 30,
                PlanTier.PREMIUM.value: 100
            }
            
            current_time = datetime.utcnow()
            
            # Update with set/merge instead of update
            self.users_data_ref.document(user_id).set({
                "stripe_customers": {
                    customer_id: {
                        "billing_period_start": current_time.isoformat(),
                        "billing_period_end": (current_time + timedelta(days=30)).isoformat(),
                        "last_payment_date": current_time.isoformat(),
                        "image_limit": image_limits.get(customer_data['plan_tier'], 0),
                        "plan_tier": customer_data['plan_tier'],
                    }
                },
                "plan_tier": customer_data['plan_tier']
            }, merge=True)


            logger.info(
                f"Confirmed paid status and reset usage for user {user_id} "
                f"with Stripe customer ID {customer_id}"
            )   

        except Exception as e:
            logger.error(f"Error handling payment intent: {str(e)}")
            raise

    def _handle_payment_failed(self, data: Dict):
        """Handle failed payment by reverting to free plan and sending notification"""
        try:
            payment_intent = data.get("data", {}).get("object", {})
            customer_id = payment_intent.get("customer")
            failure_message = payment_intent.get("last_payment_error", {}).get("message", "Unknown error")
            payment_failed_at = payment_intent.get("created")
            
            if not customer_id:
                raise ValueError("Missing customer ID in payment intent")


            user_doc = self.users_data_ref.where(
                filter=FieldFilter("stripe_customer_id", "==", customer_id)
            ).get()
            
            if not user_doc:
                raise ValueError(f"No user found for Stripe customer {customer_id}")

            user_id = user_doc.id
            user_details = user_doc.to_dict()
            customer_data = user_details['stripe_customers'][customer_id]

            self.users_data_ref.document(user_id).update({
                f"stripe_customers.{customer_id}.plan_tier": PlanTier.FREE.value,
                f"stripe_customers.{customer_id}.image_limit": 0,
                f"stripe_customers.{customer_id}.payment_failed": True,
                f"stripe_customers.{customer_id}.payment_failure_reason": failure_message,
                f"stripe_customers.{customer_id}.payment_failed_at": payment_failed_at,
                "plan_tier": PlanTier.FREE.value
            })

            logger.warning(
                f"Payment failed for user {user_id}. "
                f"Customer ID: {customer_id}. "
                f"Reason: {failure_message}. "
                f"Reverted to free plan."
            )

            # Get user details for email
            user_email = user_details.get("email")
            user_name = user_details.get("name", "Valued Customer")
            previous_plan = customer_data.get("plan_tier")

            # Send email notification
            self.email_service.send_payment_failed_notification(
                recipient=user_email,
                user_name=user_name,
                plan_tier=previous_plan,
                failure_reason=failure_message
            )

            logger.info(f"Payment failure notification sent to {user_email}")

        except Exception as e:
            logger.error(f"Error handling payment failure: {str(e)}")
            raise
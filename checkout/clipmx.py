import requests
import json
from django.conf import settings
from decimal import Decimal
import uuid

class ClipMX:
    """
    CLIP.MX payment gateway integration
    """
    def __init__(self):
        self.api_key = settings.CLIPMX['API_KEY']
        self.secret_key = settings.CLIPMX['SECRET_KEY']
        self.token = settings.CLIPMX['TOKEN']
        self.mode = settings.CLIPMX['MODE']
        
        # Set the appropriate base URL based on mode
        if self.mode == 'test':
            self.base_url = 'https://api-clip.com/test'
        else:
            self.base_url = 'https://api-clip.com/live'
    
    def create_payment(self, order, return_url):
        """
        Create a payment session with CLIP.MX for the given order
        """
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        
        # Format the amount as required by CLIP.MX (assuming they want cents/centavos)
        amount = int(order.get_total_cost() * 100)
        
        # Create a unique reference for this transaction
        reference = f"RAOT-{order.id}"
        
        payload = {
            'amount': amount,
            'currency': 'MXN',  # Mexican Peso
            'description': f'Order #{order.id} from RAOT Supplements',
            'reference': reference,
            'return_url': return_url,
            'customer_email': order.email,
            'customer_name': f"{order.first_name} {order.last_name}"
        }
        
        try:
            # Make API call to create payment
            response = requests.post(
                f"{self.base_url}/payments/create",
                headers=headers,
                data=json.dumps(payload)
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'payment_id': data.get('payment_id'),
                    'payment_url': data.get('payment_url')
                }
            else:
                return {
                    'success': False,
                    'error': f"Error {response.status_code}: {response.text}"
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_payment(self, payment_id):
        """
        Verify the status of a payment
        """
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/payments/{payment_id}/status",
                headers=headers
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'error': f"Error {response.status_code}: {response.text}"
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_webhook(self, data, signature):
        """
        Process webhook notifications from CLIP.MX
        """
        # Verify signature if needed
        # ...
        
        # Process different event types
        event_type = data.get('type')
        
        if event_type == 'payment.succeeded':
            payment_id = data.get('data', {}).get('id')
            reference = data.get('data', {}).get('reference')
            
            # Example: extract order ID from reference
            if reference and reference.startswith('RAOT-'):
                order_id = reference[5:]  # Remove 'RAOT-' prefix
                return {
                    'success': True,
                    'order_id': order_id,
                    'status': 'paid'
                }
        
        return {
            'success': True,
            'status': 'ignored',
            'message': f"Event {event_type} was ignored"
        }
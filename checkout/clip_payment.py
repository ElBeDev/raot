import requests
import json
import uuid
import hmac
import hashlib
import logging
import os
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

class ClipPaymentGateway:
    """
    Integration with CLIP.MX payment gateway
    
    This class handles:
    - Creating payment links
    - Verifying payment status
    - Processing refunds
    """
    
    def __init__(self):
        """Initialize the CLIP.MX payment gateway with API credentials"""
        # Get API credentials from settings
        self.api_key = getattr(settings, 'CLIP_API_KEY', 'f1544953-c525-470c-a912-1f65c11a57ee')
        self.secret_key = getattr(settings, 'CLIP_SECRET_KEY', 'f254c93d-e7e8-41cf-ab14-a313f3c0d2b3')
        
        # API endpoints - use IP directly to avoid DNS issues
        # 52.52.40.44 is the IP for api.clip.mx
        self.api_base_url = 'https://52.52.40.44/api'
        self.checkout_url = 'https://checkout.clip.mx'
        
        # Standard headers for API requests
        self.headers = {
            'Api-Key': self.api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            # Add Host header to make the server recognize the request
            'Host': 'api.clip.mx'
        }
        
        # Log initialization
        logger.info(f"ClipPaymentGateway initialized")
    
    def _generate_signature(self, payload):
        """Generate signature for CLIP.MX API requests"""
        # Convert payload to string if it's not already
        if isinstance(payload, dict):
            message = json.dumps(payload).encode()
        else:
            message = payload
        
        # Create HMAC signature
        signature = hmac.new(
            key=self.secret_key.encode(),
            msg=message,
            digestmod=hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def create_payment_link(self, order):
        """
        Create a payment link with CLIP.MX API
        For development: Creates a simulated payment link
        For production: Creates a real CLIP.MX payment link
        """
        # Development mode detection
        is_development = settings.DEBUG
        # If running on localhost or 127.0.0.1
        is_local = ('REMOTE_ADDR' in os.environ and 
                    os.environ['REMOTE_ADDR'] in ['127.0.0.1', 'localhost'])
        
        # Production mode - when running on the real server
        if not is_development and not is_local:
            # ========== PRODUCTION MODE ==========
            try:
                # Real implementation for production
                amount_in_cents = int(order.get_total_cost() * 100)
                reference_id = f"RAOT-{order.id}-{uuid.uuid4().hex[:8]}"
                site_url = getattr(settings, 'SITE_URL', 'https://raotsuplementos.com.mx')
                
                payload = {
                    'amount': amount_in_cents,
                    'currency': 'MXN',
                    'description': f'Orden #{order.id} - RAOT Suplementos',
                    'order_id': str(order.id),
                    'reference': reference_id,
                    'email': order.email,
                    'name': f'{order.first_name} {order.last_name}',
                    'redirect_url': f'{site_url}/checkout/payment/success/?order_id={order.id}',
                    'cancel_url': f'{site_url}/checkout/payment/cancel/?order_id={order.id}',
                    'webhook_url': f'{site_url}/checkout/webhook/clip/',
                    'metadata': {
                        'order_id': str(order.id),
                        'customer_email': order.email,
                        'shipping_address': f"{order.address}, {order.postal_code}, {order.city}"
                    }
                }
                
                # Generate signature
                signature = self._generate_signature(payload)
                
                # Add signature to headers
                headers = self.headers.copy()
                headers['Signature'] = signature
                
                # Log the API request
                logger.info(f"Creating payment link for order #{order.id} with amount {amount_in_cents/100} MXN")
                
                # Make request to CLIP.MX API
                response = requests.post(
                    f"{self.api_base_url}/v1/payments/links",
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=15
                )
                
                # Process the response
                if response.status_code == 200 or response.status_code == 201:
                    data = response.json()
                    
                    # Save payment ID to the order
                    order.payment_id = data.get('id')
                    order.payment_reference = reference_id
                    order.save(update_fields=['payment_id', 'payment_reference'])
                    
                    logger.info(f"Successfully created payment link for order #{order.id}")
                    
                    return {
                        'success': True,
                        'payment_url': data.get('checkout_url') or f"{self.checkout_url}/{data.get('id')}",
                        'payment_id': data.get('id')
                    }
                else:
                    error_data = response.json() if response.content else {'message': 'Unknown error'}
                    error_message = error_data.get('message', 'Error creating payment')
                    
                    logger.error(f"Failed to create payment link: {error_message} (Status code: {response.status_code})")
                    
                    return {
                        'success': False,
                        'error': error_message,
                        'status_code': response.status_code
                    }
                    
            except Exception as e:
                logger.exception(f"Exception in create_payment_link: {str(e)}")
                
                return {
                    'success': False,
                    'error': str(e)
                }
        else:
            # ========== DEVELOPMENT MODE ==========
            # For local development, we'll provide a page that lets the developer choose:
            # 1. Attempt a real connection to CLIP.MX (might fail)
            # 2. Simulate a successful payment
            try:
                # Generate a test payment ID
                payment_id = f"sim_payment_{uuid.uuid4().hex[:10]}"
                reference_id = f"RAOT-{order.id}-{uuid.uuid4().hex[:8]}"
                
                # Save payment ID to the order
                order.payment_id = payment_id
                order.payment_reference = reference_id
                order.save(update_fields=['payment_id', 'payment_reference'])
                
                # Log development mode
                logger.info(f"Using development mode for order #{order.id}")
                
                # Return URL to the test_or_real page
                site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
                if 'http' not in site_url:
                    site_url = f"http://{site_url}"
                    
                return {
                    'success': True,
                    'payment_url': f"{site_url}/checkout/test_or_real/{order.id}/",
                    'payment_id': payment_id,
                    'is_development': True
                }
                
            except Exception as e:
                logger.exception(f"Exception in create_payment_link (dev mode): {str(e)}")
                
                return {
                    'success': False,
                    'error': str(e)
                }
    
    def verify_payment(self, payment_id):
        """
        Verify the payment status with CLIP.MX API
        
        Args:
            payment_id: The payment ID to verify
            
        Returns:
            dict: Result with payment status information
        """
        try:
            # Generate signature for the request
            payload = {'id': payment_id}
            signature = self._generate_signature(payload)
            
            # Add signature to headers
            headers = self.headers.copy()
            headers['Signature'] = signature
            
            # Log the request
            logger.info(f"Verifying payment status for payment ID: {payment_id}")
            
            # Make request to CLIP.MX API
            response = requests.get(
                f"{self.api_base_url}/v1/payments/{payment_id}",
                headers=headers
            )
            
            # Check for successful response
            if response.status_code == 200:
                data = response.json()
                
                # Log payment status
                logger.info(f"Payment status for {payment_id}: {data.get('status', 'unknown')}")
                
                # Check payment status
                if data.get('status') == 'completed' or data.get('status') == 'paid':
                    return {
                        'success': True,
                        'status': 'paid',
                        'transaction_id': data.get('id'),
                        'payment_method': data.get('payment_method', 'card')
                    }
                else:
                    return {
                        'success': True,
                        'status': data.get('status', 'pending')
                    }
            else:
                # Handle error response
                error_data = response.json() if response.content else {'message': 'Unknown error'}
                error_message = error_data.get('message', 'Error verifying payment')
                
                # Log error
                logger.error(f"Failed to verify payment: {error_message} (Status code: {response.status_code})")
                
                return {
                    'success': False,
                    'error': error_message,
                    'status_code': response.status_code
                }
                
        except Exception as e:
            # Log the exception
            logger.exception(f"Exception in verify_payment: {str(e)}")
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_refund(self, payment_id, amount=None, reason=None):
        """
        Process a refund for a payment
        
        Args:
            payment_id: The payment ID to refund
            amount: Optional amount to refund (partial refund)
            reason: Optional reason for the refund
            
        Returns:
            dict: Result with refund status information
        """
        try:
            # Create refund payload
            payload = {
                'payment_id': payment_id,
            }
            
            if amount:
                # Convert to cents/centavos
                from decimal import Decimal
                payload['amount'] = int(Decimal(amount) * 100)
            
            if reason:
                payload['reason'] = reason
            
            # Generate signature
            signature = self._generate_signature(payload)
            
            # Add signature to headers
            headers = self.headers.copy()
            headers['Signature'] = signature
            
            # Log the request
            logger.info(f"Processing refund for payment ID: {payment_id}")
                
            # Make request to CLIP.MX API
            response = requests.post(
                f"{self.api_base_url}/v1/refunds",
                headers=headers,
                data=json.dumps(payload)
            )
            
            # Check for successful response
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                
                # Log successful refund
                logger.info(f"Successfully processed refund for payment {payment_id}")
                
                return {
                    'success': True,
                    'refund_id': data.get('id'),
                    'status': data.get('status')
                }
            else:
                # Handle error response
                error_data = response.json() if response.content else {'message': 'Unknown error'}
                error_message = error_data.get('message', 'Error processing refund')
                
                # Log error
                logger.error(f"Failed to process refund: {error_message} (Status code: {response.status_code})")
                
                return {
                    'success': False,
                    'error': error_message,
                    'status_code': response.status_code
                }
                
        except Exception as e:
            # Log the exception
            logger.exception(f"Exception in process_refund: {str(e)}")
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def _direct_api_call(self, order):
        """
        Make a direct API call to CLIP.MX without fallback
        Used for testing the real API connection
        """
        try:
            # Convert order total to cents/centavos (as integers)
            amount_in_cents = int(order.get_total_cost() * 100)
            
            # Generate a unique reference ID for the order
            reference_id = f"RAOT-{order.id}-{uuid.uuid4().hex[:8]}"
            
            # Get the site URL from settings, default to localhost for development
            site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
            
            # Create payload according to CLIP.MX documentation
            payload = {
                'amount': amount_in_cents,
                'currency': 'MXN',
                'description': f'Orden #{order.id} - RAOT Suplementos',
                'order_id': str(order.id),  # Convert UUID to string
                'reference': reference_id,
                'email': order.email,
                'name': f'{order.first_name} {order.last_name}',
                'redirect_url': f'{site_url}/checkout/payment/success/?order_id={order.id}',
                'cancel_url': f'{site_url}/checkout/payment/cancel/?order_id={order.id}',
                'webhook_url': f'{site_url}/checkout/webhook/clip/',
                'metadata': {
                    'order_id': str(order.id),  # Convert UUID to string
                    'customer_email': order.email,
                    'shipping_address': f"{order.address}, {order.postal_code}, {order.city}"
                }
            }
            
            # Generate signature
            signature = self._generate_signature(payload)
            
            # Add signature to headers
            headers = self.headers.copy()
            headers['Signature'] = signature
            
            # Log the API request
            logger.info(f"Making direct API call to CLIP.MX for order #{order.id}")
            
            # Make request to CLIP.MX API
            response = requests.post(
                f"{self.api_base_url}/v1/payments/links",
                headers=headers,
                data=json.dumps(payload),
                timeout=10  # Add timeout for the request
            )
            
            # Check for successful response
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                
                # Save payment ID to the order
                order.payment_id = data.get('id')
                order.payment_reference = reference_id
                order.save(update_fields=['payment_id', 'payment_reference'])
                
                # Log successful payment link creation
                logger.info(f"Successfully created payment link for order #{order.id}")
                
                # Return payment details
                return {
                    'success': True,
                    'payment_url': data.get('checkout_url') or f"{self.checkout_url}/{data.get('id')}",
                    'payment_id': data.get('id')
                }
            else:
                # Handle error response
                error_data = response.json() if response.content else {'message': 'Unknown error'}
                error_message = error_data.get('message', 'Error creating payment')
                
                # Log error
                logger.error(f"Failed to create payment link: {error_message} (Status code: {response.status_code})")
                
                return {
                    'success': False,
                    'error': error_message,
                    'status_code': response.status_code
                }
        
        except requests.exceptions.RequestException as e:
            # Handle connection errors
            logger.error(f"Connection error to CLIP.MX API: {str(e)}")
            return {
                'success': False,
                'error': f"Error de conexión: {str(e)}"
            }
        except Exception as e:
            # Handle other errors
            logger.exception(f"Exception in _direct_api_call: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
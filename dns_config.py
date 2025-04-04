"""
Configure DNS over HTTPS for better API connectivity
Run this once before starting your development server
"""

import urllib3
import json
import socket
import logging

def configure_dns_over_https():
    """Configure DNS over HTTPS for better connectivity to payment gateways"""
    try:
        # Create HTTP connection pool
        http = urllib3.PoolManager()
        
        # Cloudflare DNS over HTTPS API URL
        url = "https://cloudflare-dns.com/dns-query"
        
        # Test domain resolution for CLIP.MX
        response = http.request(
            'GET',
            url,
            headers={
                'Accept': 'application/dns-json'
            },
            fields={
                'name': 'api.clip.mx',
                'type': 'A'
            }
        )
        
        # Parse response
        data = json.loads(response.data.decode('utf-8'))
        
        if data.get('Status') == 0 and data.get('Answer'):
            # Get the first IP address
            ip_address = data['Answer'][0]['data']
            print(f"Resolved api.clip.mx to {ip_address}")
            
            # You can add this to your hosts file or use a socket wrapper
            # Here we'll just print instructions
            print("\nTo improve connectivity, add this line to your hosts file:")
            print(f"{ip_address} api.clip.mx")
            print("\nOn Windows, your hosts file is located at:")
            print(r"C:\Windows\System32\drivers\etc\hosts")
            
            return True
    except Exception as e:
        print(f"Error configuring DNS over HTTPS: {str(e)}")
    
    return False

if __name__ == "__main__":
    configure_dns_over_https()
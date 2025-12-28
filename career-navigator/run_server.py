#!/usr/bin/env python
"""
Run Career Navigator Flask app on all network interfaces.
Access from other devices using: http://<YOUR-IP>:5000
"""
import os
import sys
import socket

# Add project directory to path so modules can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'project'))

from app import app

def get_local_ip():
    """Get the local IP address of this machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    local_ip = get_local_ip()
    
    print("\n" + "="*70)
    print("🚀 CAREER NAVIGATOR SERVER STARTING")
    print("="*70)
    print(f"\n✅ Local Access:    http://127.0.0.1:5000")
    print(f"✅ Network Access:  http://{local_ip}:5000")
    print(f"\n📱 Access from other devices on your network using:")
    print(f"   http://{local_ip}:5000")
    print("\n⚠️  Note: Your firewall may block external access.")
    print("   If you can't access from other devices, check firewall settings.")
    print("="*70 + "\n")
    
    # Run on all interfaces (0.0.0.0) so it's accessible from other devices
    app.run(host="0.0.0.0", port=5000, debug=True)

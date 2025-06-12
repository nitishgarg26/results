import socket
import os
from dotenv import load_dotenv

def test_mysql_port_connectivity():
    """Test if MySQL port is accessible without using ping"""
    load_dotenv()
    
    host = os.getenv('DB_HOST')
    port = int(os.getenv('DB_PORT', 3306))
    
    try:
        # Test socket connection to MySQL port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # 10 second timeout
        
        result = sock.connect_ex((host, port))
        
        if result == 0:
            print(f"✅ Port {port} is open on {host}")
            return True
        else:
            print(f"❌ Port {port} is closed or filtered on {host}")
            return False
            
    except socket.gaierror as e:
        print(f"❌ DNS resolution failed for {host}: {e}")
        return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False
    finally:
        sock.close()

# Test connectivity
test_mysql_port_connectivity()

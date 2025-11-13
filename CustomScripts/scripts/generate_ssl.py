import sys
import secrets

def generate_ssl_key(size):
    key = secrets.token_bytes(size)
    hex_key = key.hex()
    
    print(f"Generated {size}-bit SSL Secret Key (hex): {hex_key}")
    return hex_key

if __name__ == "__main__":
    size = sys.argv[1] if len(sys.argv) > 1 else 32
    generate_ssl_key(size=int(size))

# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os
import socket
import subprocess
import sys
import time

def test_connection(host, port):
    try:
        # Try to create a socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 5 second timeout
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✓ Port {port} is open on {host}")
            return True
        else:
            print(f"✗ Port {port} is closed on {host}")
            print(f"Error code: {result}")
            return False
    except socket.gaierror:
        print(f"✗ Could not resolve hostname {host}")
        print("This suggests a DNS resolution issue")
        return False
    except socket.error as e:
        print(f"✗ Could not connect to {host}:{port}")
        print(f"Error: {str(e)}")
        return False

def diagnose_connection(url):
    print("\nRunning connection diagnostics...")
    
    # Parse the URL more carefully
    try:
        # Split the URL into components
        auth_part = url.split('@')[1]
        
        # Handle IPv6 addresses properly
        if '[' in auth_part:
            # Extract IPv6 address
            host = auth_part[auth_part.find('['): auth_part.find(']') + 1]
            # Remove brackets for connection testing
            clean_host = host.strip('[]')
            # Get port if it exists
            port_part = auth_part[auth_part.find(']') + 1:]
            port = int(port_part.split(':')[1].split('/')[0]) if ':' in port_part else 5432
        else:
            # Handle regular hostnames or IPv4
            host_part = auth_part.split('/')[0]
            if ':' in host_part:
                host, port = host_part.split(':')
                port = int(port)
            else:
                host = host_part
                port = 5432
    except Exception as e:
        print(f"Error parsing connection URL: {str(e)}")
        return
    
    print(f"\nTesting connection to {host}:{port}")
    
    # Try to ping the host
    try:
        print(f"\nPinging {host if '[' not in host else host.strip('[]')}...")
        if sys.platform == "win32":
            ping_cmd = ["ping", "-n", "1", host if '[' not in host else host.strip('[]')]
        else:
            ping_cmd = ["ping", "-c", "1", host if '[' not in host else host.strip('[]')]
        result = subprocess.run(ping_cmd, capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Ping failed: {str(e)}")
    
    # Test direct socket connection
    socket_result = test_connection(host if '[' not in host else host.strip('[]'), port)
    
    if not socket_result:
        print("\nPossible issues:")
        print("1. Firewall blocking outbound connection to port 5432/6543")
        print("2. DNS resolution problems")
        print("3. Host is not accepting connections from your IP")
        print("\nTroubleshooting steps:")
        print("1. Check if your firewall is blocking PostgreSQL connections")
        print("2. Try using the IP address directly instead of hostname")
        print("3. Verify the connection details in your Supabase dashboard")
        print("4. Make sure you're not on a restricted network (some corporate networks block database ports)")

# Debug connection string
db_url = settings.DATABASE_URL
print("\nConnection Details:")
print(f"Database URL: {db_url}")

# Run diagnostics before attempting connection
diagnose_connection(db_url)

# Handle connection configuration
if db_url:
    try:
        print("\nAttempting to create database engine...")
        engine = create_engine(
            db_url,
            connect_args={
                "connect_timeout": 60,  # Increased timeout for Render
                "application_name": "roofing-job-board",
                "sslmode": "require",
                "keepalives": 1,  # Enable keepalive
                "keepalives_idle": 30,  # Send keepalive every 30 seconds
                "keepalives_interval": 10,  # Retry keepalive every 10 seconds
                "keepalives_count": 5  # Retry 5 times before considering connection dead
            },
            pool_size=3,  # Reduced pool size for Render's free tier
            max_overflow=5,  # Reduced max overflow
            pool_timeout=60,  # Increased pool timeout
            pool_recycle=1800,  # Recycle connections after 30 minutes
            pool_pre_ping=True,  # Enable connection testing before use
            echo=True  # Log SQL commands
        )
        print("Engine created successfully")
    except Exception as e:
        print(f"\nError creating engine: {str(e)}")
        raise
else:
    raise ValueError("DATABASE_URL not found in environment variables")

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for database models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add this new function
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create database tables"""
    try:
        print("\nAttempting to create database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"\nError creating database tables: {str(e)}")
        raise
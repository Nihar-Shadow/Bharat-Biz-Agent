"""
Quick start script - Run this to start the server
"""
import subprocess
import sys
import os

def main():
    print("🚀 Starting SMB Business Automation Backend...")
    print("="*60)
    
    # Check if dependencies are installed
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✅ Dependencies found")
    except ImportError:
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    print("\n🗄️  Initializing database...")
    print("🌐 Starting server at http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\n" + "="*60)
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # Start the server
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])

if __name__ == "__main__":
    main()

import subprocess
import time
import sys
import os
import signal

def main():
    print("===================================================")
    print("   UDHAAR.AI - STARTING ALL SERVICES")
    print("===================================================")
    
    # Start backend server
    print("\n🚀 Starting Backend Server on http://localhost:8000...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        cwd=os.getcwd()
    )
    
    # Give backend time to start
    time.sleep(3)
    
    # Start frontend server
    print("🚀 Starting Frontend Server on http://localhost:3000...")
    frontend_process = subprocess.Popen(
        [sys.executable, "serve_frontend.py"],
        cwd=os.getcwd()
    )
    
    print("\n✅ All services started!")
    print("📝 Vendor:   http://localhost:3000")
    print("📝 Customer: http://localhost:3000/customer")
    print("📝 Backend:  http://localhost:8000")
    print("\n⚠️  Press Ctrl+C to stop all servers\n")
    
    try:
        # Monitoring loop
        while True:
            # Check if backend is running (it might restart itself due to reload, which is fine)
            if backend_process.poll() is not None:
                print("⚠️ Backend server stopped given this is unexpected. Restarting...")
                backend_process = subprocess.Popen(
                    [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
                    cwd=os.getcwd()
                )
            
            # Check if frontend is running
            if frontend_process.poll() is not None:
                print("⚠️ Frontend server stopped! Restarting...")
                frontend_process = subprocess.Popen(
                    [sys.executable, "serve_frontend.py"],
                    cwd=os.getcwd()
                )
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping all servers...")
        backend_process.terminate()
        frontend_process.terminate()
        
        # Wait for graceful shutdown
        try:
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
            frontend_process.kill()
        
        print("✅ Servers stopped successfully.")

if __name__ == "__main__":
    main()

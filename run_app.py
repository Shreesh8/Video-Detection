#!/usr/bin/env python3
"""
Script to run both backend and frontend servers
"""
import subprocess
import sys
import time
import os
from pathlib import Path

def run_backend():
    """Start the backend server"""
    print("Starting backend server...")
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("Error: backend directory not found")
        return None
    
    # Change to backend directory and start server
    process = subprocess.Popen(
        ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process

def run_frontend():
    """Start the frontend server"""
    print("Starting frontend server...")
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("Error: frontend directory not found")
        return None
    
    # Change to frontend directory and start server
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process

def main():
    print("Starting Video Object Detection Application...")
    
    # Start backend
    backend_process = run_backend()
    if not backend_process:
        print("Failed to start backend")
        return
    
    # Wait a bit for backend to start
    time.sleep(3)
    
    # Start frontend
    frontend_process = run_frontend()
    if not frontend_process:
        print("Failed to start frontend")
        backend_process.terminate()
        return
    
    print("\n" + "="*50)
    print("Application started successfully!")
    print("Backend: http://localhost:8000")
    print("Frontend: http://localhost:3000")
    print("Health check: http://localhost:8000/health")
    print("="*50)
    print("\nPress Ctrl+C to stop both servers...")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Servers stopped.")

if __name__ == "__main__":
    main() 
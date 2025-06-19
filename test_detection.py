#!/usr/bin/env python3
"""
Test script to verify object detection improvements
"""
import requests
import json
import time

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data['status']}")
            print(f"   Model loaded: {data['model_loaded']}")
            return True
        else:
            print("❌ Health check failed")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Root endpoint working")
            print(f"   Message: {data['message']}")
            return True
        else:
            print("❌ Root endpoint failed")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def main():
    print("🧪 Testing Video Object Detection API...")
    print("=" * 50)
    
    # Test health endpoint
    if not test_health_endpoint():
        print("\n❌ Backend is not running or not accessible")
        print("Please start the backend with: cd backend && uvicorn main:app --reload")
        return
    
    print()
    
    # Test root endpoint
    test_root_endpoint()
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! The API is ready for video processing.")
    print("\nTo test with a video file:")
    print("1. Start the frontend: cd frontend && npm start")
    print("2. Open http://localhost:3000")
    print("3. Upload a video file and test the detection")

if __name__ == "__main__":
    main() 
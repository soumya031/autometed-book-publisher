#!/usr/bin/env python3
"""
Test script for API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_api_endpoints():
    """Test all API endpoints"""
    print("Testing API endpoints...")
    
    # Test status endpoint
    print("\n1. Testing /api/status")
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test settings endpoint
    print("\n2. Testing /api/settings (GET)")
    try:
        response = requests.get(f"{BASE_URL}/api/settings")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test history endpoint
    print("\n3. Testing /api/history (GET)")
    try:
        response = requests.get(f"{BASE_URL}/api/history")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test search endpoint
    print("\n4. Testing /api/search (POST)")
    try:
        response = requests.post(f"{BASE_URL}/api/search", 
                               json={"query": "test", "search_type": "semantic"})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nAPI testing completed!")

if __name__ == "__main__":
    test_api_endpoints() 
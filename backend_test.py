#!/usr/bin/env python3
import requests
import json
import sys
import os
from datetime import datetime

# Get the backend URL from the frontend .env file
BACKEND_URL = "https://effd2069-8d31-4883-b892-f0c84ddbfa44.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

def test_api_health():
    """Test the API health check endpoint"""
    print("\n=== Testing API Health Check ===")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200 and "message" in response.json():
            print("✅ API Health Check: SUCCESS")
            return True
        else:
            print("❌ API Health Check: FAILED")
            return False
    except Exception as e:
        print(f"❌ API Health Check: ERROR - {str(e)}")
        return False

def test_contact_form_submission():
    """Test the contact form submission endpoint"""
    print("\n=== Testing Contact Form Submission ===")
    
    # Test data
    test_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "subject": "Test Contact Form",
        "message": "This is a test message from the automated testing script."
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/contact", json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            response_data = response.json()
            # Verify all fields are present in the response
            required_fields = ["id", "name", "email", "subject", "message", "timestamp"]
            all_fields_present = all(field in response_data for field in required_fields)
            
            # Verify the data matches what we sent
            data_matches = (
                response_data["name"] == test_data["name"] and
                response_data["email"] == test_data["email"] and
                response_data["subject"] == test_data["subject"] and
                response_data["message"] == test_data["message"]
            )
            
            if all_fields_present and data_matches:
                print("✅ Contact Form Submission: SUCCESS")
                return True
            else:
                print("❌ Contact Form Submission: FAILED - Response data doesn't match or missing fields")
                return False
        else:
            print(f"❌ Contact Form Submission: FAILED - Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Contact Form Submission: ERROR - {str(e)}")
        return False

def test_get_contact_messages():
    """Test the get contact messages endpoint"""
    print("\n=== Testing Get Contact Messages ===")
    
    try:
        response = requests.get(f"{API_BASE_URL}/contact")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            messages = response.json()
            print(f"Retrieved {len(messages)} contact messages")
            
            # Check if we have at least one message (from our previous test)
            if len(messages) > 0:
                # Verify the structure of the first message
                first_message = messages[0]
                required_fields = ["id", "name", "email", "subject", "message", "timestamp"]
                all_fields_present = all(field in first_message for field in required_fields)
                
                if all_fields_present:
                    print("✅ Get Contact Messages: SUCCESS")
                    return True
                else:
                    print("❌ Get Contact Messages: FAILED - Message missing required fields")
                    return False
            else:
                print("⚠️ Get Contact Messages: WARNING - No messages found, but endpoint works")
                return True  # Still consider it a success if the endpoint works but no data
        else:
            print(f"❌ Get Contact Messages: FAILED - Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get Contact Messages: ERROR - {str(e)}")
        return False

def run_all_tests():
    """Run all tests and return overall status"""
    print(f"Running backend API tests against {API_BASE_URL}")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Dictionary to track test results
    results = {}
    
    # Run tests
    results["api_health"] = test_api_health()
    results["contact_form"] = test_contact_form_submission()
    results["get_messages"] = test_get_contact_messages()
    
    # Print summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    # Overall result
    all_passed = all(results.values())
    print("\nOVERALL RESULT:", "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
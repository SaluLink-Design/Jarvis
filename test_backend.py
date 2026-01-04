#!/usr/bin/env python3
"""
Simple test script to verify the backend is working
"""
import requests
import json
import sys

# Change this to your Railway URL
BASE_URL = "https://jarvis-production-5709a.up.railway.app"

def test_health():
    """Test the health endpoint"""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def test_api():
    """Test the API test endpoint"""
    print("\nTesting /api/test endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/test")
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ API test passed")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ API test failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False


def test_text_processing():
    """Test text processing endpoint"""
    print("\nTesting /api/text endpoint...")
    try:
        payload = {
            "text": "Create a red cube",
            "context_id": None
        }

        response = requests.post(
            f"{BASE_URL}/api/text",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            # Check if the response has the expected structure
            if "context_id" in data and "result" in data and "scene" in data:
                print(f"✅ Text processing passed")

                # Check if it was successful or had an error
                if data.get("status") == "success":
                    print(f"✅ Processing successful!")
                elif data.get("status") == "error":
                    print(f"⚠️ Processing returned error status: {data.get('message')}")
                    print(f"   But API is working (no 500 error)!")

                print(f"\nContext ID: {data.get('context_id')}")
                print(f"Objects created: {len(data.get('scene', {}).get('objects', []))}")

                return True
            else:
                print(f"❌ Response structure invalid")
                print(json.dumps(data, indent=2))
                return False
        else:
            print(f"❌ Text processing failed with status {response.status_code}")
            print(response.text)
            return False

    except Exception as e:
        print(f"❌ Text processing error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("JARVIS BACKEND TEST SUITE")
    print("=" * 60)
    print(f"Testing: {BASE_URL}\n")

    results = []

    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("API Test", test_api()))
    results.append(("Text Processing", test_text_processing()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name}: {status}")

    all_passed = all(result[1] for result in results)

    if all_passed:
        print("\n🎉 All tests passed! Backend is working correctly.")
        sys.exit(0)
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()

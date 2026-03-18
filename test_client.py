import httpx
import time

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    with httpx.Client(base_url=base_url) as client:
        print("Testing Health Check:")
        r = client.get("/")
        print(f"Status: {r.status_code}")
        print("Response (HTML snippet):", r.text[:100].replace('\n', ' ') + "...")
        print("-" * 50)
        
        print("Testing Authentication:")
        r = client.post("/api/v1/auth/token", data={"username": "testuser", "password": "password"})
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            token = r.json()["access_token"]
            print("Successfully retrieved token.")
            print("-" * 50)
            
            headers = {"Authorization": f"Bearer {token}"}
            print("Testing Sector Analysis (Without Token):")
            r_unauth = client.get("/api/v1/analyze/pharmaceuticals")
            print(f"Status: {r_unauth.status_code} - Expected 401")
            print("-" * 50)
            
            print("Testing Sector Analysis (With Token & Mock data due to no key):")
            r_auth = client.get("/api/v1/analyze/pharmaceuticals", headers=headers)
            print(f"Status: {r_auth.status_code}")
            print(f"Content-Type: {r_auth.headers.get('content-type')}")
            print(f"Content-Disposition: {r_auth.headers.get('content-disposition')}")
            if r_auth.status_code == 200:
                print("\nSuccessfully generated report! Here is the snippet:")
                print(r_auth.text[:200] + "...\n")
            else:
                 print(r_auth.text)
            print("-" * 50)
            
            print("Testing Rate Limiting (Analyze Endpoint):")
            # We hit rate-limit (10/min defaults)
            for i in range(12):
                res = client.get("/api/v1/analyze/pharmaceuticals", headers=headers)
                if res.status_code == 429:
                    print(f"Request {i+1} got expected 429 Rate Limit Exceeded")
                    break
            print("-" * 50)
            
if __name__ == "__main__":
    test_api()

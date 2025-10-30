import requests

# Test recipe search
try:
    response = requests.get('http://localhost:8000/recipes?s=rice,milk,carrot')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

import requests
import json

response = requests.get("https://api.fda.gov/drug/label.json?search=aspirin&limit=1")
data = response.json()

print("Drug:", data['results'][0]['openfda']['brand_name'])
print("Uses:", data['results'][0]['indications_and_usage'][:200])
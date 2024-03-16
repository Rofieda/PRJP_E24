import requests

# Define the URL of your API endpoint
url = 'http://127.0.0.1:8000/api/projects/'

# Define the payload (data) to send in the request
payload = {
    "titre_projet": "Projet2cp",
    "chef_de_projet": "Rofieda",
    "domaine": "La recherche scientifique",
    "annee_debut": 2024,
    "annee_fin": 2024
}

# Send a POST request to the API endpoint with the payload
response = requests.post(url, json=payload)

# Print the response from the server
print(response.text)

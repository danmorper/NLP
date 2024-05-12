import requests
import os

def download_pdf(url: str):
    base_url = "https://boe.es"
    full_url = base_url + url 
    filename = full_url.split("/")[-1]
    path = f"pdfs/{filename}"

    if not os.path.exists('pdfs'):
        os.makedirs('pdfs')

    if os.path.exists(path):
        print(f"PDF {filename} already downloaded.")
    else:
        response = requests.get(full_url)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                f.write(response.content)
            print(f"PDF {filename} downloaded successfully.")
        else:
            print("Failed to download PDF. Status code:", response.status_code)


# Download all pdfs from resoluciones_50_embeddings.json

import json

def download_all_resoluciones():
    with open("licitaciones.json", "r") as file:
        resoluciones = json.load(file)

    for _, items in resoluciones.items():
        for item in items:
            url = item[2]
            download_pdf(url)
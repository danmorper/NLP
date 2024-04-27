import requests

def download_pdf(url: str = "/boe/dias/2012/03/08/pdfs/BOE-B-2012-7789.pdf"):

    url = "https://boe.es" + url 
    filename = url.split("/")[-1]

    response = requests.get(url)

    if response.status_code == 200:
        path = "pdfs/" + filename
        with open(path, 'wb') as f:
            f.write(response.content)
        print(f"PDF {filename} downloaded successfully.")
    else:
        print("Failed to download PDF. Status code:", response.status_code)

# Download all pdfs from resoluciones_50_embeddings.json

import json

def download_all_resoluciones():
    with open("resoluciones_50_embeddings.json", "r") as file:
        resoluciones = json.load(file)

    for _, items in resoluciones.items():
        for item in items:
            url = item[3]
            download_pdf(url)
import os
import requests


def download_url_to_file(url, filename):
    if not os.path.exists(filename):
        response = requests.get(url)

        if response.status_code == 200:
            with open(filename, "wb") as file:
                file.write(response.content)
            return True
        else:
            print("Failed to download file.")
            return False
    return True

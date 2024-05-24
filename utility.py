import os
import base64
from openai import OpenAI
import requests

def format_data_for_openai(diffs, readme_content, commit_messages):
    prompt = None

    # Combine the changes into a string with clear delineation.

    # Combine all commit messages

    # Decode the README content

    # Construct the prompt with clear instructions for the LLM.

    return prompt

def call_openai(prompt):
    pass

def update_readme_and_create_pr(repo, updated_readme, readme_sha):
    pass


def download_url_to_file(url, filename):
    if not os.path.exists(filename):
        response = requests.get(url)
        
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            return True
        else:
            print('Failed to download file.')
            return False
    return True
import os

import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_latest_release(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("tag_name")
    else:
        print(f"Error fetching release: {response.status_code}")
        return None


if __name__ == "__main__":
    print("Building the project...")
    latest_tag = get_latest_release("kaitranntt", "ccs")
    if latest_tag:
        print(f"Latest tag: {latest_tag}")

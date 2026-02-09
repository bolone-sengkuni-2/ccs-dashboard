import os
import shutil
import subprocess
import sys

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


def clone_repo(tag):
    print(f"Cloning repository at tag {tag}...")
    if os.path.exists("./temp_repo"):
        shutil.rmtree("./temp_repo")
    try:
        subprocess.check_call(
            [
                "git",
                "clone",
                "--branch",
                tag,
                "--depth",
                "1",
                "https://github.com/kaitranntt/ccs.git",
                "./temp_repo",
            ]
        )
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        sys.exit(1)


def build_and_push_docker(tag):
    print(f"Building Docker image for tag {tag}...")
    image_name = "ghcr.io/bolone-sengkuni-2/ccs-dashboard"

    try:
        # Build
        subprocess.check_call(
            [
                "docker",
                "build",
                "-t",
                f"{image_name}:{tag}",
                "-t",
                f"{image_name}:latest",
                "./temp_repo/docker",
            ]
        )
        # Push
        print(f"Pushing Docker image {image_name}:{tag}...")
        subprocess.check_call(["docker", "push", f"{image_name}:{tag}"])
        print(f"Pushing Docker image {image_name}:latest...")
        subprocess.check_call(["docker", "push", f"{image_name}:latest"])
    except subprocess.CalledProcessError as e:
        print(f"Error building or pushing Docker image: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("Building the project...")
    latest_tag = get_latest_release("kaitranntt", "ccs")
    if latest_tag:
        print(f"Latest tag: {latest_tag}")
        clone_repo(latest_tag)
        build_and_push_docker(latest_tag)
    else:
        print("Failed to get latest tag, exiting.")
        sys.exit(1)

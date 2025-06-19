# dfs_client.py

import requests

NAMING_SERVER_URL = "http://127.0.0.1:8000"


def create_file(filename, content):
    response = requests.post(
        f"{NAMING_SERVER_URL}/create_file/",
        json={"filename": filename, "content": content},
    )
    print(response.json())


def read_file(filename):
    response = requests.get(
        f"{NAMING_SERVER_URL}/read_file/", params={"filename": filename}
    )
    if response.status_code == 200:
        print("File content:")
        print(response.text)
    else:
        print(response.json())


def delete_file(filename):
    response = requests.post(
        f"{NAMING_SERVER_URL}/delete_file/", json={"filename": filename}
    )
    print(response.json())


def get_file_size(filename):
    response = requests.get(
        f"{NAMING_SERVER_URL}/get_file_size/", params={"filename": filename}
    )
    print(response.json())


if __name__ == "__main__":
    create_file("example.txt", "This is a test.")
    read_file("example.txt")
    get_file_size("example.txt")
    delete_file("example.txt")

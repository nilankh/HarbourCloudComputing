# import requests

# NAMING_SERVER = 'http://localhost:8000'

# def create_file(filename, content):
#     resp = requests.post(f"{NAMING_SERVER}/create_file/", json={
#         'filename': filename,
#         'content': content
#     })
#     print(resp.json())

# def read_file(filename):
#     resp = requests.get(f"{NAMING_SERVER}/read_file/", params={'filename': filename})
#     print(resp.text)

# # Example usage
# if __name__ == "__main__":
#     create_file("hello.txt", "This is a test file content. It will be split into chunks.")

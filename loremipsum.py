import requests

# Lorem Ipsum API, get one short paragraph
url = "http://loripsum.net/api/1/short/plaintext"
text = requests.get(url).text
# Remove unused lines
text = text.split('\n')[0]

print(text)
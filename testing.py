import requests


with open('61oAh3XrX+L._AC_UF894,1000_QL80_.jpg', 'rb') as file:

    response = requests.post("https://telegra.ph/upload", files={"file": file})

    print("https://telegra.ph" + response.json())
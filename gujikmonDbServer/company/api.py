import requests

key = "WNKMX52ZNNR93DRDACH6X2VR1HJ"
url = "http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey={}&callTp=L&returnType=XML&startPage=1&display=10".format(key)

content = requests.get(url).content
print(content)
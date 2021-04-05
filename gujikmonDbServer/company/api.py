import requests, xmltodict, json

key = "WNKMX52ZNNR93DRDACH6X2VR1HJ"
url_recruit = "http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey={}&callTp=L&returnType=XML&startPage=1&display=10&dtlSmlgntYn=Y".format(key)

content_recruit = requests.get(url_recruit).content
dict = xmltodict.parse(content_recruit)
jsonString = json.dumps(dict['wantedRoot']['wanted'], ensure_ascii=False)
jsonObj = json.loads(jsonString)

# for i in jsonObj:
#     print(i)

jsonString_recuit = json.dumps(dict['wantedRoot']['total'], ensure_ascii=False)
print("강소기업 채용공고 수" + jsonString_recuit)


url_corpor = "http://openapi.work.go.kr/opi/smallGiants/smallGiants.do?authKey={}&returnType=XML".format(key)

content_copor = requests.get(url_corpor).content
dict_corpor = xmltodict.parse(content_copor)
jsonString_copor = json.dumps(dict_corpor['smallGiantsList']['total'], ensure_ascii=False)
print("강소기업 수" + jsonString_copor)

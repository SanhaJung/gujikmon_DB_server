import requests, xmltodict, json

key = "WNKMX52ZNNR93DRDACH6X2VR1HJ"
page = 1

recruite_list = []
recruite_total = 0
while 1:
    url_recruit = "http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey={}&callTp=L&returnType=XML&startPage={}&display=100&dtlSmlgntYn=Y".format(key, page)

    content_recruit = requests.get(url_recruit).content
    dict = xmltodict.parse(content_recruit)
    jsonString = json.dumps(dict['wantedRoot'], ensure_ascii=False)
    jsonObj = json.loads(jsonString)
    

    # print(jsonObj)

    # data가 없는 page를 만나면 반복을 멈춤
    if 'messageCd' in list(jsonObj.keys()):
        if jsonObj['messageCd'] == "006":
            break

    recruite_list.extend(jsonObj['wanted'])
    recruite_total = jsonObj['total']

    page += 1

print(page)
print(len(recruite_list))
print(recruite_total)
if len(recruite_list) == int(recruite_total):
    print('{}개의 채용정보를 불러왔습니다.'.format(recruite_total))
else:
    print("불러온 채용정보의 개수가 맞지 않습니다.")


with open('./sg_recruite.json', 'w', encoding='utf-8') as make_file:
    json.dump(recruite_list, make_file, ensure_ascii=False, indent='\t')

# jsonString_recuit = json.dumps(dict['wantedRoot']['total'], ensure_ascii=False)
# print("강소기업 채용공고 수" + jsonString_recuit)

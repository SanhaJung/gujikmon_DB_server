import requests, xmltodict, json

def recrut_store_api():
    print('recrut_store  start!!!')
    key = "WNKMX52ZNNR93DRDACH6X2VR1HJ"

    # 채용정보 API는 page별로 data 받아옴
    page = 1

    recruite_list = []
    # data 없는 페이지 만날때까지 반복
    while 1:
        # 한 페이지에 100개씩 받아옴
        url_recruit = "http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey={}&callTp=L&returnType=XML&startPage={}&display=100&dtlSmlgntYn=Y".format(key, page)

        content_recruit = requests.get(url_recruit).content
        dict = xmltodict.parse(content_recruit)
        jsonString = json.dumps(dict['wantedRoot'], ensure_ascii=False)
        jsonObj = json.loads(jsonString)

        # data가 없는 page를 만나면 반복을 멈춤
        if 'messageCd' in list(jsonObj.keys()):
            if jsonObj['messageCd'] == "006":
                break

        recruite_list.extend(jsonObj['wanted'])
        page += 1
    print('recrut_store  end!!!')
    with open('../data/sg_recruit_test.json', 'w', encoding='utf-8') as make_file:
        json.dump(recruite_list, make_file, ensure_ascii=False, indent='\t')
    return recruite_list
    

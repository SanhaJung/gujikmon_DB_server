import requests, xmltodict, json

def sg_store_api():
    print('sg_store  start!!!')
    key = "WNKMX52ZNNR93DRDACH6X2VR1HJ"
    # 강소기업 API
    url_corpor = "http://openapi.work.go.kr/opi/smallGiants/smallGiants.do?authKey={}&returnType=XML".format(key)
    content_copor = requests.get(url_corpor).content
    dict_corpor = xmltodict.parse(content_copor)
    jsonString_copor = json.dumps(dict_corpor['smallGiantsList']['smallGiant'], ensure_ascii=False)
    smallGiant_list = json.loads(jsonString_copor) # 강소기업 리스트(json)

    # 청년친화 API
    url_young = "http://openapi.work.go.kr/opi/smallGiants/smallGiantsYoung.do?authKey={}&returnType=XML".format(key)
    content_young = requests.get(url_young).content
    dict_young = xmltodict.parse(content_young)
    jsonString_young = json.dumps(dict_young['smallGiantsList']['smallGiant'], ensure_ascii=False)
    smallGiant_young_list = json.loads(jsonString_young) # 청년친화 강소기업 리스트(json)

    # 지역 코드
    with open('./region_code.json', 'r', encoding='UTF-8') as f:
        json_region_code = json.load(f)

    # 강소기업이면서 청년친화인 기업에 브랜드 네임(청년친화 인증) 추가
    for i in smallGiant_young_list:
        for e in smallGiant_list:
            if e['regionCd'] == 'NULL':
                    e['regionNm'] = e['coAddr'].split(' ')[0] +' '+e['coAddr'].split(' ')[1]
                    for k in json_region_code.keys():
                        if json_region_code[k][0] ==  e['regionNm']:
                            e['regionCd'] = k
            if e['busiNo'] == i['busiNo']:
                e['sgBrandNm2'] = '청년친화'
                break
    print('sg_store  end!!!')

    # with open('../data/sg_test.json', 'w', encoding='utf-8') as make_file:
    #     json.dump(smallGiant_list, make_file, ensure_ascii=False, indent='\t')

    return smallGiant_list
    # # 청년친화 키값 추가한 강소기업json
    # with open('./data/origin/sg.json', 'w', encoding='utf-8') as make_file:
    #     json.dump(smallGiant_list, make_file, ensure_ascii=False, indent='\t')

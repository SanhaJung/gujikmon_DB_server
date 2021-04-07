import requests, xmltodict, json



key = "WNKMX52ZNNR93DRDACH6X2VR1HJ"
url_corpor = "http://openapi.work.go.kr/opi/smallGiants/smallGiants.do?authKey={}&returnType=XML".format(key)
url_young = "http://openapi.work.go.kr/opi/smallGiants/smallGiantsYoung.do?authKey={}&returnType=XML".format(key)


content_copor = requests.get(url_corpor).content
dict_corpor = xmltodict.parse(content_copor)
jsonString_copor = json.dumps(dict_corpor['smallGiantsList']['smallGiant'], ensure_ascii=False)
smallGiant_list = json.loads(jsonString_copor) 
print(len(smallGiant_list)) 

# print(smallGiant_list[0].keys())
# ['selYear', 'sgBrandNm', 'coNm', 'busiNo', 'reperNm', 'superIndTpCd', 'superIndTpNm', 
# 'indTpCd', 'indTpNm', 'coTelNo', 'regionCd', 'regionNm', 'coAddr', 'coMainProd',
#  'coHomePage', 'alwaysWorkerCnt', 'smlgntCoClcd']

brandcnt = {"기술혁신":0, "경영혁신":0, "가족친화":0, "강소기업":0}

for element in smallGiant_list:
    if element['sgBrandNm'] == "기술혁신형 중소기업(이노비즈)":
        brandcnt["기술혁신"] += 1
    elif element['sgBrandNm'] ==  "경영혁신형 중소기업(메인비즈)":
        brandcnt["경영혁신"] += 1
    elif element['sgBrandNm'] ==  "가족친화기업":
        brandcnt["가족친화"] += 1
    else:
        brandcnt["강소기업"] += 1

print(brandcnt)
total = brandcnt['기술혁신']+brandcnt['경영혁신']+brandcnt['가족친화']+brandcnt['강소기업']
print(total)

content_young = requests.get(url_young).content
dict_young = xmltodict.parse(content_young)
jsonString_young = json.dumps(dict_young['smallGiantsList']['smallGiant'], ensure_ascii=False)
smallGiant_young_list = json.loads(jsonString_young) 
print(len(smallGiant_young_list)) 

c = 0
only_young_list = []  # 청년친화 강소기업 dict 저장 list

for i in smallGiant_young_list:
    for e in smallGiant_list:
        if e['busiNo'] == i['busiNo']:
            e['sgBrandNm2'] = '청년친화'
            c += 1
            break
    else:
        only_young_list.append(i)

print(c)
print(len(only_young_list))



# 청년친화 키값 추가한 강소기업json
with open('./sg.json', 'w', encoding='utf-8') as make_file:
    json.dump(smallGiant_list, make_file, ensure_ascii=False, indent='\t')

# 강소기업이 아닌 청년친화
with open('./sg_young.json', 'w', encoding='utf-8') as make_file:
    json.dump(only_young_list, make_file, ensure_ascii=False, indent='\t')


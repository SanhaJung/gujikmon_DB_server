import json

# 강소기업 정보
with open('./sg.json', 'r', encoding='UTF-8') as f:
    json_data_sg = json.load(f)
# dict_sg = json.dumps(json_data_sg, ensure_ascii=False, indent='\t')
# print(type(dict_sg))
print(type(json_data_sg[0]))
print(json_data_sg[0])

# 청년친화 기업 정보
with open('./sg_young.json', 'r', encoding='UTF-8') as f:
    json_data_sg_young = json.load(f)
# dict_sg = json.dumps(json_data_sg, ensure_ascii=False, indent='\t')
# print(type(dict_sg))
print(type(json_data_sg_young[0]))
print(json_data_sg_young[0])

# 채용정보 
with open('./sg_recruite.json', 'r', encoding='UTF-8') as f:
    json_data_sg_recruite = json.load(f)
# dict_sg_recruite = json.dumps(json_data_sg_recruite, ensure_ascii=False, indent='\t')
# print(type(json_data_sg_recruite))
print(type(json_data_sg_recruite[0]))
print(json_data_sg_recruite[0])

# 구인 인증 번호 리스트 생성
recruit_no_list = []
for e in json_data_sg_recruite:
    recruit_no_list.append(e['wantedAuthNo'])
# print(recruit_no_list)
print(type(recruit_no_list[0]))

# 회사명 완전 일치
# for i in json_data_sg_recruite:
#     for j in json_data_sg:
#         if i['company'] == j['coNm']:
#             recruit_no_list.remove(i['wantedAuthNo'])
#             break
#     # else:
#     #     print(i['company'])
# print(len(recruit_no_list))

# 주식회사, (주) 삭제하고 비교
for i in json_data_sg_recruite:
    for j in json_data_sg:
        if i['company'] == j['coNm']:
            recruit_no_list.remove(i['wantedAuthNo'])
            break
    else:
        if '(주)' in i['company']:
            re_name = i['company'].replace('(주)','')
        elif '주식회사' in i['company']:
            re_name = i['company'].replace('주식회사','')
        elif '주)' in i['company']:
            re_name = i['company'].replace('주)','')
        elif '(주' in i['company']:
            re_name = i['company'].replace('주)','')
        elif '㈜' in i['company']:
            re_name = i['company'].replace('주)','')

        temp = re_name
        temp2 = ""
        if "(" in temp:
            for c in temp :
                if c != "(":
                    temp2 += c
                else:
                    break
            re_name = temp2


        for j in json_data_sg:
            if re_name.replace(" ", "") in j['coNm']:
                recruit_no_list.remove(i['wantedAuthNo'])
                break
        else:
            print(i['company'])

print(recruit_no_list)
print(len(recruit_no_list))



# for i in json_data_sg_recruite:
#     for j in json_data_sg_young:
#         if i['company'] == j['coNm']:
#             recruit_no_list.remove(i['wantedAuthNo'])
#             break

# print(recruit_no_list)
# print(len(recruit_no_list))
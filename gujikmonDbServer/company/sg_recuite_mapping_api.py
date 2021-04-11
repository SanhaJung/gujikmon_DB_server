import json
import csv
import requests, urllib

# 강소기업 정보
with open('./sg.json', 'r', encoding='UTF-8') as f:
    json_data_sg = json.load(f)
# print(type(json_data_sg[0]))
# print(json_data_sg[0])

# 청년친화 기업 정보
# with open('./sg_young.json', 'r', encoding='UTF-8') as f:
#     json_data_sg_young = json.load(f)
# print(type(json_data_sg_young[0]))
# print(json_data_sg_young[0])

# 채용정보 
with open('./sg_recruite.json', 'r', encoding='UTF-8') as f:
    json_data_sg_recruite = json.load(f)
# print(type(json_data_sg_recruite[0]))
# print(json_data_sg_recruite[0])

# {
#     "sg": [
#         {
#             "busiNo" : "사업자 등록 번호",
#             "coNm": "기업명(string)",
#             "coAddr": "기업 주소",
            
#             "superRegionCd": 1100,
#             "superRegionNm": "지역코드 이름(상)", 
#             "regionCd": 1121,
#             "regionNm": "지역코드이름 (중)",

#             "x": "위도",  //  카카오 api 주소 검색으로 받아와야함
#             "y": "경도", 

#             "superIndTpCd": "A", 
#             "superIndTpNm": "업종 코드 이름(상)",
#             "indTpCd": "1234",
#             "indTpNm": "업종코드 이름(중)",

#             "coMainProd": "주요생산 품목",

#             "coHomePage": "기업 홈페이지 url",
#             "allwaysWorkerCnt": "상시 근로자수",

#             "sgBrandNm": ['강소기업', '청년친화', ... ],
#             "recruitement": False,
#             "info":[
#                 {
#                     "wantedAuthNo": "공고번호"
#                     "title": "채용공고 명",
#                     "wantedInfoUrl": "채용공고 웹 url",
#                     "wantedMobileInfoUrl": "채용공고 모바일 url"
#                 },
#                 ...
#             ]
#         }, 
#         ...
#     ], 

#     "sg_young": [
#         {
#             "busiNo" : "사업자 등록 번호",
#             "coNm": "기업명(string)",
#             "coAddr": "기업 주소",  // 카카오 api 키워드(기업명) 검색으로 받아와야함

#             "superIndTpCd": "A", 
#             "superIndTpNm": "업종 코드 이름(상)",
#             "indTpCd": "1234",
#             "indTpNm": "업종코드 이름(중)",

#             "superRegionCd": 1100,
#             "superRegionNm": "지역코드 이름(상)", 
#             "regionCd": 1121,
#             "regionNm": "지역코드이름 (중)",
#         }
#     ]
# }



db_insert_dict = {
    "sg": [],
    "sg_young": []
}
e_addr = []
e_coMainprod = []
e_homePage = []
e_workerCnt = []
e_regionNm = []
#  j: 강소기업 dict
# 강소기업 정보 add
for j in json_data_sg:
    temp_dict = {}
    temp_dict['busiNo'] = j['busiNo']
    temp_dict['coNm'] = j['coNm']
    try:
        temp_dict['coAddr'] = j['coAddr']
    except:
        temp_dict['coAddr'] = ""
        tmp = []
        tmp.append(j['busiNo'])
        tmp.append(j['coNm'])
        e_addr.append(tmp)

    temp_dict['superRegionCd'] = ""
    temp_dict['superRegionNm'] = ""
    temp_dict['regionCd'] = j['regionCd']
    try:
        temp_dict['regionNm'] = j['regionNm']
    except:
        temp_dict['regionNm'] = ""
        tmp = []
        tmp.append(j['busiNo'])
        tmp.append(j['coNm'])
        e_regionNm.append(tmp)
    temp_dict['x'] = ""
    temp_dict['y'] = ""
    temp_dict['superIndTpCd'] = j['superIndTpCd']
    temp_dict['superIndTpNm'] = j['superIndTpNm']
    temp_dict['indTpCd'] = j['indTpCd']
    temp_dict['indTpNm'] = j['indTpNm']

    try:
        temp_dict['coMainProd'] = j['coMainProd']
    except:
        temp_dict['coMainProd'] = ""
        tmp = []
        tmp.append(j['busiNo'])
        tmp.append(j['coNm'])
        e_coMainprod.append(tmp)

    try:
        temp_dict['coHomePage'] = j['coHomePage']
    except:
        temp_dict['coHomePage'] = ""
        tmp = []
        tmp.append(j['busiNo'])
        tmp.append(j['coNm'])
        e_homePage.append(tmp)
    try:
        temp_dict['allwaysWorkerCnt'] = j['alwaysWorkerCnt']
    except:
        temp_dict['allwaysWorkerCnt'] = ""
        tmp = []
        tmp.append(j['busiNo'])
        tmp.append(j['coNm'])
        e_workerCnt.append(tmp)

    temp_dict['sgBrandNm'] = []
    temp_dict['sgBrandNm'].append('강소기업')
    if 'sgBrandNm2' in j.keys():
        temp_dict['sgBrandNm'].append('청년친화')

    if j['sgBrandNm'] == "기술혁신형 중소기업(이노비즈)":
        temp_dict['sgBrandNm'].append('기술혁신')
    elif j['sgBrandNm'] ==  "경영혁신형 중소기업(메인비즈)":
        temp_dict['sgBrandNm'].append('경영혁신')
    elif j['sgBrandNm'] ==  "가족친화기업":
        temp_dict['sgBrandNm'].append('가족친화')

    temp_dict['recruitement'] = False
    temp_dict['info'] = []

# 채용정보 추가 참고 코드
    # temp_dict['recruitement'] = False
    # temp_dict['info'] = []
    db_insert_dict['sg'].append(temp_dict)

# print(len(e_coMainprod))
# print(len(e_addr))
# print(len(e_homePage))
# print(len(e_workerCnt))
# print(len(e_regionNm))



# ---------------------------------------------------------------------------
# 구인 인증 번호 리스트 생성
recruit_no_list = []
for e in json_data_sg_recruite:
    recruit_no_list.append(e['wantedAuthNo'])
# print(recruit_no_list)
# print(type(recruit_no_list[0]))

# 회사명 완전 일치
# for i in json_data_sg_recruite:
#     for j in json_data_sg:
#         if i['company'] == j['coNm']:
#             recruit_no_list.remove(i['wantedAuthNo'])
#             break
#     # else:
#     #     print(i['company'])
# print(len(recruit_no_list))

# 기업정보, 채용정보 매칭하여 채용여부 및 채용정보 insert
for i in json_data_sg_recruite:
    for j in db_insert_dict['sg']:
        if i['company'] == j['coNm'] and i['region'] == j['regionNm']:
            recruit_no_list.remove(i['wantedAuthNo'])
            j['recruitement'] = True
            temp_recruite_dict = {}
            temp_recruite_dict['wantedAuthNo'] = i['wantedAuthNo']
            temp_recruite_dict['title'] = i['title']
            temp_recruite_dict['wantedInfoUrl'] = i['wantedInfoUrl']
            temp_recruite_dict['wantedMobileInfoUrl'] = i['wantedMobileInfoUrl']
            j['info'].append(temp_recruite_dict)

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

        for j in db_insert_dict['sg']:
            if re_name.replace(" ", "") in j['coNm'] and i['region'] == j['regionNm']:
                recruit_no_list.remove(i['wantedAuthNo'])
                j['recruitement'] = True
                temp_recruite_dict = {}
                temp_recruite_dict['wantedAuthNo'] = i['wantedAuthNo']
                temp_recruite_dict['title'] = i['title']
                temp_recruite_dict['wantedInfoUrl'] = i['wantedInfoUrl']
                temp_recruite_dict['wantedMobileInfoUrl'] = i['wantedMobileInfoUrl']
                j['info'].append(temp_recruite_dict)
                break
        # else:
            # print(i['company'])

# print(recruit_no_list)
# print(len(recruit_no_list))


with open('./region_code.json', 'r', encoding='UTF-8') as f:
    json_region_code = json.load(f)
# 지역코드(상) 추가, regionNm(중) 보충 알고리즘
for j in db_insert_dict['sg']:
    try:
        tmp_list = json_region_code[j['regionCd']]
        j['regionNm'] = tmp_list[0]
        j['superRegionCd'] = tmp_list[1]['superRegionCd']
        j['superRegionNm'] = tmp_list[1]['superRegionNm']
    except:
        j['coNm']


'''
 카카오 geodata 가져오기 
 error  구분은 if ( 'error_type' in r )
 위도, 경도 위치는 
 r['documents'][0]['road_address']['x']
 r['documents'][0]['road_address']['y']
'''
def getGPS_coordinate_for_KAKAO(address, MYAPP_KEY):

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)
    }
    address = address.encode("utf-8")

    p = urllib.parse.urlencode(
        {
            'query': address
        }
    )
    result = requests.get("https://dapi.kakao.com/v2/local/search/address.json", headers=headers, params=p)
    return result.json()

db_insert_dict_only_xy_ex = {
    "sg": [],
    "sg_young": []
}
# 주소로 좌표 넣기
for j in db_insert_dict['sg']:
    temp_GPS_dict = getGPS_coordinate_for_KAKAO(j['coAddr'], '4a525c4285544fd8b63ed453df03c0e5')
    try:
        if len(temp_GPS_dict['documents']) == 0:
            pass
            # print('len0: {}'.format(j['coNm']))
        elif len(temp_GPS_dict['documents']) == 1:
            j['x'] = temp_GPS_dict['documents'][0]['x']
            j['y'] = temp_GPS_dict['documents'][0]['y']
            db_insert_dict_only_xy_ex['sg'].append(j)
        else:
            pass
            # print('len{}: {}'.format(len(temp_GPS_dict['documents']) ,j['coNm']))
    except:
        pass
        # print(temp_GPS_dict)



with open('./db_insert_only_xy_ex.json', 'w', encoding='utf-8') as make_file:
    json.dump(db_insert_dict_only_xy_ex, make_file, ensure_ascii=False, indent='\t')
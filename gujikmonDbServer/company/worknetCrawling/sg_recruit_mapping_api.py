import json
import csv
import requests, urllib

from .sg_store_api import sg_store_api
from .recuit_store_api import recrut_store_api



def sg_recrut_mapping_api():
    print('sg_recrut_mapping_api  start!!!')
    # 강소기업 정보
    json_data_sg = sg_store_api()
    # with open('./data/origin/sg.json', 'r', encoding='UTF-8') as f:
    #     json_data_sg = json.load(f)

    # 채용정보 
    json_data_sg_recruite = recrut_store_api()
    # with open('./data/origin/sg_recruit.json', 'r', encoding='UTF-8') as f:
    #     json_data_sg_recruite = json.load(f)

    # 기업정보, 채용정보 저장 json
    db_insert_dict = { "sg": [] }

    # 강소기업 정보 저장
    for j in json_data_sg:
        temp_dict = {}
        temp_dict['busiNo'] = j['busiNo']
        temp_dict['coNm'] = j['coNm']
        try:
            temp_dict['coAddr'] = j['coAddr']
        except:
            temp_dict['coAddr'] = ""
        temp_dict['superRegionCd'] = ""
        temp_dict['superRegionNm'] = ""
        temp_dict['regionCd'] = j['regionCd']
        try:
            temp_dict['regionNm'] = j['regionNm']
        except:
            temp_dict['regionNm'] = ""
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
        try:
            temp_dict['coHomePage'] = j['coHomePage']
        except:
            temp_dict['coHomePage'] = ""
        try:
            temp_dict['allwaysWorkerCnt'] = j['alwaysWorkerCnt']
        except:
            temp_dict['allwaysWorkerCnt'] = ""
        # 기업 인증 브랜드 네임 저장
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

        db_insert_dict['sg'].append(temp_dict)

    # 기업정보, 채용정보 매칭하여(기업명, 지역코드)  채용정보 저장
    for i in json_data_sg_recruite:
        for j in db_insert_dict['sg']:
            # 기업명, 지역코드 일치
            if i['company'] == j['coNm'] and i['region'] == j['regionNm']:
                j['recruitement'] = True
                temp_recruite_dict = {}
                temp_recruite_dict['wantedAuthNo'] = i['wantedAuthNo']
                temp_recruite_dict['title'] = i['title']
                temp_recruite_dict['wantedInfoUrl'] = i['wantedInfoUrl']
                temp_recruite_dict['wantedMobileInfoUrl'] = i['wantedMobileInfoUrl']
                j['info'].append(temp_recruite_dict)
                break
        # 기업명 주요 용어 일치, 지역코드 일치
        else:
            re_name = ''
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
            # 기업명에 설명 부분 삭제
            temp = re_name
            temp2 = ""
            if "(" in temp:
                for c in temp :
                    if c != "(":
                        temp2 += c
                    else:
                        break
                re_name = temp2

            # 기업명에서 의미없는 빈칸 삭제
            for j in db_insert_dict['sg']:
                if re_name.replace(" ", "") in j['coNm'] and i['region'] == j['regionNm']:
                    j['recruitement'] = True
                    temp_recruite_dict = {}
                    temp_recruite_dict['wantedAuthNo'] = i['wantedAuthNo']
                    temp_recruite_dict['title'] = i['title']
                    temp_recruite_dict['wantedInfoUrl'] = i['wantedInfoUrl']
                    temp_recruite_dict['wantedMobileInfoUrl'] = i['wantedMobileInfoUrl']
                    j['info'].append(temp_recruite_dict)
                    break


    # 지역코드(상) 추가, regionNm(중) 보충 알고리즘
    with open('../data/region_code.json', 'r', encoding='UTF-8') as f:
        json_region_code = json.load(f)

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

    db_insert_dict_only_xy_ex = { "sg": [] }
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

        except:
            pass
    print('sg_recrut_mapping_api  end!!!')

    with open('../data/db_update_data_test_final.json', 'w', encoding='utf-8') as make_file:
        json.dump(db_insert_dict_only_xy_ex, make_file, ensure_ascii=False, indent='\t')

    return db_insert_dict_only_xy_ex
    # with open('./data/DB_insert_data/db_insert_data2.json', 'w', encoding='utf-8') as make_file:
    #     json.dump(db_insert_dict_only_xy_ex, make_file, ensure_ascii=False, indent='\t')
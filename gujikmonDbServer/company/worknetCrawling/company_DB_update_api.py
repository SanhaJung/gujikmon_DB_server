
from django import db
from ..models import Companies
from .sg_recruit_mapping_api import sg_recrut_mapping_api
import json

def company_DB_update():
    # update 할 데이터
    update_data = sg_recrut_mapping_api()
    # with open('../data/db_update_data_test_final.json', 'r', encoding='UTF-8') as f:
    #     update_data = json.load(f)

    for company in update_data['sg']:
        co_busiNo = company['busiNo']
        co_recruitement = company['recruitement']
        co_info = company['info']
        # update데이터와 db 저장 데이터 비교하여 update
        db_origin = Companies.objects.get(busiNo=co_busiNo)
        # 둘다 채용중일 경우
        if  co_recruitement==True and co_recruitement==db_origin.recruitment:
            db_origin.info = []
            for up_info_e in co_info:
                db_origin.info.append({'wantedAuthNo':up_info_e['wantedAuthNo'],
                                        'title':up_info_e['title'],
                                        'wantedInfoUrl':up_info_e['wantedInfoUrl'],
                                        'wantedMobileInfoUrl':up_info_e['wantedMobileInfoUrl']})
            db_origin.save()
        # 채용 여부가 다를경우
        # update data  |  origin db
        #      O              X
        #      X              O
        elif co_recruitement != db_origin.recruitment:
            # update data  |  origin db (info 데이터 추가)
            #      O              X
            if db_origin.recruitment == False: 
                db_origin.recruitment = True
                for up_info_e in co_info:
                    db_origin.info.append({'wantedAuthNo':up_info_e['wantedAuthNo'],
                                            'title':up_info_e['title'],
                                            'wantedInfoUrl':up_info_e['wantedInfoUrl'],
                                            'wantedMobileInfoUrl':up_info_e['wantedMobileInfoUrl']})
                db_origin.save()

            # update data  |  origin db (info 데이터 삭제)
            #      X              O
            else:
                db_origin.recruitment = False
                db_origin.info = []
                db_origin.save()
from .models import Companies
from django.http import HttpResponse
import requests, xmltodict, json
import urllib

from .worknetCrawling.sg_recruit_mapping_api import sg_recrut_mapping_api
from .worknetCrawling.company_DB_update_api import company_DB_update

def companyDbInsert(request):
    db_insert = sg_recrut_mapping_api()
    # with open('../data/DB_insert_data/db_insert_data.json', 'r', encoding='UTF-8') as f:
    #     db_insert = json.load(f)

    for co in db_insert['sg']:
        insert_company = Companies(busiNo=co['busiNo'],
                                   coNm=co['coNm'],
                                   coAddr=co['coAddr'],
                                   superRegionCd=int(co['superRegionCd']), 
                                   superRegionNm=co['superRegionNm'], 
                                   regionCd=int(co['regionCd']),
                                   regionNm=co['regionNm'], 
                                   x=co['x'], 
                                   y=co['y'], 
                                   superIndTpCd=co['superIndTpCd'],
                                   superIndTpNm=co['superIndTpNm'],
                                   indTpCd=co['indTpCd'], 
                                   indTpNm=co['indTpNm'],
                                   coMainProd=co['coMainProd'],
                                   coHomePage=co['coHomePage'],
                                   alwaysWorkerCnt=co['allwaysWorkerCnt'],
                                   recruitment=co['recruitement'],
                                   sgBrandNm=[],
                                   info=[])
        for bNm in co['sgBrandNm']:
            insert_company.sgBrandNm.append({'ceNm':bNm})
        if co['recruitement'] == True:
            for i in co['info']:
                insert_company.info.append({'wantedAuthNo':i['wantedAuthNo'],
                                            'title':i['title'],
                                            'wantedInfoUrl':i['wantedInfoUrl'],
                                            'wantedMobileInfoUrl':i['wantedMobileInfoUrl']})
        insert_company.save()

    return HttpResponse('DB Insert Done!')

def companyDBupdate(reauest):
    company_DB_update()
    return HttpResponse('DB Update Done!')

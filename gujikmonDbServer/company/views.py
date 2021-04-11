from .models import Companies
from django.http import JsonResponse
import json

# Create your views here.
def companyDbInsert(request):
    with open('../db_insert_only_xy_ex.json', 'r', encoding='UTF-8') as f:
        db_insert = json.load(f)



    for co in db_insert['sg']:
        insert_company = Companies(coNm=co['coNm'],
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
                insert_company.info.append({'title':i['title'],
                                            'wantedInfoUrl':i['wantedInfoUrl'],
                                            'wantedMobileInfoUrl':i['wantedMobileInfoUrl']})

        insert_company.save()

    return JsonResponse(db_insert['sg'][11698])

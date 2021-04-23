from ..models import Companies
import json


def region_test():
    # 지역 코드
    with open('./region_code.json', 'r', encoding='UTF-8') as f:
        json_region_code = json.load(f)
    j = 0
    for i in range(1, 1581):
        test_db = Companies.objects.get(id=i)
        if json_region_code[str(test_db.regionCd)][0] in test_db.coAddr:
            pass
        else: 
            j = j + 1
            print(test_db.id)
            print(test_db.coAddr)
            print(test_db.regionCd)
            print(test_db.regionNm)
            print(test_db.superRegionCd)
            print(test_db.superRegionNm)
            print()
    print(j)
        
            


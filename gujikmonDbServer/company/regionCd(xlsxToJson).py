import csv
import pandas as pd
import json


xl = pd.read_excel("./지역코드.xlsx")
xl.to_csv('./지역코드.csv')

f = open('./지역코드.csv','r', encoding='UTF-8')
rdr = csv.reader(f)
 
region_code_dict = {}

temp_dict = {}
for line in rdr:
    if line[1][2:] == "000":
        temp_dict = {}
        temp_dict['superRegionCd'] = line[1]
        temp_dict['superRegionNm'] = line[2]
    elif line[1][2] == "36110":
        temp_dict = {}
        temp_dict['superRegionCd'] = "36110"
        temp_dict['superRegionNm'] = "세종"
    else:
        region_code_dict[line[1]] = []
        region_code_dict[line[1]].append(line[3])
        region_code_dict[line[1]].append(temp_dict)

with open('./region_code.json', 'w', encoding='utf-8') as make_file:
    json.dump(region_code_dict, make_file, ensure_ascii=False, indent='\t')

 
f.close()


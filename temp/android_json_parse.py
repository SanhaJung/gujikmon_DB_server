import json


with open('./region_code.json', 'r', encoding='UTF-8') as f:
    region_cd = json.load(f)

save_dict = {}

key_li = list(region_cd.keys())

for e in key_li:
    r_Nm1 = region_cd[e][0].split(' ')[0]
    s = len(r_Nm1)+1
    r_Nm2 = region_cd[e][0][s:]
    print(r_Nm1)
    print(r_Nm2)

    if r_Nm1 in list(save_dict.keys()):
        temp_dict = {}
        temp_dict[r_Nm2]=int(e)
        save_dict[r_Nm1].append(temp_dict)
    else:
        if r_Nm1 == '세종':
            save_dict[r_Nm1] = []
            temp_dict = {}
            temp_dict[r_Nm1]=int(e)
            save_dict[r_Nm1].append(temp_dict)
        else:
            save_dict[r_Nm1] = []
            temp_dict = {}
            temp_dict[r_Nm2]=int(e)
            save_dict[r_Nm1].append(temp_dict)



with open('./android_region_code.json', 'w', encoding='utf-8') as make_file:
    json.dump(save_dict, make_file, ensure_ascii=False, indent='\t')
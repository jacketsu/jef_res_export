import json
import os
import time
from requests import get, post, delete


def accession_list_v2():
    directory = "/media/tx-deepocean/Data/DICOMS/CT_Lung"
    folders = []
    for pid in os.listdir(directory):
        if "." in pid:
            continue
        path = "/".join([directory, pid])
        pid_f = os.listdir(path)
        if not pid_f:
            continue
        path = "/".join([path, pid_f[0]])
        for subf in os.listdir(path):
            fname = "/".join([pid, subf])
            print(fname)
            # count = len(os.listdir("/".join([path, subf])))
            # mtime = time.ctime(os.path.getmtime("/".join([directory, pid])))
            mtime = os.path.getmtime("/".join([directory, pid]))
            folders.append([fname, mtime, pid])
        
    # folders = sorted(folders, key=lambda f:-os.path.getmtime("/".join([directory, f[3]])))
    return folders



if __name__ == "__main__":
    folders = accession_list_v2()
    for f in folders:
        sid = str(f[0].split('/')[-1])
        predict_url = "/".join(['http://127.0.0.1:3000/api2/series', sid, 'predict', 'ct_lung'])
        print(predict_url)
        r = get(predict_url)

        # dic
        dic = {"L_super_": "upper left lobe", "L_infer_": "lower left lobe", "R_super_": "upper right lobe", "R_middle_": "middle right lobe", "R_infer_": "lower right lobe"}

        n_dic = {"calcific nodule": "Calcified Nodule", "solid nodule": "Solid Nodule", "GGN": "Nonsolid/GGN", "0-3nodule": "Solid Nodule", "nodule": "Nodule", "pGGN": "Nonsolid/GGN", "3-6nodule": "Solid Nodule", "mass": "Suspicious Mass Area", "pleural nodule": "Solid Nodule",
            "0-3mm nodule": "Solid Nodule",
            "3-6mm nodule": "3-6mm Solid Nodule",
            "6-10mm nodule": "6-10mm Solid Nodule",
            "10-30mm nodule": "10-30mm Solid Nodule",
            "0-5mm GGN": "0-5mm GGN",
            "5mm GGN": ">5mm GGN",
            "glass_shadow": "Ground Glass Opacity",
            "pleural": "Pleural Nodule",
            "interlobular nodule": "Solid Nodule",
            "mGGN": "Nonsolid/GGN"
        }

        if r:
            # tname = str(f[0].replace('/', '_')) + '.txt'
            tname = 'report_Aug_above_6mm.txt'
            save_path = '/'.join(['/home/tx-deepocean/res_export/txt_files', tname])
            j = r.json()
            # f = open(save_path, 'w')
            ff = open(save_path, 'a')
            for nn in j:
                ave = (float(nn['longDiameter']) + float(nn['longDiameter'])) / 2.0
                lobe_key = nn["lobePosition"].split("lb")[0]
                lobe_p = dic[str(lobe_key)]
                if ave > 6.0:
                    ff.write("PID: " + str(f[0].split("/")[0]) + ", Series ID: " + str(f[0].split("/")[1]) + ", " + "In slice " + str(nn['keySliceId']) + " " + str(lobe_p) + " found a " + str(n_dic[str(nn['type'])]) + ' nodule, which is ' + str(round(nn['longDiameter'], 2)) + 'mm x ' + str(round(nn['shortDiameter'], 2)) + 'mm.\n')
            ff.close()
            # with open(save_path, 'w') as f:
            #     json.dump(j, f)
            # print(j)

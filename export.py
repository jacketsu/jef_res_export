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
        if r:
            
            jname = str(f[0].replace('/', '_')) + '.json'
            save_path = '/'.join(['/home/tx-deepocean/res_export/jsons_files', jname])
            j = r.json()
            with open(save_path, 'w') as f:
                json.dump(j, f)
            # print(j)

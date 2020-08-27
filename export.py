import json
import os
import time
from requests import post, delete


def accession_list_v2():
    directory = "/media/tx-deepocean/Data/TMP"
    folders = []
    for pid in os.listdir(directory):
        if "." in pid:
            continue
        path = "/".join([directory, pid])
        pid_f = os.listdir(path)
        path = "/".join([path, pid_f[0]])
        for subf in os.listdir(path):
            fname = "/".join([pid, subf])
            count = len(os.listdir("/".join([path, subf])))
            # mtime = time.ctime(os.path.getmtime("/".join([directory, pid])))
            mtime = os.path.getmtime("/".join([directory, pid]))
            folders.append([fname, mtime, count, pid])
    folders = sorted(folders, key=lambda f:-os.path.getmtime("/".join([directory, f[3]])))
    return folders



if __name__ == "__main__":
    folders = accession_list_v2()
    sid = str(folders[0][0])
    predict_url = "/".join(['http://127.0.0.1:3000/api2/series', sid, 'predict', 'ct_lung'])
    r = requests.get(predict_url)
    j = r.json()
    print(j)

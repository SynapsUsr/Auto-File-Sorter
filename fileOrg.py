from os import listdir
from os.path import isfile, join
import time
import os
import shutil
import json
from configparser import ConfigParser
import hashlib
currentPath = "Images"
path = [

]

hashStore = {
    
}

isRunning = False

getHashes = False


parser = ConfigParser()

if(not os.path.exists('config.ini')):
    parser['settings'] = {
        'isRunning' : "true",
        'getHashes' : "true",
        'currentPathName' : "Images"
    }
    with open('config.ini', 'w') as f:
        parser.write(f)

if(not os.path.exists('filePaths.json')):
    data = [
        "empty",
    ]
    with open('filePaths.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

parser.read('config.ini')

currentPath = parser.get('settings', 'currentPathName')
if(parser.get('settings', 'getHashes') == 'true'):
    getHashes = True
if(parser.get('settings', 'getHashes') == 'false'):
    getHashes = False
if(parser.get('settings', 'isRunning') == 'true'):
     isRunning = True
if(parser.get('settings', 'isRunning') == 'false'):
    isRunning = False

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    onlyfiles = [f for f in listdir(currentPath) if isfile(join(currentPath, f))]
    print("Running")
    print(onlyfiles)
    for file in onlyfiles:
        for b in path:
            if file.startswith(b):
                shutil.move(currentPath + "/" + file, b + "/" + file.replace(b + " ", ""))
                if(getHashes == True):
                    if not os.path.exists("/fileHashes.json"):
                        os.makedirs("/fileHashes.json")
                    hashStore.update({ b + " | " + file.replace(b + " ", "") : md5(b + "/" + file.replace(b + " ", ""))})
                    json.dump(hashStore, open('fileHashes.json', 'w', encoding='utf-8'))
                    with open('fileHashes.json', 'w') as outfile:
                        json.dump(hashStore, outfile, ensure_ascii=False, indent=4)
                        outfile.close()


time.sleep(2)

if(isRunning):
    paths = open('filePaths.json')
    pathData = json.load(paths)
    for i in pathData:
        path.append(i)
    for a in path: 
        if not os.path.exists(a):
            os.makedirs(a)
    if(not os.path.exists(currentPath)): 
        os.makedirs(currentPath)
    while isRunning:
        parser.read('config.ini')
        if(parser.get('settings', 'isRunning') == "true"): isRunning = True
        if(parser.get('settings', 'isRunning') == "false"): isRunning = False
        main()
        time.sleep(3)
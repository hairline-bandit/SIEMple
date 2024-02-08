"""
This file is part of SIEMple.

SIEMple is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SIEMple is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SIEMple. If not, see https://www.gnu.org/licenses/.
"""

import ast, hashlib, os, time, requests
from checksumdir import dirhash

url = "http://127.0.0.1:5000/"

def createacc():
    a = input("Enter the password you want to use: ")
    r = requests.post(url + "create", data={"password": a})
    resp = ast.literal_eval(r.text)
    with open("mem.txt", "w+") as f:
        pass
    with open("mem.txt", "a") as f:
        f.write(a + "\n" + hashlib.sha256(resp["username"].encode("utf-8")).hexdigest() + "\n")
    print(f"Your username is: {resp['username']}")

# mem.txt ->
# password
# username
# full path to directories
# ...

def hashfile(path):
    buffer = 65536
    sha256b = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            dat = f.read(buffer)
            if not dat:
                break
            sha256b.update(dat)
    return sha256b.hexdigest()

def update(password, username, has):
    data = [i.strip().strip("/") for i in open("mem.txt", "r").readlines() if i != "\n"]
    out = {}
    if len(data) > 2:
        for i in data[2:]:
            cur = "*" + i.split("/")[-1]
            out[cur] = []
            stuff = os.listdir(i)
            for j in stuff:
                if "." not in j:
                    out[cur].append([j, dirhash(i+"/" + j + "/")])
                else:
                    out[cur].append([j, hashfile(i+ "/" + j)])
        r = requests.post(url + "update2", data={"id": username, "password":password, "hash": has, "files": str(out), "time":time.strftime("%H:%M:%S", time.localtime())})
        temp = ast.literal_eval(r.text)
        match temp["resp"]:
            case "wrong password":
                exit()
            case "id does not exist":
                exit()
        a = temp["change"]
        b = [i.strip() for i in open("mem.txt", "r").readlines() if i != "\n"]
        for i in range(2, len(b)):
            if b[i].split("/")[-1] in a:
                b[i] = " "
        with open("mem.txt", "w") as f:
            pass
        with open("mem.txt", "a") as f:
            for i in b:
                if i != " ":
                    f.write(i + "\n")
    else:
        r = requests.post(url + "update2", data={"id": username, "password":password, "hash": has, "files": "|NONE|", "time":time.strftime("%H:%M:%S", time.localtime())})
        temp = ast.literal_eval(r.text)
        match temp["resp"]:
            case "wrong password":
                exit()
            case "id does not exist":
                exit()
        a = temp["change"]
        b = [i.strip() for i in open("mem.txt", "r").readlines() if i != "\n"]
        for i in range(2, len(b)):
            if b[i].split("/")[-1] in a:
                b[i] = " "
        with open("mem.txt", "w") as f:
            pass
        with open("mem.txt", "a") as f:
            for i in b:
                if i != " ":
                    f.write(i + "\n")


def loop():
    data = [i.strip() for i in open("mem.txt", "r").readlines() if i != "\n"]
    passw = data[0]
    usern = data[1]
    if len(data) < 3:
        has = "0"
    else:
        has = hashlib.sha256("".join([dirhash(data[i], "sha256") for i in range(2, len(data))]).encode("utf-8")).hexdigest()
    r = requests.post(url + "update", data={"id":usern, "password":passw, "hash":has})
    temp = ast.literal_eval(r.text)
    match temp["resp"]:
        case "wrong password":
            exit()
        case "id does not exist":
            exit()
        case "no change":
            pass
        case "update":
            update(passw, usern, has)
    a = temp["change"]
    b = [i.strip() for i in open("mem.txt", "r").readlines() if i != "\n"]
    for i in range(2, len(b)):
        if b[i].split("/")[-1] in a:
            b[i] = " "
    with open("mem.txt", "w") as f:
        pass
    with open("mem.txt", "a") as f:
        for i in b:
            if i != " ":
                f.write(i + "\n")
    

def main():
    if not os.path.isfile("mem.txt"):
        createacc()
    print("Put the full path to a directory (using forward slashes) in mem.txt to start monitoring it and delete the line to stop monitoring.")
    while True:
        loop()
        time.sleep(10)
    


if __name__ == "__main__":
    main()

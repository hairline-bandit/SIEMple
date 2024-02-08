"""
This file is part of SIEMple.

SIEMple is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SIEMple is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SIEMple. If not, see https://www.gnu.org/licenses/.
"""



from flask import Flask, render_template, request, url_for, send_file, redirect
import ast, os.path, hashlib, time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST", "GET"])
def download():
    if request.method == "POST":
        user = request.values["username"]
        if len(user) != 64:
            usern = hashlib.sha256(user.encode("utf-8")).hexdigest()
        else:
            usern = user
        password = request.values["password"]
        passw = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if os.path.isfile("msgs/" + usern + ".txt"):
            dat = [i.strip() for i in open("msgs/" + usern + ".txt", "r").readlines() if i != "\n"]
            if passw == dat[0]:
                return send_file("msgs/" + usern + ".txt", as_attachment=True)
            else:
                return render_template("wrongpassword.html")
        else:
            return render_template("wrongusername.html")
    else:
        return render_template("download.html")


@app.route("/get", methods=["POST", "GET"])
def get():
    if request.method == "POST":
        user = request.values["username"]
        if len(user) != 64:
            usern = hashlib.sha256(user.encode("utf-8")).hexdigest()
        else:
            usern = user
        password = request.values["password"]
        passw = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if os.path.isfile("msgs/" + usern + ".txt"):
            dat = [i.strip() for i in open("msgs/" + usern + ".txt", "r").readlines() if i != "\n"]
            if passw == dat[0]:
                dat.pop(0)
                if len(dat) < 100:
                    return render_template("display.html", data=dat)
                return render_template("display.html", data=dat[-100:])
            else:
                return render_template("wrongpassword.html")
        else:
            return render_template("wrongusername.html")
    else:
        return render_template("get.html")

@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        t = time.time()
        passw = request.values["password"]
        hpass = hashlib.sha256(passw.encode("utf-8")).hexdigest()
        username = hashlib.sha256(str(t).encode("utf-8")).hexdigest()
        with open("db/" + username + ".txt", "a+") as f:
            f.write(hpass + "\ntemp\n/files\n ")
        with open("msgs/" + username + ".txt", "a+") as f:
            f.write(hpass + "\n")
        with open("cmds/" + username + ".txt", "a+") as f:
            pass
        return {"username": str(t)}
    else:
        return render_template("create.html")

@app.route("/stop", methods=["POST", "GET"])
def stop():
    if request.method == "POST":
        passw = request.values["password"]
        user = request.values["username"]
        if len(user) != 64:
            username = hashlib.sha256(user.encode("utf-8")).hexdigest()
        else:
            username = user
        password = hashlib.sha256(passw.encode("utf-8")).hexdigest()
        if os.path.isfile("db/" + username + ".txt"):
            dat = [i.strip() for i in open("db/" + username + ".txt", "r").readlines() if i != "\n"]
            if password == dat[0]:
                dat.pop(0)
                dat.pop(0)
                dat.pop(0)
                out = []
                for i in dat:
                    if i[0] == "*":
                        out.append(i[1:])
                return render_template("dirs.html", data=out, user=username, pas=password)
            else:
                return render_template("wrongpassword.html")
        else:
            return render_template("wrongusername.html")
    else:
        return render_template("stop.html")

@app.route("/dell/<dirr>/<user>/<pas>")
def dell(dirr, user, pas):
    if os.path.isfile("db/" + user + ".txt"):
        if open("db/" + user + ".txt", "r").readlines()[0].strip() == pas:
            pass
        else:
            return render_template("wrongpassword.html")
    else:
        return render_template("wrongusername.html")
    with open("cmds/" + user + ".txt", "a+") as f:
        f.write(dirr + "\n")
    return redirect(url_for("index"))


@app.route("/system", methods=["POST", "GET"])
def system():
    if request.method == "POST":
        passw = request.values["password"]
        user = request.values["username"]
        if len(user) != 64:
            username = hashlib.sha256(user.encode("utf-8")).hexdigest()
        else:
            username = user
        password = hashlib.sha256(passw.encode("utf-8")).hexdigest()
        if os.path.isfile("db/" + username + ".txt"):
            dat = [i.strip() for i in open("db/" + username + ".txt", "r").readlines() if i != "\n"]
            if password == dat[0]:
                dat.pop(0)
                dat.pop(0)
                dat.pop(0)
                return render_template("sysdisplay.html", data=dat)
            else:
                return render_template("wrongpassword.html")
        else:
            return render_template("wrongusername.html")
    else:
        return render_template("system.html")

@app.route("/update", methods=["POST", "GET"])
def update():
    if request.method == "POST":
        if os.path.isfile("db/" + request.values["id"] + ".txt"):
            dat = [i.strip() for i in open("db/" + request.values["id"] + ".txt", "r").readlines() if i != "\n"]
            if hashlib.sha256(request.values["password"].encode("utf-8")).hexdigest() == dat[0]:
                if request.values["hash"] == dat[1]:
                    x = [i.strip() for i in open("cmds/" + request.values["id"] + ".txt", "r").readlines() if i != "\n"]
                    with open("cmds/" + request.values["id"] + ".txt", "w") as f:
                        pass
                    return {"resp": "no change", "change": str(x)} # add stuff to return commands to application and delete command log
                else:
                    x = [i.strip() for i in open("cmds/" + request.values["id"] + ".txt", "r").readlines() if i != "\n"]
                    with open("cmds/" + request.values["id"] + ".txt", "w") as f:
                        pass
                    return {"resp": "update", "change": str(x)}
            else:
                x = [i.strip() for i in open("cmds/" + request.values["id"] + ".txt", "r").readlines() if i != "\n"]
                with open("cmds/" + request.values["id"] + ".txt", "w") as f:
                    pass
                return {"resp": "wrong password", "change": str(x)}
        else:
            x = [i.strip() for i in open("cmds/" + request.values["id"] + ".txt", "r").readlines() if i != "\n"]
            with open("cmds/" + request.values["id"] + ".txt", "w") as f:
                pass
            return {"resp": "id does not exist", "change": str(x)}
    else:
        return render_template("update.html")

@app.route("/update2", methods=["POST", "GET"])
def update2():
    if request.method == "POST":
        if os.path.isfile("db/" + request.values["id"] + ".txt"):
            dat = [i.strip() for i in open("db/" + request.values["id"] + ".txt", "r").readlines() if i != "\n"]
            if hashlib.sha256(request.values["password"].encode("utf-8")).hexdigest() == dat[0]:
                files = dat[dat.index("/files") + 1:]
                # files from monitored computer
                if request.values["files"] == "|NONE|":
                    with open("msgs/" + request.values["id"] + ".txt", "a") as f:
                        f.write(f"{request.values['time']} All directories have had their monitoring stopped.\n")
                    u = dat[0]
                    with open("db/" + request.values["id"] + ".txt", "w") as f:
                        pass
                    with open("db/" + request.values["id"] + ".txt", "a") as f:
                        f.write(u + "\n0\n/files\n ")
                    x = [i.strip() for i in open("cmds/" + request.values["id"] + ".txt", "r").readlines() if i != "\n"]
                    with open("cmds/" + request.values["id"] + ".txt", "w") as f:
                        pass
                    return {"resp": "success", "change": str(x)}
                else:
                    fin = ast.literal_eval(request.values["files"])
                # files stored in database (last screenshot)
                dfiles = {}

                # !!!!! both fin and dfiles in this format -> 
                # {"*directory": [[file_name, file_hash], [file_name, file_hash]...]}

                for i in range(len(files)):
                    if len(files[i]) > 0 and files[i][0] == "*":
                        dfiles[files[i]] = []
                        c = i + 1
                        while c < len(files) and files[c][0] != "*":
                            dfiles[files[i]].append(files[c].split(" | "))
                            c+=1
                        i = c-1
                cdfiles = dfiles.copy()
                for i in dfiles:
                    if i not in fin:
                        del cdfiles[i]
                        with open("msgs/" + request.values["id"] + ".txt", "a") as f:
                            f.write(f"{request.values['time']} Directory \"{i[1:]}\" was deleted OR monitoring has been stopped.\n")
                        continue
                    a = [k[0] for k in fin[i]]
                    b = [k[1] for k in fin[i]]
                    for j in dfiles[i]:
                        # check to see if file was deleted
                        if j[0] not in a:
                            with open("msgs/" + request.values["id"] + ".txt", "a") as f:
                                f.write(f"{request.values['time']} File/sub-directory \"{j[0]}\" was deleted within the directory \"{i[1:]}\".\n")
                            cdfiles[i].remove(j)
                        # check to see if file was changed
                        elif j[0] in a and b[a.index(j[0])] != j[1]:
                            with open("msgs/" + request.values["id"] + ".txt", "a") as f:
                                f.write(f"{request.values['time']} File/sub-directory \"{j[0]}\" was edited within the directory \"{i[1:]}\".\n")
                            cdfiles[i][cdfiles[i].index(j)] = [j[0], b[a.index(j[0])]]
                for i in fin:
                    if i not in dfiles:
                        cdfiles[i] = fin[i]
                        with open("msgs/" + request.values["id"] + ".txt", "a") as f:
                            f.write(f"{request.values['time']} Monitoring for directory \"{i[1:]}\" has started.\n")
                        continue
                    # check to see if file was added
                    a = [k[0] for k in dfiles[i]]
                    for j in fin[i]:
                        if j[0] not in a:
                            with open("msgs/" + request.values["id"] + ".txt", "a") as f:
                                f.write(f"{request.values['time']} File/sub-directory \"{j[0]}\" was created within the directory \"{i[1:]}\".\n")
                                cdfiles[i].append(j)
                # write to database
                with open("db/" + request.values["id"] + ".txt", "w") as f:
                    pass
                with open("db/" + request.values["id"] + ".txt", "a") as f:
                    f.write(dat[0] + "\n")
                    f.write(request.values["hash"] + "\n")
                    f.write("/files\n")
                    for k, v in cdfiles.items():
                        f.write(k + "\n")
                        f.write("\n".join([" | ".join([i[0], i[1]]) for i in v]))
                        f.write("\n")
                x = [i.strip() for i in open("cmds/" + request.values["id"] + ".txt", "r").readlines() if i != "\n"]
                with open("cmds/" + request.values["id"] + ".txt", "w") as f:
                    pass
                return {"resp": "success", "change": str(x)}     
                # get file names as key and list of files as value key starts with an *
            else:
                x = [i.strip() for i in open("cmds/" + request.values["id"] + ".txt", "r").readlines() if i != "\n"]
                with open("cmds/" + request.values["id"] + ".txt", "w") as f:
                    pass
                return {"resp": "wrong password", "change": str(x)}
        else:
            x = [i.strip() for i in open("cmds/" + request.values["id"] + ".txt", "r").readlines() if i != "\n"]
            with open("cmds/" + request.values["id"] + ".txt", "w") as f:
                pass
            return {"resp": "id does not exist", "change": str(x)}
    else:
        return render_template("update2.html")

if __name__ == "__main__":
    app.run(debug=True)

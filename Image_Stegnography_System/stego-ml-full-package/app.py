from flask import Flask, render_template, request, send_file
from stego import LSBSteganography, DCTSteganography
from detector import detect
import os, uuid

app=Flask(__name__)
os.makedirs("uploads",exist_ok=True)
lsb=LSBSteganography(); dct=DCTSteganography()

@app.route("/",methods=["GET","POST"])
def index():
    result=None
    if request.method=="POST":
        action=request.form["action"]
        method=request.form["method"]
        password=request.form.get("password") or None
        file=request.files["image"]
        name=str(uuid.uuid4())+"_"+file.filename
        path="uploads/"+name
        file.save(path)
        try:
            if action=="encode":
                msg=request.form.get("message")
                out=lsb.encode_lsb(path,msg,password) if method=="LSB" else dct.encode_dct(path,msg,password)
                return send_file(out,as_attachment=True)
            elif action=="decode":
                result=lsb.decode_lsb(path,password) if method=="LSB" else dct.decode_dct(path,password)
            else:
                result=detect(path)
        except Exception as e:
            result=str(e)
    return render_template("index.html",result=result)

if __name__=="__main__":
    app.run(debug=True)

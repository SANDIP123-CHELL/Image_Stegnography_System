import hashlib, base64
from PIL import Image
import numpy as np
from scipy.fftpack import dct, idct
from cryptography.fernet import Fernet

class ImageSteganography:
    def __init__(self): self.delimiter="###END###"
    def string_to_binary(self,t): return ''.join(format(ord(c),'08b') for c in t)
    def binary_to_string(self,b):
        return ''.join(chr(int(b[i:i+8],2)) for i in range(0,len(b),8) if len(b[i:i+8])==8)
    def generate_key_from_password(self,p):
        return base64.urlsafe_b64encode(hashlib.sha256(p.encode()).digest())
    def encrypt_message(self,m,p):
        if p:
            f=Fernet(self.generate_key_from_password(p))
            return base64.b64encode(f.encrypt(m.encode())).decode()
        return m
    def decrypt_message(self,e,p):
        if p:
            f=Fernet(self.generate_key_from_password(p))
            return f.decrypt(base64.b64decode(e.encode())).decode()
        return e

class LSBSteganography(ImageSteganography):
    def encode_lsb(self,img_path,msg,p=None,out=None):
        img=Image.open(img_path).convert("RGB")
        arr=np.array(img)
        data=self.encrypt_message(msg,p)+self.delimiter
        bits=self.string_to_binary(data)
        flat=arr.flatten()
        for i,b in enumerate(bits): flat[i]=(flat[i]&0xFE)|int(b)
        enc=flat.reshape(arr.shape)
        outimg=Image.fromarray(enc.astype("uint8"))
        if not out: out=img_path.rsplit('.',1)[0]+"_encoded.png"
        outimg.save(out); return out
    def decode_lsb(self,img_path,p=None):
        arr=np.array(Image.open(img_path).convert("RGB")).flatten()
        bits=""
        for px in arr:
            bits+=str(px&1)
            if bits.endswith(self.string_to_binary(self.delimiter)):
                txt=self.binary_to_string(bits)
                return self.decrypt_message(txt[:-len(self.delimiter)],p)
        raise Exception("No message found")

class DCTSteganography(ImageSteganography):
    def encode_dct(self,img_path,msg,p=None,out=None):
        img=np.array(Image.open(img_path).convert("RGB"),dtype=float)
        b=img[:,:,2]
        data=self.encrypt_message(msg,p)+self.delimiter
        bits=self.string_to_binary(data); k=0
        for i in range(0,b.shape[0]-8,8):
            for j in range(0,b.shape[1]-8,8):
                if k>=len(bits): break
                block=b[i:i+8,j:j+8]
                d=dct(dct(block.T,norm='ortho').T,norm='ortho')
                d[4,4]=abs(d[4,4])+10 if bits[k]=="1" else abs(d[4,4])-10
                b[i:i+8,j:j+8]=idct(idct(d.T,norm='ortho').T,norm='ortho')
                k+=1
        img[:,:,2]=b
        outimg=Image.fromarray(np.clip(img,0,255).astype("uint8"))
        if not out: out=img_path.rsplit('.',1)[0]+"_dct.png"
        outimg.save(out); return out
    def decode_dct(self,img_path,p=None):
        img=np.array(Image.open(img_path).convert("RGB"),dtype=float)
        b=img[:,:,2]; bits=""
        for i in range(0,b.shape[0]-8,8):
            for j in range(0,b.shape[1]-8,8):
                d=dct(dct(b[i:i+8,j:j+8].T,norm='ortho').T,norm='ortho')
                bits+="1" if d[4,4]>0 else "0"
                try:
                    txt=self.binary_to_string(bits)
                    if txt.endswith(self.delimiter):
                        return self.decrypt_message(txt[:-len(self.delimiter)],p)
                except: pass
        raise Exception("No message found")

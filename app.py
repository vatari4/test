from pygost.gost3410 import CURVES, public_key, GOST3410Curve, pub_marshal
from pygost.gost3410_vko import verify
from pygost.gost34112012 import GOST34112012
from pygost.gost3410 import GOST3410
from asn1crypto import cms, core
import os

def read_file(path):
    with open(path, "rb") as f:
        return f.read()

def verify_signature(data: bytes, signature: bytes, pubkey: bytes, curve: GOST3410Curve):
    digest = GOST34112012(data).digest()
    r = int.from_bytes(signature[:32], "big")
    s = int.from_bytes(signature[32:], "big")
    qx = int.from_bytes(pubkey[:32], "big")
    qy = int.from_bytes(pubkey[32:], "big")
    pub = (qx, qy)
    gost = GOST3410(curve)
    return gost.verify(pub, digest, (r, s))

data_path = "Свидетельство Купсик К.Г. ГИП И.pdf.pdf"
sig_path = "Свидетельство Купсик К.Г. ГИП И.pdfSGN1.sig"

data = read_file(data_path)
signature_der = read_file(sig_path)

content_info = cms.ContentInfo.load(signature_der)
signed_data = content_info['content']

signer_infos = signed_data['signer_infos']
signer_info = signer_infos[0]

signature = signer_info['signature'].native  # bytes, длина 64 байта

certs = signed_data['certificates']
cert = certs[0].chosen
pubkey_bytes = cert['tbs_certificate']['subject_public_key_info']['public_key'].native

curve_name = "id-tc26-gost-3410-12-256-paramSetA"
curve = CURVES[curve_name]

# Проверка подписи
if verify_signature(data, signature, pubkey_bytes, curve):
    print("Подпись корректна.")
else:
    print("Подпись недействительна.")

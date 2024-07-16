# SPDX-License-Identifier: MIT

import subprocess
from auth_modules import files
import pickle
import hmac
import sys

PROVIDERPATH = "~/oqs-provider-0.4.0/_build/oqsprov" # change if needed
OPENSSL_CONF = "/usr/lib/ssl/openssl.cnf" # change if needed

##### This function is not used at the moment.
##### Keys and certificate are generated using script sinature_authentication/generate_dilithium_keys.py
#def create_pk_and_cert(subject):
#    PRIVATE_KEY_PATH = f"./tmp/{subject}.key"
#    CERTIFICATE_PATH = f"./tmp/{subject}.crt"
#    CERT_DER_PATH = f"./tmp/{subject}.der"
#    cmd_x509 = f'openssl req -x509 -new -newkey dilithium3 -keyout {PRIVATE_KEY_PATH} -out {CERTIFICATE_PATH} -nodes -subj "/CN=oqstest" -days 365 -config {OPENSSL_CONF} -provider-path {PROVIDERPATH} -provider oqsprovider -provider default'
#    subprocess.run(cmd_x509, shell=True)
#    cmd_convert = f"openssl x509 -in {CERTIFICATE_PATH} -outform DER -out {CERT_DER_PATH} -provider-path {PROVIDERPATH} -provider oqsprovider -provider default"
#    subprocess.run(cmd_convert, shell=True)


def extract_pk(PATH_TO_CRT, PATH_TO_PUBKEY):
    cmd_extract_pk = f'openssl x509 -provider-path {PROVIDERPATH} -provider oqsprovider -provider default -in {PATH_TO_CRT} -pubkey -noout > {PATH_TO_PUBKEY}'
    subprocess.run(cmd_extract_pk, shell=True)


def sign_data(data, signer):
    PATH_TO_FILE = "./tmp/outputfile" # write outgoing message to this file
    PATH_TO_DGST = f"./tmp/dgst_signed_by_{signer}" # write signed dgst to this file
    with open(PATH_TO_FILE, "wb") as f:
        f.write(pickle.dumps(data))
    cmd_sign = f'openssl dgst -provider-path {PROVIDERPATH} -provider oqsprovider -provider default -sign ./tmp/{signer}.key -out {PATH_TO_DGST} {PATH_TO_FILE}'
    subprocess.run(cmd_sign, shell=True)
    signature_data = files.read_file(PATH_TO_DGST)
    size = sys.getsizeof(signature_data)
    print(f"Signature data size {size} bytes")
    return signature_data


def verify_signature(data, dgst_data, signer):
    PLAINFILE = "./tmp/received_msg_file"
    DGSTFILE = f"./tmp/msg_signed_by_{signer}"
    PUBKEY = f"./tmp/{signer}.pubkey"

    with open(PLAINFILE, "wb") as f:
        f.write(pickle.dumps(data))
    with open(DGSTFILE, "wb") as f:
        f.write(dgst_data)

    cmd_verify = f'openssl dgst -provider-path {PROVIDERPATH} -provider oqsprovider -provider default -signature {DGSTFILE} -verify {PUBKEY} {PLAINFILE}'
    subprocess.run(cmd_verify, shell=True)


def get_certificate(subject, cert_format="der"):
    # return cert in .der format (bytes)
    if cert_format == "der":
        data = files.read_file(f"./tmp/{subject}.der")
    else:
        data = files.read_file(f"./tmp/{subject}.crt", binarymod=False) # PEM format (not likely to be used
    return data

def verify_certificate(PATH_TO_CRT):
    # function returns subject and issuer of the certificate as dictionary
    cmd_verify = f'openssl x509 -subject -issuer -in {PATH_TO_CRT} -noout -provider-path {PROVIDERPATH} -provider oqsprovider -provider default'
    cmd_object = subprocess.run(cmd_verify, shell=True, capture_output=True)
    subject_and_issuer = cmd_object.stdout.decode().split("\n") # decode because stdout returns bytes encoded string
    print(subject_and_issuer)
    subject_and_issuer = {"subject": subject_and_issuer[0][8:].split(", "), "issuer": subject_and_issuer[1][7:].split(", ")}
    return subject_and_issuer["subject"] == ['C = FI', 'O = Teknologian tutkimuskeskus VTT', 'CN = QKD-LAPTOP']

def create_hmac(plain_msg, sender):
	PATH_TO_KEY = f"./tmp/shared_secret.{sender}"
	shared_secret = files.read_file(PATH_TO_KEY)
	h = hmac.new(key=shared_secret, digestmod="SHA256")
	h.update(pickle.dumps(plain_msg)) # HAS TO BE BYTES, NOT RANDOM DATA STRUCTURE
	hmac_data = h.digest()
	size = sys.getsizeof(hmac_data)
	print(f"Hmac size {size} bytes")
	return hmac_data

def compare_message_authentication_codes(senders_mac, receivers_mac):
    if hmac.compare_digest(senders_mac, receivers_mac):
        print("Authentication with MAC successful.")
    else:
        print("Warning, authentication failed")



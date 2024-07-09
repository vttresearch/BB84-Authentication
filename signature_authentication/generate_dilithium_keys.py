import subprocess
import sys
import os

PROVIDERPATH = "~/oqs-provider-0.4.0/_build/oqsprov"

if len(sys.argv) == 1:
    raise Exception("Usage: python generate_keys.py SUBJECT \n- SUBJECT either 'alice' or 'bob'")
elif not (sys.argv[1] == "alice" or sys.argv[1] == "bob"):
    raise Exception("Usage: python generate_keys.py SUBJECT \n- SUBJECT either 'alice' or 'bob'")

SUBJECT = sys.argv[1]


if __name__=="__main__":
    if not os.path.exists("./tmp/"):
        os.mkdir("./tmp/")

    # generate the dilithium keypair and certificate for Alice
    gen_key = f'openssl genpkey -out ./tmp/{SUBJECT}.key -algorithm dilithium3 -provider-path {PROVIDERPATH} -provider oqsprovider -provider default'
    subprocess.run(gen_key, shell=True)

    self_sign_cert = f'openssl req -x509 -new -key ./tmp/{SUBJECT}.key -outform DER -out ./tmp/{SUBJECT}.der -nodes -subj "/C=FI/O=VTT Technical Research Centre of Finland Ltd/CN=QKD-LAPTOP" -days 365 -provider-path {PROVIDERPATH} -provider oqsprovider -provider default'
    subprocess.run(self_sign_cert, shell=True)

#    extract_pub_key = 'openssl x509 -provider-path ~/oqs-provider/_build/oqsprov -provider oqsprovider -provider default -in qsc.crt -pubkey -noout > qsc.pubkey'
#    subprocess.run(extract_pub_key, shell=True)

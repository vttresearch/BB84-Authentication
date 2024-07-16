# SPDX-License-Identifier: MIT

import socket
from sockets import msging
from auth_modules import auth_controller
import oqs
import os

#############################################################
# Key exhange using kyber for key gen. and dilithium for auth 
#############################################################

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65530

if __name__ == "__main__":

    if os.path.exists("./tmp/"):
        print("tmp found")
    else:
        os.mkdir("./tmp")
    
    # create dilithium keypair and certificate
    print("Creating keypair and cert")
    auth_controller.create_pk_and_cert("bob")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # receive certificate and signed data
        s.connect((HOST, PORT))
        alice_data = msging.recv_msg(s)

        with open("./tmp/alice2.crt", "w") as f:
            f.write(alice_data["certificate"])

        print("extracting public dilithium key from certificate")
        auth_controller.extract_pk('./tmp/alice2.crt', './tmp/alice.pubkey')

        print("Verifying dilithium signature...")
        auth_controller.verify_signature(data=alice_data['pub_key'], dgst_data=alice_data['signature'], signer="alice")

        with oqs.KeyEncapsulation("Kyber512") as bob:
            print("encapsulating secret...")
            alice_pk = alice_data["pub_key"]
            cipher, shared_secret_bob = bob.encap_secret(alice_pk)
        
        with open("./tmp/cipher", "wb") as f:
            f.write(cipher)

        print("Signing data with private dilithium key")
        auth_controller.sign_data(data=cipher, signer="bob")

        with open("./tmp/dgst_signed_by_bob", "rb") as f:
            signed_cipher = f.read()

        with open("./tmp/bob.crt", "r") as f:
            bob_crt = f.read()

        data_out = {"certificate": bob_crt, "signature": signed_cipher, "shared_secret": cipher, "shared_secret_bob": shared_secret_bob}
        msging.send_msg(s, data_out)
        print("Bob sent all his data to Alice")
        print("Packet contains:\n- dilithium certificate\n- signed ciphertext of shared secret\n- ciphertext of shared secret (for signature verification)\n- Bob's version of shared secret (for demo purposes only)")
        print("<----------------")



# SPDX-License-Identifier: MIT

import socket
from sockets import msging
from auth_modules import auth_controller
import oqs
import os

##############################################################################
# Key exhange using kyber for key gen. and hmac for message authentication
# 
# - Scripts alice.py and bob.py use ML-KEM (Kyber) to create a shared
# secret which is then used to create message authentication codes.
# - Before sending their public key to Bob, Alice digitally signs it
# using ML-DSA (Dilithium).
# - Alice then sends the signed public ML-KEM key, and self-signed certificate
# containing the public ML-DSA key to Bob.
# - Finally, Alice and Bob test the hmac using their shared secret generated
# using ML-KEM.
##############################################################################

HOST = '127.0.0.1'
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

        with open("./tmp/shared_secret.bob", "wb") as f:
            f.write(shared_secret_bob)
        
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
        print("---------------->")
        message = msging.recv_msg(s)
        mac_bob = auth_controller.create_hmac(message['msg'], "bob")
        auth_controller.compare_message_authentication_codes(senders_mac=message['mac'], receivers_mac=mac_bob)

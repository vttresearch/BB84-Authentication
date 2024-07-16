# SPDX-License-Identifier: MIT

from sockets import msging
import socket
from auth_modules import auth_controller
import oqs
import os

#############################################################
# Key exhange using kyber for key gen. and dilithium for auth
#############################################################

HOST = '127.0.0.1'
PORT = 65530

if __name__ == "__main__":

    if os.path.exists("./tmp/"):
        print("tmp found")
    else:
        os.mkdir("./tmp")
    
    # create dilithium keypair and certificate
    print("Creating private dilithium key and cert")
    auth_controller.create_pk_and_cert("alice")


    with oqs.KeyEncapsulation("Kyber512") as alice:
        print("creating Kyber keypair and writing pk to file...")
        public_key = alice.generate_keypair()

        with open("./tmp/alice_kyber.pubkey", "wb") as f:
            f.write(public_key)

        print("Signing data with private dilithium key")
        auth_controller.sign_data(data=public_key, signer="alice")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen() # listen for connenctions
            conn, addr = s.accept()
            print(f"\nConnection accepted from: {addr[0]}:{addr[1]}")

            data_out = {}

            with open("./tmp/alice.crt", "r") as f:
                # read certificate data from file
                data = f.read()
                data_out["certificate"] = data

            with open("./tmp/alice_kyber.pubkey", "rb") as f:
                data = f.read()
                data_out["pub_key"] = data

            with open("./tmp/dgst_signed_by_alice", "rb") as f:
                # read the signed data
                binary_data = f.read()
                data_out["signature"] = binary_data
            
            msging.send_msg(conn, data_out)
            print("Alice sent all her data to Bob")
            print("Packet contains:\n- dilithium certificate\n- signed public kyber key\n- plain public kyber key")
            print("------------->")

            print("<-------------")
            data_bob = msging.recv_msg(conn)
            print("Received data from Bob")

            with open("./tmp/bob.crt", "w") as f:
                f.write(data_bob["certificate"])
            
            print("extract Bob's public key from cert")
            auth_controller.extract_pk("./tmp/bob.crt", "./tmp/bob.pubkey")
            print("verify signature")
            auth_controller.verify_signature(data=data_bob['shared_secret'], dgst_data=data_bob['signature'], signer='bob')

           
            print("decapsulating shared secret")
            shared_secret_alice = alice.decap_secret(data_bob["shared_secret"])
            #this is for demo only
            if shared_secret_alice == data_bob["shared_secret_bob"]:
                print("shared secret OK")

            with open("./tmp/shared_secret.alice", "wb") as f:
                f.write(shared_secret_alice)

            print('Creating message authentication code for key distillation message')
            key_distillation_message = "THIS IS A KEY DISTILLATION MESSAGE THAT MUST BE AUTHENTICATED"
            mac = auth_controller.create_hmac(plain_msg=key_distillation_message, sender="alice")
            data_out = {'msg': key_distillation_message, 'mac': mac}
            msging.send_msg(conn, data_out)
            print('Sent message and MAC to Bob.\n------------->\n')

            conn.close()

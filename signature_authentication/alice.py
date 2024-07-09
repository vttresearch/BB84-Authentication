from sockets import msging
import socket
import os
from auth_modules import auth_controller

#######################################
# SIGNATURE EXAMPLE USING dilithium
#######################################

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65530        # Port to listen on

SIGNED_DGST = "./tmp/alice_dgst" # this file contains the signed digest of msg data
DATA = [x%2 for x in range(10000)] # random data to send to Bob.

def sign_data():
    print("Signing data with private key")
    print(f"DATA: {DATA[:10]}")
    signed_data = auth_controller.sign_data(DATA, signer="alice")
    return signed_data # return the data, no need to open the file later

if __name__ == "__main__":

    if os.path.exists("./tmp/alice.der"):
        print("Certificate alice.der found")
    else:
        raise FileNotFoundError("You must create keypair and certificate before proceeding.\nRun python generate_dilithium_keys.py alice")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen() # listen for connenctions
        conn, addr = s.accept()
        print(f"\nConnection accepted from: {addr[0]}:{addr[1]}")
        certificate = auth_controller.get_certificate("alice")
        print(f"cert type {type(certificate)}")
        msging.send_msg(conn, certificate)
        print("Responded by sending certificate to client\n")

        msging.send_msg(conn, DATA) # random data list (msging-module pickles it during sending)
        signed_dgst = sign_data() # sign the data
        msging.send_msg(conn, signed_dgst)
        print("Alice sent all her data to Bob")
        print("Packets contain:\n- certificate\n- plaintext message\n- signed message digest")
        conn.close()

#        with oqs.Signature("Dilithium2") as alice:
#            alice_pk = alice.generate_keypair()
#            print("\nSending public key to Bob")
#            msging.send_msg(conn, alice_pk)
#
#            print("\nSending signed message to Bob...")
#            message = "This is a signed msg from Alice".encode()
#            signature = alice.sign(message)
#            msging.send_msg(conn, [message, signature])

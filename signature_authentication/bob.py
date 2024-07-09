import socket
from sockets import msging
from auth_modules import auth_controller

####################################
# SIGNATURE EXAMPLE USING dilithium
####################################

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65530        # Port to listen on

# These are file locations in the filesystem
ALICE_DER = "./tmp/alice2.der"
RECVD_MSG = "./tmp/bob_msg"
SIGNED_DGST = "./tmp/bob_dgstfile"
ALICE_PUBKEY = "./tmp/alice.pubkey"

if __name__ == "__main__":

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # receive certificate, plaintext and signed digest
        s.connect((HOST, PORT))
        certificate = msging.recv_msg(s)

        with open(ALICE_DER, "wb") as f:
            f.write(certificate)
        print("Alice responded with their certificate.")
        is_trusted = auth_controller.verify_certificate(ALICE_DER)
        if is_trusted:
            print("Certificate subject verified")

        plain_data = msging.recv_msg(s)
        signed_dgst_data = msging.recv_msg(s)
        print("\nReceived data from Alice")


    with open(SIGNED_DGST, "wb") as f:
        f.write(signed_dgst_data)

    print("extracting public key from certificate")
    auth_controller.extract_pk(ALICE_DER, ALICE_PUBKEY)

    print("Verifying signature...")
    auth_controller.verify_signature(plain_data, signed_dgst_data, signer="alice")


#        with oqs.Signature("Dilithium2") as bob:
#            alice_pk = msging.recv_msg(s)
#
#            print("\nReceiving signed msg from Alice...")
#            data = msging.recv_msg(s)
#            msg = data[0]
#            signature = data[1]
#            is_valid = bob.verify(msg, signature, alice_pk)
#
#            print("\nSignature is valid:", is_valid)

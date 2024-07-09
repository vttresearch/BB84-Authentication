import struct
import pickle

def send_msg(connected_sock, msg):
    """
    Attach prefix (msg-length) to the message and send it to connected socket
    """
    pickled_msg = pickle.dumps(msg)
    msg_byte_size = len(pickled_msg)
    prefix = struct.pack('>I', msg_byte_size)   # encode integer length into 4 bytes prefix
    msg_packet = prefix + pickled_msg
    connected_sock.sendall(msg_packet)  # use conn.sendall() to make sure socket sends all the data


def recv_msg(sock):
    """
    Function takes care that socket receives all the data sent by Alice.
    """
    msglen_as_bytes = recv_all(sock, 4)  # first 4 bytes express the incoming msg length
    if not msglen_as_bytes:
        # nothing received
        return None
    msglen = struct.unpack('>I', msglen_as_bytes)[0]   # unpack the prefix (n. of bytes) into integer
    pickled_data = recv_all(sock, msglen)    # read the actual message
    data = pickle.loads(pickled_data)
    return data


def recv_all(sock, n):
    """
    Socket helper function to receive n bytes of data.
    Application has to take care that all the data is actually received
    because socket.recv only receives max buffer size.
    """
    packets = bytearray()
    while len(packets) < n:
        block = sock.recv(n - len(packets))
        if not block:
            # nothing received
            return None
        packets.extend(block)
    return packets
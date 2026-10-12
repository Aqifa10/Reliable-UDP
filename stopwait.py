"""stopwait.py: Stop-and-Wait reliable file transfer. Owner: Atul."""

import socket
import time

from packet import ACK, DATA, FIN, make_ack, receive

LINGER = 2.0
IDLE = 30.0


def recv_file(sock: socket.socket, window: int) -> bytes:
    chunks = []
    expected = 0
    fin_seen = False

    while True:
        timeout = LINGER if fin_seen else IDLE
        pkt, addr = receive(sock, timeout)

        if pkt is None:
            break

        if not pkt["flags"] & DATA:
            continue

        seq = pkt["seq"]

        if seq == expected:
            chunks.append(pkt["payload"])
            expected += 1

            if pkt["flags"] & FIN:
                fin_seen = True

            sock.sendto(make_ack(seq), addr)

        elif seq < expected:
            sock.sendto(make_ack(seq), addr)

    return b"".join(chunks)
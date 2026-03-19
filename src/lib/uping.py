# µPing (MicroPing) for MicroPython
# copyright (c) 2018 Shawwwn <shawwwn1@gmail.com>
# License: MIT
# Source: https://gist.github.com/shawwwn/91cc8979e33e82af6d99ec34c38195fb


def checksum(data):
    if len(data) & 0x1:
        data += b'\0'
    cs = 0
    for pos in range(0, len(data), 2):
        b1 = data[pos]
        b2 = data[pos + 1]
        cs += (b1 << 8) + b2
    while cs >= 0x10000:
        cs = (cs & 0xffff) + (cs >> 16)
    cs = ~cs & 0xffff
    return cs


def ping(host, count=4, timeout=5000, interval=10, quiet=False, size=64):
    import utime, uselect, uctypes, usocket, ustruct, urandom

    assert size >= 16, "pkt size too small"
    pkt = b'Q' * size
    pkt_desc = {
        "type":      uctypes.UINT8  | 0,
        "code":      uctypes.UINT8  | 1,
        "checksum":  uctypes.UINT16 | 2,
        "id":        uctypes.UINT16 | 4,
        "seq":       uctypes.INT16  | 6,
        "timestamp": uctypes.UINT64 | 8,
    }

    h = uctypes.struct(uctypes.addressof(pkt), pkt_desc, uctypes.BIG_ENDIAN)
    h.type = 8
    h.code = 0
    h.checksum = 0
    h.id = urandom.getrandbits(16)
    h.seq = 1

    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_RAW, 1)
    sock.setblocking(0)
    sock.settimeout(timeout / 1000)
    addr = usocket.getaddrinfo(host, 1)[0][-1][0]
    sock.connect((addr, 1))

    not quiet and print("PING %s (%s): %u data bytes" % (host, addr, len(pkt)))

    seqs = list(range(1, count + 1))
    c, t, n_trans, n_recv = 1, 0, 0, 0
    finish = False

    while t < timeout:
        if t == interval and c <= count:
            h.checksum = 0
            h.seq = c
            h.timestamp = utime.ticks_us()
            h.checksum = checksum(pkt)
            if sock.send(pkt) == size:
                n_trans += 1
                t = 0
            else:
                seqs.remove(c)
            c += 1

        while 1:
            socks, _, _ = uselect.select([sock], [], [], 0)
            if socks:
                resp = socks[0].recv(4096)
                resp_mv = memoryview(resp)
                h2 = uctypes.struct(uctypes.addressof(resp_mv[20:]), pkt_desc, uctypes.BIG_ENDIAN)
                seq = h2.seq
                if h2.type == 0 and h2.id == h.id and (seq in seqs):
                    t_elapsed = (utime.ticks_us() - h2.timestamp) / 1000
                    ttl = ustruct.unpack('!B', resp_mv[8:9])[0]
                    n_recv += 1
                    not quiet and print("%u bytes from %s: icmp_seq=%u, ttl=%u, time=%f ms" % (len(resp), addr, seq, ttl, t_elapsed))
                    seqs.remove(seq)
                    if len(seqs) == 0:
                        finish = True
                        break
            else:
                break

        if finish:
            break
        utime.sleep_ms(1)
        t += 1

    sock.close()
    not quiet and print("%u packets transmitted, %u packets received" % (n_trans, n_recv))
    return (n_trans, n_recv)

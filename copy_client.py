#!/usr/bin/python3
# Echo client program
# Version con dos threads: uno lee un archivo binario hacia el socket y el otro al revés
# Los sincronizamos para ir uno a uno, salvo que haya un timeout
import jsockets
import sys, threading
import time

TIMEOUT = 2.0
SIZE = 1000
MAXDIST = 10
dist = 0
mm = 0
MAX_SEQ = 10000  # 0000-9999
HDR = 4
dups = 0
losts = 0

def from_seq(c1,c2,c3,c4):
    return (c1-ord('0'))*1000+(c2-ord('0'))*100+(c3-ord('0'))*10+(c4-ord('0'))

def to_seq(num):
    if(num > 9999):
        print(f"to_char: bad num: {num}");
        return None

    return bytearray([ord('0')+num // 1000, ord('0')+num // 100%10, ord('0')+num // 10%10, ord('0')+num %10])

# Revisar si x está en la ventana:
def between(x, min, max):      # min <= x < max
    if min <= max:
        return min <= x and x < max
    else:
        return (min <= x or x < max)

def Rdr(s,pack,fdout):
    global dist, SIZE, MAXDIST, dups, losts
    dups = 0
    losts = 0
    cnt = 0

    while True:
        try:
            data=s.recv(SIZE)
        except:
            break
        if not data:
            break
        seq = from_seq(data[0],data[1],data[2],data[3])
        if seq != cnt:
            print(f'err: espero:{cnt}, recibo:{seq}', file=sys.stderr)
            i = cnt - MAXDIST
            if i < 0:
                i = MAX_SEQ-i
            if between(seq, i, cnt):
                dups += 1
            elif between(seq, cnt, (cnt+MAXDIST)%MAX_SEQ):
                i = seq-cnt
                if i < 0:
                    i = MAX_SEQ-i
                losts += seq-cnt
            cnt = seq
        fdout.write(data[HDR:])
        cnt = (cnt+1)%MAX_SEQ
        with pack:
            dist = dist - 1
            if dist < 0:
                dist = 0
            pack.notify()
            #print(f"dist: {dist}")


if len(sys.argv) != 7:
    print('Use: '+sys.argv[0]+' maxpack dist filein fileout host port', file=sys.stderr)
    sys.exit(1)

SIZE = int(sys.argv[1])
MAXDIST = int(sys.argv[2])
if MAXDIST > MAX_SEQ/2:
    print(f'dist no puede ser mayor que max_seq/2={MAX_SEQ/2}')
    sys.exit(1)

fdin = open(sys.argv[3], "rb")
fdout = open(sys.argv[4], "wb")
s = jsockets.socket_udp_connect(sys.argv[5], sys.argv[6])
if s is None:
    print('could not open socket')
    sys.exit(1)
print(s.getsockname(), file=sys.stderr)

# Esto es para dejar tiempo al server para conectar el socket
s.send(b'hola')
s.recv(1024)

pack = threading.Condition()

# Creo thread que lee desde el socket hacia stdout:
# Parece que tiene que ser Daemon, para que muera sí o sí
newthread = threading.Thread(target=Rdr, args=(s,pack,fdout), daemon=True)
newthread.start()

# En este otro thread leo desde stdin hacia socket:
start = time.time()
cnt = 0
while True:
    data = fdin.read(SIZE-HDR)
    if not data:
        break
    try:
        s.send(to_seq(cnt)+data)
        cnt = (cnt+1)%MAX_SEQ
    except:
        continue
    with pack:
        dist = dist + 1
        if dist > mm:
            mm = dist
        if dist >= MAXDIST:
            if not pack.wait(TIMEOUT): # fue timeout
                print(f'TIMEOUT, dist={dist}', file=sys.stderr)
                dist = 0
        # print(f"dist: {dist}")

with pack:
    while dist > 0:
        if not pack.wait(TIMEOUT):
            print('TIMEOUT2')
            dist = 0

print(f'Usando: pack: {SIZE}, maxdist: {MAXDIST}')
print(f'Tiempo total: {time.time()-start}s')
print(f'dist max: {mm}')
print(f'dups: {dups}, losts: {losts}')
s.close()

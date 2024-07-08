# Inyectar paquetes erróneos a un cliente

El archivo `pirata.py` script utiliza la biblioteca Scapy para enviar paquetes UDP falsificados desde una dirección IP y puerto especificados hacia otra dirección IP y puerto. Está diseñado para enviar un mensaje en formato específico hasta 10.000 veces.

## Sistema Operativo

Esta tarea se ejecutó bajo las siguientes especificaciones:

**Sistema Operativo:** Windows Subsystem for Linux (Ubuntu)

## Requisitos

Actualizar el sistema e instalar dependencias:
```
sudo apt update
sudo apt upgrade -y
sudo apt install python3 python3-pip -y
```

Instalar Scapy:
```
sudo pip3 install scapy
```

Generar archivo con contenido aleatorio:
```
dd if=/dev/urandom of=IN bs=1024 count=5000
```

Modificar permisos de script:
```
chmod +x pirata.py
chmod +x copy_client.py
```

## Cómo usar

Para inyectar paquetes erróneos al cliente se debe realizar la siguiente ejecución:

En una terminal ejecutar el siguiente comando para ejecutar el cliente (servidor anakena):
```
./copy_client.py 15 1000 IN OUT  anakena.dcc.uchile.cl 1818
```
Luego de la ejecución se obtendrá la IP y el puerto a utilizar para ejecutar el pirata, de la siguiente manera: `('<client_ip>', <client_port>)`. Además empezará a escribirse el archivo OUT.

En otra terminal ejecutar el siguiente comando para ejecutar el pirata con la IP y puertos entregados por el cliente:
```
sudo ./pirata.py anakena.dcc.uchile.cl 1818 <client_ip> <client_port>
```

Una vez finaliza la ejecución del cliente el pirata podría continuar ejecutandose debido a la cantidad de iteraciones que realiza, pero puede detenerse manualmente ya que ya no tendrá nada que "hackear". Podemos revisar el archivo OUT y buscar en él la palabra _hackeado_ con Ctrl+F.

* Para ejecutar en servidor local, cambiar `anakena.dcc.uchile.cl` por `127.0.0.1`.

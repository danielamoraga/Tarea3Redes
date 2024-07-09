# Preguntas:
1. Si usara este mismo pirata para la T1: ¿funcionaría inyectar un paquete? ¿Sería más fácil o más difícil?

Si funcionaría inyectar un paquete al servidor de eco, pero podría no manejar correctamente los paquetes si no están en el formato esperado. En este caso el procedimiento podría ser más difícil ya que los paquetes deben cumplir con los requisitos específicos del protocolo utilizado.

2. Este ejercicio muestra lo trivial que es la seguridad en UDP. Si uno quisiera tener un sistema seguro en UDP, ¿cómo podríamos protegernos de este tipo de falsificaciones?

Se podría implementar la autenticación de paquetes con una clave compartida entre sender y receiver, o con firmas digitales basadas en criptografía asimétrica. También podría hacerse un cifrado del contenido de los paquetes para asegurar que no puedan ser leídos o modificados. 

3. En TCP, ¿sería igual de trivial inyectar un paquete de datos?

No, es más difícil debido a que TCP utiliza números de secuencia y ACK para garantizar la entrega ordenada de los datos, y el paquete inyectado debe tener los números de secuencia y ACK válidos para ser aceptado. Además, el uso de ventanas deslizantes haría que paquetes fuera de la ventana de secuencia de datos válida sean descartados.

4. Si ahora queremos que el pirata esté en otro computador que el cliente, ¿se podría hacer lo mismo con scapy? ¿Cómo?

Podría hacerse, para ello es necesario incorporar la falsificación de la dirección IP de origen (en el mismo computador no es necesario falsificarla ya que el origen es genuino), ejecutar los programas con permisos de root, y asegurarse de que esté permitido el tráfico UDP desde la IP del pirata.

5. Revise el tamaño del archivo de salida una vez que logró inyectar al menos un paquete pirata. ¿es más grande o más chico? Explique por qué.

El archivo de salida con paquetes pirata inyectados pesa 4.995KB mientras que el archivo de entrada pesa 5.000KB. Esto puede deberse a que durante la transferencia de paquetes pueden haber ocurrido pérdidas de datos, y aunque los paquetes pirata inyectados añaden bytes al archivo probablemente la pérdida fue mayor.
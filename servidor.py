import socket

HOST = '127.0.0.1'
PORT = 5000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# SO_REUSEADDR permite reutilizar el puerto inmediatamente si el servidor se reinicia
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind((HOST, PORT))
servidor.listen()

print(f"=== SERVIDOR DEL BANCO ACTIVO EN {HOST}:{PORT} ===")

while True:
    conexion, direccion = servidor.accept()
    
    try:
        datos = conexion.recv(1024).decode('utf-8').strip()
        
        if not datos:
            respuesta = "ERROR: No se recibieron datos."
        else:
            try:
                capital = float(datos)
                
                if capital <= 0:
                    respuesta = "ERROR: El capital debe ser un valor numérico mayor a 0."
                else:
                    ganancia = capital * 0.02
                    total = capital + ganancia
                    respuesta = (
                        f"--- RESUMEN DEL BANCO ---\n"
                        f"Capital ingresado:     ${capital:,.2f}\n"
                        f"Ganancia (2% mensual): ${ganancia:,.2f}\n"
                        f"Monto total acumulado: ${total:,.2f}"
                    )
            except ValueError:
                respuesta = "ERROR: El servidor recibió datos no numéricos inválidos."
                
    except Exception as e:
        respuesta = f"ERROR: Ocurrió un fallo en la solicitud ({e})."
        
    try:
        conexion.send(respuesta.encode('utf-8'))
    except Exception:
        pass
    finally:
        conexion.close()
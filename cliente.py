import socket

HOST = '127.0.0.1'
PORT = 5000

def obtener_capital_valido():
    """Solicita y valida que la entrada del usuario sea un número válido y mayor a 0."""
    while True:
        entrada = input("\nIngrese el capital a invertir ($): ").strip()
        
        if not entrada:
            print(" [!] La entrada no puede estar vacía. Intente de nuevo.")
            continue
            
        try:
            monto = float(entrada)
            if monto <= 0:
                print(" [!] El capital debe ser un número mayor a 0. Intente de nuevo.")
                continue
            return monto
        except ValueError:
            print(" [!] Entrada inválida: Solo se permiten números (ej. 150000 o 5000.50).")

def enviar_calculo(monto):
    """Envía el monto al servidor y muestra la respuesta."""
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((HOST, PORT))
        cliente.send(str(monto).encode('utf-8'))
        respuesta = cliente.recv(1024).decode('utf-8')
        
        print("\n" + "="*30)
        print(respuesta)
        print("="*30)
        
    except ConnectionRefusedError:
        print("\n [!] Error: No se pudo conectar al servidor. Asegúrese de que 'servidor.py' esté activo.")
    except Exception as e:
        print(f"\n [!] Error inesperado durante la comunicación: {e}")
    finally:
        cliente.close()

def menu_principal():
    """Muestra el menú interactivo para realizar cálculos o salir."""
    while True:
        print("\n=== SERVICIO DE INVERSIONES BANCO ===")
        print("1. Realizar cálculo de inversión")
        print("2. Salir")
        
        opcion = input("Seleccione una opción (1-2): ").strip()
        
        if opcion == '1':
            monto = obtener_capital_valido()
            enviar_calculo(monto)
        elif opcion == '2':
            print("\nGracias por utilizar nuestros servicios bancarios. ¡Hasta luego!\n")
            break
        else:
            print(" [!] Opción no válida. Por favor, ingrese 1 o 2.")

if __name__ == "__main__":
    menu_principal()
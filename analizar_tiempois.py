def analizar_tiempos(tiempos):

    # Precondiciones: la lista no puede ser None ni estar vacia,
    # y todos los valores deben ser > 0.
    if tiempos is None:
        raise ValueError("El arreglo no puede ser nulo")
    if len(tiempos) == 0:
        raise ValueError("El arreglo no puede estar vacio")
    for t in tiempos:
        if t <= 0:
            raise ValueError(f"Tiempo invalido encontrado: {t} (debe ser > 0)")

    maximo = tiempos[0]
    posicion = 0
    frecuencia = 1

    # Un solo recorrido del arreglo, de izquierda a derecha
    for i in range(1, len(tiempos)):
        if tiempos[i] > maximo:
            maximo = tiempos[i]
            posicion = i
            frecuencia = 1
        elif tiempos[i] == maximo:
            frecuencia += 1

    # posicion se retorna en base 1 para el usuario final
    return maximo, posicion + 1, frecuencia


def mostrar_resultados(tiempos):
    maximo, posicion, frecuencia = analizar_tiempos(tiempos)
    print(f"Arreglo: {tiempos}")
    print(f"Mayor tiempo de respuesta: {maximo} ms")
    print(f"Primera posicion: {posicion}")
    print(f"Numero de apariciones: {frecuencia}")
    print("-" * 40)


# para colocar el numero
if __name__ == "__main__":
    print("=== ANÁLISIS DE TIEMPOS DE RESPUESTA ===")
    try:
        entrada_n = input("Ingrese la cantidad de elementos del arreglo (n): ")
        if entrada_n.strip() == "":
            raise ValueError("La cantidad de elementos no puede estar vacía.")

        n = int(entrada_n)

        if n <= 0:
            print("Error: La cantidad de elementos debe ser mayor a 0.")
        else:
            tiempos = []
            print(f"Ingrese uno por uno los {n} valores del arreglo:")
            for i in range(n):
                entrada_val = input(f"  Elemento {i + 1}: ")
                if entrada_val.strip() == "":
                    raise ValueError(f"El Elemento {i + 1} no puede estar vacío.")

                valor = int(entrada_val)
                tiempos.append(valor)

            # Validar y mostrar los resultados con la función existente
            mostrar_resultados(tiempos)

    except ValueError as e:
        # Aquí atrapa tanto si dejas un campo vacío como si pones letras
        print(f"Error de entrada: {e}")

# pruebas unitarias
if __name__ == "__main__":
    # Caso del ejemplo del taller
    mostrar_resultados([120, 200, 150, 310, 90, 310])

    # Un solo elemento
    mostrar_resultados([500])

    # Todos los valores iguales
    mostrar_resultados([100, 100, 100, 100])

    # Maximo al final
    mostrar_resultados([10, 20, 5, 999])

    # Maximo al inicio
    mostrar_resultados([999, 10, 20, 5])

    # Casos invalidos (se capturan para mostrar el mensaje)
    for caso in [None, [], [50, -10, 30], [50, 0, 30]]:
        try:
            analizar_tiempos(caso)
        except ValueError as e:
            print(f"Entrada: {caso} -> Error controlado: {e}")

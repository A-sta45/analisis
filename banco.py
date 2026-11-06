"""
Proyecto: banco
Módulo de Transferencias Bancarias con Control Optimista de Concurrencia (OCC)
"""

import uuid

# Simulación de almacenamiento global (Base de datos e idempotencia en memoria)
I_MAP = {}  # Diccionario de idempotencia: id -> resultado
A_CUENTAS = {}  # Diccionario de cuentas: num_cuenta -> {sal, acu, mon, ver}
LOG_L = []  # Log de transacciones y auditoría

MAX_REINTENTOS = 3


class ConflictoVersionError(Exception):
    """Excepción lanzada cuando ocurre un conflicto de versión optimista."""

    pass


class ClaveDuplicadaError(Exception):
    """Excepción lanzada cuando la clave de idempotencia ya existe."""

    pass


def a_centavos(m_texto):
    """Convierte un monto de texto a centavos para evitar problemas de punto flotante."""
    try:
        valor = float(m_texto)
        return int(round(valor * 100))
    except (ValueError, TypeError):
        return None


def validar_reglas_negocio(c_o, c_d, m):
    """Valida reglas 2, 3, 4, 5, 6 (fondos, moneda, etc.)."""
    if not c_o or not c_d:
        return "CUENTA_NO_EXISTE"
    if c_o["mon"] != c_d["mon"]:
        return "MONEDAS_DIFERENTES"
    if c_o["sal"] < m:
        return "SALDO_INSUFICIENTE"
    return None


def transferir(o, d, m_texto, id_solicitud):
    """Ejecuta una transferencia entre cuentas (o -> d) de manera segura y concurrente."""

    # ==========================================
    # FASE 1 — Validación sintáctica
    # ==========================================
    if not id_solicitud:
        return {"estado": "RECHAZADA", "motivo": "ID_SOLICITUD_REQUERIDO"}

    m = a_centavos(m_texto)
    if m is None:
        return {"estado": "RECHAZADA", "motivo": "PRECISION_INVALIDA"}

    if m <= 0:
        return {"estado": "RECHAZADA", "motivo": "MONTO_NO_POSITIVO"}

    if o == d:
        return {"estado": "RECHAZADA", "motivo": "CUENTAS_IGUALES"}

    # ==========================================
    # FASE 2 — Idempotencia (consulta rápida)
    # ==========================================
    if id_solicitud in I_MAP:
        return {"estado": "REPETIDA", "resultado": I_MAP[id_solicitud]}

    # ==========================================
    # FASE 3 — Núcleo transaccional con control optimista
    # ==========================================
    intentos = 0
    while intentos < MAX_REINTENTOS:
        intentos += 1

        # INICIAR TRANSACCIÓN
        try:
            # Lectura de idempotencia dentro de la transacción (cierra ventana de carrera)
            if id_solicitud in I_MAP:
                # CONFIRMAR implícito y retornar
                return {"estado": "REPETIDA", "resultado": I_MAP[id_solicitud]}

            # Leer o y d en orden creciente de número de cuenta (evita interbloqueo)
            cuenta_min, cuenta_max = sorted([o, d])

            if o not in A_CUENTAS or d not in A_CUENTAS:
                raise ValueError("CUENTA_NO_EXISTE")

            c_o = A_CUENTAS[o].copy()
            c_d = A_CUENTAS[d].copy()
            v_o = c_o["ver"]
            v_d = c_d["ver"]

            motivo = validar_reglas_negocio(c_o, c_d, m)
            if motivo is not None:
                # ABORTAR TRANSACCIÓN
                LOG_L.append({"tipo": "rechazo", "id": id_solicitud, "motivo": motivo})
                return {"estado": "RECHAZADA", "motivo": motivo}

            # --- SEGMENTO ATÓMICO S1 ---
            # DÉBITO: actualizar A[o] SI A[o].ver == v_o
            if A_CUENTAS[o]["ver"] == v_o:
                A_CUENTAS[o]["sal"] -= m
                A_CUENTAS[o]["acu"] += m
                A_CUENTAS[o]["ver"] += 1
            else:
                raise ConflictoVersionError()

            # CRÉDITO: actualizar A[d] SI A[d].ver == v_d
            if A_CUENTAS[d]["ver"] == v_d:
                A_CUENTAS[d]["sal"] += m
                A_CUENTAS[d]["ver"] += 1
            else:
                raise ConflictoVersionError()
            # --- fin S1 ---

            t = str(uuid.uuid4())
            LOG_L.append(
                {
                    "tipo": "mov",
                    "t": t,
                    "id": id_solicitud,
                    "o": o,
                    "d": d,
                    "m": m,
                    "mon": c_o["mon"],
                }
            )

            resultado_aprobado = {"estado": "APROBADA", "t": t}

            if id_solicitud in I_MAP:
                raise ClaveDuplicadaError(id_solicitud)

            I_MAP[id_solicitud] = resultado_aprobado

            # CONFIRMAR TRANSACCIÓN (Punto de linealización)
            return resultado_aprobado

        except ClaveDuplicadaError:
            # REVERTIR (simulado)
            return {"estado": "REPETIDA", "resultado": I_MAP.get(id_solicitud)}

        except ConflictoVersionError:
            # REVERTIR y registrar fallo de concurrencia
            LOG_L.append({"tipo": "fallo", "id": id_solicitud, "intentos": intentos})
            continue  # Continuar el bucle de reintentos

        except Exception as e:
            # REVERTIR TRANSACCIÓN por fallo técnico
            LOG_L.append(
                {
                    "tipo": "fallo",
                    "id": id_solicitud,
                    "error": str(e),
                    "intentos": intentos,
                }
            )
            return {"estado": "FALLIDA", "motivo": "ERROR_TÉCNICO"}

    return {"estado": "FALLIDA", "motivo": "CONFLICTO_CONCURRENCIA"}

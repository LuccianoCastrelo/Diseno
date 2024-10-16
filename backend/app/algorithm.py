# algorithm.py

import math
from datetime import datetime, timedelta

def calcular_turnos_y_pago_trabajador(trabajador, registros_jornadas):
    tipo = trabajador['tipo']  # 'permanente' o 'eventual'
    pago_total = 0
    pagos_semanales = {}
    pagos_mensuales = {}
    total_turnos = 0  # Variable para contar el total de turnos

    salario_base = trabajador.get('salario_base', 0)  # Para trabajadores permanentes

    for registro in registros_jornadas:
        fecha = registro['fecha']
        horas_trabajadas = registro['horas_trabajadas']
        es_festivo_o_domingo = registro.get('es_festivo_o_domingo', False)

        # Calcular el primer día de la semana y del mes
        primer_dia_semana = obtener_primer_dia_semana(fecha).strftime('%d-%m-%Y')
        primer_dia_mes = obtener_primer_dia_mes(fecha).strftime('%d-%m-%Y')

        # Determinar turnos y pago por jornada
        turnos, pago_jornada = calcular_turnos_y_pago_jornada(
            trabajador, horas_trabajadas, es_festivo_o_domingo
        )

        # Acumular total de turnos
        total_turnos += turnos

        # Acumular el pago total
        pago_total += pago_jornada

        # Acumular pagos semanales y mensuales
        pagos_semanales.setdefault(primer_dia_semana, 0)
        pagos_semanales[primer_dia_semana] += pago_jornada

        pagos_mensuales.setdefault(primer_dia_mes, 0)
        pagos_mensuales[primer_dia_mes] += pago_jornada

    # Para trabajadores permanentes, agregar el salario base mensual
    if tipo == 'permanente':
        for mes in pagos_mensuales:
            pagos_mensuales[mes] += salario_base

    # Redondear hacia arriba los pagos semanales y mensuales
    pago_total = math.ceil(pago_total)
    pagos_semanales = {fecha: math.ceil(pago) for fecha, pago in pagos_semanales.items()}
    pagos_mensuales = {fecha: math.ceil(pago) for fecha, pago in pagos_mensuales.items()}

    return {
        'pago_total': pago_total,
        'total_turnos': total_turnos,  # Agregamos los turnos totales al resultado
        'pagos_semanales': pagos_semanales,
        'pagos_mensuales': pagos_mensuales
    }

def calcular_turnos_y_pago_jornada(trabajador, horas_trabajadas, es_festivo_o_domingo):
    pago_base_por_turno = trabajador['pago_por_turno']
    turnos, pago_jornada = calcular_turnos(horas_trabajadas, pago_base_por_turno, es_festivo_o_domingo)
    return turnos, pago_jornada

def calcular_turnos(horas_trabajadas, pago_base_por_turno, es_festivo_o_domingo):
    horas_adicionales = 0
    turnos = 0

    # Determinación de turnos según las horas trabajadas
    if horas_trabajadas > 11:
        turnos = 2
    elif 7 <= horas_trabajadas <= 11:
        turnos = 1
        horas_adicionales = horas_trabajadas - 7
    else:
        turnos = 0.5  # Menos de 7 horas se considera medio turno

    # Calcular el pago base por los turnos
    total_pagar = turnos * pago_base_por_turno

    # Calcular pago adicional por horas extra (doble pago)
    if horas_adicionales > 0:
        pago_hora_adicional = (pago_base_por_turno / 7) * 2  # Pago doble por hora extra
        total_pagar += horas_adicionales * pago_hora_adicional

    # Si es festivo o domingo, el pago se duplica
    if es_festivo_o_domingo:
        total_pagar *= 2

    # Redondear el total hacia arriba
    return turnos, math.ceil(total_pagar)

def obtener_primer_dia_semana(fecha):
    return fecha - timedelta(days=fecha.weekday())

def obtener_primer_dia_mes(fecha):
    return fecha.replace(day=1)

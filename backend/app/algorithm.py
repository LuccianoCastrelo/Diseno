# algorithm.py

import math
from datetime import datetime, timedelta
def calcular_turnos(horas_trabajadas):
    turnos = 0

    # Determinación de turnos según las horas trabajadas
    if horas_trabajadas > 11:
        turnos = 2
    elif 7.5 <= horas_trabajadas <= 11:
        turnos = 1
    else:
        turnos = 0.5  # Menos de 7.5 horas se considera medio turno
    
    return turnos

def calcular_pago_por_jornada(trabajador, horas_trabajadas, es_domingo=False):
    """
    Calcula el pago de una jornada (un solo día).
    Si se trabaja en domingo, se paga el doble.
    """
    pago_base_por_turno = trabajador['pago_por_turno']
    
    # Obtener el número de turnos en función de las horas trabajadas
    turnos = calcular_turnos(horas_trabajadas)
    
    # Calcular el pago base por la jornada (turnos * pago por turno)
    pago_jornada = turnos * pago_base_por_turno

    # Si es domingo o festivo, el pago se duplica
    if es_domingo:
        pago_jornada *= 2

    return turnos,math.ceil(pago_jornada)  # Redondeamos hacia arriba

def calcular_sueldo_semanal(trabajador, registros_jornadas_semanales):
    """
    Calcula el monto de sueldo semanal y los turnos trabajados.
    Considera días trabajados en domingos que se pagan doble.
    """
    pago_total_semanal = 0
    total_turnos_semanal = 0

    for registro in registros_jornadas_semanales:
        horas_trabajadas = registro['horas_trabajadas']
        es_domingo = registro.get('es_festivo_o_domingo', False)

        # Usamos la función calcular_pago_por_jornada para obtener turnos y pago
        turnos, pago_jornada = calcular_pago_por_jornada(trabajador, horas_trabajadas, es_domingo)
        
        # Acumulamos el pago y los turnos de la jornada
        pago_total_semanal += pago_jornada
        total_turnos_semanal += turnos

    return total_turnos_semanal, math.ceil(pago_total_semanal)

def calcular_sueldo_mensual(trabajador, registros_jornadas_mensuales):
    """
    Calcula el monto de sueldo mensual y los turnos trabajados.
    Considera días trabajados en domingos que se pagan doble.
    """
    pago_total_mensual = 0
    total_turnos_mensual = 0
    salario_base = trabajador.get('salario_base', 0)  # Para trabajadores permanentes

    for registro in registros_jornadas_mensuales:
        horas_trabajadas = registro['horas_trabajadas']
        es_domingo = registro.get('es_festivo_o_domingo', False)

        # Usamos la función calcular_pago_por_jornada para obtener turnos y pago
        turnos, pago_jornada = calcular_pago_por_jornada(trabajador, horas_trabajadas, es_domingo)

        # Acumulamos el pago y los turnos de la jornada
        pago_total_mensual += pago_jornada
        total_turnos_mensual += turnos

    # Si es trabajador permanente, sumar el salario base mensual
    if trabajador['tipo'] == 'permanente':
        pago_total_mensual += salario_base

    return total_turnos_mensual, math.ceil(pago_total_mensual)

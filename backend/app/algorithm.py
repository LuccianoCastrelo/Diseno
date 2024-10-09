import math
from datetime import datetime, timedelta

def calcular_pago_trabajador(trabajador, registros_jornadas):
    tipo = trabajador['tipo']  # 'permanente' o 'eventual'
    pago_total = 0
    pagos_semanales = {}
    pagos_mensuales = {}
    
    salario_base = trabajador.get('salario_base', 0)  # Para trabajadores permanentes
    
    for registro in registros_jornadas:
        fecha = registro['fecha']
        horas_trabajadas = registro['horas_trabajadas']
        es_festivo_o_domingo = registro.get('es_festivo_o_domingo', False)
        
        primer_dia_semana = obtener_primer_dia_semana(fecha).strftime('%d-%m-%Y')  # Primer día de la semana en formato texto
        primer_dia_mes = obtener_primer_dia_mes(fecha).strftime('%d-%m-%Y')  # Primer día del mes en formato texto
        
        pago_jornada = 0
        
        if tipo == 'eventual':
            pago_jornada = calcular_pago_jornada_eventual(trabajador, horas_trabajadas, es_festivo_o_domingo)
        elif tipo == 'permanente':
            pago_jornada = calcular_pago_jornada_permanente(trabajador, horas_trabajadas, es_festivo_o_domingo)
        
        # Sumar al total
        pago_total += pago_jornada
        
        # Acumular pagos semanales con la fecha del primer día de la semana
        pagos_semanales.setdefault(primer_dia_semana, 0)
        pagos_semanales[primer_dia_semana] += pago_jornada
        
        # Acumular pagos mensuales con la fecha del primer día del mes
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
        'pagos_semanales': pagos_semanales,
        'pagos_mensuales': pagos_mensuales
    }

def calcular_pago_jornada_eventual(trabajador, horas_trabajadas, es_festivo_o_domingo):
    pago_base_por_turno = trabajador['pago_por_turno']
    return calcular_pago_turnos(horas_trabajadas, pago_base_por_turno, es_festivo_o_domingo)

def calcular_pago_jornada_permanente(trabajador, horas_trabajadas, es_festivo_o_domingo):
    # Solo se calculan las horas adicionales (horas extras)
    horas_jornada_regular = trabajador.get('horas_jornada_regular', 8)
    horas_extras = max(0, horas_trabajadas - horas_jornada_regular)
    if horas_extras == 0:
        return 0
    pago_base_por_turno = trabajador['pago_por_turno']
    return calcular_pago_turnos(horas_extras, pago_base_por_turno, es_festivo_o_domingo)

def calcular_pago_turnos(horas_trabajadas, pago_base_por_turno, es_festivo_o_domingo):
    total_pagar = 0
    horas_adicionales = 0
    turnos = 0
    
    if horas_trabajadas > 11:
        turnos = 2
    elif 7 <= horas_trabajadas <= 11:
        turnos = 1
        horas_adicionales = horas_trabajadas - 7
    else:
        turnos = 0.5  # Menos de 7 horas, se considera medio turno
    
    total_pagar = turnos * pago_base_por_turno
    
    # Calcular el pago por horas adicionales (doble pago)
    if horas_adicionales > 0:
        pago_hora_adicional = (pago_base_por_turno / 7) * 2  # Pago doble por hora extra
        total_pagar += horas_adicionales * pago_hora_adicional
    
    # Si es festivo o domingo, el pago es doble
    if es_festivo_o_domingo:
        total_pagar *= 2

    # Redondear el total hacia arriba si hay decimales
    return math.ceil(total_pagar)

def obtener_primer_dia_semana(fecha):
    # Obtener el lunes de la semana correspondiente
    return fecha - timedelta(days=fecha.weekday())

def obtener_primer_dia_mes(fecha):
    # Retorna el primer día del mes
    return fecha.replace(day=1)

# Ejemplo de uso
"""
trabajador_eventual = {
    'nombre': 'Juan Pérez',
    'tipo': 'eventual',
    'pago_por_turno': 50000  # Pago base por turno completo
}

trabajador_permanente = {
    'nombre': 'María Gómez',
    'tipo': 'permanente',
    'salario_base': 800000,      # Salario mensual fijo
    'horas_jornada_regular': 8,  # Horas de jornada regular diaria
    'pago_por_turno': 50000      # Pago base por turno (para horas extras)
}

# Registro de jornadas (ejemplo)
registros_jornadas = [
    {'fecha': datetime(2024, 9, 1), 'horas_trabajadas': 9, 'es_festivo_o_domingo': True},
    {'fecha': datetime(2024, 9, 2), 'horas_trabajadas': 8, 'es_festivo_o_domingo': False},
    {'fecha': datetime(2024, 9, 3), 'horas_trabajadas': 12, 'es_festivo_o_domingo': False},
    # Agrega más registros según sea necesario
]

# Cálculo para trabajador eventual
resultado_eventual = calcular_pago_trabajador(trabajador_eventual, registros_jornadas)
print(f"Pago total trabajador eventual: {resultado_eventual['pago_total']}")
print(f"Pagos semanales: {resultado_eventual['pagos_semanales']}")
print(f"Pagos mensuales: {resultado_eventual['pagos_mensuales']}")

# Cálculo para trabajador permanente
resultado_permanente = calcular_pago_trabajador(trabajador_permanente, registros_jornadas)
print(f"Pago total trabajador permanente: {resultado_permanente['pago_total']}")
print(f"Pagos semanales: {resultado_permanente['pagos_semanales']}")
print(f"Pagos mensuales: {resultado_permanente['pagos_mensuales']}")
"""
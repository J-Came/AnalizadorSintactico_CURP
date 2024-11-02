import re

def analizar_curp(curp):
    # Patrón de validación de CURP
    patron = r"([A-Z]{2})([A-Z]{1})([A-Z]{1})(\d{6})([HM])([A-Z]{2})([A-Z]{3})([A-Z\d]{1})(\d{1})"
    es_valido = bool(re.match(patron, curp))

    if not es_valido:
        return None, False

    resultado_lexico = {
        'Apellido Paterno': curp[0:2],      # Dos primeras letras
        'Apellido Materno': curp[2:3],      # La tercera letra
        'Nombre': curp[3:4],                 # La cuarta letra
        'Fecha de Nacimiento': curp[4:10],   # AA/MM/DD
        'Género': curp[10],                  # 'H' o 'M'
        'Estado': curp[11:13],               # Código de estado (dos letras)
        'Consonantes Internas': curp[13:16],  # Tres letras
        'Homoclave': curp[16:18],            # Dos caracteres alfanuméricos
        'Dígito Verificador': curp[17],       # Un dígito
    }
    return resultado_lexico, es_valido

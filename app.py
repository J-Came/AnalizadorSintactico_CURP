from flask import Flask, render_template, request, jsonify
from curp_lexer import analizar_curp
import re

app = Flask(__name__)

def sintactico(curp):
    pattern = (
        r"^[A-Z]{1}[AEIOU]{1}[A-Z]{2}"            
        r"\d{2}(0[1-9]|1[0-2])"                   
        r"(0[1-9]|[12][0-9]|3[01])"               
        r"[HM]"                                   
        r"(AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS)"  
        r"[B-DF-HJ-NP-TV-Z]{3}"                   
        r"[A-Z\d]{1}[0-9]{1}$"                    
    )
    
    match = re.match(pattern, curp)
    if not match:
        return "CURP no válida: formato incorrecto"
    
    year = int(curp[4:6])
    month = int(curp[6:8])
    day = int(curp[8:10])

    if year < 50:
        year += 2000
    else:
        year += 1900

    meses_31_dias = [1, 3, 5, 7, 8, 10, 12]
    if month == 2:
        if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):  # Año bisiesto
            if day > 29:
                return f"CURP no válida: febrero {year} solo tiene hasta 29 días (Día ingresado: {day})"
        else:
            if day > 28:
                return f"CURP no válida: febrero {year} solo tiene hasta 28 días (Día ingresado: {day})"
    elif month in meses_31_dias:
        if day > 31:
            return f"CURP no válida: el mes {month} solo tiene hasta 31 días (Día ingresado: {day})"
    else:
        if day > 30:
            return f"CURP no válida: el mes {month} solo tiene hasta 30 días (Día ingresado: {day})"
    
    return "CURP válida"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    curp = request.form.get('curp', '')
    
    resultado_lexico, es_valido_lexico = analizar_curp(curp)
    
    resultado_sintactico = sintactico(curp)

    return jsonify({
        'lexical_analysis': resultado_lexico,
        'syntactic_validation': resultado_sintactico
    })

if __name__ == '__main__':
    app.run(debug=True)

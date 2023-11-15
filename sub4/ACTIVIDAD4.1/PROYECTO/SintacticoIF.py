# Importando Librerias
import re
import tkinter as tk
from tkinter import messagebox
from ply import lex, yacc
from subprocess import call

reserved = {
   'if': 'IF',
   'else': 'ELSE',
   'int': 'INT',
}


# Definir los tokens
tokens = (
    'ID',
    'NUM',
    'STRING',
    'SEMICOLON',
    'LESS',
    'GREATER',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'ASSIGN',
    'ASSIGNS',
    'INCREMENT',
) + tuple(reserved.values())

# Reglas simples para tokens
t_SEMICOLON = r';'
t_LESS = r'<'
t_GREATER = r'>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ASSIGNS = r'=='
t_ASSIGN = r'='
t_INCREMENT = r'\+\+'
t_ignore = ' \t'  

# Reglas complejas para tokens
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID')  # Verifica las palabras reservadas
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    error_message(f"Token desconocido '{t.value[0]}'", t.lineno)
    t.lexer.skip(1)


# Construcción del lexer
lexer = lex.lex()

# Definición de la gramática para el análisis sintáctico
def p_statement(p):
    '''
    statement : conditional_structure
    '''
    
def p_conditional_structure(p):
    'conditional_structure : IF LPAREN condition RPAREN LBRACE declaration RBRACE ELSE LBRACE increment_statement RBRACE'

def p_condition(p):
    '''condition : ID LESS NUM
                 | ID GREATER NUM
                 | ID ASSIGNS NUM'''
    # Esta regla tendría que ser expandida para manejar diferentes tipos de condiciones

def p_declaration(p):
    'declaration : INT ID ASSIGN NUM SEMICOLON'

def p_increment_statement(p):
    'increment_statement : ID INCREMENT SEMICOLON'


# Manejo de errores de sintaxis
def p_error(p):
    if p:
        error_message(f"Error de sintaxis en '{p.value}'", p.lineno)
    else:
        error_message("Error de sintaxis: final inesperado del código", len(code_text.get("1.0", "end-1c").split('\n')))

# Construcción del parser
parser = yacc.yacc()

# Función para el análisis léxico
def lex_analyzer(code):
    lexer.input(code)
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append((tok.lineno, tok.type, tok.value))
    return tokens_list

# Función para el análisis sintáctico
def parse_code(code):
    parser.parse(code, lexer=lexer)

def error_message(message, line_number):
    messagebox.showerror("Error de sintaxis", f"{message}\nEn la línea {line_number}")

# Función para procesar el código ingresado
def process_code():
    code = code_text.get("1.0", "end-1c")
    tokens_list = lex_analyzer(code)
    result_text.delete("1.0", "end")
    for token in tokens_list:
        line_number, token_type, token_value = token
        result_text.insert("end", f"Línea {line_number}: {token_type} -> {token_value}\n")
    
    try:
        parse_code(code)
    except Exception as e:
        messagebox.showerror("Error al analizar", str(e))

def lexico():
    window.destroy()
    call(["python", "lexico.py"])

# Creación de la ventana de la interfaz gráfica
window = tk.Tk()
window.title("Lexer and Parser")
window.geometry("600x500")
window.configure(bg="black")

# Etiqueta y campo de texto para ingresar el código
code_label = tk.Label(window, text="Ingrese el código:", font=("Arial", 20, 'bold'), fg="white", bg="black")
code_label.pack()

code_text = tk.Text(window, height=10, width=50)
code_text.pack()

# Crear un frame para los botones
button_frame = tk.Frame(window, bg='black')
button_frame.pack(pady=10)

# Botón para procesar el código
process_button = tk.Button(button_frame, text="Procesar", command=process_code, font=("ARIAL", 14), bg="#83A2FF")
process_button.grid(row=0, column=0, padx=5)

# Botón para limpiar el código ingresado
clear_button = tk.Button(button_frame, text="Limpiar", command=lambda: (code_text.delete("1.0", "end-1c"), result_text.delete("1.0", "end")), font=("ARIAL", 14), bg="#83A2FF")
clear_button.grid(row=0, column=1, padx=5)

lexico_button = tk.Button(button_frame, text="Ir a Lexico", command=lexico, font=("Arial", 16, 'bold'), bg="#FFC436")
lexico_button.grid(row=0, column=2, padx=5)

# Botón para salir del programa
exit_button = tk.Button(button_frame, text="Salir", command=window.destroy, font=("ARIAL", 14), bg="#FF6969")
exit_button.grid(row=0, column=3, padx=5)

# Etiqueta y campo de texto para mostrar los tokens
result_label = tk.Label(window, text="Tokens:", font=("Arial", 20, 'bold'), fg="white", bg="black")
result_label.pack()

result_text = tk.Text(window, height=10, width=50)
result_text.pack()

# Ejecución de la interfaz gráfica
window.mainloop()

import re
import tkinter as tk
from tkinter import ttk
from subprocess import call

class Lexer:
    def __init__(self):
        self.reservada_keywords = ['while', 'System', 'out', 'println', 'int']
        self.Simboloss = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=',  '(', ')', '{', '}', ';', ',', '"', "'","."]
        self.token_patterns = [
            ('Cadena', r'"(?:[^"\\]|\\.)*"'),
            ('VARIABLE', r'\$\w+'),
            ('Numero', r'\d+(\.\d+)?'),
            ('reservada', '|'.join(r'\b' + re.escape(keyword) + r'\b' for keyword in self.reservada_keywords)),
            ('Identificador', r'[A-Za-z_][A-Za-z0-9_]*'),
            ('Simbolos', '|'.join(map(re.escape, self.Simboloss))),
            ('SPACE', r'\s+'),
        ]
        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_patterns)
        self.token_pattern = re.compile(self.token_regex)

    def tokenize(self, text):
        tokens = []
        position = 0
        while position < len(text):
            match = self.token_pattern.match(text, position)
            if match:
                token_type = match.lastgroup
                if token_type != 'SPACE':
                    token_value = match.group(token_type)
                    tokens.append((token_type, token_value))
                position = match.end()
            else:
                position += 1
        return tokens

class LexerApp:
    def __init__(self):
        self.windows = tk.Tk() #Crea una ventana de la clase
        self.windows.title("Analizador léxico") #Establece el titulo de la ventana
        self.windows.configure(bg="black")

        #Crea una etiqueta para el titulo de la aplicacion
        self.text_label = tk.Label(text="----- ANALIZADOR LÉXICO -----", height=1, width=41, font=("Arial", 20, 'bold'), fg="white", bg="black")
        self.text_label.pack()
        
        # Crea una etiqueta para el ingreso del código
        self.text_label_input = tk.Label(text="Ingrese el código:", height=1, width=20, font=("Arial", 14,), fg="white", bg="black")
        self.text_label_input.pack(pady=5)
        
        #Crea un cuadro de texto para la entrada de texto
        self.text_input = tk.Text(self.windows, height=6, width=70, font=("Arial", 12))
        self.text_input.pack(pady=5)

        #Crea un marco para los botones
        self.button_frame = tk.Frame(self.windows, bg="black")
        self.button_frame.pack(pady=5)

        #crea un boton para realizar el analisis lexico del texto de entrada
        self.analyze_button = tk.Button(self.button_frame, text="Analizar", command=self.analyze_text, bg="#83A2FF", font=("Arial", 14, 'bold'))
        self.analyze_button.grid(row=0, column=0, padx=30, pady=10)

        #crea un boton para limpiar el cuadro de texto
        self.clean_button = tk.Button(self.button_frame, text="Limpiar", command=self.clean_text, bg="#83A2FF", font=("Arial", 14, 'bold'))
        self.clean_button.grid(row=0, column=1, padx=30, pady=10)

        #Boton  para ir al codigo de sintactico
        self.sintactico_button = tk.Button(self.button_frame, text="Ir A Sictactico", command=self.sintactico, bg="#FFC436", font=("Arial", 14, 'bold'))
        self.sintactico_button.grid(row=0, column=2, padx=30, pady=10)
        
        #Crea un boton para salir del programa
        self.exit_button = tk.Button(self.button_frame, text="Salir", command=self.exit_app, bg="#FF6969", font=("Arial", 14, 'bold'))
        self.exit_button.grid(row=0, column=3, padx=30, pady=10)

        self.tree = ttk.Treeview(self.windows, columns=("Linea", "Token", "Funcion", "Reservada", "Cadena", "Identificador", "Símbolo", "Numero"),show="headings")
        self.tree.heading("Linea", text="Linea")
        self.tree.heading("Token", text="Token")
        self.tree.heading("Funcion", text="Funcion")
        self.tree.heading("Reservada", text="Reservada")
        self.tree.heading("Cadena", text="Cadena")
        self.tree.heading("Identificador", text="Identificador")
        self.tree.heading("Símbolo", text="Símbolo")
        self.tree.heading("Numero", text="Numero")
        self.tree.pack()

         # Configura la alineación y el ancho de las columnas
        columns = ("Linea", "Token", "Funcion", "Reservada", "Cadena", "Identificador", "Símbolo", "Numero")
        column_widths = (70, 100, 80, 100, 70, 90, 70, 80)  # Define los anchos deseados

        for column, width in zip(columns, column_widths):
            self.tree.column(column, anchor="center", width=width)

        self.text_label = tk.Label(text=" ---- Contador de Elementos --- ", height=1, width=50, font=("Arial", 15, 'bold'), fg="white", bg="black")
        self.text_label.pack(pady=2)

        self.count_tree = ttk.Treeview(self.windows, columns=("Elemento", "Cantidad"), show="headings")
        self.count_tree.heading("Elemento", text="Elemento")
        self.count_tree.heading("Cantidad", text="Cantidad")
        self.count_tree.pack(pady=10)
        
        columns = ("Elemento", "Cantidad")
        column_widths = (300, 300)  # Define los anchos deseados

        for column, width in zip(columns, column_widths):
            self.count_tree.column(column, anchor="center", width=width)
        
        self.count_tree['height'] = 6
        
        
    def analyze_text(self):
        lexer = Lexer()
        text = self.text_input.get("1.0", "end")
        lines = text.split('\n')
        tokens_by_line = [lexer.tokenize(line) for line in lines]

        self.tree.delete(*self.tree.get_children())
        self.count_tree.delete(*self.count_tree.get_children())
        
        # Diccionario para contar los tokens
        count_tokens = {
            'Cadena': 0,
            'reservada': 0,
            'Numero': 0,
            'Identificador': 0,
            'Simbolos': 0
        }

    
         # Count elements
        count_elements = {
            ';': 0,
            '(': 0,
            ')': 0,
            '{': 0,
            '}': 0,
            '+': 0,
            '.': 0,
            '=': 0,
        }

        for line_number, line_tokens in enumerate(tokens_by_line, start=1):
            for token_type, token_value in line_tokens:
                row_data = [line_number, token_type, token_value, "", "", "", "", ""]  # Aseguramos que hay 8 elementos
                if token_type == 'Numero':
                    row_data[7] = "x"
                    count_tokens['Numero'] += 1
                elif token_type == 'reservada':
                    row_data[3] = "x"
                    count_tokens['reservada'] += 1
                elif token_type == 'Identificador':
                    row_data[5] = "x"
                    count_tokens['Identificador'] += 1
                elif token_type == 'Simbolos':
                    row_data[6] = "x"
                    count_tokens['Simbolos'] += 1
                    if token_value in count_elements:
                        count_elements[token_value] += 1
                elif token_type == 'Cadena':
                    row_data[4] = "x"
                    count_tokens['Cadena'] += 1

                self.tree.insert("", "end", values=row_data)

        for element, count in count_elements.items():
            self.count_tree.insert("", "end", values=(element, count))

        for token_type, count in count_tokens.items():
            self.count_tree.insert("", "end", values=(token_type, count))

        for token_value in token:
            if token_value in count_elements:
                count_elements[token_value] += 1

        for element, count in count_elements.items():
            self.count_tree.insert("", "end", values=(element, count))


        # Insertar resultados en la tabla de conteo
        for token_type, count in count_tokens.items():
            self.count_tree.insert("", "end", values=(token_type, count))
    
    def clean_text(self):
        self.text_input.delete("1.0", "end")
        self.tree.delete(*self.tree.get_children())
        self.count_tree.delete(*self.count_tree.get_children())

    def exit_app(self): #Define un metodo para salir del programa
        self.windows.destroy()

    def run(self):
        self.windows.mainloop()
    
    def sintactico(self):
        self.windows.destroy()
        call(["python", "SintacticoIF.py"])
    
app = LexerApp()
app.run()

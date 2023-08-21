import tkinter as tk


class Lexer:
    def tokenize(self, text):
        self.tokens = ['for', 'do', 'while', 'if', 'else']
        arreglo = []
        current_token = ""
        for char in text:
            if char in self.tokens:
                if current_token != "":
                    arreglo.append(current_token)
                    current_token = ""

                arreglo.append(char)
            elif char.isspace():
                if current_token != "":
                    arreglo.append(current_token)
                    current_token = ""
            else:
                current_token += char
        if current_token != "":
            arreglo.append(current_token)
        return arreglo

    def analyze(self, text):
        arreglo = self.tokenize(text)
        result = ""
        for token in arreglo:
            if token in self.tokens:
                result += f"{token} es reservada \n"
                print("\n")
            else:
                 
                result += f"({token}) No se encuntra, es error de lexico\n"
                

        return result


class LexerApp:
    def __init__(self):
        self.windows = tk.Tk()
        self.windows.title("Analizando el lexico")

        self.text_input = tk.Text(self.windows, height=10, width=50)
        self.text_input.pack()

        self.analyze_button = tk.Button(self.windows, text="Analizar", command=self.analyze_text, bg="blue")
        self.analyze_button.pack()

        self.clean_button = tk.Button(self.windows, text="Eliminar", command=self.clean_text, bg = "orange")
        self.clean_button.pack()

        self.result_label = tk.Label(self.windows, text="", height=10, width=50, bg = "yellow")
        self.result_label.pack()

    def analyze_text(self):
        lexer = Lexer()
        text = self.text_input.get("1.0", "end")
        result = lexer.analyze(text)
        self.result_label.config(text=result)

    def clean_text(self):
        self.text_input.delete("1.0", "end")
        self.result_label.config(text="")

    def run(self):
        self.windows.mainloop()


app = LexerApp()
app.run()
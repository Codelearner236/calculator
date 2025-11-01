import customtkinter as ctk
import math
import os

class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x600")
        if os.path.exists("calculator.ico"):
            self.iconbitmap('calculator.ico')
        else:
            try:
                self.iconbitmap("Calculator/calculator.ico")
            except:
                pass  # Skip if icon not found
        self.resizable(False, False)
        self.title("Colored Calculator")
        ctk.set_appearance_mode("dark")
        
        self.bg_color = "#121212"
        self.button_color = "#1e1e1e"
        self.accent_color = "#4fd1c5"
        
        self.configure(fg_color=self.bg_color)
        self.current_expression = ""
        self.is_scientific = False
        self.create_widgets()
        self.current_font_size = 64

    def create_widgets(self):
        # Mode toggle frame
        mode_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        mode_frame.pack(fill="x", padx=20, pady=(20, 10))
        self.normal_btn = ctk.CTkButton(mode_frame, text="Normal", command=self.set_normal_mode, 
                                        fg_color=self.accent_color, text_color="black", font=("Arial", 16))
        self.normal_btn.pack(side="left", padx=(0, 10))
        self.scientific_btn = ctk.CTkButton(mode_frame, text="Scientific", command=self.set_scientific_mode, 
                                            fg_color=self.button_color, text_color="white", font=("Arial", 16))
        self.scientific_btn.pack(side="left")

        # Display frame
        display_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        display_frame.pack(fill="x", padx=20, pady=(10, 10))

        # Result display (shows full expression)
        self.result = ctk.CTkEntry(display_frame, font=("Arial", 32), 
                                   fg_color=self.bg_color, text_color="white", 
                                   border_width=0, justify="right")
        self.result.pack(fill="x", expand=True)
        self.result.insert(0, "0")
        self.result.configure(state="readonly")

        # Button frame
        self.button_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.button_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.create_buttons()

    def create_buttons(self):
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        buttons = []
        if self.is_scientific:
            buttons = [
                'C', '+/-', '%', '/', 'sin',
                '7', '8', '9', '*', 'cos',
                '4', '5', '6', '-', 'tan',
                '1', '2', '3', '+', 'log',
                '0', '.', '=', 'sqrt'
            ]
            cols = 5
        else:
            buttons = [
                'C', '+/-', '%', '/',
                '7', '8', '9', '*',
                '4', '5', '6', '-',
                '1', '2', '3', '+',
                '0', '.', '='
            ]
            cols = 4

        row, col = 0, 0
        for button in buttons:
            if button in ['C', '+/-', '%', '/', '*', '-', '+', '=', 'sin', 'cos', 'tan', 'log', 'sqrt']:
                color = self.accent_color
                text_color = "black"
                hover_color = self.lighten_color(self.accent_color, 0.1)
            else:
                color = self.button_color
                text_color = "white"
                hover_color = self.lighten_color(self.button_color, 0.1)
            
            btn = ctk.CTkButton(self.button_frame, text=button, width=60, height=60, 
                                fg_color=color, text_color=text_color, 
                                font=("Arial", 20), corner_radius=10,
                                hover_color=hover_color,
                                command=lambda x=button: self.button_click(x))
            
            # Special case for '0' button
            if button == '0':
                btn.grid(row=row, column=col, columnspan=2, padx=5, pady=5, sticky="nsew")
                col += 2
            else:
                btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                col += 1
            
            if col >= cols:
                col = 0
                row += 1

        # Configure grid
        for i in range(row + 1):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for i in range(cols):
            self.button_frame.grid_columnconfigure(i, weight=1)

    def set_normal_mode(self):
        self.is_scientific = False
        self.normal_btn.configure(fg_color=self.accent_color, text_color="black")
        self.scientific_btn.configure(fg_color=self.button_color, text_color="white")
        self.create_buttons()

    def set_scientific_mode(self):
        self.is_scientific = True
        self.scientific_btn.configure(fg_color=self.accent_color, text_color="black")
        self.normal_btn.configure(fg_color=self.button_color, text_color="white")
        self.create_buttons()

    def lighten_color(self, color, factor=0.1):
        # Convert hex to RGB
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # Lighten
        new_rgb = [min(int(c + (255 - c) * factor), 255) for c in rgb]
        
        # Convert back to hex
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)

    def button_click(self, key):
        if key == "=":
            self.calculate()
        elif key == "C":
            self.clear()
        elif key == "+/-":
            self.negate()
        elif key == "%":
            self.percentage()
        elif key in ['sin', 'cos', 'tan', 'log', 'sqrt']:
            self.apply_function(key)
        else:
            self.add_to_expression(key)

    def add_to_expression(self, value):
        if self.current_expression == "0" or self.current_expression == "":
            self.current_expression = str(value)
        else:
            self.current_expression += str(value)
        self.update_result()

    def calculate(self):
        try:
            # Replace functions with math equivalents for eval
            expr = self.current_expression
            expr = expr.replace('sin', 'math.sin(math.radians')
            expr = expr.replace('cos', 'math.cos(math.radians')
            expr = expr.replace('tan', 'math.tan(math.radians')
            expr = expr.replace('log', 'math.log10')
            expr = expr.replace('sqrt', 'math.sqrt')
            # Close parentheses for trig functions
            expr = expr.replace('sin(math.radians', 'math.sin(math.radians(')
            expr = expr.replace('cos(math.radians', 'math.cos(math.radians(')
            expr = expr.replace('tan(math.radians', 'math.tan(math.radians(')
            # But this is tricky; better to handle separately, but for simplicity, assume no chained functions
            result = eval(expr)
            self.current_expression = str(result)
        except:
            self.current_expression = "Error"
        self.update_result()

    def clear(self):
        self.current_expression = ""
        self.update_result()

    def negate(self):
        try:
            # Negate the last number in expression
            parts = self.current_expression.split()
            if parts:
                last = parts[-1]
                if last.replace('.', '').replace('-', '').isdigit():
                    parts[-1] = str(-float(last))
                    self.current_expression = ' '.join(parts)
        except:
            pass
        self.update_result()

    def percentage(self):
        try:
            # Percentage the last number
            parts = self.current_expression.split()
            if parts:
                last = parts[-1]
                if last.replace('.', '').replace('-', '').isdigit():
                    parts[-1] = str(float(last) / 100)
                    self.current_expression = ' '.join(parts)
        except:
            pass
        self.update_result()

    def apply_function(self, func):
        try:
            # Apply function to the last number
            parts = self.current_expression.split()
            if parts:
                last = parts[-1]
                if last.replace('.', '').replace('-', '').isdigit():
                    num = float(last)
                    if func == 'sin':
                        result = math.sin(math.radians(num))
                    elif func == 'cos':
                        result = math.cos(math.radians(num))
                    elif func == 'tan':
                        result = math.tan(math.radians(num))
                    elif func == 'log':
                        result = math.log10(num)
                    elif func == 'sqrt':
                        result = math.sqrt(num)
                    parts[-1] = str(result)
                    self.current_expression = ' '.join(parts)
        except:
            pass
        self.update_result()

    def update_result(self):
        self.result.configure(state="normal")
        self.result.delete(0, ctk.END)
        display_text = self.current_expression if self.current_expression else "0"
        self.result.insert(0, display_text)
        
        # Adjust font size based on text length
        text_length = len(display_text)
        if text_length > 10:
            new_font_size = 24
        elif text_length > 7:
            new_font_size = 32
        else:
            new_font_size = 48
        
        self.result.configure(font=("Arial", new_font_size))
        self.result.configure(state="readonly")

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
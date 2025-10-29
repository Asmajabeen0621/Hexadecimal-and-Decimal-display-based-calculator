import tkinter as tk
from tkinter import ttk, messagebox

class HexDecimalCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Visible Hex/Dec Calculator")
        master.resizable(False, False) # Prevent resizing the window

        # Store the current expression and the last result
        self.current_expression = ""
        self.result_value = 0

        # --- Styling ---
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 14), padding=10)
        style.configure('Number.TButton', background='#e0e0e0')
        style.configure('Operator.TButton', background='#ff9800', foreground='white')
        style.configure('Clear.TButton', background='#f44336', foreground='white')
        style.configure('Convert.TButton', background='#2196f3', foreground='white')

        # --- Display Frames ---
        
        # 1. Expression/Input Display
        self.input_text = tk.StringVar()
        self.input_entry = ttk.Entry(
            master, 
            textvariable=self.input_text, 
            font=('Arial', 24), 
            justify='right', 
            state='readonly' # Read-only so user can't type directly
        )
        self.input_entry.grid(row=0, column=0, columnspan=4, sticky='nsew', ipady=10)

        # 2. Conversion Display
        self.hex_var = tk.StringVar(value="HEX: 0")
        self.dec_var = tk.StringVar(value="DEC: 0")

        ttk.Label(master, textvariable=self.dec_var, font=('Arial', 12), foreground='#0000ff').grid(row=1, column=0, columnspan=2, sticky='w', padx=5)
        ttk.Label(master, textvariable=self.hex_var, font=('Arial', 12), foreground='#800080').grid(row=1, column=2, columnspan=2, sticky='e', padx=5)


        # --- Buttons Layout ---
        buttons = [
            ('C', 2, 0, 'Clear.TButton'), ('(', 2, 1, 'Operator.TButton'), (')', 2, 2, 'Operator.TButton'), ('/', 2, 3, 'Operator.TButton'),
            ('7', 3, 0, 'Number.TButton'), ('8', 3, 1, 'Number.TButton'), ('9', 3, 2, 'Number.TButton'), ('*', 3, 3, 'Operator.TButton'),
            ('4', 4, 0, 'Number.TButton'), ('5', 4, 1, 'Number.TButton'), ('6', 4, 2, 'Number.TButton'), ('-', 4, 3, 'Operator.TButton'),
            ('1', 5, 0, 'Number.TButton'), ('2', 5, 1, 'Number.TButton'), ('3', 5, 2, 'Number.TButton'), ('+', 5, 3, 'Operator.TButton'),
            ('0', 6, 0, 'Number.TButton'), ('.', 6, 1, 'Number.TButton'), ('\u232B', 6, 2, 'Clear.TButton'), ('=', 6, 3, 'Operator.TButton') # \u232B is the backspace symbol
        ]

        # Create buttons
        for (text, row, col, style_name) in buttons:
            self.create_button(text, row, col, style_name)

    def create_button(self, text, row, col, style_name):
        """Creates a button and binds it to the appropriate action."""
        action = lambda t=text: self.button_click(t)
        
        button = ttk.Button(
            self.master, 
            text=text, 
            command=action, 
            style=style_name
        )
        # Use sticky 'nsew' to make buttons fill the cell
        button.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        
        # Configure row and column weights to make the grid expand nicely
        self.master.grid_columnconfigure(col, weight=1)
        self.master.grid_rowconfigure(row, weight=1)

    def button_click(self, text):
        """Handles button clicks and updates the display."""
        if text == 'C':
            self.clear_all()
        elif text == '=':
            self.calculate()
        elif text == '\u232B': # Backspace
            self.current_expression = self.current_expression[:-1]
        else:
            # Append number or operator to the expression
            self.current_expression += str(text)

        # Update the main display
        self.input_text.set(self.current_expression)
        
        # Update the converter display
        self.update_converters()

    def clear_all(self):
        """Clears the current expression and resets the result."""
        self.current_expression = ""
        self.result_value = 0
        self.input_text.set("")
        self.update_converters(0)

    def calculate(self):
        """Evaluates the mathematical expression."""
        try:
            # Use 'eval' carefully, assuming controlled input from buttons
            # Replace 'x' with '*' for Python's eval
            safe_expression = self.current_expression.replace('×', '*').replace('÷', '/')
            
            # Use float for evaluation to handle decimals
            self.result_value = eval(safe_expression)
            
            # Format the result nicely (e.g., remove .0 if it's an integer)
            if self.result_value == int(self.result_value):
                self.result_value = int(self.result_value)
                
            self.current_expression = str(self.result_value)
            self.input_text.set(self.current_expression)
            self.update_converters(self.result_value)

        except (SyntaxError, NameError, TypeError, ZeroDivisionError) as e:
            messagebox.showerror("Calculation Error", f"Invalid Expression or Error: {e}")
            self.clear_all()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.clear_all()

    def update_converters(self, value=None):
        """Updates the Hexadecimal and Decimal displays based on the current input/result."""
        
        # If a specific value is passed (e.g., from calculate), use it.
        # Otherwise, try to parse the current expression.
        if value is not None:
            num = value
        elif self.current_expression:
            try:
                # Attempt to safely parse the current input as a number
                num = float(self.current_expression)
            except ValueError:
                # If the input isn't a valid single number yet (e.g., '5+3'), just keep the old value
                return
        else:
            num = 0
        
        # Only convert if the number is an integer (since hex/dec are for integers)
        if isinstance(num, int) or num == int(num):
            integer_num = int(num)
            
            # Handle negative numbers for hex display
            hex_str = hex(abs(integer_num)).replace('0x', '')
            if integer_num < 0:
                hex_str = "-" + hex_str
                
            self.dec_var.set(f"DEC: {integer_num:,}") # Use thousands separator
            self.hex_var.set(f"HEX: {hex_str.upper()}")
        else:
            # Clear converters if the number is a float
            self.dec_var.set(f"DEC: {num}")
            self.hex_var.set(f"HEX: N/A (Float)")
            

if __name__ == '__main__':
    root = tk.Tk()
    app = HexDecimalCalculator(root)
    # Start the GUI event loop
    root.mainloop()
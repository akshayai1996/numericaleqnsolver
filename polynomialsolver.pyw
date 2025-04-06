import tkinter as tk
from tkinter import messagebox
import sympy as sp

def newton_raphson(poly, x0, tol=1e-6, max_iter=100):
    x = sp.symbols('x')
    f = sp.sympify(poly)
    f_prime = sp.diff(f, x)
    
    for i in range(max_iter):
        f_val = f.subs(x, x0)
        f_prime_val = f_prime.subs(x, x0)
        
        if f_prime_val == 0:
            raise ValueError("Derivative is zero. No solution found.")
        
        x1 = x0 - f_val / f_prime_val
        
        if abs(x1 - x0) < tol:
            return x1.evalf()
        
        x0 = x1
    
    raise ValueError("Maximum iterations exceeded. No solution found.")

def solve_polynomial():
    try:
        degree = int(entry_degree.get())
        coefficients = [float(entry_coefficients[i].get()) for i in range(degree + 1)]
        
        x = sp.symbols('x')
        poly = sum(coefficients[i] * x**i for i in range(degree + 1))
        
        # Format the polynomial string
        terms = []
        for i in range(degree, -1, -1):
            coeff = coefficients[i]
            if coeff == int(coeff):
                coeff = int(coeff)
            if i == 0:
                terms.append(f"{coeff}")
            elif i == 1:
                terms.append(f"{coeff}x")
            else:
                terms.append(f"{coeff}x^{i}")
        
        poly_str = " + ".join(terms)
        
        label_poly.config(text=f"Polynomial: {poly_str} = 0")
        
        x0 = float(entry_initial_guess.get())
        root = newton_raphson(poly, x0)
        
        label_result.config(text=f"Closest Root: {root:.6f}")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input. Please enter valid numbers. Details: {str(e)}")

def create_coefficient_entries():
    try:
        degree = int(entry_degree.get())
        
        for widget in frame_coefficients.winfo_children():
            widget.destroy()
        
        global entry_coefficients
        entry_coefficients = []
        
        for i in range(degree + 1):
            frame = tk.Frame(frame_coefficients)
            tk.Label(frame, text=f"Coefficient a{i}:").pack(side=tk.LEFT, padx=10, pady=10)
            entry = tk.Entry(frame, width=30)
            entry.pack(side=tk.LEFT, padx=10, pady=10)
            frame.pack()
            entry_coefficients.append(entry)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Polynomial Solver")
root.minsize(360, 400)

# Create and place the widgets using pack for center alignment
tk.Label(root, text="Polynomial Solver using Newton-Raphson Method").pack(padx=10, pady=10)

frame_degree = tk.Frame(root)
tk.Label(frame_degree, text="Degree of Polynomial:").pack(side=tk.LEFT, padx=10, pady=10)
entry_degree = tk.Entry(frame_degree, width=30)
entry_degree.pack(side=tk.LEFT, padx=10, pady=10)
frame_degree.pack()

button_create_entries = tk.Button(root, text="Create Coefficient Entries", command=create_coefficient_entries)
button_create_entries.pack(padx=10, pady=10)

frame_coefficients = tk.Frame(root)
frame_coefficients.pack()

frame_initial_guess = tk.Frame(root)
tk.Label(frame_initial_guess, text="Initial Guess:").pack(side=tk.LEFT, padx=10, pady=10)
entry_initial_guess = tk.Entry(frame_initial_guess, width=30)
entry_initial_guess.pack(side=tk.LEFT, padx=10, pady=10)
frame_initial_guess.pack()

button_solve = tk.Button(root, text="Solve Polynomial", command=solve_polynomial)
button_solve.pack(padx=10, pady=10)

label_poly = tk.Label(root, text="Polynomial:")
label_poly.pack(padx=10, pady=10)

label_result = tk.Label(root, text="Closest Root:")
label_result.pack(padx=10, pady=10)

# Run the main loop
root.mainloop()
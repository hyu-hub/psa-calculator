import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

class PSACalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("PSA Calculator")
        self.root.geometry("800x900")
        self.iteration = 1
        self.base_sens = None
        self.history = []
        
        # Custom Colors
        self.COLORS = {
            'bg': '#2C3E50',
            'fg': '#ECF0F1',
            'accent': '#3498DB',
            'button': '#2980B9',
            'button_hover': '#3498DB',
            'history_bg': '#34495E'
        }
        
        # Configure root window
        self.root.configure(bg=self.COLORS['bg'])
        
        # Custom Style
        style = ttk.Style()
        style.configure('Custom.TFrame', background=self.COLORS['bg'])
        style.configure('Custom.TLabel', 
                       background=self.COLORS['bg'], 
                       foreground=self.COLORS['fg'],
                       font=('Segoe UI', 10))
        style.configure('Title.TLabel',
                       background=self.COLORS['bg'],
                       foreground=self.COLORS['fg'],
                       font=('Segoe UI', 24, 'bold'))
        style.configure('Custom.TButton',
                       background=self.COLORS['button'],
                       foreground=self.COLORS['fg'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        
        # Main Container
        main_container = ttk.Frame(root, style='Custom.TFrame')
        main_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Title
        ttk.Label(main_container, 
                 text="PSA Calculator", 
                 style='Title.TLabel').pack(pady=(0, 20))
        
        # Description
        desc_text = ("Enter your starting sensitivity (360° across mousepad)\n"
                    "Test both values and choose which feels better.")
        ttk.Label(main_container, 
                 text=desc_text,
                 style='Custom.TLabel',
                 font=('Segoe UI', 12)).pack(pady=(0, 20))
        
        # Input Section
        input_frame = ttk.Frame(main_container, style='Custom.TFrame')
        input_frame.pack(fill='x', pady=20)
        
        # Add validation and tooltip functions
        vcmd = (self.root.register(self.validate_input), '%P')
        self.sens_entry = tk.Entry(input_frame,
                                 font=('Segoe UI', 14),
                                 width=15,
                                 justify='center',
                                 bg=self.COLORS['fg'],
                                 validate='key',
                                 validatecommand=vcmd)
        self.create_tooltip(self.sens_entry, "Enter a sensitivity value between 0.1 and 100")
        self.sens_entry.pack(pady=10)
        
        # Reorganize buttons in input frame
        button_container = ttk.Frame(input_frame, style='Custom.TFrame')
        button_container.pack(pady=10)
        
        start_btn = tk.Button(button_container,
                            text="Start Calculation",
                            font=('Segoe UI', 12, 'bold'),
                            bg=self.COLORS['accent'],
                            fg=self.COLORS['fg'],
                            command=self.start_calculation,
                            relief='flat',
                            padx=20, pady=10)
        
        reset_btn = tk.Button(button_container,
                            text="Reset",
                            font=('Segoe UI', 12, 'bold'),
                            bg='#E74C3C',
                            fg=self.COLORS['fg'],
                            command=self.reset_calculator,
                            relief='flat',
                            padx=20, pady=10)
        
        start_btn.pack(side='left', padx=5)
        reset_btn.pack(side='left', padx=5)
        
        # Add hover effects
        for btn in [start_btn, reset_btn]:
            btn.bind('<Enter>', lambda e, b=btn: self.on_hover(b, True))
            btn.bind('<Leave>', lambda e, b=btn: self.on_hover(b, False))
        
        # Remove this duplicate line
        # start_btn.pack(pady=10)  <- DELETE THIS LINE
        
        # Results Section
        self.results_frame = ttk.Frame(main_container, style='Custom.TFrame')
        self.results_frame.pack(fill='x', pady=20)
        
        self.current_label = ttk.Label(self.results_frame,
                                     text="",
                                     style='Custom.TLabel',
                                     font=('Segoe UI', 14))
        self.current_label.pack()
        
        # Choice Buttons
        self.buttons_frame = ttk.Frame(self.results_frame, style='Custom.TFrame')
        self.buttons_frame.pack(pady=20)
        
        button_style = {'font': ('Segoe UI', 12),
                       'relief': 'flat',
                       'padx': 20,
                       'pady': 10}
        
        self.higher_btn = tk.Button(self.buttons_frame,
                                  text="Higher feels better",
                                  bg=self.COLORS['button'],
                                  fg=self.COLORS['fg'],
                                  command=lambda: self.make_choice('H'),
                                  **button_style)
        
        self.lower_btn = tk.Button(self.buttons_frame,
                                 text="Lower feels better",
                                 bg=self.COLORS['button'],
                                 fg=self.COLORS['fg'],
                                 command=lambda: self.make_choice('L'),
                                 **button_style)
        
        self.quit_btn = tk.Button(self.buttons_frame,
                                text="Found my sensitivity!",
                                bg='#27AE60',
                                fg=self.COLORS['fg'],
                                command=self.quit_calculation,
                                **button_style)
        
        # History Section
        self.history_text = ScrolledText(main_container,
                                       font=('Consolas', 11),
                                       height=12,
                                       bg=self.COLORS['history_bg'],
                                       fg=self.COLORS['fg'],
                                       relief='flat')
        self.history_text.pack(fill='both', expand=True)
        
        # Add credit label
        credit_label = ttk.Label(main_container,
                               text="Made by HYU",
                               style='Custom.TLabel',
                               font=('Segoe UI', 8))
        credit_label.pack(pady=(10, 0))
        history_label = ttk.Label(main_container,
                                text="Calculation History",
                                style='Custom.TLabel',
                                font=('Segoe UI', 14, 'bold'))
        history_label.pack(pady=(20, 10))

    def calculate_psa_values(self, base_sensitivity):
        higher = round(base_sensitivity * 1.5, 3)
        lower = round(base_sensitivity * 0.5, 3)
        return lower, higher
    
    def start_calculation(self):
        try:
            self.base_sens = float(self.sens_entry.get())
            self.history = []
            self.iteration = 1
            self.update_display()
            self.show_choice_buttons()
            self.history_text.delete(1.0, tk.END)
            self.add_to_history(f"Starting sensitivity: {self.base_sens}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def update_display(self):
        lower, higher = self.calculate_psa_values(self.base_sens)
        self.current_label.config(
            text=f"Iteration {self.iteration}\n"
                f"Higher: {higher}\n"
                f"Lower: {lower}\n"
                f"Current: {self.base_sens}"
        )
    
    def show_choice_buttons(self):
        self.higher_btn.pack(side='left', padx=5)
        self.lower_btn.pack(side='left', padx=5)
        self.quit_btn.pack(side='left', padx=5)
    
    def add_to_history(self, text):
        self.history_text.insert(tk.END, f"{text}\n")
        self.history_text.see(tk.END)
    
    def make_choice(self, choice):
        lower, higher = self.calculate_psa_values(self.base_sens)
        old_sens = self.base_sens
        if choice == 'H':
            self.base_sens = higher
            choice_text = "Higher"
        else:
            self.base_sens = lower
            choice_text = "Lower"
            
        self.add_to_history(
            f"Iteration {self.iteration}: {choice_text} chosen"
            f" ({old_sens} → {self.base_sens})"
        )
        self.iteration += 1
        self.update_display()
    
    # Add these new methods
    def validate_input(self, value):
        if value == "" or value == "." or value.startswith("0."):
            return True
        try:
            if value.count('.') <= 1:  # Allow one decimal point
                if '.' in value:
                    # If there's a decimal, validate only if enough digits are entered
                    if len(value.split('.')[1]) <= 3:  # Allow up to 3 decimal places
                        if float(value) <= 100:
                            return True
                else:
                    # For whole numbers
                    if float(value) <= 100:
                        return True
            return False
        except ValueError:
            return False

    def create_tooltip(self, widget, text):
        tooltip = tk.Label(widget,
                         text=text,
                         bg='#2C3E50',
                         fg='white',
                         padx=5,
                         pady=3)
        tooltip.pack_forget()
        
        def enter(event):
            tooltip.lift()
            tooltip.place(x=0, y=-30)
        
        def leave(event):
            tooltip.place_forget()
        
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)

    def on_hover(self, button, entering):
        button.configure(bg=self.COLORS['button_hover'] if entering else self.COLORS['button'])

    def reset_calculator(self):
        self.sens_entry.delete(0, tk.END)
        self.history_text.delete(1.0, tk.END)
        self.current_label.config(text="")
        self.base_sens = None
        self.iteration = 1
        for btn in [self.higher_btn, self.lower_btn, self.quit_btn]:
            btn.pack_forget()

    # Modify the quit_calculation method
    def quit_calculation(self):
        final_sens = round(self.base_sens, 3)
        self.add_to_history(f"\nFinal sensitivity: {final_sens}")
        
        # Create custom dialog with copy button
        dialog = tk.Toplevel(self.root)
        dialog.title("Final Sensitivity")
        dialog.geometry("300x150")
        dialog.configure(bg=self.COLORS['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        msg = ttk.Label(dialog,
                       text=f"Your perfect sensitivity is:\n{final_sens}",
                       style='Custom.TLabel',
                       font=('Segoe UI', 12, 'bold'))
        msg.pack(pady=20)
        
        def copy_value():
            self.root.clipboard_clear()
            self.root.clipboard_append(str(final_sens))
            copy_btn.configure(text="Copied!")
            dialog.after(1000, lambda: copy_btn.configure(text="Copy Value"))
        
        copy_btn = tk.Button(dialog,
                           text="Copy Value",
                           command=copy_value,
                           bg=self.COLORS['accent'],
                           fg=self.COLORS['fg'],
                           font=('Segoe UI', 10),
                           relief='flat',
                           padx=10,
                           pady=5)
        copy_btn.pack(pady=10)
        
        ok_btn = tk.Button(dialog,
                          text="OK",
                          command=dialog.destroy,
                          bg=self.COLORS['button'],
                          fg=self.COLORS['fg'],
                          font=('Segoe UI', 10),
                          relief='flat',
                          padx=10,
                          pady=5)
        ok_btn.pack(pady=5)

# Add this at the end of the file
if __name__ == "__main__":
    root = tk.Tk()
    app = PSACalculator(root)
    root.mainloop()
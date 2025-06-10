import customtkinter as ctk
from tkinter import Canvas

class HowtousePage(ctk.CTkFrame): 
    def __init__(self, master, back_to_main_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.back_to_main_callback = back_to_main_callback
        
        # Main title
        title = ctk.CTkLabel(self, text="Tutorial", font=("Segoe UI", 60, "bold"))
        title.pack(pady=20)

        # Create main container for left and right sections
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=20)

        # Left side - bordered button panel
        self.border_frame = ctk.CTkFrame(main_container, fg_color="transparent", 
                                       border_width=2, corner_radius=10)
        self.border_frame.pack(side="left", fill="y", padx=(0, 40))

        # Title inside border
        title = ctk.CTkLabel(self.border_frame, text="Gaming with Bare Hands", 
                            font=("Segoe UI", 32, "bold"))
        title.pack(pady=20)

        # Create all buttons with consistent styling
        button_font = ("Segoe UI", 16)
        button_width = 300
        button_height = 40
        button_pady = 10

        self.btn_start = ctk.CTkButton(self.border_frame, text="Start", 
                                     font=button_font, width=button_width, 
                                     height=button_height, state="disabled")
        self.btn_start.pack(pady=button_pady)

        self.btn_currentpreset = ctk.CTkButton(self.border_frame, text="Current Preset", 
                                             font=button_font, width=button_width, 
                                             height=button_height, state="disabled")
        self.btn_currentpreset.pack(pady=button_pady)

        self.btn_changepreset = ctk.CTkButton(self.border_frame, text="Change Preset", 
                                            font=button_font, width=button_width, 
                                            height=button_height, state="disabled")
        self.btn_changepreset.pack(pady=button_pady)

        self.btn_gestures = ctk.CTkButton(self.border_frame, text="Gestures", 
                                        font=button_font, width=button_width, 
                                        height=button_height, state="disabled")
        self.btn_gestures.pack(pady=button_pady)

        self.btn_howtouse = ctk.CTkButton(self.border_frame, text="How To Use", 
                                        font=button_font, width=button_width, 
                                        height=button_height, state="disabled")
        self.btn_howtouse.pack(pady=button_pady)

        self.btn_settings = ctk.CTkButton(self.border_frame, text="Settings", 
                                        font=button_font, width=button_width, 
                                        height=button_height, state="disabled")
        self.btn_settings.pack(pady=button_pady)

        self.btn_exit = ctk.CTkButton(self.border_frame, text="Exit", 
                                    font=button_font, width=button_width, 
                                    height=button_height, state="disabled")
        self.btn_exit.pack(pady=button_pady)

        # Right side - tutorial canvas
        self.canvas = Canvas(main_container, width=500, height=600, 
                           bg=self._apply_appearance_mode("#2b2b2b"), 
                           highlightthickness=0)
        self.canvas.pack(side="right", fill="both", expand=True)

        # Draw arrows after everything is rendered
        self.after(100, self.draw_all_arrows)

        # Back button at bottom
        cancel_button = ctk.CTkButton(self, text="Back", 
                                    command=self.cancel_and_return, 
                                    font=("Segoe UI", 16, "bold"))
        cancel_button.pack(pady=10)

    def draw_all_arrows(self):
        """Draw arrows pointing to all buttons with descriptions"""
        self.canvas.delete("all")
    
    # Get the vertical positions of all buttons relative to canvas
        button_positions = []
        for widget in [self.btn_start, self.btn_currentpreset, self.btn_changepreset, 
                      self.btn_gestures, self.btn_howtouse, self.btn_settings, self.btn_exit]:
            btn_x, btn_y = self.get_widget_position(widget)
            button_positions.append((btn_x, btn_y))
    
    # Arrow configurations for each button
        arrow_configs = [
            ("Starts the gesture recognition system", 50),
            ("Shows your currently active preset", 50),
            ("Change between different preset configurations", 50),
            ("View and customize gesture mappings", 50),
            ("View this tutorial page", 50),
            ("Adjust application settings", 50),
            ("Exit the application", 50)
        ]
    
    # Draw each arrow with correct target coordinates
        for i, ((btn_x, btn_y), (text, start_x)) in enumerate(zip(button_positions, arrow_configs)):
            start_y = 200 + i * 90  # Vertical spacing between arrows
            self.draw_button_arrow(btn_x, btn_y, text, start_x, start_y)

    def draw_button_arrow(self, btn_x, btn_y, text, arrow_start_x, arrow_start_y):
        """Draw arrow pointing to specific coordinates"""
        # Draw arrow line
        self.canvas.create_line(
            arrow_start_x, arrow_start_y, 
            btn_x, btn_y, 
            arrow="last", 
            width=3, 
            fill="#3a7ebf",
            smooth=True
        )
    
        # Draw text background
        text_bg = self.canvas.create_rectangle(
            arrow_start_x + 5, arrow_start_y - 40,
            arrow_start_x + 400, arrow_start_y - 10,
            fill="#2b2b2b",
            outline="#3a7ebf"
        )
    
        # Draw description text
        self.canvas.create_text(
            arrow_start_x + 10, arrow_start_y - 30,
            text=text,
            font=("Segoe UI", 12, "bold"),
            fill="white",
            anchor="w"
        )

    def get_widget_position(self, widget):
        """Get widget position relative to canvas"""
        self.update_idletasks()
    
        # Get widget position in root window
        widget_x = widget.winfo_rootx() + widget.winfo_width() // 2
        widget_y = widget.winfo_rooty() + widget.winfo_height() // 2
    
        # Get canvas position in root window
        canvas_x = self.canvas.winfo_rootx()
        canvas_y = self.canvas.winfo_rooty()
    
        # Calculate position relative to canvas
        x = widget_x - canvas_x
        y = widget_y - canvas_y
    
        return x, y

    def cancel_and_return(self):
        self.back_to_main_callback()
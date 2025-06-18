import time
import threading
import keyboard
import customtkinter
import mouse
from tkinter import font as tkfont

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

class KeyPressApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title(" LOTBS AUTOMATION ")
        self.geometry("720x580")
        self.configure(fg_color="#1a1a1a")
        
        # Custom fonts
        self.title_font = customtkinter.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.header_font = customtkinter.CTkFont(family="Segoe UI", size=16, weight="bold")
        self.body_font = customtkinter.CTkFont(family="Segoe UI", size=13)
        self.small_font = customtkinter.CTkFont(family="Segoe UI", size=10)
        
        # Control variables
        self.is_running_24 = False
        self.is_running_ws = False
        self.is_running_clicker = False
        self.thread_24 = None
        self.thread_ws = None
        self.thread_clicker = None
        
        # Setup UI first
        self.setup_ui()
        
        # Then setup hotkeys
        self.init_hotkeys()
        
        # Handle window closing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Main container with shadow effect
        self.main_frame = customtkinter.CTkFrame(self, fg_color="#1a1a1a", border_width=0, corner_radius=12)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Header section
        self.header_frame = customtkinter.CTkFrame(self.main_frame, fg_color="#2a2a2a", corner_radius=10)
        self.header_frame.pack(fill="x", padx=10, pady=(10, 15))
        
        # Title with icon placeholder
        self.title_label = customtkinter.CTkLabel(
            self.header_frame, 
            text="⚔️ LOTBS AUTOMATION", 
            font=self.title_font,
            text_color="#9b59b6"
        )
        self.title_label.pack(pady=(10, 5))
        
        # Instructions in a rounded frame
        self.instruction_frame = customtkinter.CTkFrame(self.header_frame, fg_color="#252525", corner_radius=8)
        self.instruction_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.instruction_label = customtkinter.CTkLabel(
            self.instruction_frame,
            text="1. Preferred Weapon in second slot\n"
                 "2. Heal in fourth slot\n"
                 "3. Toggle with B (Weapon/Heal) & N (Anti-Kick)\n"
                 "4. Enable autoclicker (M) at 5ms\n"
                 "5. Enjoy your advantage!",
            font=self.body_font,
            text_color="#dddddd",
            justify="left",
            anchor="w"
        )
        self.instruction_label.pack(padx=15, pady=10)
        
        # Feature cards
        self.features_frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
        self.features_frame.pack(fill="x", padx=10, pady=5)
        
        # Weapon & Heal Automation Card
        self.card_24 = customtkinter.CTkFrame(self.features_frame, fg_color="#252525", corner_radius=10)
        self.card_24.pack(fill="x", pady=5, padx=5)
        
        customtkinter.CTkLabel(
            self.card_24, 
            text="⚔️ Weapon & Heal Automation", 
            font=self.header_font,
            text_color="#9b59b6",
            anchor="w"
        ).pack(fill="x", padx=15, pady=(10, 0))
        
        self.status_24 = customtkinter.CTkLabel(
            self.card_24,
            text="❌ Stopped (Press B to activate)",
            font=self.body_font,
            text_color="#ff5555",
            anchor="w"
        )
        self.status_24.pack(fill="x", padx=15, pady=(0, 10))
        
        # Anti Kick Card
        self.card_ws = customtkinter.CTkFrame(self.features_frame, fg_color="#252525", corner_radius=10)
        self.card_ws.pack(fill="x", pady=5, padx=5)
        
        customtkinter.CTkLabel(
            self.card_ws, 
            text="🛡️ Anti-Kick System", 
            font=self.header_font,
            text_color="#9b59b6",
            anchor="w"
        ).pack(fill="x", padx=15, pady=(10, 0))
        
        self.status_ws = customtkinter.CTkLabel(
            self.card_ws,
            text="❌ Stopped (Press N to activate)",
            font=self.body_font,
            text_color="#ff5555",
            anchor="w"
        )
        self.status_ws.pack(fill="x", padx=15, pady=(0, 10))
        
        # Autoclicker Card
        self.card_clicker = customtkinter.CTkFrame(self.features_frame, fg_color="#252525", corner_radius=10)
        self.card_clicker.pack(fill="x", pady=5, padx=5)
        
        customtkinter.CTkLabel(
            self.card_clicker, 
            text="🖱️ Autoclicker (5ms)", 
            font=self.header_font,
            text_color="#9b59b6",
            anchor="w"
        ).pack(fill="x", padx=15, pady=(10, 0))
        
        self.status_clicker = customtkinter.CTkLabel(
            self.card_clicker,
            text="❌ Stopped (Press M to activate)",
            font=self.body_font,
            text_color="#ff5555",
            anchor="w"
        )
        self.status_clicker.pack(fill="x", padx=15, pady=(0, 10))
        
        # Footer
        self.footer_frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
        self.footer_frame.pack(fill="x", pady=(10, 0))
        
        self.credits_label = customtkinter.CTkLabel(
            self.footer_frame,
            text="✨ Crafted by Salcido",
            font=self.small_font,
            text_color="#666666"
        )
        self.credits_label.pack(side="right", padx=10, pady=5)
        
        # Version tag
        self.version_label = customtkinter.CTkLabel(
            self.footer_frame,
            text="v1.0",
            font=self.small_font,
            text_color="#444444"
        )
        self.version_label.pack(side="left", padx=10, pady=5)
    
    # [Rest of your methods remain exactly the same]
    def init_hotkeys(self):
        keyboard.add_hotkey('b', self.toggle_24_sequence)
        keyboard.add_hotkey('n', self.toggle_ws_sequence)
        keyboard.add_hotkey('m', self.toggle_clicker)
    
    def toggle_24_sequence(self):
        if self.is_running_24:
            self.stop_24_sequence()
        else:
            self.start_24_sequence()
    
    def toggle_ws_sequence(self):
        if self.is_running_ws:
            self.stop_ws_sequence()
        else:
            self.start_ws_sequence()
    
    def toggle_clicker(self):
        if self.is_running_clicker:
            self.stop_clicker()
        else:
            self.start_clicker()
    
    def start_24_sequence(self):
        self.is_running_24 = True
        self.status_24.configure(text="✅ Running (B to stop)", text_color="#55ff55")
        self.thread_24 = threading.Thread(target=self.key_24_sequence, daemon=True)
        self.thread_24.start()
    
    def stop_24_sequence(self):
        self.is_running_24 = False
        self.status_24.configure(text="❌ Stopped (B to start)", text_color="#ff5555")
    
    def start_ws_sequence(self):
        self.is_running_ws = True
        self.status_ws.configure(text="✅ Running (N to stop)", text_color="#55ff55")
        self.thread_ws = threading.Thread(target=self.key_ws_sequence, daemon=True)
        self.thread_ws.start()
    
    def stop_ws_sequence(self):
        self.is_running_ws = False
        self.status_ws.configure(text="❌ Stopped (N to start)", text_color="#ff5555")
    
    def start_clicker(self):
        self.is_running_clicker = True
        self.status_clicker.configure(text="✅ Running (M to stop)", text_color="#55ff55")
        self.thread_clicker = threading.Thread(target=self.auto_clicker, daemon=True)
        self.thread_clicker.start()
    
    def stop_clicker(self):
        self.is_running_clicker = False
        self.status_clicker.configure(text="❌ Stopped (M to start)", text_color="#ff5555")
    
    def key_24_sequence(self):
        while self.is_running_24:
            keyboard.press('2')
            keyboard.release('2')
            time.sleep(2)
            keyboard.press('4')
            keyboard.release('4')
            time.sleep(1)
    
    def key_ws_sequence(self):
        while self.is_running_ws:
            keyboard.press('w')
            keyboard.release('w')
            time.sleep(10)
            keyboard.press('s')
            keyboard.release('s')
            time.sleep(10)
    
    def auto_clicker(self):
        while self.is_running_clicker:
            mouse.click()
            time.sleep(0.005)
    
    def on_closing(self):
        self.is_running_24 = False
        self.is_running_ws = False
        self.is_running_clicker = False
        keyboard.unhook_all()
        self.destroy()

if __name__ == "__main__":
    app = KeyPressApp()
    app.mainloop()
import customtkinter as ctk
import re
from typing import Callable, Optional
from ..core.auth import create_user, authenticate_user

print('DEBUG: CustomTkinter version:', ctk.__version__)

class LoginDialog(ctk.CTkToplevel):
    """Login dialog window"""
    
    def __init__(self, parent, on_login_success: Callable):
        super().__init__(parent)
        print("DEBUG: LoginDialog __init__ ejecutado")
        self.on_login_success = on_login_success
        self.result = None
        
        # Window setup
        self.title("Login - Bills Tracker [DEBUG]")
        self.geometry("400x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Cerrar toda la app si se cierra la ventana de login
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Center window
        self.center_window()
        
        # Create widgets
        self.create_widgets()
        
        # Focus on username entry
        try:
            self.username_entry.focus()
        except Exception:
            pass
        
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (300 // 2)
        self.geometry(f"400x300+{x}+{y}")
        try:
            self.focus_force()
        except Exception:
            pass
    
    def create_widgets(self):
        """Create login form widgets"""
        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.configure(bg_color="green")
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="🔐 Login", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 30))
        
        # Username frame
        username_label = ctk.CTkLabel(main_frame, text="Username:")
        username_label.grid(row=1, column=0, sticky="w", padx=10, pady=(10, 5))
        self.username_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Enter your username",
            height=35
        )
        self.username_entry.grid(row=1, column=1, padx=10, pady=(10, 5))
        
        # Password frame
        password_label = ctk.CTkLabel(main_frame, text="Password:")
        password_label.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 5))
        self.password_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Enter your password",
            show="*",
            height=35
        )
        self.password_entry.grid(row=2, column=1, padx=10, pady=(10, 5))
        
        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Login y Create Account en la misma fila, más pequeños
        self.login_button = ctk.CTkButton(
            main_frame,
            text="Login",
            command=self.login,
            width=100,
            height=32,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.login_button.grid(row=3, column=0, sticky="e", padx=(20, 5), pady=(15, 5))

        self.signup_button = ctk.CTkButton(
            main_frame,
            text="Create Account",
            command=self.show_signup,
            width=120,
            height=32
        )
        self.signup_button.grid(row=3, column=1, sticky="w", padx=(5, 20), pady=(15, 5))
        print('DEBUG: Después de crear signup_button')

        # Signup label debajo de los botones
        signup_label = ctk.CTkLabel(
            main_frame,
            text="¿No tienes cuenta?",
            font=ctk.CTkFont(size=12),
            bg_color="orange"
        )
        signup_label.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(5, 15))
        print('DEBUG: Después de crear signup_label')
        
        # Status label
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="red"
        )
        self.status_label.grid(row=6, column=0, columnspan=2, pady=5)
    
    def login(self):
        """Handle login attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        print(f"DEBUG: Intentando login con usuario: {username}")
        
        # Validation
        if not username:
            self.show_error("Please enter a username")
            print("DEBUG: Falta username")
            return
        
        if not password:
            self.show_error("Please enter a password")
            print("DEBUG: Falta password")
            return
        
        # Disable login button
        self.login_button.configure(state="disabled", text="Logging in...")
        self.status_label.configure(text="")
        
        # Attempt authentication
        result = authenticate_user(username, password)
        print(f"DEBUG: Resultado de authenticate_user: {result}")
        
        if result["success"]:
            print("DEBUG: Login exitoso, llamando on_login_success")
            self.result = result
            self.on_login_success(result)
            self.destroy()
        else:
            print(f"DEBUG: Login fallido: {result['error']}")
            self.show_error(result["error"])
            self.login_button.configure(state="normal", text="Login")
    
    def show_error(self, message: str):
        """Show error message"""
        self.status_label.configure(text=message)
        self.status_label.grid(row=7, column=0, columnspan=2, pady=5)

    def show_signup(self):
        """Show signup dialog"""
        self.withdraw()  # Hide login window
        signup_dialog = SignupDialog(self, self.on_signup_complete)
        signup_dialog.wait_window()
        try:
            self.deiconify()  # Show login window again
            self.username_entry.focus()
        except Exception:
            pass

    def on_signup_complete(self, result):
        """Handle signup completion"""
        if result and result.get("success"):
            try:
                self.username_entry.delete(0, "end")
                self.username_entry.insert(0, result["username"])
                self.password_entry.delete(0, "end")
                self.status_label.configure(text="Account created successfully! Please login.", text_color="green")
                self.username_entry.focus()
            except Exception:
                pass

    def _on_close(self):
        import sys
        self.destroy()
        self.update()
        sys.exit(0)

class SignupDialog(ctk.CTkToplevel):
    """Signup dialog window"""
    
    def __init__(self, parent, on_signup_complete: Callable):
        super().__init__(parent)
        
        self.on_signup_complete = on_signup_complete
        self.result = None
        
        # Window setup
        self.title("Create Account - Bills Tracker")
        self.geometry("450x500")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Center window
        self.center_window()
        
        # Create widgets
        self.create_widgets()
        
        # Focus on username entry
        try:
            self.username_entry.focus()
        except Exception:
            pass
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"450x500+{x}+{y}")
        try:
            self.focus_force()
        except Exception:
            pass
    
    def create_widgets(self):
        """Create signup form widgets"""
        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="📝 Create Account", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Username frame
        username_frame = ctk.CTkFrame(main_frame)
        username_frame.pack(fill="x", padx=20, pady=5)
        
        username_label = ctk.CTkLabel(username_frame, text="Username:")
        username_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.username_entry = ctk.CTkEntry(
            username_frame, 
            placeholder_text="Choose a username (3-20 characters)",
            height=35
        )
        self.username_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Email frame
        email_frame = ctk.CTkFrame(main_frame)
        email_frame.pack(fill="x", padx=20, pady=5)
        
        email_label = ctk.CTkLabel(email_frame, text="Email:")
        email_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.email_entry = ctk.CTkEntry(
            email_frame, 
            placeholder_text="Enter your email address",
            height=35
        )
        self.email_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Password frame
        password_frame = ctk.CTkFrame(main_frame)
        password_frame.pack(fill="x", padx=20, pady=5)
        
        password_label = ctk.CTkLabel(password_frame, text="Password:")
        password_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.password_entry = ctk.CTkEntry(
            password_frame, 
            placeholder_text="Choose a password (min 6 characters)",
            show="*",
            height=35
        )
        self.password_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Confirm password frame
        confirm_frame = ctk.CTkFrame(main_frame)
        confirm_frame.pack(fill="x", padx=20, pady=5)
        
        confirm_label = ctk.CTkLabel(confirm_frame, text="Confirm Password:")
        confirm_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.confirm_entry = ctk.CTkEntry(
            confirm_frame, 
            placeholder_text="Confirm your password",
            show="*",
            height=35
        )
        self.confirm_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.email_entry.focus())
        self.email_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.confirm_entry.focus())
        self.confirm_entry.bind("<Return>", lambda e: self.signup())
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Signup button
        self.signup_button = ctk.CTkButton(
            buttons_frame,
            text="Create Account",
            command=self.signup,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.signup_button.pack(fill="x", padx=10, pady=(10, 5))
        
        # Back to login
        back_button = ctk.CTkButton(
            buttons_frame,
            text="Back to Login",
            command=self.destroy,
            height=30,
            fg_color="transparent",
            text_color=("blue", "lightblue"),
            hover_color=("lightblue", "darkblue")
        )
        back_button.pack(pady=(0, 10))
        
        # Status label
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="red"
        )
        self.status_label.pack(pady=5)
    
    def validate_inputs(self) -> tuple[bool, str]:
        """Validate form inputs"""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        
        # Username validation
        if not username:
            return False, "Username is required"
        
        if len(username) < 3 or len(username) > 20:
            return False, "Username must be 3-20 characters long"
        
        if not username.replace("_", "").replace("-", "").isalnum():
            return False, "Username can only contain letters, numbers, underscores, and hyphens"
        
        # Email validation
        if not email:
            return False, "Email is required"
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Please enter a valid email address"
        
        # Password validation
        if not password:
            return False, "Password is required"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        if password != confirm:
            return False, "Passwords do not match"
        
        return True, ""
    
    def signup(self):
        """Handle signup attempt"""
        print("DEBUG: Intentando crear cuenta...")
        # Validate inputs
        is_valid, error_message = self.validate_inputs()
        if not is_valid:
            print(f"DEBUG: Validación fallida: {error_message}")
            self.show_error(error_message)
            return
        
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        # Attempt to create user
        result = create_user(username, email, password)
        print(f"DEBUG: Resultado de create_user: {result}")
        if result["success"]:
            print("DEBUG: Signup exitoso, cerrando dialogo")
            self.result = {"success": True, "username": username}
            self.on_signup_complete(self.result)
            self.destroy()
        else:
            print(f"DEBUG: Signup fallido: {result['error']}")
            self.show_error(result["error"])
    
    def show_error(self, message: str):
        """Show error message"""
        self.status_label.configure(text=message)
        self.status_label.pack(pady=5)

class UserProfileDialog(ctk.CTkToplevel):
    """User profile dialog for changing password and viewing account info"""
    
    def __init__(self, parent, user_info: dict, on_password_change: Callable):
        super().__init__(parent)
        
        self.user_info = user_info
        self.on_password_change = on_password_change
        
        # Window setup
        self.title("User Profile - Bills Tracker")
        self.geometry("400x450")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Center window
        self.center_window()
        
        # Create widgets
        self.create_widgets()
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (450 // 2)
        self.geometry(f"400x450+{x}+{y}")
    
    def create_widgets(self):
        """Create profile widgets"""
        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="👤 User Profile", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # User info frame
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_label = ctk.CTkLabel(
            info_frame, 
            text="Account Information", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_label.pack(pady=(15, 10))
        
        # Username
        username_text = f"Username: {self.user_info['username']}"
        username_label = ctk.CTkLabel(info_frame, text=username_text)
        username_label.pack(pady=2)
        
        # Email
        email_text = f"Email: {self.user_info['email']}"
        email_label = ctk.CTkLabel(info_frame, text=email_text)
        email_label.pack(pady=2)
        
        # Role
        role_text = f"Role: {'Administrator' if self.user_info['is_admin'] else 'User'}"
        role_label = ctk.CTkLabel(info_frame, text=role_text)
        role_label.pack(pady=2)
        
        # Created date
        if 'created_at' in self.user_info:
            created_text = f"Created: {self.user_info['created_at']}"
            created_label = ctk.CTkLabel(info_frame, text=created_text)
            created_label.pack(pady=2)
        
        # Last login
        if 'last_login' in self.user_info and self.user_info['last_login']:
            login_text = f"Last Login: {self.user_info['last_login']}"
            login_label = ctk.CTkLabel(info_frame, text=login_text)
            login_label.pack(pady=2)
        
        info_frame.pack(pady=(0, 20))
        
        # Change password frame
        password_frame = ctk.CTkFrame(main_frame)
        password_frame.pack(fill="x", padx=20, pady=10)
        
        password_title = ctk.CTkLabel(
            password_frame, 
            text="Change Password", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        password_title.pack(pady=(15, 10))
        
        # Current password
        current_label = ctk.CTkLabel(password_frame, text="Current Password:")
        current_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.current_password = ctk.CTkEntry(
            password_frame, 
            placeholder_text="Enter current password",
            show="*",
            height=35
        )
        self.current_password.pack(fill="x", padx=10, pady=(0, 10))
        
        # New password
        new_label = ctk.CTkLabel(password_frame, text="New Password:")
        new_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.new_password = ctk.CTkEntry(
            password_frame, 
            placeholder_text="Enter new password (min 6 characters)",
            show="*",
            height=35
        )
        self.new_password.pack(fill="x", padx=10, pady=(0, 10))
        
        # Confirm new password
        confirm_label = ctk.CTkLabel(password_frame, text="Confirm New Password:")
        confirm_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.confirm_password = ctk.CTkEntry(
            password_frame, 
            placeholder_text="Confirm new password",
            show="*",
            height=35
        )
        self.confirm_password.pack(fill="x", padx=10, pady=(0, 10))
        
        # Change password button
        self.change_button = ctk.CTkButton(
            password_frame,
            text="Change Password",
            command=self.change_password,
            height=35
        )
        self.change_button.pack(fill="x", padx=10, pady=(0, 15))
        
        # Status label
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=5)
    
    def change_password(self):
        """Handle password change"""
        current = self.current_password.get()
        new = self.new_password.get()
        confirm = self.confirm_password.get()
        
        # Validation
        if not current:
            self.show_message("Please enter your current password", "red")
            return
        
        if not new:
            self.show_message("Please enter a new password", "red")
            return
        
        if len(new) < 6:
            self.show_message("New password must be at least 6 characters long", "red")
            return
        
        if new != confirm:
            self.show_message("New passwords do not match", "red")
            return
        
        # Call the password change function
        result = self.on_password_change(current, new)
        
        if result["success"]:
            self.show_message("Password changed successfully!", "green")
            # Clear fields
            self.current_password.delete(0, "end")
            self.new_password.delete(0, "end")
            self.confirm_password.delete(0, "end")
        else:
            self.show_message(result["error"], "red")
    
    def show_message(self, message: str, color: str = "red"):
        """Show status message"""
        self.status_label.configure(text=message, text_color=color)
        self.status_label.pack(pady=5) 
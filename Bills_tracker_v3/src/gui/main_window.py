import customtkinter as ctk

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bills Tracker Desktop")
        self.geometry("900x600")
        self._setup_ui()

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_rowconfigure(3, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="Bills Tracker", font=("Arial", 20, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.bills_button = ctk.CTkButton(self.sidebar, text="Bills")
        self.bills_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.categories_button = ctk.CTkButton(self.sidebar, text="Categories")
        self.categories_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.settings_button = ctk.CTkButton(self.sidebar, text="Settings")
        self.settings_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Main content area
        self.content = ctk.CTkFrame(self, corner_radius=10)
        self.content.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.content_label = ctk.CTkLabel(self.content, text="Main Content Area", font=("Arial", 18))
        self.content_label.grid(row=0, column=0, padx=20, pady=20)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop() 
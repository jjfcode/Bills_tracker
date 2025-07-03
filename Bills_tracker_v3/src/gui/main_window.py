import customtkinter as ctk
from tkinter import ttk

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

        self.bills_button = ctk.CTkButton(self.sidebar, text="Bills", command=self.show_bills_view)
        self.bills_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.categories_button = ctk.CTkButton(self.sidebar, text="Categories", command=self.show_categories_view)
        self.categories_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.settings_button = ctk.CTkButton(self.sidebar, text="Settings", command=self.show_settings_view)
        self.settings_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Main content area
        self.content = ctk.CTkFrame(self, corner_radius=10)
        self.content.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        # Initialize views
        self.bills_table_frame = None
        self.categories_frame = None
        self.settings_frame = None
        self.show_bills_view()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_bills_view(self):
        self.clear_content()
        self.bills_table_frame = ctk.CTkFrame(self.content)
        self.bills_table_frame.grid(row=0, column=0, sticky="nswe")
        self.bills_table_frame.grid_rowconfigure(0, weight=1)
        self.bills_table_frame.grid_columnconfigure(0, weight=1)

        columns = ("Name", "Due Date", "Amount", "Category", "Status")
        self.bills_table = ttk.Treeview(self.bills_table_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.bills_table.heading(col, text=col)
            self.bills_table.column(col, width=120, anchor="center")

        sample_bills = [
            ("Electricity", "2025-07-10", "$50.00", "Utilities", "Pending"),
            ("Internet", "2025-07-12", "$40.00", "Utilities", "Paid"),
            ("Netflix", "2025-07-15", "$15.99", "Subscriptions", "Pending"),
            ("Water", "2025-07-20", "$30.00", "Utilities", "Pending"),
            ("Car Loan", "2025-07-25", "$250.00", "Loans", "Paid"),
        ]
        for bill in sample_bills:
            self.bills_table.insert("", "end", values=bill)

        scrollbar = ttk.Scrollbar(self.bills_table_frame, orient="vertical", command=self.bills_table.yview)
        self.bills_table.configure(yscrollcommand=scrollbar.set)
        self.bills_table.grid(row=0, column=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def show_categories_view(self):
        self.clear_content()
        self.categories_frame = ctk.CTkFrame(self.content)
        self.categories_frame.grid(row=0, column=0, sticky="nswe")
        label = ctk.CTkLabel(self.categories_frame, text="Categories View (Coming Soon)", font=("Arial", 18))
        label.pack(padx=40, pady=40)

    def show_settings_view(self):
        self.clear_content()
        self.settings_frame = ctk.CTkFrame(self.content)
        self.settings_frame.grid(row=0, column=0, sticky="nswe")
        label = ctk.CTkLabel(self.settings_frame, text="Settings View (Coming Soon)", font=("Arial", 18))
        label.pack(padx=40, pady=40)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop() 
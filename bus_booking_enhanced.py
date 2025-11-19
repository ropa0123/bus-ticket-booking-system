import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import uuid
import datetime
import json
import os
from typing import Dict, List, Optional
import hashlib

# Admin credentials (in production, use proper authentication)
ADMIN_CREDENTIALS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "manager": hashlib.sha256("manager123".encode()).hexdigest()
}

DATA_FILE = "bookings_data.json"
CONFIG_FILE = "system_config.json"

class DataManager:
    """Manages persistent storage of bookings and configuration"""
    
    @staticmethod
    def load_bookings() -> Dict:
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    @staticmethod
    def save_bookings(bookings: Dict):
        with open(DATA_FILE, 'w') as f:
            json.dump(bookings, f, indent=2)
    
    @staticmethod
    def load_config() -> Dict:
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except:
                return DataManager.get_default_config()
        return DataManager.get_default_config()
    
    @staticmethod
    def save_config(config: Dict):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    
    @staticmethod
    def get_default_config() -> Dict:
        return {
            "bus_routes": {
                "Bulawayo to Gweru": 5, "Gweru to Bulawayo": 5,
                "Bulawayo to Kwekwe": 7, "Kwekwe to Bulawayo": 7,
                "Bulawayo to Kadoma": 8, "Kadoma to Bulawayo": 8,
                "Bulawayo to Chegutu": 10, "Chegutu to Bulawayo": 10,
                "Bulawayo to Norton": 13, "Norton to Bulawayo": 13,
                "Bulawayo to Harare": 15, "Harare to Bulawayo": 15,
                "Gweru to Kwekwe": 3, "Kwekwe to Gweru": 3,
                "Gweru to Kadoma": 4, "Kadoma to Gweru": 4,
                "Gweru to Chegutu": 5, "Chegutu to Gweru": 5,
                "Gweru to Norton": 6, "Norton to Gweru": 6,
                "Gweru to Harare": 7, "Harare to Gweru": 7,
                "Kwekwe to Kadoma": 2, "Kadoma to Kwekwe": 2,
                "Kwekwe to Chegutu": 6, "Chegutu to Kwekwe": 6,
                "Kwekwe to Norton": 9, "Norton to Kwekwe": 9,
                "Kwekwe to Harare": 10, "Harare to Kwekwe": 10,
                "Kadoma to Chegutu": 4, "Chegutu to Kadoma": 4,
                "Kadoma to Norton": 5, "Norton to Kadoma": 5,
                "Kadoma to Harare": 6, "Harare to Kadoma": 6,
                "Chegutu to Norton": 1, "Norton to Chegutu": 1,
                "Chegutu to Harare": 3, "Harare to Chegutu": 3,
                "Norton to Harare": 2, "Harare to Norton": 2,
            },
            "bus_schedules": {
                "Bulawayo to Gweru": "08:00 AM", "Gweru to Bulawayo": "02:00 PM",
                "Gweru to Kwekwe": "09:00 AM", "Kwekwe to Gweru": "03:00 PM",
                "Bulawayo to Kwekwe": "09:00 AM", "Kwekwe to Bulawayo": "03:30 PM",
                "Kwekwe to Kadoma": "10:00 AM", "Kadoma to Kwekwe": "04:00 PM",
                "Bulawayo to Kadoma": "10:00 AM", "Kadoma to Bulawayo": "04:30 PM",
                "Kadoma to Chegutu": "10:30 AM", "Chegutu to Kadoma": "04:45 PM",
                "Bulawayo to Chegutu": "11:00 AM", "Chegutu to Bulawayo": "05:00 PM",
                "Bulawayo to Harare": "12:00 PM", "Harare to Bulawayo": "06:00 PM",
                "Gweru to Kadoma": "09:30 AM", "Kadoma to Gweru": "02:30 PM",
                "Gweru to Chegutu": "10:15 AM", "Chegutu to Gweru": "03:15 PM",
                "Gweru to Norton": "11:00 AM", "Norton to Gweru": "04:00 PM",
                "Gweru to Harare": "11:30 AM", "Harare to Gweru": "05:00 PM",
                "Kwekwe to Chegutu": "10:45 AM", "Chegutu to Kwekwe": "04:15 PM",
                "Kwekwe to Norton": "11:30 AM", "Norton to Kwekwe": "05:15 PM",
                "Kwekwe to Harare": "12:15 PM", "Harare to Kwekwe": "06:15 PM",
                "Kadoma to Norton": "11:00 AM", "Norton to Kadoma": "05:00 PM",
                "Kadoma to Harare": "11:30 AM", "Harare to Kadoma": "05:30 PM",
                "Chegutu to Norton": "11:45 AM", "Norton to Chegutu": "05:45 PM",
                "Chegutu to Harare": "12:15 PM", "Harare to Chegutu": "06:15 PM",
                "Norton to Harare": "12:30 PM", "Harare to Norton": "06:30 PM",
            },
            "bus_stops": {
                "Bulawayo": "City Hall, Renkini Bus Terminus, and National Railways of Zimbabwe Station.",
                "Gweru": "Main Street, City Centre, and Railway Station.",
                "Kwekwe": "City Centre, Kwekwe Mall, and Railway Station.",
                "Kadoma": "City Centre, Kadoma Mall, and Railway Station.",
                "Chegutu": "City Centre, Chegutu Mall, and Railway Station.",
                "Norton": "Main Street, Town Centre, and near the Post Office.",
                "Harare": "City Centre, Avondale, and Mbare Musika Bus Terminus."
            },
            "total_seats": 50,
            "company_name": "Chikukwa Bus Services",
            "contact_phone": "+263777189947",
            "contact_email": "support@chikukwabus.com"
        }

class BusBookingSystem:
    def __init__(self, master):
        self.master = master
        master.title("Chikukwa Bus Booking System - Enhanced")
        master.geometry("1200x800")
        master.resizable(True, True)
        
        self.is_admin = False
        self.admin_username = None
        
        self.bookings = DataManager.load_bookings()
        self.config = DataManager.load_config()
        
        self.setup_styles()
        self.create_main_interface()
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.COLOR_PRIMARY = "#2c3e50"
        self.COLOR_ACCENT = "#3498db"
        self.COLOR_LIGHT_BG = "#ecf0f1"
        self.COLOR_MEDIUM_BG = "#e0f2f7"
        self.COLOR_TEXT_LIGHT = "white"
        self.COLOR_TEXT_DARK = "#34495e"
        self.COLOR_SUCCESS = "#28a745"
        self.COLOR_ERROR = "#dc3545"
        self.COLOR_WARNING = "#ffc107"
        self.COLOR_ADMIN = "#9b59b6"
        
        self.style.configure('TFrame', background=self.COLOR_MEDIUM_BG)
        self.style.configure('TLabel', background=self.COLOR_MEDIUM_BG, 
                           foreground=self.COLOR_TEXT_DARK, font=('Segoe UI', 11))
        self.style.configure('Header.TLabel', background=self.COLOR_MEDIUM_BG, 
                           foreground=self.COLOR_ACCENT, font=('Segoe UI', 24, 'bold'))
        self.style.configure('SubHeader.TLabel', foreground=self.COLOR_PRIMARY, 
                           font=('Segoe UI', 16, 'bold'))
        self.style.configure('Admin.TLabel', foreground=self.COLOR_ADMIN, 
                           font=('Segoe UI', 12, 'bold'))
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), 
                           background=self.COLOR_ACCENT, foreground=self.COLOR_TEXT_LIGHT)
        self.style.configure('Admin.TButton', background=self.COLOR_ADMIN)
        self.style.configure('Success.TButton', background=self.COLOR_SUCCESS)
        self.style.configure('Danger.TButton', background=self.COLOR_ERROR)
        
    def create_main_interface(self):
        self.main_frame = ttk.Frame(self.master, padding="20")
        self.main_frame.pack(fill='both', expand=True)
        
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="🚌 Chikukwa Bus Booking System 🇿🇼",
                 style='Header.TLabel').pack(side='left')
        
        self.admin_status_label = ttk.Label(header_frame, text="", style='Admin.TLabel')
        self.admin_status_label.pack(side='right', padx=10)
        
        self.update_admin_status()
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        self.create_customer_tab()
        self.create_admin_tab()
        
    def update_admin_status(self):
        if self.is_admin:
            self.admin_status_label.config(text=f"👤 Admin: {self.admin_username}")
        else:
            self.admin_status_label.config(text="")
    
    def create_customer_tab(self):
        customer_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(customer_frame, text="🎫 Customer Services")
        
        button_frame = ttk.Frame(customer_frame)
        button_frame.pack(pady=20)
        
        buttons = [
            ("Book Ticket", self.show_book_ticket),
            ("View My Ticket", self.show_view_ticket),
            ("Cancel Ticket", self.show_cancel_ticket),
            ("Modify Booking", self.show_modify_booking),
            ("Check Route & Fare", self.show_route_fare),
            ("View Schedule", self.show_schedule),
            ("Bus Stops", self.show_bus_stops),
        ]
        
        for i, (text, cmd) in enumerate(buttons):
            ttk.Button(button_frame, text=text, command=cmd, width=18).grid(
                row=i//4, column=i%4, padx=5, pady=5)
        
        self.customer_content = ttk.Frame(customer_frame, padding="20", 
                                         relief='groove', borderwidth=2)
        self.customer_content.pack(fill='both', expand=True, pady=20)
        
        self.show_welcome_customer()
    
    def create_admin_tab(self):
        admin_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(admin_frame, text="🔐 Admin Panel")
        
        self.admin_content_frame = ttk.Frame(admin_frame)
        self.admin_content_frame.pack(fill='both', expand=True)
        
        self.show_admin_login()
    
    def show_admin_login(self):
        self.clear_frame(self.admin_content_frame)
        
        if self.is_admin:
            self.show_admin_dashboard()
            return
        
        login_frame = ttk.Frame(self.admin_content_frame, padding="50")
        login_frame.pack(expand=True)
        
        ttk.Label(login_frame, text="🔐 Admin Login", 
                 style='SubHeader.TLabel').grid(row=0, column=0, columnspan=2, pady=30)
        
        ttk.Label(login_frame, text="Username:").grid(row=1, column=0, sticky='e', padx=10, pady=10)
        username_entry = ttk.Entry(login_frame, width=30)
        username_entry.grid(row=1, column=1, pady=10)
        
        ttk.Label(login_frame, text="Password:").grid(row=2, column=0, sticky='e', padx=10, pady=10)
        password_entry = ttk.Entry(login_frame, width=30, show="*")
        password_entry.grid(row=2, column=1, pady=10)
        
        def attempt_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if username in ADMIN_CREDENTIALS:
                if ADMIN_CREDENTIALS[username] == hashlib.sha256(password.encode()).hexdigest():
                    self.is_admin = True
                    self.admin_username = username
                    self.update_admin_status()
                    messagebox.showinfo("Success", f"Welcome, {username}!")
                    self.show_admin_dashboard()
                    return
            
            messagebox.showerror("Login Failed", "Invalid credentials")
            password_entry.delete(0, 'end')
        
        ttk.Button(login_frame, text="Login", command=attempt_login, 
                  style='Admin.TButton', width=15).grid(row=3, column=0, columnspan=2, pady=30)
        
        info_label = ttk.Label(login_frame, 
                              text="Default credentials:\nUsername: admin | Password: admin123\nUsername: manager | Password: manager123",
                              font=('Segoe UI', 9), foreground='gray')
        info_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        password_entry.bind('<Return>', lambda e: attempt_login())
    
    def show_admin_dashboard(self):
        self.clear_frame(self.admin_content_frame)
        
        header_frame = ttk.Frame(self.admin_content_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="📊 Admin Dashboard", 
                 style='SubHeader.TLabel').pack(side='left')
        
        ttk.Button(header_frame, text="Logout", command=self.admin_logout,
                  style='Danger.TButton').pack(side='right')
        
        stats_frame = ttk.LabelFrame(self.admin_content_frame, text="Statistics", padding="15")
        stats_frame.pack(fill='x', pady=10)
        
        total_bookings = len(self.bookings)
        confirmed = sum(1 for b in self.bookings.values() if b.get('status') == 'confirmed')
        cancelled = sum(1 for b in self.bookings.values() if b.get('status') == 'cancelled')
        total_revenue = sum(b.get('fare', 0) for b in self.bookings.values() 
                          if b.get('status') == 'confirmed')
        
        stats = [
            (f"Total Bookings: {total_bookings}", 0),
            (f"Confirmed: {confirmed}", 1),
            (f"Cancelled: {cancelled}", 2),
            (f"Revenue: ${total_revenue}", 3)
        ]
        
        for text, col in stats:
            ttk.Label(stats_frame, text=text, font=('Segoe UI', 12, 'bold')).grid(
                row=0, column=col, padx=20, pady=10)
        
        button_frame = ttk.Frame(self.admin_content_frame)
        button_frame.pack(fill='x', pady=10)
        
        admin_buttons = [
            ("View All Bookings", self.admin_view_bookings),
            ("Search Bookings", self.admin_search_bookings),
            ("Manage Routes", self.admin_manage_routes),
            ("Generate Report", self.admin_generate_report),
        ]
        
        for i, (text, cmd) in enumerate(admin_buttons):
            ttk.Button(button_frame, text=text, command=cmd, 
                      style='Admin.TButton', width=20).grid(row=0, column=i, padx=5)
        
        self.admin_work_area = ttk.Frame(self.admin_content_frame, padding="10")
        self.admin_work_area.pack(fill='both', expand=True)
        
        self.admin_view_bookings()
    
    def admin_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.is_admin = False
            self.admin_username = None
            self.update_admin_status()
            self.show_admin_login()
    
    def admin_view_bookings(self):
        self.clear_frame(self.admin_work_area)
        
        ttk.Label(self.admin_work_area, text="All Bookings", 
                 font=('Segoe UI', 14, 'bold')).pack(pady=10)
        
        if not self.bookings:
            ttk.Label(self.admin_work_area, text="No bookings found.", 
                     font=('Segoe UI', 12)).pack(pady=50)
            return
        
        tree_frame = ttk.Frame(self.admin_work_area)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ("ID", "Name", "Route", "Date", "Time", "Seat", "Fare", "Status", "Phone")
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(tree, c, False))
            tree.column(col, width=100)
        
        for ticket_id, booking in self.bookings.items():
            tree.insert("", "end", values=(
                booking.get('ticket_id', ticket_id),
                booking.get('name', 'N/A'),
                f"{booking.get('departure', '')} → {booking.get('destination', '')}",
                booking.get('date', 'N/A'),
                booking.get('time', 'N/A'),
                booking.get('seat', 'N/A'),
                f"${booking.get('fare', 0)}",
                booking.get('status', 'confirmed'),
                booking.get('phone', 'N/A')
            ))
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)
        
        button_frame = ttk.Frame(self.admin_work_area)
        button_frame.pack(fill='x', pady=10)
        
        def admin_cancel_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Selection Required", "Please select a booking")
                return
            
            item = tree.item(selected[0])
            ticket_id = item['values'][0]
            
            if messagebox.askyesno("Confirm", f"Cancel booking {ticket_id}?"):
                if ticket_id in self.bookings:
                    self.bookings[ticket_id]['status'] = 'cancelled'
                    DataManager.save_bookings(self.bookings)
                    messagebox.showinfo("Success", "Booking cancelled")
                    self.admin_view_bookings()
        
        def view_details():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Selection Required", "Please select a booking")
                return
            
            item = tree.item(selected[0])
            ticket_id = item['values'][0]
            
            if ticket_id in self.bookings:
                booking = self.bookings[ticket_id]
                details = "\n".join([f"{k.title()}: {v}" for k, v in booking.items()])
                messagebox.showinfo(f"Booking Details - {ticket_id}", details)
        
        ttk.Button(button_frame, text="View Details", command=view_details).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel Booking", command=admin_cancel_selected,
                  style='Danger.TButton').pack(side='left', padx=5)
    
    def admin_search_bookings(self):
        self.clear_frame(self.admin_work_area)
        
        ttk.Label(self.admin_work_area, text="Search Bookings", 
                 font=('Segoe UI', 14, 'bold')).pack(pady=10)
        
        search_frame = ttk.Frame(self.admin_work_area, padding="15")
        search_frame.pack(fill='x')
        
        ttk.Label(search_frame, text="Search by:").grid(row=0, column=0, padx=5)
        
        search_type = ttk.Combobox(search_frame, 
                                   values=["Ticket ID", "Name", "Phone", "Route", "Date"],
                                   state="readonly", width=15)
        search_type.set("Ticket ID")
        search_type.grid(row=0, column=1, padx=5)
        
        search_entry = ttk.Entry(search_frame, width=30)
        search_entry.grid(row=0, column=2, padx=5)
        
        results_frame = ttk.Frame(self.admin_work_area)
        results_frame.pack(fill='both', expand=True, pady=20)
        
        def perform_search():
            self.clear_frame(results_frame)
            
            search_term = search_entry.get().strip().upper()
            if not search_term:
                messagebox.showwarning("Input Required", "Enter search term")
                return
            
            search_field = search_type.get().lower().replace(" ", "_")
            if search_field == "ticket_id":
                search_field = "ticket_id"
            
            results = []
            for ticket_id, booking in self.bookings.items():
                if search_field == "route":
                    route = f"{booking.get('departure', '')} to {booking.get('destination', '')}"
                    if search_term in route.upper():
                        results.append((ticket_id, booking))
                elif search_term in str(booking.get(search_field, '')).upper():
                    results.append((ticket_id, booking))
            
            if not results:
                ttk.Label(results_frame, text="No results found", 
                         font=('Segoe UI', 12)).pack(pady=30)
                return
            
            ttk.Label(results_frame, text=f"Found {len(results)} result(s)", 
                     font=('Segoe UI', 12, 'bold')).pack(pady=10)
            
            for ticket_id, booking in results:
                result_card = ttk.LabelFrame(results_frame, text=f"Ticket: {ticket_id}", 
                                            padding="10")
                result_card.pack(fill='x', pady=5)
                
                info_text = f"Name: {booking.get('name')} | Phone: {booking.get('phone', 'N/A')}\n"
                info_text += f"Route: {booking.get('departure')} → {booking.get('destination')}\n"
                info_text += f"Date: {booking.get('date')} | Time: {booking.get('time')} | Seat: {booking.get('seat')}\n"
                info_text += f"Fare: ${booking.get('fare')} | Status: {booking.get('status', 'confirmed')}"
                
                ttk.Label(result_card, text=info_text).pack()
        
        ttk.Button(search_frame, text="Search", command=perform_search).grid(row=0, column=3, padx=5)
    
    def admin_manage_routes(self):
        self.clear_frame(self.admin_work_area)
        
        ttk.Label(self.admin_work_area, text="Manage Routes & Pricing", 
                 font=('Segoe UI', 14, 'bold')).pack(pady=10)
        
        tree_frame = ttk.Frame(self.admin_work_area)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ("Route", "Fare", "Schedule")
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        tree.heading("Route", text="Route")
        tree.heading("Fare", text="Fare ($)")
        tree.heading("Schedule", text="Departure Time")
        
        tree.column("Route", width=250)
        tree.column("Fare", width=100)
        tree.column("Schedule", width=150)
        
        for route, fare in self.config['bus_routes'].items():
            schedule = self.config['bus_schedules'].get(route, 'N/A')
            tree.insert("", "end", values=(route, f"${fare}", schedule))
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)
        
        button_frame = ttk.Frame(self.admin_work_area)
        button_frame.pack(fill='x', pady=10)
        
        def edit_fare():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Selection Required", "Select a route")
                return
            
            item = tree.item(selected[0])
            route = item['values'][0]
            current_fare = item['values'][1].replace('$', '')
            
            new_fare = simpledialog.askfloat("Edit Fare", 
                                            f"Enter new fare for {route}:",
                                            initialvalue=current_fare)
            if new_fare is not None:
                self.config['bus_routes'][route] = new_fare
                DataManager.save_config(self.config)
                messagebox.showinfo("Success", "Fare updated")
                self.admin_manage_routes()
        
        ttk.Button(button_frame, text="Edit Fare", command=edit_fare).pack(side='left', padx=5)
    
    def admin_generate_report(self):
        self.clear_frame(self.admin_work_area)
        
        ttk.Label(self.admin_work_area, text="Generate Reports", 
                 font=('Segoe UI', 14, 'bold')).pack(pady=10)
        
        report_frame = ttk.LabelFrame(self.admin_work_area, text="Booking Summary", padding="20")
        report_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        total_bookings = len(self.bookings)
        confirmed = sum(1 for b in self.bookings.values() if b.get('status') == 'confirmed')
        cancelled = sum(1 for b in self.bookings.values() if b.get('status') == 'cancelled')
        pending = total_bookings - confirmed - cancelled
        
        total_revenue = sum(b.get('fare', 0) for b in self.bookings.values() 
                          if b.get('status') == 'confirmed')
        
        route_stats = {}
        for booking in self.bookings.values():
            if booking.get('status') == 'confirmed':
                route = f"{booking.get('departure')} to {booking.get('destination')}"
                route_stats[route] = route_stats.get(route, 0) + 1
        
        report_text = f"""
╔══════════════════════════════════════╗
║       BOOKING STATISTICS REPORT       ║
╚══════════════════════════════════════╝

Total Bookings: {total_bookings}
├─ Confirmed: {confirmed}
├─ Cancelled: {cancelled}
└─ Pending: {pending}

Financial Summary:
├─ Total Revenue: ${total_revenue:.2f}
└─ Average per Booking: ${total_revenue/confirmed if confirmed > 0 else 0:.2f}

Top Routes:
"""
        
        top_routes = sorted(route_stats.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (route, count) in enumerate(top_routes, 1):
            report_text += f"  {i}. {route}: {count} bookings\n"
        
        report_text += f"\nReport Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        text_widget = tk.Text(report_frame, wrap='word', font=('Courier New', 10), 
                            height=20, width=60)
        text_widget.pack(fill='both', expand=True)
        text_widget.insert('1.0', report_text)
        text_widget.config(state='disabled')
        
        def export_report():
            filename = f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(report_text)
            messagebox.showinfo("Success", f"Report exported to {filename}")
        
        ttk.Button(report_frame, text="Export Report", command=export_report).pack(pady=10)
    
    def sort_treeview(self, tree, col, reverse):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=reverse)
        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)
        tree.heading(col, command=lambda: self.sort_treeview(tree, col, not reverse))
    
    def show_welcome_customer(self):
        self.clear_frame(self.customer_content)
        welcome_text = f"""
        Welcome to {self.config['company_name']}!
        
        Your trusted partner for comfortable and safe travel across Zimbabwe.
        
        📞 Contact: {self.config['contact_phone']}
        📧 Email: {self.config['contact_email']}
        
        Please select an option above to get started.
        """
        ttk.Label(self.customer_content, text=welcome_text, 
                 font=('Segoe UI', 13), justify='center').pack(expand=True)
    
    def show_book_ticket(self):
        self.clear_frame(self.customer_content)
        
        canvas = tk.Canvas(self.customer_content, bg=self.COLOR_MEDIUM_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.customer_content, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        ttk.Label(scrollable_frame, text="Book Your Ticket", 
                 style='SubHeader.TLabel').grid(row=0, column=0, columnspan=2, pady=15)
        
        fields = [
            ("Full Name:", "name"),
            ("Age:", "age"),
            ("Phone Number:", "phone"),
            ("Email (optional):", "email"),
            ("Departure:", "departure"),
            ("Destination:", "destination"),
            ("Date (YYYY-MM-DD):", "date"),
            ("Time (HH:MM AM/PM):", "time"),
            ("Seat Number:", "seat"),
        ]
        
        self.book_entries = {}
        
        all_cities = sorted(set([r.split(' to ')[0] for r in self.config['bus_routes'].keys()] +
                               [r.split(' to ')[1] for r in self.config['bus_routes'].keys()]))
        
        for i, (label, key) in enumerate(fields):
            ttk.Label(scrollable_frame, text=label).grid(row=i+1, column=0, 
                                                              sticky='e', padx=10, pady=8)
            
            if key in ["departure", "destination"]:
                entry = ttk.Combobox(scrollable_frame, values=all_cities, 
                                    state="readonly", width=28)
                entry.bind('<<ComboboxSelected>>', lambda e: self.update_fare_preview())
            elif key == "age":
                entry = ttk.Combobox(scrollable_frame, 
                                    values=[str(i) for i in range(1, 101)], 
                                    state="readonly", width=28)
            elif key == "seat":
                entry = ttk.Combobox(scrollable_frame, 
                                    values=[str(i) for i in range(1, self.config['total_seats']+1)], 
                                    state="readonly", width=28)
            else:
                entry = ttk.Entry(scrollable_frame, width=30)
            
            entry.grid(row=i+1, column=1, sticky='w', padx=10, pady=8)
            self.book_entries[key] = entry
        
        self.fare_label = ttk.Label(scrollable_frame, text="Fare: $0", 
                                   font=('Segoe UI', 13, 'bold'), 
                                   foreground=self.COLOR_SUCCESS)
        self.fare_label.grid(row=len(fields)+1, column=0, columnspan=2, pady=15)
        
        ttk.Button(scrollable_frame, text="Confirm Booking", 
                  command=self.process_booking, 
                  style='Success.TButton', width=20).grid(row=len(fields)+2, column=0, 
                                                         columnspan=2, pady=20)
        
        scrollable_frame.grid_columnconfigure(1, weight=1)
    
    def update_fare_preview(self):
        departure = self.book_entries['departure'].get()
        destination = self.book_entries['destination'].get()
        
        if departure and destination:
            route = f"{departure} to {destination}"
            fare = self.config['bus_routes'].get(route, 0)
            self.fare_label.config(text=f"Fare: ${fare}")
    
    def process_booking(self):
        data = {key: entry.get().strip() for key, entry in self.book_entries.items()}
        
        if not all([data['name'], data['age'], data['phone'], data['departure'], 
                   data['destination'], data['date'], data['time'], data['seat']]):
            messagebox.showwarning("Missing Information", "Please fill all required fields")
            return
        
        try:
            age = int(data['age'])
            if age < 1 or age > 120:
                raise ValueError
        except:
            messagebox.showerror("Invalid Age", "Please enter a valid age")
            return
        
        try:
            travel_date = datetime.datetime.strptime(data['date'], "%Y-%m-%d").date()
            if travel_date < datetime.date.today():
                messagebox.showerror("Invalid Date", "Please enter a future date")
                return
        except:
            messagebox.showerror("Invalid Date", "Use format YYYY-MM-DD")
            return
        
        try:
            travel_time = datetime.datetime.strptime(data['time'], "%I:%M %p").time()
        except:
            try:
                travel_time = datetime.datetime.strptime(data['time'], "%H:%M").time()
            except:
                messagebox.showerror("Invalid Time", "Use format HH:MM AM/PM or HH:MM")
                return
        
        travel_datetime = datetime.datetime.combine(travel_date, travel_time)
        if travel_datetime <= datetime.datetime.now():
            messagebox.showerror("Invalid Time", "Please enter a future date/time")
            return
        
        try:
            seat = int(data['seat'])
            if seat < 1 or seat > self.config['total_seats']:
                raise ValueError
        except:
            messagebox.showerror("Invalid Seat", f"Choose seat 1-{self.config['total_seats']}")
            return
        
        for booking in self.bookings.values():
            if (booking['departure'] == data['departure'] and 
                booking['destination'] == data['destination'] and
                booking['date'] == data['date'] and
                booking['time'] == data['time'] and
                booking['seat'] == seat and
                booking.get('status') != 'cancelled'):
                messagebox.showerror("Seat Taken", "This seat is already booked for this journey")
                return
        
        route = f"{data['departure']} to {data['destination']}"
        if route not in self.config['bus_routes']:
            messagebox.showerror("Invalid Route", "No direct route available")
            return
        
        fare = self.config['bus_routes'][route]
        ticket_id = str(uuid.uuid4())[:8].upper()
        
        booking_data = {
            'ticket_id': ticket_id,
            'name': data['name'],
            'age': int(data['age']),
            'phone': data['phone'],
            'email': data['email'],
            'departure': data['departure'],
            'destination': data['destination'],
            'date': data['date'],
            'time': data['time'],
            'seat': seat,
            'fare': fare,
            'status': 'confirmed',
            'booked_at': datetime.datetime.now().isoformat(),
        }
        
        self.bookings[ticket_id] = booking_data
        DataManager.save_bookings(self.bookings)
        
        receipt = f"""
╔══════════════════════════════════════╗
║         BOOKING CONFIRMATION          ║
╚══════════════════════════════════════╝

Ticket ID: {ticket_id}
Name: {data['name']}
Age: {data['age']}
Phone: {data['phone']}

Journey Details:
From: {data['departure']}
To: {data['destination']}
Date: {data['date']}
Time: {data['time']}
Seat: {seat}

Fare: ${fare}
Status: CONFIRMED

Thank you for choosing {self.config['company_name']}!
Please arrive 15 minutes before departure.
        """
        
        messagebox.showinfo("Booking Successful", receipt)
        self.show_welcome_customer()
    
    def show_view_ticket(self):
        self.clear_frame(self.customer_content)
        
        ttk.Label(self.customer_content, text="View My Ticket", 
                 style='SubHeader.TLabel').pack(pady=20)
        
        ttk.Label(self.customer_content, text="Enter Ticket ID:").pack(pady=5)
        ticket_entry = ttk.Entry(self.customer_content, width=30)
        ticket_entry.pack(pady=5)
        
        def search_ticket():
            ticket_id = ticket_entry.get().strip().upper()
            if not ticket_id:
                messagebox.showwarning("Input Required", "Enter Ticket ID")
                return
            
            if ticket_id in self.bookings:
                booking = self.bookings[ticket_id]
                details = f"""
Ticket ID: {booking['ticket_id']}
Name: {booking['name']}
Phone: {booking['phone']}
Route: {booking['departure']} → {booking['destination']}
Date: {booking['date']} | Time: {booking['time']}
Seat: {booking['seat']}
Fare: ${booking['fare']}
Status: {booking['status'].upper()}
                """
                messagebox.showinfo("Ticket Details", details)
            else:
                messagebox.showerror("Not Found", "Invalid Ticket ID")
        
        ttk.Button(self.customer_content, text="Search", command=search_ticket).pack(pady=10)
    
    def show_cancel_ticket(self):
        self.clear_frame(self.customer_content)
        
        ttk.Label(self.customer_content, text="Cancel Ticket", 
                 style='SubHeader.TLabel').pack(pady=20)
        
        ttk.Label(self.customer_content, text="Enter Ticket ID:").pack(pady=5)
        ticket_entry = ttk.Entry(self.customer_content, width=30)
        ticket_entry.pack(pady=5)
        
        def cancel_ticket():
            ticket_id = ticket_entry.get().strip().upper()
            if not ticket_id:
                messagebox.showwarning("Input Required", "Enter Ticket ID")
                return
            
            if ticket_id not in self.bookings:
                messagebox.showerror("Not Found", "Invalid Ticket ID")
                return
            
            if self.bookings[ticket_id].get('status') == 'cancelled':
                messagebox.showinfo("Already Cancelled", "This ticket is already cancelled")
                return
            
            if messagebox.askyesno("Confirm", f"Cancel ticket {ticket_id}?"):
                self.bookings[ticket_id]['status'] = 'cancelled'
                DataManager.save_bookings(self.bookings)
                messagebox.showinfo("Success", "Ticket cancelled successfully")
                self.show_welcome_customer()
        
        ttk.Button(self.customer_content, text="Cancel Ticket", 
                  command=cancel_ticket, style='Danger.TButton').pack(pady=10)
    
    def show_modify_booking(self):
        self.clear_frame(self.customer_content)
        
        ttk.Label(self.customer_content, text="Modify Booking", 
                 style='SubHeader.TLabel').pack(pady=20)
        
        ttk.Label(self.customer_content, text="Enter Ticket ID:").pack(pady=5)
        ticket_entry = ttk.Entry(self.customer_content, width=30)
        ticket_entry.pack(pady=5)
        
        def load_booking():
            ticket_id = ticket_entry.get().strip().upper()
            if not ticket_id:
                messagebox.showwarning("Input Required", "Enter Ticket ID")
                return
            
            if ticket_id not in self.bookings:
                messagebox.showerror("Not Found", "Invalid Ticket ID")
                return
            
            messagebox.showinfo("Info", "Modification feature: Please cancel and create new booking")
        
        ttk.Button(self.customer_content, text="Load Booking", command=load_booking).pack(pady=10)
    
    def show_route_fare(self):
        self.clear_frame(self.customer_content)
        
        ttk.Label(self.customer_content, text="Check Route & Fare", 
                 style='SubHeader.TLabel').pack(pady=20)
        
        all_cities = sorted(set([r.split(' to ')[0] for r in self.config['bus_routes'].keys()] +
                               [r.split(' to ')[1] for r in self.config['bus_routes'].keys()]))
        
        ttk.Label(self.customer_content, text="Departure:").pack(pady=5)
        dep_combo = ttk.Combobox(self.customer_content, values=all_cities, 
                                state="readonly", width=28)
        dep_combo.pack(pady=5)
        
        ttk.Label(self.customer_content, text="Destination:").pack(pady=5)
        dest_combo = ttk.Combobox(self.customer_content, values=all_cities, 
                                 state="readonly", width=28)
        dest_combo.pack(pady=5)
        
        result_label = ttk.Label(self.customer_content, text="", 
                                font=('Segoe UI', 13, 'bold'))
        result_label.pack(pady=20)
        
        def check_fare():
            dep = dep_combo.get()
            dest = dest_combo.get()
            
            if not dep or not dest:
                messagebox.showwarning("Input Required", "Select both locations")
                return
            
            route = f"{dep} to {dest}"
            if route in self.config['bus_routes']:
                fare = self.config['bus_routes'][route]
                schedule = self.config['bus_schedules'].get(route, 'N/A')
                result_label.config(text=f"Fare: ${fare}\nDeparture: {schedule}",
                                  foreground=self.COLOR_SUCCESS)
            else:
                result_label.config(text="No direct route available",
                                  foreground=self.COLOR_ERROR)
        
        ttk.Button(self.customer_content, text="Check", command=check_fare).pack(pady=10)
    
    def show_schedule(self):
        self.clear_frame(self.customer_content)
        
        ttk.Label(self.customer_content, text="Bus Schedules", 
                 style='SubHeader.TLabel').pack(pady=20)
        
        tree_frame = ttk.Frame(self.customer_content)
        tree_frame.pack(fill='both', expand=True, padx=20)
        
        columns = ("Route", "Departure Time", "Fare")
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        for route, schedule in sorted(self.config['bus_schedules'].items()):
            fare = self.config['bus_routes'].get(route, 0)
            tree.insert("", "end", values=(route, schedule, f"${fare}"))
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)
    
    def show_bus_stops(self):
        self.clear_frame(self.customer_content)
        
        ttk.Label(self.customer_content, text="Bus Stop Locations", 
                 style='SubHeader.TLabel').pack(pady=20)
        
        cities = sorted(self.config['bus_stops'].keys())
        
        ttk.Label(self.customer_content, text="Select City:").pack(pady=5)
        city_combo = ttk.Combobox(self.customer_content, values=cities, 
                                 state="readonly", width=28)
        city_combo.pack(pady=5)
        
        result_label = ttk.Label(self.customer_content, text="", 
                                font=('Segoe UI', 11), wraplength=500)
        result_label.pack(pady=20)
        
        def show_stops():
            city = city_combo.get()
            if not city:
                messagebox.showwarning("Input Required", "Select a city")
                return
            
            stops = self.config['bus_stops'].get(city, 'No information available')
            result_label.config(text=f"Bus stops in {city}:\n\n{stops}")
        
        ttk.Button(self.customer_content, text="Show Stops", command=show_stops).pack(pady=10)
    
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = BusBookingSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()

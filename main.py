from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
import pandas as pd

from modules.storage import initialize_storage
from modules.donor import (
    get_all_donors, add_donor, update_donor, delete_donor, search_donors
)
from modules.donation import (
    get_all_donations, add_donation, update_donation, delete_donation,
    search_donations
)
from modules.validation import (
    validate_donor, validate_donation, validate_search_amount
)
from modules.analytics import (
    get_summary_stats, donations_by_cause, donations_by_source,
    donations_by_month, get_top_donor
)
from modules.visualization import (
    create_cause_chart, create_source_chart, create_month_chart,
    save_all_reports, show_chart_in_frame
)


BASE_DIR = Path(__file__).resolve().parent


class DonationManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Donation Management & Transparency System")
        self.geometry("1280x820")
        self.minsize(1100, 700)
        self.configure(bg="#f4f6f8")

        initialize_storage(BASE_DIR)
        self.configure_styles()
        self.create_header()
        self.create_notebook()
        self.refresh_all()

    def configure_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background="#f4f6f8")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("TLabel", background="#f4f6f8", font=("Segoe UI", 10))
        style.configure("Title.TLabel", background="#16324f", foreground="white",
                        font=("Segoe UI", 18, "bold"))
        style.configure("Subtitle.TLabel", background="#16324f", foreground="#d9e7f5",
                        font=("Segoe UI", 10))
        style.configure("CardTitle.TLabel", background="#ffffff", foreground="#5a6773",
                        font=("Segoe UI", 10, "bold"))
        style.configure("CardValue.TLabel", background="#ffffff", foreground="#16324f",
                        font=("Segoe UI", 18, "bold"))
        style.configure("Section.TLabel", background="#f4f6f8", foreground="#16324f",
                        font=("Segoe UI", 14, "bold"))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=7)
        style.configure("Accent.TButton", foreground="white", background="#1f6aa5")
        style.map("Accent.TButton", background=[("active", "#15517f")])
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def create_header(self):
        header = tk.Frame(self, bg="#16324f", height=82)
        header.pack(fill="x")
        header.pack_propagate(False)

        ttk.Label(header, text="Donation Management & Transparency System",
                  style="Title.TLabel").pack(anchor="w", padx=24, pady=(14, 0))
        ttk.Label(header,
                  text="Python + Tkinter + Pandas + NumPy + Matplotlib + CSV",
                  style="Subtitle.TLabel").pack(anchor="w", padx=24, pady=(2, 8))

    def create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self.dashboard_tab = ttk.Frame(self.notebook)
        self.donor_tab = ttk.Frame(self.notebook)
        self.donation_tab = ttk.Frame(self.notebook)
        self.analytics_tab = ttk.Frame(self.notebook)
        self.reports_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.donor_tab, text="Donor Management")
        self.notebook.add(self.donation_tab, text="Donation Management")
        self.notebook.add(self.analytics_tab, text="Analytics")
        self.notebook.add(self.reports_tab, text="Reports")

        self.build_dashboard()
        self.build_donor_tab()
        self.build_donation_tab()
        self.build_analytics_tab()
        self.build_reports_tab()

    # ---------------- Dashboard ----------------
    def build_dashboard(self):
        container = ttk.Frame(self.dashboard_tab)
        container.pack(fill="both", expand=True, padx=18, pady=18)

        ttk.Label(container, text="Dashboard", style="Section.TLabel").pack(anchor="w")
        ttk.Label(container,
                  text="Transparent summary of donor and donation activity.",
                  foreground="#66727d").pack(anchor="w", pady=(0, 12))

        self.card_frame = ttk.Frame(container)
        self.card_frame.pack(fill="x")

        self.card_vars = {}
        cards = [
            ("Total Donations", "total"),
            ("Total Donors", "donors"),
            ("Average Donation", "average"),
            ("Largest Donation", "maximum"),
            ("This Month", "month"),
            ("Top Cause", "cause"),
        ]
        for i, (title, key) in enumerate(cards):
            card = ttk.Frame(self.card_frame, style="Card.TFrame", padding=14)
            card.grid(row=0, column=i, sticky="nsew", padx=5)
            self.card_frame.columnconfigure(i, weight=1)
            ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
            self.card_vars[key] = tk.StringVar(value="—")
            ttk.Label(card, textvariable=self.card_vars[key],
                      style="CardValue.TLabel").pack(anchor="w", pady=(6, 0))

        summary_box = ttk.Frame(container, style="Card.TFrame", padding=16)
        summary_box.pack(fill="both", expand=True, pady=(18, 0))
        ttk.Label(summary_box, text="Quick Summary",
                  background="#ffffff", foreground="#16324f",
                  font=("Segoe UI", 13, "bold")).pack(anchor="w")
        self.dashboard_summary = tk.Text(summary_box, height=12, wrap="word",
                                         bg="white", relief="flat",
                                         font=("Segoe UI", 10))
        self.dashboard_summary.pack(fill="both", expand=True, pady=(8, 0))

    def refresh_dashboard(self):
        donations = get_all_donations(BASE_DIR)
        donors = get_all_donors(BASE_DIR)
        stats = get_summary_stats(donations)
        top = get_top_donor(donations, donors)

        self.card_vars["total"].set(f"₹{stats['total']:,.2f}")
        self.card_vars["donors"].set(str(len(donors)))
        self.card_vars["average"].set(f"₹{stats['average']:,.2f}")
        self.card_vars["maximum"].set(f"₹{stats['maximum']:,.2f}")
        self.card_vars["month"].set(f"₹{stats['this_month']:,.2f}")
        self.card_vars["cause"].set(stats["top_cause"] or "—")

        lines = [
            f"Total donation records: {stats['count']}",
            f"Unique donors contributing: {stats['unique_donors']}",
            f"Total donation value: ₹{stats['total']:,.2f}",
            f"Average donation: ₹{stats['average']:,.2f}",
            f"Median donation: ₹{stats['median']:,.2f}",
            f"Minimum donation: ₹{stats['minimum']:,.2f}",
            f"Maximum donation: ₹{stats['maximum']:,.2f}",
            f"Most supported cause: {stats['top_cause'] or 'No data'}",
            f"Most common donation source: {stats['top_source'] or 'No data'}",
        ]
        if top:
            lines.append(
                f"Top donor by total contribution: {top['name']} "
                f"(₹{top['total']:,.2f})"
            )
        self.dashboard_summary.delete("1.0", "end")
        self.dashboard_summary.insert("1.0", "\n".join(lines))

    # ---------------- Donors ----------------
    def build_donor_tab(self):
        self.donor_tab.columnconfigure(1, weight=1)
        self.donor_tab.rowconfigure(0, weight=1)

        form = ttk.Frame(self.donor_tab, style="Card.TFrame", padding=16)
        form.grid(row=0, column=0, sticky="nsw", padx=(12, 6), pady=12)

        ttk.Label(form, text="Donor Details", background="#ffffff",
                  foreground="#16324f", font=("Segoe UI", 13, "bold")).grid(
                      row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        self.donor_id = tk.StringVar()
        self.donor_name = tk.StringVar()
        self.donor_phone = tk.StringVar()
        self.donor_email = tk.StringVar()
        self.donor_city = tk.StringVar()
        self.donor_type = tk.StringVar(value="Individual")

        donor_fields = [
            ("Donor ID", self.donor_id),
            ("Name", self.donor_name),
            ("Phone", self.donor_phone),
            ("Email", self.donor_email),
            ("City", self.donor_city),
        ]
        for r, (label, var) in enumerate(donor_fields, start=1):
            ttk.Label(form, text=label, background="#ffffff").grid(
                row=r, column=0, sticky="w", pady=5)
            ttk.Entry(form, textvariable=var, width=27).grid(
                row=r, column=1, sticky="ew", pady=5)

        ttk.Label(form, text="Donor Type", background="#ffffff").grid(
            row=6, column=0, sticky="w", pady=5)
        ttk.Combobox(form, textvariable=self.donor_type, state="readonly",
                     values=["Individual", "Organization", "Corporate", "NGO", "Other"],
                     width=24).grid(row=6, column=1, sticky="ew", pady=5)

        btns = ttk.Frame(form, style="Card.TFrame")
        btns.grid(row=7, column=0, columnspan=2, pady=(14, 0), sticky="ew")
        ttk.Button(btns, text="Add / Save", style="Accent.TButton",
                   command=self.save_donor).pack(fill="x", pady=3)
        ttk.Button(btns, text="Update Selected",
                   command=self.update_selected_donor).pack(fill="x", pady=3)
        ttk.Button(btns, text="Delete Selected",
                   command=self.delete_selected_donor).pack(fill="x", pady=3)
        ttk.Button(btns, text="Clear", command=self.clear_donor_form).pack(
            fill="x", pady=3)

        list_frame = ttk.Frame(self.donor_tab, style="Card.TFrame", padding=12)
        list_frame.grid(row=0, column=1, sticky="nsew", padx=(6, 12), pady=12)
        list_frame.rowconfigure(2, weight=1)
        list_frame.columnconfigure(0, weight=1)

        ttk.Label(list_frame, text="Donor Records", background="#ffffff",
                  foreground="#16324f", font=("Segoe UI", 13, "bold")).grid(
                      row=0, column=0, sticky="w")
        search_bar = ttk.Frame(list_frame, style="Card.TFrame")
        search_bar.grid(row=1, column=0, sticky="ew", pady=8)
        search_bar.columnconfigure(1, weight=1)
        ttk.Label(search_bar, text="Search:", background="#ffffff").grid(
            row=0, column=0, padx=(0, 6))
        self.donor_search = tk.StringVar()
        entry = ttk.Entry(search_bar, textvariable=self.donor_search)
        entry.grid(row=0, column=1, sticky="ew")
        entry.bind("<Return>", lambda _e: self.refresh_donors())
        ttk.Button(search_bar, text="Search",
                   command=self.refresh_donors).grid(row=0, column=2, padx=5)
        ttk.Button(search_bar, text="Show All",
                   command=lambda: [self.donor_search.set(""), self.refresh_donors()]
                   ).grid(row=0, column=3)

        columns = ("donor_id", "name", "phone", "email", "city", "donor_type")
        self.donor_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        headings = ["Donor ID", "Name", "Phone", "Email", "City", "Type"]
        widths = [90, 150, 110, 190, 110, 110]
        for col, heading, width in zip(columns, headings, widths):
            self.donor_tree.heading(col, text=heading)
            self.donor_tree.column(col, width=width, anchor="w")
        self.donor_tree.grid(row=2, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(list_frame, orient="vertical",
                               command=self.donor_tree.yview)
        scroll.grid(row=2, column=1, sticky="ns")
        self.donor_tree.configure(yscrollcommand=scroll.set)
        self.donor_tree.bind("<<TreeviewSelect>>", self.on_donor_select)

    def save_donor(self):
        data = {
            "donor_id": self.donor_id.get().strip(),
            "name": self.donor_name.get().strip(),
            "phone": self.donor_phone.get().strip(),
            "email": self.donor_email.get().strip(),
            "city": self.donor_city.get().strip(),
            "donor_type": self.donor_type.get().strip(),
        }
        ok, message = validate_donor(data)
        if not ok:
            messagebox.showerror("Validation Error", message)
            return
        try:
            add_donor(BASE_DIR, data)
            messagebox.showinfo("Success", "Donor added successfully.")
            self.clear_donor_form()
            self.refresh_all()
        except ValueError as exc:
            messagebox.showerror("Cannot Add Donor", str(exc))
        except Exception as exc:
            messagebox.showerror("Error", f"Unexpected error:\n{exc}")

    def update_selected_donor(self):
        data = {
            "donor_id": self.donor_id.get().strip(),
            "name": self.donor_name.get().strip(),
            "phone": self.donor_phone.get().strip(),
            "email": self.donor_email.get().strip(),
            "city": self.donor_city.get().strip(),
            "donor_type": self.donor_type.get().strip(),
        }
        ok, message = validate_donor(data)
        if not ok:
            messagebox.showerror("Validation Error", message)
            return
        try:
            updated = update_donor(BASE_DIR, data["donor_id"], data)
            if not updated:
                messagebox.showwarning("Not Found", "Donor ID was not found.")
                return
            messagebox.showinfo("Success", "Donor updated successfully.")
            self.clear_donor_form()
            self.refresh_all()
        except Exception as exc:
            messagebox.showerror("Error", f"Unable to update donor:\n{exc}")

    def delete_selected_donor(self):
        donor_id = self.donor_id.get().strip()
        if not donor_id:
            messagebox.showwarning("Select Donor", "Please select a donor first.")
            return
        donations = get_all_donations(BASE_DIR)
        linked = [d for d in donations if d["donor_id"] == donor_id]
        if linked:
            messagebox.showwarning(
                "Delete Blocked",
                "This donor has donation records. Delete or reassign those "
                "donations first to preserve data integrity."
            )
            return
        if not messagebox.askyesno("Confirm Delete",
                                   f"Delete donor {donor_id}?"):
            return
        try:
            if delete_donor(BASE_DIR, donor_id):
                messagebox.showinfo("Deleted", "Donor deleted successfully.")
                self.clear_donor_form()
                self.refresh_all()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def on_donor_select(self, _event=None):
        selection = self.donor_tree.selection()
        if not selection:
            return
        vals = self.donor_tree.item(selection[0], "values")
        self.donor_id.set(vals[0])
        self.donor_name.set(vals[1])
        self.donor_phone.set(vals[2])
        self.donor_email.set(vals[3])
        self.donor_city.set(vals[4])
        self.donor_type.set(vals[5])

    def clear_donor_form(self):
        self.donor_id.set("")
        self.donor_name.set("")
        self.donor_phone.set("")
        self.donor_email.set("")
        self.donor_city.set("")
        self.donor_type.set("Individual")

    def refresh_donors(self):
        for item in self.donor_tree.get_children():
            self.donor_tree.delete(item)
        query = self.donor_search.get().strip()
        records = search_donors(BASE_DIR, query) if query else get_all_donors(BASE_DIR)
        for d in records:
            self.donor_tree.insert("", "end", values=(
                d["donor_id"], d["name"], d["phone"], d["email"],
                d["city"], d["donor_type"]
            ))

    # ---------------- Donations ----------------
    def build_donation_tab(self):
        self.donation_tab.columnconfigure(1, weight=1)
        self.donation_tab.rowconfigure(0, weight=1)

        form = ttk.Frame(self.donation_tab, style="Card.TFrame", padding=16)
        form.grid(row=0, column=0, sticky="nsw", padx=(12, 6), pady=12)

        ttk.Label(form, text="Donation Details", background="#ffffff",
                  foreground="#16324f", font=("Segoe UI", 13, "bold")).grid(
                      row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        self.donation_id = tk.StringVar()
        self.donation_donor_id = tk.StringVar()
        self.donation_date = tk.StringVar(value=date.today().isoformat())
        self.donation_amount = tk.StringVar()
        self.donation_cause = tk.StringVar(value="Education")
        self.donation_source = tk.StringVar(value="Individual")
        self.donation_payment = tk.StringVar(value="UPI")
        self.donation_description = tk.StringVar()

        fields = [
            ("Donation ID", self.donation_id),
            ("Donor ID", self.donation_donor_id),
            ("Date (YYYY-MM-DD)", self.donation_date),
            ("Amount (₹)", self.donation_amount),
        ]
        for r, (label, var) in enumerate(fields, start=1):
            ttk.Label(form, text=label, background="#ffffff").grid(
                row=r, column=0, sticky="w", pady=5)
            ttk.Entry(form, textvariable=var, width=27).grid(
                row=r, column=1, sticky="ew", pady=5)

        ttk.Label(form, text="Cause", background="#ffffff").grid(
            row=5, column=0, sticky="w", pady=5)
        ttk.Combobox(form, textvariable=self.donation_cause, state="readonly",
                     values=[
                         "Education", "Healthcare", "Food", "Child Welfare",
                         "Animal Welfare", "Disaster Relief", "Environment",
                         "Community Development", "Other"
                     ], width=24).grid(row=5, column=1, sticky="ew", pady=5)

        ttk.Label(form, text="Source", background="#ffffff").grid(
            row=6, column=0, sticky="w", pady=5)
        ttk.Combobox(form, textvariable=self.donation_source, state="readonly",
                     values=[
                         "Individual", "Organization", "Corporate", "NGO",
                         "Event", "Online Campaign", "Other"
                     ], width=24).grid(row=6, column=1, sticky="ew", pady=5)

        ttk.Label(form, text="Payment Mode", background="#ffffff").grid(
            row=7, column=0, sticky="w", pady=5)
        ttk.Combobox(form, textvariable=self.donation_payment, state="readonly",
                     values=["UPI", "Cash", "Bank Transfer", "Card", "Cheque", "Other"],
                     width=24).grid(row=7, column=1, sticky="ew", pady=5)

        ttk.Label(form, text="Description", background="#ffffff").grid(
            row=8, column=0, sticky="w", pady=5)
        ttk.Entry(form, textvariable=self.donation_description,
                  width=27).grid(row=8, column=1, sticky="ew", pady=5)

        btns = ttk.Frame(form, style="Card.TFrame")
        btns.grid(row=9, column=0, columnspan=2, pady=(14, 0), sticky="ew")
        ttk.Button(btns, text="Add / Save", style="Accent.TButton",
                   command=self.save_donation).pack(fill="x", pady=3)
        ttk.Button(btns, text="Update Selected",
                   command=self.update_selected_donation).pack(fill="x", pady=3)
        ttk.Button(btns, text="Delete Selected",
                   command=self.delete_selected_donation).pack(fill="x", pady=3)
        ttk.Button(btns, text="Clear",
                   command=self.clear_donation_form).pack(fill="x", pady=3)

        list_frame = ttk.Frame(self.donation_tab, style="Card.TFrame", padding=12)
        list_frame.grid(row=0, column=1, sticky="nsew", padx=(6, 12), pady=12)
        list_frame.rowconfigure(2, weight=1)
        list_frame.columnconfigure(0, weight=1)

        ttk.Label(list_frame, text="Donation Records", background="#ffffff",
                  foreground="#16324f", font=("Segoe UI", 13, "bold")).grid(
                      row=0, column=0, sticky="w")

        search_bar = ttk.Frame(list_frame, style="Card.TFrame")
        search_bar.grid(row=1, column=0, sticky="ew", pady=8)
        search_bar.columnconfigure(1, weight=1)

        ttk.Label(search_bar, text="Search:", background="#ffffff").grid(
            row=0, column=0, padx=(0, 6))
        self.donation_search = tk.StringVar()
        ttk.Entry(search_bar, textvariable=self.donation_search).grid(
            row=0, column=1, sticky="ew")
        ttk.Button(search_bar, text="Search",
                   command=self.refresh_donations).grid(row=0, column=2, padx=5)
        ttk.Button(search_bar, text="Show All",
                   command=lambda: [self.donation_search.set(""),
                                    self.refresh_donations()]).grid(row=0, column=3)

        columns = ("donation_id", "donor_id", "date", "amount", "cause",
                   "source", "payment_mode", "description")
        self.donation_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        headings = ["Donation ID", "Donor ID", "Date", "Amount", "Cause",
                    "Source", "Payment", "Description"]
        widths = [95, 80, 95, 100, 130, 120, 110, 190]
        for col, heading, width in zip(columns, headings, widths):
            self.donation_tree.heading(col, text=heading)
            self.donation_tree.column(col, width=width, anchor="w")
        self.donation_tree.grid(row=2, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(list_frame, orient="vertical",
                               command=self.donation_tree.yview)
        scroll.grid(row=2, column=1, sticky="ns")
        self.donation_tree.configure(yscrollcommand=scroll.set)
        self.donation_tree.bind("<<TreeviewSelect>>", self.on_donation_select)

    def save_donation(self):
        data = {
            "donation_id": self.donation_id.get().strip(),
            "donor_id": self.donation_donor_id.get().strip(),
            "date": self.donation_date.get().strip(),
            "amount": self.donation_amount.get().strip(),
            "cause": self.donation_cause.get().strip(),
            "source": self.donation_source.get().strip(),
            "payment_mode": self.donation_payment.get().strip(),
            "description": self.donation_description.get().strip(),
        }
        ok, message = validate_donation(data)
        if not ok:
            messagebox.showerror("Validation Error", message)
            return

        donor_ids = {d["donor_id"] for d in get_all_donors(BASE_DIR)}
        if data["donor_id"] not in donor_ids:
            messagebox.showerror("Invalid Donor",
                                 "The selected Donor ID does not exist.")
            return

        try:
            add_donation(BASE_DIR, data)
            messagebox.showinfo("Success", "Donation added successfully.")
            self.clear_donation_form()
            self.refresh_all()
        except ValueError as exc:
            messagebox.showerror("Cannot Add Donation", str(exc))
        except Exception as exc:
            messagebox.showerror("Error", f"Unexpected error:\n{exc}")

    def update_selected_donation(self):
        data = {
            "donation_id": self.donation_id.get().strip(),
            "donor_id": self.donation_donor_id.get().strip(),
            "date": self.donation_date.get().strip(),
            "amount": self.donation_amount.get().strip(),
            "cause": self.donation_cause.get().strip(),
            "source": self.donation_source.get().strip(),
            "payment_mode": self.donation_payment.get().strip(),
            "description": self.donation_description.get().strip(),
        }
        ok, message = validate_donation(data)
        if not ok:
            messagebox.showerror("Validation Error", message)
            return
        donor_ids = {d["donor_id"] for d in get_all_donors(BASE_DIR)}
        if data["donor_id"] not in donor_ids:
            messagebox.showerror("Invalid Donor",
                                 "The Donor ID does not exist.")
            return
        try:
            updated = update_donation(BASE_DIR, data["donation_id"], data)
            if not updated:
                messagebox.showwarning("Not Found",
                                       "Donation ID was not found.")
                return
            messagebox.showinfo("Success", "Donation updated successfully.")
            self.clear_donation_form()
            self.refresh_all()
        except Exception as exc:
            messagebox.showerror("Error",
                                 f"Unable to update donation:\n{exc}")

    def delete_selected_donation(self):
        donation_id = self.donation_id.get().strip()
        if not donation_id:
            messagebox.showwarning("Select Donation",
                                   "Please select a donation first.")
            return
        if not messagebox.askyesno("Confirm Delete",
                                   f"Delete donation {donation_id}?"):
            return
        try:
            if delete_donation(BASE_DIR, donation_id):
                messagebox.showinfo("Deleted",
                                    "Donation deleted successfully.")
                self.clear_donation_form()
                self.refresh_all()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def on_donation_select(self, _event=None):
        selection = self.donation_tree.selection()
        if not selection:
            return
        vals = self.donation_tree.item(selection[0], "values")
        self.donation_id.set(vals[0])
        self.donation_donor_id.set(vals[1])
        self.donation_date.set(vals[2])
        self.donation_amount.set(vals[3])
        self.donation_cause.set(vals[4])
        self.donation_source.set(vals[5])
        self.donation_payment.set(vals[6])
        self.donation_description.set(vals[7])

    def clear_donation_form(self):
        self.donation_id.set("")
        self.donation_donor_id.set("")
        self.donation_date.set(date.today().isoformat())
        self.donation_amount.set("")
        self.donation_cause.set("Education")
        self.donation_source.set("Individual")
        self.donation_payment.set("UPI")
        self.donation_description.set("")

    def refresh_donations(self):
        for item in self.donation_tree.get_children():
            self.donation_tree.delete(item)
        query = self.donation_search.get().strip()
        records = (search_donations(BASE_DIR, query)
                   if query else get_all_donations(BASE_DIR))
        for d in records:
            self.donation_tree.insert("", "end", values=(
                d["donation_id"], d["donor_id"], d["date"],
                f"₹{float(d['amount']):,.2f}", d["cause"], d["source"],
                d["payment_mode"], d["description"]
            ))

    # ---------------- Analytics ----------------
    def build_analytics_tab(self):
        outer = ttk.Frame(self.analytics_tab)
        outer.pack(fill="both", expand=True, padx=18, pady=18)
        ttk.Label(outer, text="Analytics", style="Section.TLabel").pack(anchor="w")
        ttk.Label(outer,
                  text="Use Pandas and NumPy to analyze contribution patterns.",
                  foreground="#66727d").pack(anchor="w", pady=(0, 10))

        controls = ttk.Frame(outer, style="Card.TFrame", padding=10)
        controls.pack(fill="x")
        ttk.Label(controls, text="Analysis:", background="#ffffff").pack(
            side="left", padx=(0, 6))
        self.analysis_choice = tk.StringVar(value="By Cause")
        ttk.Combobox(controls, textvariable=self.analysis_choice, state="readonly",
                     values=["By Cause", "By Source", "By Month"],
                     width=18).pack(side="left")
        ttk.Button(controls, text="Analyze",
                   style="Accent.TButton",
                   command=self.run_analysis).pack(side="left", padx=8)
        ttk.Button(controls, text="Refresh",
                   command=self.run_analysis).pack(side="left")

        self.analysis_text = tk.Text(outer, height=10, wrap="word",
                                     bg="white", relief="flat",
                                     font=("Consolas", 10))
        self.analysis_text.pack(fill="x", pady=(12, 8))

        self.analysis_chart_frame = ttk.Frame(outer, style="Card.TFrame")
        self.analysis_chart_frame.pack(fill="both", expand=True)

    def run_analysis(self):
        try:
            donations = get_all_donations(BASE_DIR)
            choice = self.analysis_choice.get()
            if choice == "By Cause":
                data = donations_by_cause(donations)
                fig = create_cause_chart(data)
            elif choice == "By Source":
                data = donations_by_source(donations)
                fig = create_source_chart(data)
            else:
                data = donations_by_month(donations)
                fig = create_month_chart(data)

            self.analysis_text.delete("1.0", "end")
            if data.empty:
                self.analysis_text.insert("1.0", "No data available.")
            else:
                summary = data.to_string()
                self.analysis_text.insert("1.0", summary)
            show_chart_in_frame(self.analysis_chart_frame, fig)
        except Exception as exc:
            messagebox.showerror("Analytics Error", str(exc))

    # ---------------- Reports ----------------
    def build_reports_tab(self):
        outer = ttk.Frame(self.reports_tab)
        outer.pack(fill="both", expand=True, padx=18, pady=18)
        ttk.Label(outer, text="Visual Reports", style="Section.TLabel").pack(anchor="w")
        ttk.Label(
            outer,
            text="At least two meaningful Matplotlib visualizations are required; "
                 "this project provides three.",
            foreground="#66727d"
        ).pack(anchor="w", pady=(0, 12))

        button_frame = ttk.Frame(outer, style="Card.TFrame", padding=14)
        button_frame.pack(fill="x")
        ttk.Button(button_frame, text="Preview Cause Chart",
                   command=lambda: self.preview_report("cause")).pack(
                       side="left", padx=5)
        ttk.Button(button_frame, text="Preview Source Chart",
                   command=lambda: self.preview_report("source")).pack(
                       side="left", padx=5)
        ttk.Button(button_frame, text="Preview Monthly Trend",
                   command=lambda: self.preview_report("month")).pack(
                       side="left", padx=5)
        ttk.Button(button_frame, text="Save All Reports",
                   style="Accent.TButton",
                   command=self.save_reports).pack(side="left", padx=5)

        self.report_chart_frame = ttk.Frame(outer, style="Card.TFrame")
        self.report_chart_frame.pack(fill="both", expand=True, pady=(12, 0))

    def preview_report(self, report_type):
        donations = get_all_donations(BASE_DIR)
        if report_type == "cause":
            fig = create_cause_chart(donations_by_cause(donations))
        elif report_type == "source":
            fig = create_source_chart(donations_by_source(donations))
        else:
            fig = create_month_chart(donations_by_month(donations))
        show_chart_in_frame(self.report_chart_frame, fig)

    def save_reports(self):
        try:
            paths = save_all_reports(BASE_DIR, get_all_donations(BASE_DIR))
            messagebox.showinfo(
                "Reports Saved",
                "Reports generated successfully:\n\n" +
                "\n".join(str(p.relative_to(BASE_DIR)) for p in paths)
            )
        except Exception as exc:
            messagebox.showerror("Report Error", str(exc))

    # ---------------- Global ----------------
    def refresh_all(self):
        self.refresh_dashboard()
        self.refresh_donors()
        self.refresh_donations()
        self.run_analysis()

    def close_app(self):
        self.destroy()


if __name__ == "__main__":
    app = DonationManagementApp()
    app.protocol("WM_DELETE_WINDOW", app.close_app)
    app.mainloop()

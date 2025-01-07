from functions import *
from customtkinter import *

main_color = "#2A004E"
anth_color = "#500073"

def add_domain():
    domain = domain_entry_add.get()
    if domain:
        ips = get_ips(domain)
        save_blocked_ips_db(domain, ips)
        message_label = CTkLabel(tabView.tab("Add"), text=f"Domain '{domain}' added!", font=("Arial", 16), text_color="green")
        message_label.pack()
        tabView.tab("Add").after(3000, message_label.destroy)  

def delete_domain():
    domain = domain_entry_delete.get()
    if domain:
        delete_domain_from_db(domain)
        message_label = CTkLabel(tabView.tab("Delete"), text=f"Domain '{domain}' deleted!", font=("Arial", 16), text_color="red")
        message_label.pack()
        tabView.tab("Delete").after(3000, message_label.destroy)  

def view_domains():
    # Under development 
    pass

def reset_domains():
    reset_table()
    message_label = CTkLabel(tabView.tab("Reset"), text="Database reset successfully!", font=("Arial", 16), text_color="orange")
    message_label.pack()
    tabView.tab("Reset").after(3000, message_label.destroy)  

if __name__ == "__main__":
    create_db()
    clear_screen()

    app = CTk()
    app.geometry("500x300")
    app.title("Keep it Halal")

    # ------------------- Label -------------------
    lb1 = CTkLabel(app, text="Keep it Halal", font=("Arial", 40)).pack()

    # ------------------- Tabs -------------------
    tabView = CTkTabview(app)
    tabView.pack(padx=20, pady=20)
    tabView.add("Add")
    tabView.add("Delete")
    tabView.add("View")
    tabView.add("Reset")

    # ------------------- Tab 1 : Add -------------------
    CTkLabel(tabView.tab("Add"), text="Enter Domain to add", font=("Arial", 20)).pack()
    domain_entry_add = CTkEntry(tabView.tab("Add"), width=150)
    domain_entry_add.pack()
    CTkButton(tabView.tab("Add"), text="Add", command=add_domain, width=150, fg_color="#5D8736", hover_color="#809D3C").pack()

    # ------------------- Tab 2 : Delete -------------------
    CTkLabel(tabView.tab("Delete"), text="Enter Domain to delete", font=("Arial", 20)).pack()
    domain_entry_delete = CTkEntry(tabView.tab("Delete"), width=150)
    domain_entry_delete.pack()
    CTkButton(tabView.tab("Delete"), text="Delete", command=delete_domain, width=150, fg_color="#C62E2E", hover_color="#C62300").pack()

    # ------------------- Tab 3 : View -------------------
    CTkButton(tabView.tab("View"), text="Refresh", command=view_domains, width=150, fg_color="#005BBB", hover_color="#0073E6").pack()
    blocked_domains = CTkLabel(tabView.tab("View"), text="", font=("Arial", 14))
    
    # ------------------- Tab 4 : Reset -------------------
    CTkLabel(tabView.tab("Reset"), text="Delete all blocked domains\n from Database", font=("Arial", 20)).pack()
    CTkButton(tabView.tab("Reset"), text="Reset", command=reset_domains, width=150, fg_color="#EB5B00", hover_color="#FA812F").pack()

    app.mainloop()

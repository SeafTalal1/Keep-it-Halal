import dns.resolver
import sqlite3
import subprocess
import time
import os


def add_to_hosts(domain):
    hosts_path = r"C:/Windows/System32/drivers/etc/hosts"  # مسار ملف hosts
    entry = f"127.0.0.1 {domain}\n"  # الصيغة اللي هنضيفها

    try:
        with open(hosts_path, 'r+') as file:  # فتح الملف للقراءة والكتابة
            content = file.read()
            if entry not in content:  # نتأكد إن الدومين مش موجود
                file.write(entry)
                print(f"{domain} has been added to the hosts file.")
            else:
                print(f"{domain} is already in the hosts file.")
    except PermissionError:
        print("Run the script as Administrator to modify the hosts file.")
    except Exception as e:
        print(f"An error occurred: {e}")


def remove_from_hosts(domain):
    hosts_path = r"C:/Windows/System32/drivers/etc/hosts"
    try:
        with open(hosts_path, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if domain not in line:
                    file.write(line)
            file.truncate()
            print(f"{domain} has been removed from the hosts file.")
    except PermissionError:
        print("Run the script as Administrator to modify the hosts file.")
    except Exception as e:
        print(f"An error occurred: {e}")



def block_ip(ip):
    try:
        subprocess.run(
            ["netsh", "advfirewall", "firewall", "add", "rule", "name=Block IP", "dir=in", "action=block", "remoteip=" + ip, "enable=yes"], 
            check=True
        )
        subprocess.run(
            ["netsh", "advfirewall", "firewall", "add", "rule", "name=Block IP", "dir=out", "action=block", "remoteip=" + ip, "enable=yes"], 
            check=True
        )
        print(f"IP {ip} has been blocked successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to block IP {ip}: {e}")


def get_ips(domain):
    try:
        # Get all IPs for the domain
        result = dns.resolver.resolve(domain, 'A')  # A is for IPv4
        ips = [ip.address for ip in result]
        return ips
    except dns.resolver.NoAnswer:
        print("No IP addresses found for this domain.")
        return []
    except dns.resolver.NXDOMAIN:
        print("Domain does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


# Create a DB to save all IPs
def create_db():
    conn = sqlite3.connect('blocked_ips.db')    # Connect to the DB, or create a new one if not exist
    cursor = conn.cursor()                      # Cursor is the object that perform our comamnds in DB
    # Creating the table with 2 columns [ id : the primary key - ip : the ip addresses ]
    cursor.execute('''                          
        CREATE TABLE IF NOT EXISTS blocked_ips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            ip TEXT NOT NULL
        )
    ''')
    conn.commit()                               # Save changes 
    conn.close()                                # End the connection 
    print("Database and table created (if not already exists).")


# Add IPs the the DB
def save_blocked_ips_db(domain, ips):
    conn = sqlite3.connect('blocked_ips.db')    # Connect to the DB, or create a new one if not exist
    cursor = conn.cursor()                      # Cursor is the object that perform our comamnds in DB

    for ip in ips:                              # Insert each ip in ips[] in the ip column
        cursor.execute("SELECT ip FROM blocked_ips WHERE domain = ? AND ip = ?", (domain, ip))
        existing_ip = cursor.fetchone()
        if existing_ip:
            print(f"IP {ip} is already blocked for domain {domain}.")
        else:
            cursor.execute("INSERT INTO blocked_ips (domain, ip) VALUES (?, ?)", (domain, ip))
            block_ip(ip)

    
    conn.commit()                               # Save changes 
    conn.close()                                # End the connection
    for ip in ips:
        block_ip(ip)
    add_to_hosts(domain)
    print("Blocked IPs saved to database.")


def view_blocked_ips():
    conn = sqlite3.connect('blocked_ips.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blocked_ips")
    rows = cursor.fetchall()
    if rows:
        print(f"{'ID':<5} {'Domain':<25} {'IP':<15}")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<25} {row[2]:<15}")
    else:
        print("No data found.")
        
    conn.close()


def delete_domain_from_db(domain):
    ips = get_ips(domain)
    conn = sqlite3.connect('blocked_ips.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM blocked_ips WHERE domain = ?", (domain,))
    cursor.execute("DELETE FROM blocked_ips WHERE domain IS NULL OR domain = ''")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='blocked_ips'")
    conn.commit()
    conn.close()
    print(f"Domain {domain} deleted from the database.")
    for ip in ips:
        try:
            subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", "name=Block IP", "remoteip=" + ip], check=True)
            print(f"IP {ip} removed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to remove IP {ip}: {e}")
    remove_from_hosts(domain)

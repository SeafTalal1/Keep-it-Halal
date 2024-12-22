import dns.resolver
import sqlite3
import subprocess
import time


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
        cursor.execute("INSERT INTO blocked_ips (domain, ip) VALUES (?, ?)", (domain, ip))

    
    conn.commit()                               # Save changes 
    conn.close()                                # End the connection
    for ip in ips:
        block_ip(ip)
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
    




if __name__ == "__main__":
    create_db()
    while True:
        print("-" * 50)
        command = input("1. Add Domain\n2. Delete Domain\n3. View all Blocked IPs\n4. Quit\n> ")
        print("-" * 50)
        if command.isdigit():
            command = int(command)
            if command == 1:
                domain = input("Enter Domain to add : ")
                ips = get_ips(domain)
                save_blocked_ips_db(domain, ips)
            elif command == 2:
                domain = input("Enter Domain to delete : ")
                delete_domain_from_db(domain)
            elif command == 3:
                view_blocked_ips()
            elif command == 4:
                print("Program CLosed Succesfully")
                time.sleep(1)
                break

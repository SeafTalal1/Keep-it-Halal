from functions import *


if __name__ == "__main__":
    create_db()
    clear_screen()
    while True:
        print("-" * 50)
        command = input("1. Add Domain\n2. Delete Domain\n3. View all Blocked IPs\n4. Reset Database\n5. Quit\n> ")
        print("-" * 50)
        if command.isdigit():
            command = int(command)
            if command == 1:
                clear_screen()
                domain = input("Enter Domain to add : ")
                ips = get_ips(domain)
                save_blocked_ips_db(domain, ips)
            elif command == 2:
                clear_screen()
                domain = input("Enter Domain to delete : ")
                delete_domain_from_db(domain)
            elif command == 3:
                clear_screen()
                view_blocked_ips()
            elif command == 4:
                reset_table()
                print("Database reset successfully")
            elif command == 5:
                print("Program CLosed Succesfully")
                time.sleep(1)
                clear_screen()
                break

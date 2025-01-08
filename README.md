# Keep-It-Halal 🕋

## Summary
![image](https://github.com/user-attachments/assets/c916eb2f-90ef-4abd-a3b7-11f59783f7c6)

The provided text describes a Python script designed to manage IP addresses associated with a domain using the Windows Firewall. The script has the following main functionalities:

1. **Block IPs**: The script can block the IPs of a given domain using the Windows Firewall.
2. **Unblock IPs**: The script can remove the blocking rules from the firewall and delete the domain data from the database.
3. **Database Management**: The script stores the blocked IPs and their associated domains in a SQLite database.
4. **View Blocked IPs**: The script can display all the domains and their blocked IPs from the database.

The script requires Python 3.x, the `dns.resolver` library for DNS resolution, the `sqlite3` library for database management, and the `subprocess` library for executing Windows firewall commands.

## GUI-based Program

The Keep-It-Halal program is now a GUI-based application with buttons and text boxes, maintaining the same functionalities as the original script.

### Main Window

The main window of the program consists of the following tabs :

- **Add**: A button to block the IPs associated with the entered domain.
- **Delete**: A button to unblock the IPs associated with the entered domain.
- **View**: A button to display all the blocked domains and their associated IPs.
- **Reset**: A button to remove all domains and their IPs from the database and the host file.

### Functionality

1. **Block IPs**:
   - The user enters a domain in the text box.
   - The program resolves the IPs associated with the domain and adds them to the database.
   - The program blocks the IPs using the Windows Firewall.

2. **Unblock IPs**:
   - The user enters a domain in the text box.
   - The program removes the domain and its IPs from the database.
   - The program unblocks the IPs by deleting the firewall rules.

3. **View Blocked IPs**:
   - The program displays a list of all blocked domains and their associated IPs. [ Still Under Dev. ]

4. **Reset Database**:
   - The program removes all domains and their IPs from the database and the host file. 

5. **Quit**:
   - The program exits.

### Requirements

- Python 3.x
- `dns.resolver` library (for DNS resolution)
- `sqlite3` library (for database management)
- `subprocess` library (for executing Windows firewall commands)
- `tkinter` library (for creating the GUI)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/keep-it-halal.git
   ```
2. Install the required dependencies:
   - `dns.resolver` comes with the `dnspython` package, which can be installed with:
     ```bash
     pip install -r requirements.txt
     ```
3. Run the GUI-based program as Administrator:
   - Open `Command Prompt` as Administrator and then run the script with administrator privileges:
   ```bash
   python main.py
   ```

### Usage

The GUI-based Keep-It-Halal program provides a user-friendly interface to manage the blocking and unblocking of IP addresses associated with domains. Users can interact with the program using the provided buttons and text boxes.

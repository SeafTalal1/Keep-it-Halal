# Keep-It-Halal

## Purpose
The script is designed to block and unblock IP addresses associated with a domain using the Windows Firewall. It manages a SQLite database to store the IP addresses linked to domains, allowing the user to add, delete, or view the blocked IPs.

## Main Functionalities
1. **Block IPs**: The script can block the IPs of a given domain using the Windows Firewall.
2. **Unblock IPs**: The script can remove the blocking rules from the firewall and delete the domain data from the database.
3. **Database Management**: The script stores the blocked IPs and their associated domains in a SQLite database.
4. **View Blocked IPs**: The script can display all the domains and their blocked IPs from the database.

## Requirements
- Python 3.x
- `dns.resolver` library (for DNS resolution)
- `sqlite3` (for database management)
- `subprocess` (for executing Windows firewall commands)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/keep-it-halal.git
   ```
2. Install the required dependencies:
   - `dns.resolver` comes with the `dnspython` package, which can be installed with:
     ```bash
     pip install -r requirements.txt
     ```
3. Run the script:
   ```bash
   python keep-it-halal.py
   ```

## Usage
The script will prompt the user with the following options:
1. **Add Domain**: Enter a domain to block all associated IPs.
2. **Delete Domain**: Enter a domain to remove it from the database and unblock all associated IPs.
3. **View all Blocked IPs**: Display all the domains and IPs that have been blocked.
4. **Quit**: Exit the script.

## Commands Breakdown
1. **Add Domain**:
   - Prompts the user to input a domain.
   - Resolves the IPs associated with the domain and adds them to the database.
   - Blocks the IPs using the Windows firewall.
2. **Delete Domain**:
   - Prompts the user to input a domain.
   - Removes the domain and its IPs from the database.
   - Unblocks the IPs by deleting the firewall rules.
3. **View all Blocked IPs**:
   - Displays a list of all blocked domains and their associated IPs.

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init
from threading import Lock
import os
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# Lock for ensuring synchronized output
output_lock = Lock()

# Get the current script's directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Path to the text file containing the ASCII banner (in the same directory)
file_path = os.path.join(current_directory, "SubEnum_banner.txt")

# Define a function for rainbow coloring
def rainbow_text(text):
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    return "".join(colors[i % len(colors)] + char for i, char in enumerate(text))

# Open and read the banner file
try:
    with open(file_path, "r") as file:
        banner = file.read()
except FileNotFoundError:
    print(Fore.RED + f"[-] Banner file '{file_path}' not found.")
    exit()

# Apply rainbow coloring to the banner and print
print(rainbow_text(banner))

# Display the color legend before scanning
print(Fore.MAGENTA + "\n-----------------------------------")
print(Fore.GREEN +   "[+] VALID   - Found a live subdomain (200 OK)")
print(Fore.YELLOW +  "[~] REDIR   - Subdomain redirects (301/302)")
print(Fore.BLUE +    "[~] FORBID  - Access denied (403 Forbidden)")
print(Fore.CYAN +    "[~] OTHER   - Other responses (e.g., 500)")
print(Fore.RED +     "[-] ERROR   - Failed request or network issue")
print(Fore.MAGENTA + "-----------------------------------\n")

# Get user input for the target domain
target_url = input(Fore.CYAN + "[?] Enter the target domain (e.g., example.com): ").strip()

# Read the list of subdomains from the default wordlist
wordlist_path = os.path.join(current_directory, "common_subs.txt")
try:
    with open(wordlist_path, "r") as file:
        subs = file.read().splitlines()
except FileNotFoundError:
    print(Fore.RED + f"[-] Wordlist file '{wordlist_path}' not found.")
    exit()

# Storage for categorized results
valid_results = []
redir_results = []
forbid_results = []
other_results = []
error_results = []

# Adaptive threading based on CPU cores (Modified Part ✅)
max_threads = min(20, os.cpu_count() * 2)

# Function to check subdomain (Modified to include HTTPS checking ✅)
def check_subdomain(sub):
    protocols = ["https://", "http://"]  # Try HTTPS first
    for proto in protocols:
        sub_domain = f"{proto}{sub}.{target_url}"
        try:
            response = requests.get(sub_domain, timeout=5)
            with output_lock:
                if response.status_code == 200:
                    valid_results.append(sub_domain)
                    return Fore.GREEN + f"[+] VALID   | {sub_domain}"
                elif response.status_code in [301, 302]:
                    redir_results.append(sub_domain)
                    return Fore.YELLOW + f"[~] REDIR   | {sub_domain} → {response.headers.get('Location', 'Unknown')}"
                elif response.status_code == 403:
                    forbid_results.append(sub_domain)
                    return Fore.BLUE + f"[~] FORBID  | {sub_domain}"
                elif response.status_code == 404:
                    return None  # Ignore 404s
                else:
                    other_results.append(sub_domain)
                    return Fore.CYAN + f"[~] OTHER   | {sub_domain} ({response.status_code})"
        except requests.ConnectionError:
            error_results.append(sub_domain)
            return Fore.RED + f"[-] ERROR   | {sub_domain} → Connection Error"
        except requests.Timeout:
            error_results.append(sub_domain)
            return Fore.RED + f"[-] ERROR   | {sub_domain} → Timeout"
        except requests.exceptions.RequestException as e:
            error_results.append(sub_domain)
            return Fore.RED + f"[-] ERROR   | {sub_domain} → {e}"
# Use ThreadPoolExecutor with adaptive threading (Modified Part ✅)
print(Fore.MAGENTA + "\n[!] Scanning for subdomains...\n")

total_subs = len(subs)
processed_count = 0

with ThreadPoolExecutor(max_workers=max_threads) as executor:
    future_to_sub = {executor.submit(check_subdomain, sub): sub for sub in subs}
    
    for future in as_completed(future_to_sub):
        result = future.result()
        if result:
            print(result)
        processed_count += 1

print(Fore.BLUE + f"\n[✔] Scan completed! Processed {processed_count}/{total_subs} subdomains.\n")

# Tabulate results excluding invalids (404s)
print(Fore.MAGENTA + "\n[📌] Summary of Results:")
print(Fore.MAGENTA + "------------------------")
print()
if valid_results:
    print(Fore.GREEN + "[+]-----[ VALID ]--------------------------------")
    print()
    print(Fore.GREEN + f"[COUNT : {len(valid_results)}]")
    print()
    for res in valid_results:
        print(Fore.GREEN + f"    {res}")
    print(Fore.GREEN + "[+]-----------------------------------------------")
    print()


if redir_results:
    print(Fore.YELLOW + "[~]-----[ REDIR ]--------------------------------")
    print()
    print(Fore.YELLOW + f"[COUNT : {len(redir_results)}]")
    print()
    for res in redir_results:
        print(Fore.YELLOW + f"    {res}")
    print(Fore.YELLOW + "[~]-----------------------------------------------")
    print()


if forbid_results:
    print(Fore.BLUE + "[~]-----[ FORBID ]-------------------------------")
    print()
    print(Fore.BLUE + f"[COUNT : {len(forbid_results)}]")
    print()
    for res in forbid_results:
        print(Fore.BLUE + f"    {res}")
    print(Fore.BLUE + "[~]-----------------------------------------------")
    print()


if other_results:
    print(Fore.CYAN + "[~]-----[ OTHER ]--------------------------------")
    print()
    print(Fore.CYAN + f"[COUNT : {len(other_results)}]")
    print()
    for res in other_results:
        print(Fore.CYAN + f"    {res}")
    print(Fore.CYAN + "[~]-----------------------------------------------")
    print()


if error_results:  # Modified to display errors in summary ✅
    print(Fore.RED + "[-]-----[ ERRORS ]------------------------------")
    print()
    print(Fore.RED + f"[COUNT : {len(error_results)}]")
    print()
    for res in error_results:
        print(Fore.RED + f"    {res}")
    print(Fore.RED + "[-]-----------------------------------------------")
    print()

# Ask user if they want to save results
save_results = input(Fore.CYAN + "[?] Do you want to save the results to a file? (y/n): ").strip().lower()
if save_results == 'y':
    output_file = os.path.join(current_directory, "SubEnum_results.txt")
    with open(output_file, "a") as f:
        f.write("=================================================\n")
        f.write(f"Domain Name: {target_url}\n")
        f.write(f"Scan time and date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n===[scan results]===\n\n")
        f.write(f"[VALIDS : {len(valid_results)}]\n[REDIRECTS : {len(redir_results)}]\n[FORBIDS : {len(forbid_results)}]\n[OTHERS : {len(other_results)}]\n[ERRORS : {len(error_results)}]\n\n")
        
        f.write("\n[+]-----[ VALID ]--------------------------------\n\n")
        for res in valid_results:
            f.write(f"[+] {res}\n")

        f.write("\n[~]-----[ REDIR ]--------------------------------\n\n")
        for res in redir_results:
            f.write(f"[~] {res}\n")

        f.write("\n[~]-----[ FORBID ]-------------------------------\n\n")
        for res in forbid_results:
            f.write(f"[~] {res}\n")

        f.write("\n[~]-----[ OTHER ]--------------------------------\n\n")
        for res in other_results:
            f.write(f"[~] {res}\n")

        f.write("\n[-]-----[ ERRORS ]------------------------------\n\n")
        for res in error_results:
            f.write(f"[-] {res}\n")
        
        f.write("===============end of results===============\n\n")
    print(Fore.GREEN + f"[✔] Results saved to {output_file}\n")

# Immediate exit to avoid slowdown at the end
input(Fore.CYAN + "\nPress Enter to exit...")

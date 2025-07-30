import sys
import re
from collections import Counter

def analyze_logs(log_file_path):
    successful_logins = 0
    failed_logins = 0
    login_ips = Counter()
    warnings = Counter()
    errors = Counter()

    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                if "Successful login" in line:
                    successful_logins += 1
                    ip_match = re.search(r'IP: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                    if ip_match: 
                        login_ips[ip_match.group(1)] += 1
                elif "Failed login attempt" in line:
                    failed_logins += 1
                    ip_match = re.search(r'IP: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                    if ip_match:
                        login_ips[ip_match.group(1)] += 1
                elif "WARNING" in line:
                    warnings[line.strip()] += 1
                elif "ERROR" in line:
                    errors[line.strip()] += 1

    except FileNotFoundError:
        print(f"Error: Log file not found at {log_file_path}")
        return

    print("--- Log Analysis Report ---")
    print(f"Total Successful Logins: {successful_logins}")
    print(f"Total Failed Logins: {failed_logins}")
    print("\nLogin Attempts by IP:")
    for ip, count in login_ips.most_common():
        print(f"  {ip}: {count}")

    if warnings:
        print("\nWarnings Found:")
        for warning, count in warnings.most_common():
            print(f"  {warning} (Count: {count})")

    if errors:
        print("\nErrors Found:")
        for error, count in errors.most_common():
            print(f"  {error} (Count: {count})")

    print("---------------------------")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <path_to_log_file>")
    else:
        analyze_logs(sys.argv[1])

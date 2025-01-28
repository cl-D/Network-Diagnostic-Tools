import subprocess
import platform
import os
from datetime import datetime

# Function to execute a ping command
def ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "4", host]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except Exception as e:
        return f"Error running ping: {e}"
    
# Function to execute a traceroute command

def traceroute(host):
    command = ["tracert" if platform.system().lower() == "windows" else "traceroute", host]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except Exception as e:
        return f"Error running traceroute: {e}"
    
# Function to log the results to a file
def log_results(file_name, data):
    with open(file_name, "a") as f:
        f.write(data + "\n")

def main():
    # Create template for naming log file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"Network_Diagnostics_{timestamp}.log"

    # Create log file and log file directory
    os.makedirs("Logs", exist_ok=True)
    log_file_path = os.path.join("Logs", log_file)

    print(f"Logging results to {log_file_path}...\n")


    with open("hosts.txt", "r") as f:
        hosts = f.readlines()

        # Iterate through the hosts in the hosts.txt file
        for host in hosts:
            print(f"Testing host: {host.strip()}")
            log_results(log_file_path, f"Diagnostics for {host.strip()} at {datetime.now()}:")

            # Perform ping
            print("Running ping...")
            ping_results = ping(host.strip())
            log_results(log_file_path, "\n PING RESULTS:" + ping_results)

            # Perform tracert
            print("Running traceroute...")
            tracert_results = traceroute(host.strip())
            log_results(log_file_path, "\n TRACERT RESULTS:" + tracert_results)

            log_results(log_file_path, "-" * 50)
    
    print(f"\n Diagnostics complete. Results saved to {log_file_path}.")


if __name__ == "__main__":
    main()
import subprocess
import platform
import os
import concurrent.futures
import time
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
# Function to execute a nslookup command with Google's DNS server   
def dns_lookup_with_server(host, dns_server="8.8.8.8"):
    command = ["nslookup", host, dns_server]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except Exception as e:
        return f"Error running nslookup: {e}"
# Function to execute a nslookup command with local DNS server 
def dns_lookup(host):
    command = ["nslookup", host]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except Exception as e:
        return f"Error running nslookup: {e}"
        
# Function to log the results to a file
def log_results(file_name, data):
    with open(file_name, "a") as f:
        f.write(data + "\n")


def main():
    # Added timer to test how long it takes to run the script
    start_time = time.time()

    # Create template for naming log file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"Network_Diagnostics_{timestamp}.log"

    # Create log file and log file directory
    os.makedirs("Logs", exist_ok=True)
    log_file_path = os.path.join("Logs", log_file)

    print(f"Logging results to {log_file_path}...\n")

    # Opens and reads hosts.txt file which contains hosts that are being tested
    with open("hosts.txt", "r") as f:
        hosts = f.readlines()

    # Creates a ThreadPoolExecutor which runs tasks in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:

        # Dict that stores futures which are tasks that will complete in the future while the program runs
        futures = {}

        # Loops through each host and creates a dict within the futures dict for each host being tested
        # Each host gets a dict of future tasks
        for host in hosts:
            futures[host] = {
                "dns": executor.submit(dns_lookup, host.strip()),
                "dns_server": executor.submit(dns_lookup_with_server, host.strip()),
                "ping": executor.submit(ping, host.strip()),
                "traceroute": executor.submit(traceroute, host.strip())
            }
        
        # Retrieves the results using .result() attribute and stores it
        for host, futures_dict in futures.items():
            dns_results = futures_dict["dns"].result()
            dns_server_results = futures_dict["dns_server"].result()
            ping_results = futures_dict["ping"].result()
            tracert_results = futures_dict["traceroute"].result()

            # Writes the results into a log file
            log_results(log_file_path, f"Diagnostics for {host.strip()} at {datetime.now()}:")
            log_results(log_file_path, "\nNSLOOKUP RESULTS: \n" + dns_results)
            log_results(log_file_path, "\nNSLOOKUP RESULTS WITH GOOGLE DNS SERVER: \n" + dns_server_results)
            log_results(log_file_path, "\nPING RESULTS: \n" + ping_results)
            log_results(log_file_path, "\nTRACEROUTE RESULTS: \n" + tracert_results)
            log_results(log_file_path, "-" * 100)
        
    print(f"\n Diagnostics complete. Results saved to {log_file_path}.")
    end_time = time.time()
    print(end_time-start_time)

if __name__ == "__main__":
    main()
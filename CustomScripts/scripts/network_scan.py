import ipaddress
import socket
import platform
import subprocess
import concurrent.futures
import argparse
import sys

def ping(ip, timeout=1):
    """Return True if host responds to a single ping. Works cross-platform."""
    system = platform.system().lower()
    count_flag = "-n" if system == "windows" else "-c"
    # suppress output
    with open(subprocess.DEVNULL, "wb") as devnull:
        try:
            res = subprocess.run(
                ["ping", count_flag, "1", "-W" if system != "windows" else "-w", str(timeout), str(ip)],
                stdout=devnull,
                stderr=devnull
            )
            return res.returncode == 0
        except Exception:
            return False

def check_port(ip, port=3389, timeout=1.0):
    """Return True if TCP connect to (ip, port) succeeds."""
    try:
        with socket.create_connection((str(ip), port), timeout=timeout):
            return True
    except Exception:
        return False

def try_reverse_dns(ip):
    """Try to resolve hostname, return hostname or None."""
    try:
        name, _, _ = socket.gethostbyaddr(str(ip))
        return name
    except Exception:
        return None

def scan_ip(ip, port=3389, ping_first=False, ping_timeout=1, conn_timeout=1.0):
    """Scan single IP: optionally ping then check port. Return tuple (ip, rdp_open, ping_ok, hostname)."""
    ping_ok = None
    if ping_first:
        ping_ok = ping(ip, timeout=ping_timeout)
        if not ping_ok:
            return (str(ip), False, False, None)

    rdp_open = check_port(ip, port=port, timeout=conn_timeout)
    hostname = try_reverse_dns(ip) if rdp_open else None
    return (str(ip), rdp_open, ping_ok, hostname)

def scan_network(network_cidr, port=3389, workers=100, ping_first=False, ping_timeout=1, conn_timeout=1.0):
    network = ipaddress.ip_network(network_cidr, strict=False)
    hosts = list(network.hosts())
    results = []

    print(f"Scanning {len(hosts)} hosts on {network_cidr} for TCP/{port} (RDP)...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(scan_ip, ip, port, ping_first, ping_timeout, conn_timeout): ip
            for ip in hosts
        }
        try:
            for future in concurrent.futures.as_completed(futures):
                ip = futures[future]
                try:
                    ip_str, rdp_open, ping_ok, hostname = future.result()
                    if rdp_open:
                        results.append({"ip": ip_str, "hostname": hostname or "", "port": port})
                        print(f"✅ RDP open: {ip_str}" + (f" ({hostname})" if hostname else ""))
                except Exception as e:
                    # Keep scanning even if an IP scan failed
                    print(f"error scanning {ip}: {e}")
        except KeyboardInterrupt:
            print("Scan cancelled by user.")
            executor.shutdown(wait=False)
            raise

    print(f"\nScan complete. {len(results)} host(s) with TCP/{port} open.")
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan local subnet for hosts with RDP (TCP/3389) open.")
    parser.add_argument("--subnet", "-s", help="Subnet, e.g. 192.168.1.0/24", default=None)
    parser.add_argument("--workers", "-w", type=int, default=200, help="Number of parallel workers (threads).")
    parser.add_argument("--ping-first", action="store_true", help="Ping hosts before checking port (may be slower and ping may be blocked).")
    parser.add_argument("--port", "-p", type=int, default=3389, help="Port to check (default 3389).")
    parser.add_argument("--conn-timeout", type=float, default=1.0, help="TCP connect timeout in seconds.")
    args = parser.parse_args()

    subnet = args.subnet
    if not subnet:
        subnet = input("Enter your network subnet (e.g. 192.168.1.0/24): ").strip() or "192.168.1.0/24"

    try:
        res = scan_network(
            subnet,
            port=args.port,
            workers=args.workers,
            ping_first=args.ping_first,
            conn_timeout=args.conn_timeout
        )
        if res:
            print("\nHosts that appear to accept RDP connections:")
            for r in res:
                print(f" - {r['ip']}" + (f" ({r['hostname']})" if r['hostname'] else ""))
        else:
            print("No hosts with RDP port open were found.")
    except ValueError as ve:
        print(f"Invalid subnet: {ve}")
        sys.exit(2)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)

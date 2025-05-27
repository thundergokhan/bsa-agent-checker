import socket
import subprocess

def check_port(host, port=4750, timeout=3):
    """Check if the given port is open on the host."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def restart_service_winrm(host, service="RSCD", user=None, password=None):
    """
    Restart a Windows service (requires pywinrm and configured WinRM on the host).
    """
    try:
        import winrm
        s = winrm.Session(host, auth=(user, password))
        r1 = s.run_cmd(f'net stop {service}')
        r2 = s.run_cmd(f'net start {service}')
        return r1.status_code == 0 and r2.status_code == 0, r1.std_out + r2.std_out
    except ImportError:
        return False, b"winrm module not installed"
    except Exception as e:
        return False, str(e).encode()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Check RSCD agent port & restart service via WinRM")
    parser.add_argument("hostfile", help="Path to file with server hostnames/IPs (one per line)")
    parser.add_argument("--user", help="WinRM username for Windows hosts")
    parser.add_argument("--password", help="WinRM password for Windows hosts")
    args = parser.parse_args()

    with open(args.hostfile) as f:
        hosts = [line.strip() for line in f if line.strip()]

    for host in hosts:
        print(f"[{host}] Checking port 4750...", end="")
        if check_port(host):
            print("OPEN")
            if args.user and args.password:
                print(f"[{host}] Attempting to restart RSCD service via WinRM...")
                ok, output = restart_service_winrm(host, user=args.user, password=args.password)
                if ok:
                    print(f"[{host}] ✅ RSCD service restarted successfully.")
                else:
                    print(f"[{host}] ❌ Failed to restart RSCD service. Reason: {output.decode(errors='ignore')}")
        else:
            print("CLOSED or HOST DOWN")

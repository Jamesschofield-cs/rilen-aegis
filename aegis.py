from datetime import datetime
import subprocess
from pathlib import Path
from collections import deque

def write_audit_log(message):
    log_folder = Path(__file__).resolve().parent / "logs"
    log_folder.mkdir(exist_ok=True)
    log_file = log_folder / "aegis.log"

    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

    with log_file.open("a", encoding="utf-8") as log:
        log.write(f"{timestamp} | {message}\n")

def check_firewall():
    # Check Windows Firewall
    firewall = subprocess.run(
        ["powershell", "-Command",
         "Get-NetFirewallProfile | Select-Object Name, Enabled"],
        capture_output=True,
        text=True
    )

    print("WINDOWS FIREWALL")
    print(firewall.stdout)

    if firewall.returncode != 0 or not firewall.stdout.strip():
        return None

    firewall_ok = "False" not in firewall.stdout
    return firewall_ok

def check_defender():

       # Check Microsoft Defender
    defender = subprocess.run(
    ["powershell", "-Command",
    "(Get-MpComputerStatus).AntivirusSignatureLastUpdated.ToString('yyyy-MM-dd HH:mm:ss'); "
    "(Get-MpComputerStatus).AntivirusEnabled; "
    "(Get-MpComputerStatus).RealTimeProtectionEnabled"],
    capture_output=True,
    text=True
    )
     
    print("MICROSOFT DEFENDER")
    print(defender.stdout)

    defender_lines = defender.stdout.strip().splitlines()
    if (
        defender.returncode != 0
        or len(defender_lines) != 3
        or defender_lines[1] not in ("True", "False")
        or defender_lines[2] not in ("True", "False")
    ):
        return None, None

    try:
        signature_time = datetime.strptime(
            defender_lines[0],
            "%Y-%m-%d %H:%M:%S"
        )
    except ValueError:
        return None, None

    antivirus_enabled = defender_lines[1] == "True"
    realtime_enabled = defender_lines[2] == "True"

    defender_ok = antivirus_enabled and realtime_enabled

    signature_age = datetime.now() - signature_time
    signatures_current = signature_age.days <= 2

    return defender_ok, signatures_current

def generate_security_report():

    firewall_ok = check_firewall()
    if firewall_ok is None:
        return "AEGIS security check incomplete. Unable to verify Windows Firewall status."

    defender_ok, signatures_current = check_defender()
    if defender_ok is None or signatures_current is None:
        return "AEGIS security check incomplete. Unable to verify Microsoft Defender status."

        # Create AEGIS report
    if firewall_ok and defender_ok and signatures_current:
        return "AEGIS security check complete. Windows Firewall and Microsoft Defender are active. Defender security intelligence is up to date."

    elif firewall_ok and defender_ok and not signatures_current:
        return "AEGIS security alert. Microsoft Defender is active, but its security intelligence may be out of date."

    elif not firewall_ok and not defender_ok:
        return "AEGIS security alert. Windows Firewall and Microsoft Defender require attention."

    elif not firewall_ok:
        return "AEGIS security alert. One or more Windows Firewall profiles are disabled."

    else:
        return "AEGIS security alert. Microsoft Defender requires attention."

def security_check():
    report = generate_security_report()

    try:
        write_audit_log(report)
    except OSError:
        return report + " Warning: AEGIS could not save the audit log."

    return report

def view_audit_log():
    log_file = Path(__file__).resolve().parent / "logs" / "aegis.log"

    try:
        with log_file.open("r", encoding="utf-8") as log:
            entries = deque(log, maxlen=5)
    except FileNotFoundError:
        return "No AEGIS audit log exists yet. Run a security check first."
    except (OSError, UnicodeError):
        return "AEGIS could not read the audit log."

    recent_entries = "".join(entries).strip()
    if not recent_entries:
        return "The AEGIS audit log is empty. Run a security check first."

    return "Recent AEGIS security checks:\n" + recent_entries
from datetime import datetime
import subprocess

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

    signature_time = datetime.strptime(
    defender_lines[0],
    "%Y-%m-%d %H:%M:%S"
    )

    antivirus_enabled = defender_lines[1] == "True"
    realtime_enabled = defender_lines[2] == "True"

    defender_ok = antivirus_enabled and realtime_enabled

    signature_age = datetime.now() - signature_time
    signatures_current = signature_age.days <= 2

    return defender_ok, signatures_current

def security_check():

    firewall_ok = check_firewall()
    if firewall_ok is None:
        return "AEGIS security check incomplete. Unable to verify Windows Firewall status."

    defender_ok, signatures_current = check_defender()

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
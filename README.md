# RILEN

**Reasoning Intelligence for Learning, Execution & Navigation**
RILEN is a Python-based AI assistant being developed as a practical learning project in artificial intelligence, automation and cybersecurity.

## AEGIS

**Autonomous Executive for Governance, Intelligence & Security**
AEGIS is RILEN's security and governance subsystem. It is being developed to monitor system security, identify potential risks and provide clear security reports.

## Current Features

- Voice command recognition
- Spoken responses using Windows text-to-speech
- Time and date commands
- Windows Firewall status monitoring
- Microsoft Defender status monitoring
- Microsoft Defender security intelligence age checking

## Project Structure


- `hello.py` - Main RILEN voice assistant
- `aegis.py` - AEGIS security checks and reporting

## Security Improvements

- Speech text is passed to PowerShell through standard input, separately
  from the command code. This prevents spoken text from being interpreted
  as PowerShell instructions.
- Manual test: RILEN spoke its greeting and goodbye successfully,
  recognised the exit command, and closed without visible errors.
  - AEGIS reports the security check as incomplete if the firewall command
  fails or returns no output.
- Testing: the live security check completed successfully. A simulated
  command failure produced the expected incomplete-check message without
  changing Windows security settings.
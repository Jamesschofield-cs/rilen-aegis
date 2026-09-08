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
  - AEGIS checks Microsoft Defender command results for failures, missing
  data, unexpected protection values and unreadable update dates.
  Results that cannot be verified produce an incomplete-check message.
- Testing: the live security check completed successfully. Simulated
  Defender command failure and invalid-date results both produced the
  expected incomplete-check message without crashing or changing
  Windows security settings.

## Audit Logging

AEGIS saves security-check reports to `logs/aegis.log`.

- Each entry includes a timestamp with the local time-zone offset.
- New reports are appended, preserving previous entries.
- Generated logs are excluded from Git through `.gitignore`.
- If saving fails, AEGIS returns the security report with a warning.

Testing:

- Two live checks produced two separate timestamped log entries.
- Git confirmed that the generated log is ignored.
- A simulated log-writing failure produced the expected warning.

## Audit Log Viewer

Say "RILEN, show security log" to display the five most recent
audit-log entries in the terminal, with a short spoken confirmation.

- Viewing the log does not run a security check or change the log.
- Missing, empty or unreadable logs produce an explanatory message.
- Entries are displayed oldest to newest within the latest five.

Testing:

- The viewer displayed the two existing security-check entries.
- The voice command displayed the log and spoke its confirmation.
- RILEN exited successfully after the voice test.
- With six simulated entries, the viewer displayed only entries 2–6.

## Automated Tests

Run the tests from the project folder:

```powershell
python -m unittest test_aegis -v
```

The first test verifies that a failed firewall command returns an
unknown result, even when its output appears to show enabled profiles.

The test uses simulated command results and does not run PowerShell
or change Windows security settings.

The second test verifies that empty firewall output returns an unknown
result, even when the command reports success.

The third test verifies that a failed Microsoft Defender command returns
unknown values for protection status and security intelligence freshness,
even when its output contains a valid timestamp and enabled protection states.

The fourth test verifies that a successful firewall command with a disabled
profile returns False.

The fifth test verifies that a successful firewall command with all three
profiles enabled returns True.

The sixth test verifies that a successful Microsoft Defender command with
incomplete output returns unknown values for protection status and security
intelligence freshness.

The seventh test verifies that a successful Microsoft Defender command with
an invalid timestamp returns unknown values for protection status and security
intelligence freshness, even when both protection values are valid.

All seven tests use simulated command results. They do not run PowerShell
or change Windows security settings.

Test result: 7 automated tests passed.
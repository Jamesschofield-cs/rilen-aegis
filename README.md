# RILEN

**Reasoning Intelligence for Learning, Execution & Navigation**
RILEN is a Python-based voice assistant being developed as a practical learning project in artificial intelligence, automation and cybersecurity.

## AEGIS

**Autonomous Executive for Governance, Intelligence & Security**
AEGIS currently performs on-demand Windows Firewall and Microsoft Defender checks and produces a short report. Governance and broader risk analysis are future goals.

## Current Features

- Voice command recognition
- Spoken responses using Windows text-to-speech
- Time and date commands
- On-demand Windows Firewall status checks
- On-demand Microsoft Defender status checks
- Microsoft Defender security intelligence age checking

## Scope and Limitations

This is a Windows learning project, not a complete security audit or a finished product. AEGIS runs checks when requested; it does not continuously monitor the computer. The automated tests use simulated command results and do not prove that every Windows configuration is handled. RILEN does not yet use an LLM.

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

## Running RILEN on Windows

You need Python 3.9 or newer, PowerShell, a working microphone and an internet connection. RILEN uses online speech recognition for voice commands and an online service for weather.

From the project folder, install the Python packages:

```powershell
python -m pip install requests "SpeechRecognition[audio]"
```

Start the assistant:

```powershell
python hello.py
```

Enter your name when prompted. Begin voice commands with “RILEN”; say “RILEN, help” to see the command list. Say “RILEN, exit” to close it.

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

The eighth test verifies that a successful Microsoft Defender command with
an invalid antivirus protection value returns unknown values for protection
status and security intelligence freshness.

The ninth test verifies that Microsoft Defender returns True for both
protection status and security intelligence freshness when both protections
are enabled and the updates are one day old. A fixed clock keeps the test
consistent whenever it runs.

The tenth test verifies that disabled real-time protection returns False for
Defender protection status while one-day-old updates return True for security
intelligence freshness. A fixed clock keeps the test consistent.

The eleventh test verifies that enabled Defender protection returns True while
four-day-old updates return False for security intelligence freshness.
A fixed clock keeps the test consistent.

All eleven tests use simulated command results. They do not run PowerShell
or change Windows security settings.

Test result: 11 automated tests passed.

## Voice Help

Say “RILEN, help” or “RILEN, what can you do” to display the available
commands in the terminal and hear a spoken guide.

Manual verification:
- Both help phrases produced the spoken guide.
- RILEN responded to the exit command with its goodbye.
- Both help phrases displayed the full command list in the terminal.

## Weather Reliability

The weather command now uses a network timeout and handles failed requests,
HTTP errors, and empty responses with explanatory messages.

Speech input uses UTF-8 in Python and PowerShell to support weather symbols
without the previous encoding crash.

Manual verification:
- Weather in Leeds was displayed and spoken successfully.
- A simulated timeout produced the spoken failure message.
- Time and exit commands worked after both weather responses.
- The temporary timeout simulation was removed after testing.
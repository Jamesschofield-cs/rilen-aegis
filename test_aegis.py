import unittest
from subprocess import CompletedProcess
from unittest.mock import patch

import aegis


class TestFirewallChecks(unittest.TestCase):
    def test_failed_firewall_command_returns_unknown(self):
        failed_result = CompletedProcess(
            args=[],
            returncode=1,
            stdout="Domain True\nPrivate True\nPublic True\n",
            stderr="Simulated command failure"
        )

        with patch("aegis.subprocess.run", return_value=failed_result):
            result = aegis.check_firewall()

        self.assertIsNone(result)

    def test_empty_firewall_output_returns_unknown(self):
        empty_result = CompletedProcess(
            args=[],
            returncode=0,
            stdout="",
            stderr=""
        )

        with patch("aegis.subprocess.run", return_value=empty_result):
            result = aegis.check_firewall()

        self.assertIsNone(result)

class TestDefenderChecks(unittest.TestCase):
    def test_failed_defender_command_returns_unknown(self):
        failed_result = CompletedProcess(
            args=[],
            returncode=1,
            stdout="2026-09-07 10:00:00\nTrue\nTrue\n",
            stderr="Simulated command failure"
        )

        with patch("aegis.subprocess.run", return_value=failed_result):
            result = aegis.check_defender()

        self.assertEqual(result, (None, None))

if __name__ == "__main__":
    unittest.main()
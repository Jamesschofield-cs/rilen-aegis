import unittest
from subprocess import CompletedProcess
from unittest.mock import patch
from datetime import datetime

import aegis

class TestFirewallChecks(unittest.TestCase):

    def test_all_firewall_profiles_enabled_returns_true(self):
        enabled_result = CompletedProcess(
            args=[],
            returncode=0,
            stdout="Domain True\nPrivate True\nPublic True\n",
            stderr=""
        )

        with patch("aegis.subprocess.run", return_value=enabled_result):
            result = aegis.check_firewall()

        self.assertIs(result, True)


    def test_disabled_firewall_profile_returns_false(self):
        disabled_result = CompletedProcess(
            args=[],
            returncode=0,
            stdout="Domain True\nPrivate False\nPublic True\n",
            stderr=""
        )

        with patch("aegis.subprocess.run", return_value=disabled_result):
            result = aegis.check_firewall()

        self.assertIs(result, False)

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

    def test_outdated_defender_updates_returns_false(self):
        outdated_result = CompletedProcess(
            args=[],
            returncode=0,
            stdout="2026-09-04 10:00:00\nTrue\nTrue\n",
            stderr=""
        )

        with patch("aegis.subprocess.run", return_value=outdated_result):
            with patch("aegis.datetime", wraps=datetime) as mock_datetime:
                mock_datetime.now.return_value = datetime(2026, 9, 8, 10, 0, 0)
                result = aegis.check_defender()

        self.assertEqual(result, (True, False))


    def test_disabled_defender_protection_returns_false(self):
        disabled_result = CompletedProcess(
            args=[],
            returncode=0,
            stdout="2026-09-07 10:00:00\nTrue\nFalse\n",
            stderr=""
        )

        with patch("aegis.subprocess.run", return_value=disabled_result):
            with patch("aegis.datetime", wraps=datetime) as mock_datetime:
                mock_datetime.now.return_value = datetime(2026, 9, 8, 10, 0, 0)
                result = aegis.check_defender()

        self.assertEqual(result, (False, True))


    def test_healthy_defender_returns_true_values(self):
        healthy_result = CompletedProcess(
            args=[],
            returncode=0,
            stdout="2026-09-07 10:00:00\nTrue\nTrue\n",
            stderr=""
        )

        with patch("aegis.subprocess.run", return_value=healthy_result):
            with patch("aegis.datetime", wraps=datetime) as mock_datetime:
                mock_datetime.now.return_value = datetime(2026, 9, 8, 10, 0, 0)
                result = aegis.check_defender()

        self.assertEqual(result, (True, True))


    def test_invalid_defender_protection_value_returns_unknown(self):
        invalid_protection_result = CompletedProcess(
            args=[],
            returncode=0,
            stdout="2026-09-07 10:00:00\nUnexpected\nTrue\n",
            stderr=""
        )

        with patch("aegis.subprocess.run", return_value=invalid_protection_result):
            result = aegis.check_defender()

        self.assertEqual(result, (None, None))


    def test_invalid_defender_timestamp_returns_unknown(self):
        invalid_date_result = CompletedProcess(
            args=[],
            returncode=0,
            stdout="not-a-date\nTrue\nTrue\n",
            stderr=""
        )

        with patch("aegis.subprocess.run", return_value=invalid_date_result):
            result = aegis.check_defender()

        self.assertEqual(result, (None, None))


    def test_incomplete_defender_output_returns_unknown(self):
        incomplete_result = CompletedProcess(
            args=[],
            returncode=0,
            stdout="2026-09-07 10:00:00\nTrue\n",
            stderr=""
        )

        with patch("aegis.subprocess.run", return_value=incomplete_result):
            result = aegis.check_defender()

        self.assertEqual(result, (None, None))

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
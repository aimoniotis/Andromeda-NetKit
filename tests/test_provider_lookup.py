import unittest
from unittest.mock import patch

from main import NetworkDiagnosticsApp


class ProviderLookupSchedulingTests(unittest.TestCase):
    def test_first_lookup_runs_during_first_15_minutes_after_boot(self):
        app = object.__new__(NetworkDiagnosticsApp)
        app._provider_lookup_running = False
        app._provider_last_checked = 0.0

        with (
            patch("main.time.monotonic", return_value=100),
            patch("main.threading.Thread") as thread,
        ):
            app._schedule_provider_lookup()

        thread.assert_called_once_with(
            target=app._lookup_internet_provider,
            daemon=True,
        )
        thread.return_value.start.assert_called_once_with()
        self.assertTrue(app._provider_lookup_running)

    def test_recent_lookup_remains_throttled(self):
        app = object.__new__(NetworkDiagnosticsApp)
        app._provider_lookup_running = False
        app._provider_last_checked = 100

        with (
            patch("main.time.monotonic", return_value=200),
            patch("main.threading.Thread") as thread,
        ):
            app._schedule_provider_lookup()

        thread.assert_not_called()


if __name__ == "__main__":
    unittest.main()

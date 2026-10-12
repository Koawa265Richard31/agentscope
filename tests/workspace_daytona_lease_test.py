# -*- coding: utf-8 -*-
"""Config surface for the Daytona lease parameters (issue #3277).

Daytona auto-stops a sandbox after 15 minutes of SDK idleness by
default, and ``DaytonaWorkspace`` never exposed any of the SDK's lease
parameters — a long autonomous agent turn loses its sandbox with no
way to raise the limit. These tests verify that ``auto_stop_interval``
and ``ttl_minutes`` are forwarded to the SDK create params when set,
and that unset params leave the SDK defaults in effect.
"""
# pylint: disable=protected-access

import unittest

from agentscope.workspace._daytona._daytona_workspace import DaytonaWorkspace


class TestDaytonaLeaseConfig(unittest.TestCase):
    """Lease parameters forwarded to CreateSandboxFromSnapshotParams."""

    def _create_params(self, **ws_kwargs) -> dict:
        ws = DaytonaWorkspace(**ws_kwargs)
        params = ws._create_params()
        return params

    def test_defaults_omit_lease_params(self) -> None:
        """Unset lease params stay absent — SDK defaults apply."""
        params = self._create_params(workspace_id="wid")
        self.assertNotIn("auto_stop_interval", params)
        self.assertNotIn("ttl_minutes", params)

    def test_auto_stop_interval_is_forwarded(self) -> None:
        """A configured auto_stop_interval reaches the create params."""
        params = self._create_params(
            workspace_id="wid",
            auto_stop_interval=60,
        )
        self.assertEqual(params.auto_stop_interval, 60)

    def test_ttl_minutes_is_forwarded(self) -> None:
        """A configured ttl_minutes reaches the create params."""
        params = self._create_params(workspace_id="wid", ttl_minutes=120)
        self.assertEqual(params.ttl_minutes, 120)

    def test_zero_disables_autostop(self) -> None:
        """``auto_stop_interval=0`` is forwarded (SDK: disables auto-stop)."""
        params = self._create_params(
            workspace_id="wid",
            auto_stop_interval=0,
        )
        self.assertEqual(params.auto_stop_interval, 0)

    def test_labels_and_public_unchanged(self) -> None:
        """The lease wiring does not disturb the existing params."""
        params = self._create_params(workspace_id="wid")
        self.assertEqual(
            params.labels.get("agentscope.workspace.id"),
            "wid",
        )
        self.assertFalse(params.public)


if __name__ == "__main__":
    unittest.main()

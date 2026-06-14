"""
Functional tests for pylearn2 CLI entry points (foundation milestone).

These are target_only tests because the CLI entry points are NEW in this
milestone — the old setup.py was broken and provided no working entry points.
"""

import subprocess
import sys
import os

WORKSPACE_DIR = "/Users/yotamraz/.local/share/modelcode/workspace/jobs/e744fcb5-f287-4ff6-aea5-bc77b06a558e/workspace/pylearn2"
PIXI_BIN = "/Users/yotamraz/.local/share/modelcode/workspace/.pixi/envs/16-target-app-v1/bin"
ENV = {**os.environ, "PYLEARN2_DATA_PATH": "/tmp"}


def run_cli(cmd_name, *args, input_text=None, env=None):
    """Helper to invoke a CLI command and capture output."""
    cmd_path = os.path.join(PIXI_BIN, cmd_name)
    result = subprocess.run(
        [cmd_path, *args],
        cwd=WORKSPACE_DIR,
        capture_output=True,
        text=True,
        timeout=120,
        input=input_text,
        env=env or ENV,
    )
    return result


class TestPylearn2TrainHelp:
    """pylearn2-train --help — CLI entry point"""

    def test_train_help_exits_zero(self):
        result = run_cli("pylearn2-train", "--help")
        assert result.returncode == 0, (
            f"pylearn2-train --help exited {result.returncode}, "
            f"stderr: {result.stderr}"
        )

    def test_train_help_prints_usage(self):
        result = run_cli("pylearn2-train", "--help")
        output = (result.stdout + result.stderr).lower()
        assert "usage" in output or "help" in output or "train" in output, (
            f"Expected usage information in output, got: {result.stdout}"
        )

    def test_train_help_output_is_not_empty(self):
        result = run_cli("pylearn2-train", "--help")
        combined = result.stdout + result.stderr
        assert len(combined.strip()) > 0, "pylearn2-train --help produced no output"


class TestPylearn2PlotMonitorHelp:
    """pylearn2-plot-monitor --help — CLI entry point"""

    def test_plot_monitor_help_exits_zero(self):
        result = run_cli("pylearn2-plot-monitor", "--help")
        assert result.returncode == 0, (
            f"pylearn2-plot-monitor --help exited {result.returncode}, "
            f"stderr: {result.stderr}"
        )

    def test_plot_monitor_help_prints_usage(self):
        result = run_cli("pylearn2-plot-monitor", "--help")
        output = (result.stdout + result.stderr).lower()
        assert "usage" in output or "help" in output or "monitor" in output, (
            f"Expected usage information in output, got: {result.stdout}"
        )


class TestPylearn2PrintMonitorHelp:
    """pylearn2-print-monitor --help — CLI entry point"""

    def test_print_monitor_help_exits_zero(self):
        result = run_cli("pylearn2-print-monitor", "--help")
        assert result.returncode == 0, (
            f"pylearn2-print-monitor --help exited {result.returncode}, "
            f"stderr: {result.stderr}"
        )

    def test_print_monitor_help_prints_usage(self):
        result = run_cli("pylearn2-print-monitor", "--help")
        output = (result.stdout + result.stderr).lower()
        assert "usage" in output or "help" in output or "monitor" in output or "print" in output, (
            f"Expected usage information in output, got: {result.stdout}"
        )

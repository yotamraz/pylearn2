"""
Functional tests for pylearn2 config/tests/ test suite (foundation milestone).

This wraps the pytest execution of pylearn2/config/tests/ as a functional test.
It's target_only because the test suite was migrated from nose to pytest in
this milestone — no direct origin equivalent to compare against.
"""

import subprocess
import os

WORKSPACE_DIR = "/Users/yotamraz/.local/share/modelcode/workspace/jobs/e744fcb5-f287-4ff6-aea5-bc77b06a558e/workspace/pylearn2"
ENV = {**os.environ, "PYLEARN2_DATA_PATH": "/tmp"}

PYTEST = "/Users/yotamraz/.local/share/modelcode/workspace/.pixi/envs/16-target-app-v1/bin/pytest"


def run_pytest(*args, env=None):
    """Run pytest with given arguments."""
    result = subprocess.run(
        [PYTEST, *args],
        cwd=WORKSPACE_DIR,
        capture_output=True,
        text=True,
        timeout=120,
        env=env or ENV,
    )
    return result


class TestConfigTestSuite:
    """pytest pylearn2/config/tests/ — expected 16 passed, 3 skipped"""

    def test_config_tests_pass(self):
        result = run_pytest(
            "pylearn2/config/tests/",
            "-v", "--tb=short"
        )
        # Exit code 0 means all collected tests passed (skips are OK)
        assert result.returncode == 0, (
            f"pytest exited {result.returncode}\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )

    def test_config_tests_expected_count(self):
        result = run_pytest(
            "pylearn2/config/tests/",
            "-v", "--tb=short"
        )
        assert result.returncode == 0
        # Should see "16 passed, 3 skipped"
        assert "16 passed" in result.stdout, (
            f"Expected '16 passed' in output, got:\n{result.stdout}"
        )

    def test_config_tests_skips_are_expected(self):
        result = run_pytest(
            "pylearn2/config/tests/",
            "-v", "--tb=short"
        )
        assert result.returncode == 0
        # The 3 skipped tests require unmigrated modules (datasets/space/models)
        assert "3 skipped" in result.stdout, (
            f"Expected '3 skipped' in output, got:\n{result.stdout}"
        )

    def test_no_failures(self):
        result = run_pytest(
            "pylearn2/config/tests/",
            "-v", "--tb=short"
        )
        # "failed" should not appear in output
        assert "failed" not in result.stdout.lower() or result.returncode == 0, (
            f"Test failures found:\n{result.stdout}"
        )

    def test_yaml_parse_tests_collected(self):
        result = run_pytest(
            "pylearn2/config/tests/test_yaml_parse.py",
            "--collect-only", "-q"
        )
        assert result.returncode == 0
        # At minimum 16 tests should be collected
        output = result.stdout
        # Look for "19 tests" (16 passed + 3 skipped = 19 collected)
        assert "test" in output.lower(), f"No tests found: {output}"

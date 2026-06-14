"""
Functional tests for pylearn2 core module imports (foundation milestone).

These are origin_and_target tests: the modules existed at baseline (master)
but used theano.compat.six imports; the target migrated them to native
Python 3. We verify they are still importable and export the same symbols.
"""

import subprocess
import os

WORKSPACE_DIR = "/Users/yotamraz/.local/share/modelcode/workspace/jobs/e744fcb5-f287-4ff6-aea5-bc77b06a558e/workspace/pylearn2"
ENV = {**os.environ, "PYLEARN2_DATA_PATH": "/tmp"}

PYTHON = "/Users/yotamraz/.local/share/modelcode/workspace/.pixi/envs/16-target-app-v1/bin/python3.12"


def run_python(code, env=None, timeout=120):
    """Run a Python snippet and return the result."""
    result = subprocess.run(
        [PYTHON, "-c", code],
        cwd=WORKSPACE_DIR,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env or ENV,
    )
    return result


class TestCompatModule:
    """pylearn2.compat — OrderedDict, first_key, first_value exports"""

    def test_import_ordereddict(self):
        result = run_python(
            "from pylearn2.compat import OrderedDict; "
            "d = OrderedDict([('a', 1)]); print('OK:', type(d).__name__)"
        )
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "OK: OrderedDict" in result.stdout

    def test_import_first_key(self):
        result = run_python(
            "from pylearn2.compat import first_key; "
            "d = {'x': 10, 'y': 20}; k = first_key(d); print('OK:', k)"
        )
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "OK: x" in result.stdout

    def test_import_first_value(self):
        result = run_python(
            "from pylearn2.compat import first_value; "
            "d = {'x': 10}; v = first_value(d); print('OK:', v)"
        )
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "OK: 10" in result.stdout

    def test_all_exports_present(self):
        result = run_python(
            "from pylearn2.compat import OrderedDict, first_key, first_value; "
            "print('ALL_OK')"
        )
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "ALL_OK" in result.stdout


class TestYamlParseModule:
    """pylearn2.config.yaml_parse — load, load_path exports"""

    def test_import_load(self):
        result = run_python(
            "from pylearn2.config.yaml_parse import load; print('OK')"
        )
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "OK" in result.stdout

    def test_import_load_path(self):
        result = run_python(
            "from pylearn2.config.yaml_parse import load_path; print('OK')"
        )
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "OK" in result.stdout

    def test_yaml_round_trip_obj(self):
        result = run_python(
            "from pylearn2.config.yaml_parse import load; "
            "from decimal import Decimal; "
            "result = load(\"a: !obj:decimal.Decimal { value: '1.23' }\"); "
            "assert isinstance(result['a'], Decimal), 'Expected Decimal, got: ' + str(type(result['a'])); "
            "print('OK:', result['a'])"
        )
        assert result.returncode == 0, f"YAML round-trip failed: {result.stderr}"
        assert "OK: 1.23" in result.stdout

    def test_yaml_load_simple(self):
        result = run_python(
            "from pylearn2.config.yaml_parse import load; "
            "result = load('a: 23'); "
            "assert result['a'] == 23; "
            "print('OK:', result['a'])"
        )
        assert result.returncode == 0, f"YAML simple load failed: {result.stderr}"
        assert "OK: 23" in result.stdout

    def test_yaml_load_import_tag(self):
        result = run_python(
            "from pylearn2.config.yaml_parse import load; "
            "from decimal import Decimal; "
            "result = load(\"a: !import 'decimal.Decimal'\"); "
            "assert result['a'] == Decimal; "
            "print('OK')"
        )
        assert result.returncode == 0, f"YAML import tag failed: {result.stderr}"
        assert "OK" in result.stdout


class TestSerialModule:
    """pylearn2.utils.serial — importable and load/save available"""

    def test_import_serial(self):
        result = run_python(
            "from pylearn2.utils import serial; print('OK')"
        )
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "OK" in result.stdout

    def test_import_serial_load(self):
        result = run_python(
            "from pylearn2.utils.serial import load; print('OK')"
        )
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "OK" in result.stdout

    def test_import_serial_save(self):
        result = run_python(
            "from pylearn2.utils.serial import save; print('OK')"
        )
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "OK" in result.stdout

    def test_serial_round_trip(self):
        result = run_python(
            "import tempfile, os; "
            "from pylearn2.utils import serial; "
            "fd, fname = tempfile.mkstemp(); os.close(fd); "
            "serial.save(fname, {'key': 42}); "
            "loaded = serial.load(fname); "
            "os.remove(fname); "
            "assert loaded['key'] == 42; "
            "print('OK:', loaded['key'])"
        )
        assert result.returncode == 0, f"Serial round-trip failed: {result.stderr}"
        assert "OK: 42" in result.stdout


class TestSkipModule:
    """pylearn2.testing.skip — skip helpers importable"""

    def test_import_skip_if_no_scipy(self):
        result = run_python(
            "from pylearn2.testing.skip import skip_if_no_scipy; print('OK')"
        )
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "OK" in result.stdout

    def test_skip_if_no_scipy_callable(self):
        result = run_python(
            "from pylearn2.testing.skip import skip_if_no_scipy; "
            "assert callable(skip_if_no_scipy); print('OK')"
        )
        assert result.returncode == 0, f"Failed: {result.stderr}"
        assert "OK" in result.stdout

    def test_import_all_skip_helpers(self):
        result = run_python(
            "from pylearn2.testing.skip import ("
            "    skip_if_no_scipy, skip_if_no_sklearn, skip_if_no_h5py, "
            "    skip_if_no_matplotlib, skip_if_no_data"
            "); print('ALL_OK')"
        )
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "ALL_OK" in result.stdout


class TestExcModule:
    """pylearn2.utils.exc — reraise_as importable"""

    def test_import_reraise_as(self):
        result = run_python(
            "from pylearn2.utils.exc import reraise_as; print('OK')"
        )
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "OK" in result.stdout

    def test_reraise_as_works(self):
        # Write a temp script to avoid multi-line -c issues
        import tempfile
        script = (
            "from pylearn2.utils.exc import reraise_as\n"
            "try:\n"
            "    try:\n"
            "        raise ValueError('original')\n"
            "    except ValueError:\n"
            "        reraise_as(RuntimeError('new error'))\n"
            "except RuntimeError as e:\n"
            "    print('OK:', str(e))\n"
        )
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(script)
            tmp_path = f.name
        try:
            import subprocess as sp
            res = sp.run([PYTHON, tmp_path], capture_output=True, text=True,
                         timeout=15, env=ENV, cwd=WORKSPACE_DIR)
        finally:
            import os as _os
            _os.unlink(tmp_path)
        assert res.returncode == 0, f"reraise_as failed: {res.stderr}"
        assert "OK: new error" in res.stdout

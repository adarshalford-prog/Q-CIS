"""Requirement 10: every documented experiment command must actually run.

This is a *smoke test* of the command-line entry points, on a deliberately tiny
configuration (2 families, 1 seed, few epochs). It proves the plumbing works and
that the exit codes are meaningful. It is not a reproduction of the full research
run; ``scripts/run_reproduction.py --all`` is what performs that.
"""

import json
import os
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="module")
def tiny_config(tmp_path_factory):
    cfg = {
        "base_seed": 20261116,
        "families": ["xor", "moons"],
        "mechanisms": ["incoherent", "trained_phase"],
        "seeds": [0],
        "model": {"n_states_per_class": 3, "dim": 2, "epochs": 20, "lr": 0.05},
        "split": {"test_frac": 0.3},
        "cv": {"n_splits": 3},
        "statistics": {"n_boot": 500},
        "baselines": ["nearest_centroid"],
    }
    p = tmp_path_factory.mktemp("cfg") / "tiny.json"
    p.write_text(json.dumps(cfg))
    return str(p)


def _run(args, cwd=ROOT):
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([os.path.join(ROOT, "src"), ROOT])
    return subprocess.run([sys.executable] + args, cwd=cwd, env=env,
                          capture_output=True, text=True)


def test_benchmark_command_runs(tiny_config, tmp_path):
    out = tmp_path / "fits.csv"
    r = _run(["experiments/run_benchmark.py", "--config", tiny_config,
              "--out", str(out), "--quiet"])
    assert r.returncode == 0, r.stderr
    assert out.exists()
    lines = out.read_text().strip().splitlines()
    assert len(lines) == 1 + 2 * (2 * 1 + 1)   # header + families*(mechs*seeds + baselines)


def test_benchmark_refuses_to_overwrite(tiny_config, tmp_path):
    out = tmp_path / "fits.csv"
    assert _run(["experiments/run_benchmark.py", "--config", tiny_config,
                 "--out", str(out), "--quiet"]).returncode == 0
    r = _run(["experiments/run_benchmark.py", "--config", tiny_config,
              "--out", str(out), "--quiet"])
    assert r.returncode != 0
    assert "refusing to overwrite" in (r.stderr + r.stdout)


def test_audit_command_runs(tiny_config, tmp_path):
    fits = tmp_path / "fits.csv"
    summ = tmp_path / "summ"
    assert _run(["experiments/run_benchmark.py", "--config", tiny_config,
                 "--out", str(fits), "--quiet"]).returncode == 0
    r = _run(["analysis/audit.py", "--fits", str(fits), "--outdir", str(summ), "--n-boot", "200"])
    assert r.returncode == 0, r.stderr
    assert (summ / "audit.json").exists()
    assert (summ / "summary.md").exists()
    data = json.loads((summ / "audit.json").read_text())
    assert data["n_families"] == 2
    assert "unit" in data


def test_verify_results_detects_a_mismatch(tiny_config, tmp_path):
    fits = tmp_path / "fits.csv"
    assert _run(["experiments/run_benchmark.py", "--config", tiny_config,
                 "--out", str(fits), "--quiet"]).returncode == 0

    # matching file -> pass
    ref = tmp_path / "ref.csv"
    ref.write_text(fits.read_text())
    assert _run(["scripts/verify_results.py", "--actual", str(fits),
                 "--reference", str(ref)]).returncode == 0

    # perturbed file -> fail
    bad = tmp_path / "bad.csv"
    text = fits.read_text().replace("0.5", "0.4", 1)
    bad.write_text(text if text != fits.read_text() else fits.read_text() + "\n")
    r = _run(["scripts/verify_results.py", "--actual", str(bad), "--reference", str(ref)])
    assert r.returncode != 0


def test_reproduction_script_exists_and_is_documented():
    p = os.path.join(ROOT, "scripts", "run_reproduction.py")
    assert os.path.exists(p)
    text = open(p, encoding="utf-8").read()
    assert "run_reproduction.py --all" in text

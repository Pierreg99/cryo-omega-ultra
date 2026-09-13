"""Doctor hard/soft contract."""
from ultra import doctor


def test_hard_ok_structure():
    checks = doctor.run(seed_data=True)
    assert checks
    assert all(len(row) == 4 for row in checks)
    names = {n for n, *_ in checks}
    assert "python" in names
    assert "skills" in doctor.SOFT


def test_hard_ok_true_when_core_present():
    checks = doctor.run(seed_data=True)
    # python/root/ide/data-dir/registry/git should pass in this workspace
    hard = [(n, ok) for n, ok, _note, hard in checks if hard]
    assert all(ok for n, ok in hard if n in {"python", "root", "ide", "data-dir", "registry"})

"""Experiment package.

The algorithm sources live in ``H-MCMC-FMP_algo/``. That name cannot be imported
(hyphens), so this module registers it as ``hpo_rl`` before any experiment code
loads the optimizer.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
from pathlib import Path

_ALGO_DIR = Path(__file__).resolve().parents[1] / "H-MCMC-FMP_algo"
_PKG = "hpo_rl"


class _HMcmcFmpAlgoFinder:
    """Load ``hpo_rl`` and its submodules from ``H-MCMC-FMP_algo/``."""

    is_h_mcmc_fmp_algo = True

    def find_spec(self, fullname, path, target=None):
        if fullname != _PKG and not fullname.startswith(_PKG + "."):
            return None
        if not _ALGO_DIR.is_dir():
            return None
        rel = fullname.split(".")[1:]
        base = _ALGO_DIR.joinpath(*rel) if rel else _ALGO_DIR
        init = base / "__init__.py"
        if init.is_file():
            return importlib.util.spec_from_file_location(
                fullname,
                init,
                loader=importlib.machinery.SourceFileLoader(fullname, str(init)),
                submodule_search_locations=[str(base)],
            )
        module_file = base.with_suffix(".py")
        if module_file.is_file():
            return importlib.util.spec_from_file_location(
                fullname,
                module_file,
                loader=importlib.machinery.SourceFileLoader(fullname, str(module_file)),
            )
        return None


def _install() -> None:
    if any(getattr(finder, "is_h_mcmc_fmp_algo", False) for finder in sys.meta_path):
        return
    sys.meta_path.insert(0, _HMcmcFmpAlgoFinder())


_install()

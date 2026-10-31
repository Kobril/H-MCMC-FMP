# H-MCMC-FMP

Hyperparameter optimization by Metropolis search with an HMM regime controller, factorized mixture proposals (FMP), and an optional DREAM(ZS) crossover kernel. Every reported variant is a configuration of one class, `HMM_MCMC_FMP`.

Python 3.11 or newer. The experiment stack is tested on 3.11 and 3.12.

## Layout

```
H-MCMC-FMP_algo/     algorithm source
experiments_new/     runners, analysis, and configs
pyproject.toml       package metadata
requirements.txt     experiment dependencies
```

`H-MCMC-FMP_algo/` is not a legal Python import name, so the package is imported as `hpo_rl`. `pyproject.toml` maps that name onto the folder, and importing `experiments_new` registers the same mapping when you run from the source tree.

```python
from hpo_rl.baselines import HMM_MCMC_FMP
from hpo_rl.backends import OptimizationBenchmarkBackend
```

`HMM_MCMC_FMP(objective, budget, space, seed=...)` minimizes `objective`. `seed` routes every draw, including the Sobol initial design, through `numpy.random.default_rng`.

## Install

Algorithm only (numpy and scipy):

```
pip install -e .
```

Experiments, from the repository root:

```
powershell -ExecutionPolicy Bypass -File experiments_new\setup_env.ps1
bash experiments_new/setup_env.sh
```

The script creates `.venv`, installs `requirements.txt`, installs `yahpo-gym` without its outdated dependency pins, installs this package, and clones the LCBench YAHPO surrogate data into `yahpo_data/` when it is missing. Set `PYTHON` to a 3.11 or 3.12 interpreter before running the script if `python` is something else.

SMAC has no Windows build. On Linux or WSL, `experiments_new/setup_env.sh` can install it. From Windows, build the image and mount the repo:

```
docker build -f experiments_new/docker/Dockerfile.smac -t hpo-smac .
docker run --rm -v "${PWD}:/work" -w /work hpo-smac python experiments_new/lcbench/run.py --methods SMAC --workers 4 --fmp-config tuned --baseline-config tuned
```

## Experiments

Run every command from the repository root. Each runner is resumable: a second launch skips finished jobs. Results land in `experiments_new/<exp>/results/<task>/<method>/seed_XXX.json`.

```
python experiments_new/lcbench/select_instances.py
python experiments_new/<exp>/run.py --dry-run
python experiments_new/<exp>/run.py --smoke
python experiments_new/<exp>/run.py --workers 10 --fmp-config tuned --baseline-config tuned
python experiments_new/<exp>/analyze.py
```

`--fmp-config table5` uses the class defaults. `--fmp-config tuned` reads `experiments_new/configs/fmp_tuned.json`. Baseline sampler settings come from `configs/baselines_default.json` or `configs/baselines_tuned.json`.

| folder | what it runs |
|---|---|
| `tuning_heldout/` | shared config per method on held-out LCBench instances |
| `synt_functions/` | synthetic benchmarks |
| `lcbench/` | LCBench surrogate tasks |
| `rbv2/` | rbv2_super (SVM, XGBoost) |
| `ablation_ladder/` | single-factor ladder from the paper FMP arm to DREAM |
| `ablation_controller/` | HMM controller against fixed, random, and rule-based controllers |
| `diagnostics/` | state trajectories, emission histograms, Baum-Welch traces |
| `sensitivity/` | one-at-a-time knobs and random configs |
| `paper/` | tables and figures from stored results |

FMP variants (`FMP`, `FMP_DREAM`, `L1_K1_VITERBI_SUB` … `L5_DREAM`, `CTRL_*`) are presets in `experiments_new/common/methods.py`. Baselines are Optuna `RS`, `TPE`, `GP`, and `CMAES`, plus `TPE_HB` on LCBench and `SMAC` off Windows.

# Scenarios for India's Economic Future

The Anthropic Institute's model of how AI changes an economy ("[Scenarios for our Economic Future](https://www.anthropic.com/institute/econ-scenarios)", Korinek, Jones, Sacher, Cotter and McCrory, September 2026), re-run on India.

Same model. Same assumptions about AI. India's economy.

**Live site:** <https://india-ai-economic-scenarios.vercel.app>
**Source:** <https://github.com/Sidgit11/india-ai-economic-scenarios>

The site is the single `index.html` at the repo root — a static page, no build step.

## Headline results, 2030

| | Modest | Substantial | Extreme | US extreme (paper) |
|---|---|---|---|---|
| GDP, % above the no-AI path | +0.6 | +3.0 | +9.3 | +32.4 |
| GDP growth in 2030 (6.5% without AI) | 6.7% | 8.0% | 10.8% | 15.4% (2% base) |
| Cognitive (office and professional) workers unemployed | 6.9% | 9.6% | 26.2% | 17.9% |
| All workers unemployed | 4.3% | 4.5% | 7.6% | 11.9% |
| Cognitive wage vs the no-AI path | −0.5% | −5.0% | −27.8% | −11.5% |
| Wage in all other work vs the no-AI path | +0.5% | +2.3% | +10.0% | +33.6% |
| Labour share of income (53% today) | 52.8% | 51.7% | 48.3% | 45.2% (60% base) |

The one-line finding: India's macro upside from AI is about a third of the US figure, because only 23% of Indian workers do the office and professional work the model lets AI touch (62% in the US). But those workers are hit harder than their US counterparts, because a 9% larger economy cannot re-absorb them into the office work that survives the way a 32% larger economy can.

## What is in this repo

```
index.html              The page: findings, charts, and the interactive scenario explorer
docs/METHODOLOGY.md     What the model is, what we kept, what we changed, how we validated it
docs/CALIBRATION.md     Every India input, its value, and its source
docs/RESULTS.md         Full results tables, India and US, plus sensitivities
docs/SOURCES.md         All sources with links
model/model.py          Re-implementation of the paper's model (Appendix A, Table A.1)
model/india.py          India calibration, scenarios and sensitivity runs
model/grid.py           Precomputes the 4,375 explorer combinations
results/india_results.json   Scenario outputs, monthly paths, reallocation numbers
results/grid.json            Explorer lookup table
```

## Run it yourself

```bash
cd model
pip install -r requirements.txt
python3 model.py      # replicates the paper's US Table 3 (takes ~5 seconds)
python3 india.py      # runs India base scenarios and all sensitivities
python3 grid.py       # rebuilds the explorer grid (~3 minutes on 2 cores)
```

`model.py` with default parameters reproduces every line of the paper's Table 3 to within 0.1 percentage points. That check is the first thing a reviewer should run.

## How to review this

1. **Is the model right?** Read `docs/METHODOLOGY.md` and compare `model/model.py` with Appendix A of the [technical report](https://www-cdn.anthropic.com/files/4zrzovbb/website/cf58f84d46a4a76bf5a5b039ac695fba6b80041c.pdf). Run `python3 model.py` and check it against the paper's Table 3.
2. **Are the India inputs right?** Every number is in `docs/CALIBRATION.md` with its source. The two we are least sure of are the monthly job-finding rate and the split of unemployment between the two groups; the sensitivity table in `docs/RESULTS.md` shows neither moves the headline results much.
3. **Is the interpretation fair?** The page's "Six things the model cannot see" section is ours, not the model's. Push back on it in an issue.

Issues and pull requests are welcome, especially better Indian data for any input.

## Licence

Code: MIT. Text, charts and data tables in this repo: CC BY 4.0. The underlying model and its US calibration belong to the Anthropic Institute and are used here with attribution; this project is not affiliated with or endorsed by Anthropic.

## Deploy

Static site, no build. On Vercel: import the repo, framework preset "Other", leave build and output settings empty. `vercel.json` is already there.

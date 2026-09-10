# Methodology

## The model, in brief

The framework is from Korinek, Jones, Sacher, Cotter and McCrory (2026), *Economic Scenarios for Transformative AI*, Anthropic Institute Working Paper 2026-02. We re-implemented it from the paper's equations (Sections 2 and 3, Appendix A and Table A.1). Nothing in the model's structure was changed.

The pieces:

- **Production.** Output is a CES aggregate over task instances with elasticity σ = 0.5 (tasks are gross complements). Each instance is done by labour or by capital, whichever is cheaper. AI arrives instance by instance: on an affected task, a diffusion share *d* of instances is done with AI, each with a log cost saving *a*; a share ψ of those is automated (moves to capital) and 1 − ψ is augmented (stays with a worker). New labour tasks are created at ratio ρ per automated task.
- **Two groups of workers.** Cognitive occupations (management, professional, sales, office) are the only ones AI can affect. All other occupations are unaffected. Workers are homogeneous within a group.
- **Capital.** Supplied along an upward-sloping schedule with elasticity ε = 3, so part of the productivity gain accrues to capital as a higher rental rate.
- **Ideas.** A semi-endogenous growth block in which a larger GDP funds more research. Its effect by 2030 is small (under 1% of GDP in every scenario).
- **Labour market.** A monthly search-and-matching block. Displaced cognitive workers enter an unemployment pool and search in both groups, with a discount μ on cross-group search. The cognitive wage is sticky (a gap to its clearing level closes by half each year), so part of the adjustment happens through layoffs rather than wages. Expanding occupations post vacancies for a fraction θ_H of their shortfall each month.

A scenario is a path for five AI objects (affected task mass *m*, diffusion *d*, gain *a*, automation share ψ, reinstatement ρ) plus two labour-market frictions (μ, θ_H). The affected mass and diffusion follow logistic paths anchored at mid-2026 measurements and reaching scenario values in 2030.

## Validation

`model/model.py` with its default (US) parameters reproduces the paper's Table 3:

| | Paper | Ours |
|---|---|---|
| GDP above no-AI, modest / substantial / extreme | 1.6 / 8.3 / 32.4 | 1.6 / 8.3 / 32.4 |
| Cognitive unemployment, % | 2.9 / 4.5 / 17.9 | 2.9 / 4.5 / 17.8 |
| All unemployment, % | 3.9 / 4.6 / 11.9 | 3.9 / 4.5 / 11.8 |
| Cognitive wage, % | 0.4 / −0.3 / −11.5 | 0.4 / −0.3 / −11.4 |
| Labour share, % | 59.4 / 56.1 / 45.2 | 59.4 / 56.1 / 45.2 |

All 17 rows of the table match to within 0.1 percentage points across all three scenarios (see `docs/RESULTS.md`). The steady-state labour market also matches: the unemployment pool splits 1.74 / 2.06 (paper: 1.76 / 2.08) and matching efficiency χ = 0.766 (paper: 0.76).

## What we kept

Everything that describes AI:

- σ = 0.5, ε = 3, wage rigidity ξ = 0.5, matching curvature, filling rate, quit-response share, normal-times search discount μ̄ = 0.17.
- The 2030 scenario values of diffusion (0.2 / 0.4 / 0.6), gain (0.30 / 0.45 / 0.80), automation share (0.5 / 0.75 / 0.9), reinstatement (0.5 / 0.25 / 0), search discount (0.17 / 0.08 / 0.04) and posting speed (0.10 / 0.25 / 0.50).
- The within-cognitive AI exposure measured in mid-2026 (0.22 of cognitive task time).
- The ideas-block parameters (λ = 1, fishing-out 3.1).

## What we changed

Only measured facts about the economy. See `docs/CALIBRATION.md` for values and sources.

- Share of workers in cognitive occupations: 23.0% (India, PLFS 2025) instead of 62.4% (US, CPS 2025). This also sets the ceiling on the affected task mass.
- Labour share of income: 0.53 instead of 0.60.
- Growth without AI: output per worker 5.0% and labour force 1.5% (GDP 6.5%) instead of 1.67% and 0.33% (GDP 2%).
- Capital-output ratio 3.0 instead of 3.5 (which only affects the reported level of the net return).
- Normal unemployment pool 4.3% instead of 3.8%, split so that cognitive-origin unemployment (6.6%) exceeds other-origin (3.6%), the reverse of the US pattern.
- Monthly job-finding rate 0.15 instead of 0.23, which implies a quit rate of 8% a year instead of 11%.
- Mid-2026 anchors: affected mass 0.051 (= 0.22 × 0.23) instead of 0.14; diffusion 0.05 instead of 0.10.

**Scaling the 2030 affected mass.** The paper's scenarios set the 2030 affected mass at 0.2 / 0.3 / 0.5 of all tasks, against a ceiling of 0.624 (all cognitive work). We keep the *fraction of cognitive work affected* the same: 32% / 48% / 80%, applied to India's ceiling of 0.23, giving 0.074 / 0.111 / 0.184. This is what "same AI, different economy" means operationally.

## Why India's cognitive workers fare worse

This is the result most worth checking. In the model the target for cognitive employment is the surviving cognitive task mass times a demand term that rises with output:

ℓ*_C / ℓ_C0 = (surviving share of cognitive tasks) × exp(Δln Y − σ Δln w)

The surviving share is the same in both countries by construction (same fraction of cognitive work automated). The demand term is not: in the US extreme scenario Δln Y ≈ 0.28, in India ≈ 0.09, because India's exposed base is a third the size. So the US gets a ~26% demand lift on surviving cognitive work against a ~7% lift in India. The task loss is the same; the offset is a quarter as large. The result is a deeper fall in cognitive employment and, with the same wage rigidity, a deeper fall in the cognitive wage.

The first-order version is equation (19) of the paper: ℓ̃_C ≈ −(s_N / s_C) ℓ̃_N. With s_N / s_C = 3.3 in India against 0.6 in the US, a given rise in other-group demand pulls proportionally far more out of the cognitive group.

This holds at every capital elasticity (see the ε = ∞ row in the sensitivity table), so it is structural, not a capital-market artefact.

## Heads versus pay

The paper measures the cognitive share by employment (heads) but defines task masses by labour payments. In the US the two are close. In India cognitive workers earn roughly twice what others earn, so their share of the wage bill (about 35%) is well above their share of heads (23%). The model cannot hold both at once because workers are homogeneous within a group. We use heads as the base, following the paper's method, and report the pay-weighted variant (which raises the macro numbers by about half) as a sensitivity. The truth is between them.

## The explorer

`model/grid.py` runs the India model on every combination of the page's five questions (5 × 5 × 5 × 5 × 7 = 4,375 runs). Question answers map to parameters as follows:

| Question | Parameter | Answer values |
|---|---|---|
| Share of office work AI can do by 2030 | fraction of cognitive work affected → m₂₀₃₀ = f × 0.23 | 0.20, 0.32, 0.48, 0.80, 0.95 |
| Share actually done with AI | d₂₀₃₀ | 0.10, 0.20, 0.40, 0.60, 0.80 |
| How much AI does by itself | ψ | 0.10, 0.30, 0.50, 0.75, 0.90 |
| Productivity gain on a task | a₂₀₃₀ (log) | 0.10, 0.41, 0.69, 1.39, 2.30 (≈ same, 1.5×, 2×, 4×, 10×) |
| Time to find a new job | μ | 0.60, 0.35, 0.17, 0.10, 0.08, 0.04, 0.02 |

As in the paper's survey exercise, ρ = 0.25, θ_H = 0.25, ξ = 0.5 and ε = 3 are held at their substantial-scenario values. The gain path starts at min(0.35, a₂₀₃₀) in mid-2026 and moves linearly to a₂₀₃₀.

## Limits

The paper's own caveats apply in full: no business cycles, no demand feedback from displacement, no policy response, no robotics, no catastrophic risks, and only two worker types. For India, add: no earnings gap between the groups (so no pay cut on crossing over), a closed economy (so no exported cognitive work and no foreign-owned AI capital), no informal sector, and no agricultural productivity dynamics. These are scenarios, not forecasts.

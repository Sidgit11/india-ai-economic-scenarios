# Calibration

Every input to the India run, with its value, the paper's US value, and the source. Inputs marked **kept** are the paper's and were not changed.

## A. Structure, common to the scenarios

| Symbol | Meaning | India | US (paper) | Basis for the India value |
|---|---|---|---|---|
| σ | Elasticity of substitution across tasks | 0.5 | 0.5 | Kept |
| s_L | Base-period labour share of income | 0.53 | 0.60 | Penn World Table 11, `labsh` for India (0.533, 2019–23), via [FRED](https://fred.stlouisfed.org/series/LABSHPINA156NRUG). PWT imputes the labour share of self-employed mixed income. |
| s_C / s_L | Cognitive share of employment | 0.230 | 0.624 | PLFS 2025 via [ILOSTAT](https://ilostat.ilo.org/data/), ISCO-08: managers 2.81%, professionals 5.85%, technicians 2.65%, clerical 2.32%, sales workers (52) 9.41%. This mirrors the paper's SOC groups 11–29, 41, 43. Total employed 476.6 million. |
| ε | Elasticity of capital supply | 3 | 3 | Kept. ε = 1 and ∞ in sensitivities. |
| K/Y; r̄; δ | Capital-output ratio; gross rental rate; depreciation | 3.0; 0.157; 0.05 | 3.5; 0.115; 0.05 | GFCF ≈ 31% of GDP ([World Bank](https://tradingeconomics.com/india/gross-fixed-capital-formation-percent-of-gdp-wb-data.html), NSO) over trend growth plus depreciation gives K/Y ≈ 2.7; rounded to 3.0. Net return = s_K/(K/Y) − δ = 10.7%. Affects only the reported level of the return. |
| g; n | Growth of output per worker; of the labour force | 0.050; 0.015 | 0.0167; 0.0033 | No-AI GDP growth 6.5%: RBI projects 6.7% for FY27, IMF 6.4%; FY26 actual 7.7% ([MoSPI PE](https://www.mospi.gov.in/uploads/latestReleases/latest_release_1780655857536_5ac01869-ca4a-422d-b7a7-57b81da60932_Press_Note_on_GDP_Estimates_for_Q4_2025-26_and_PE_FY_2025-26_F.pdf)). Labour-force growth 1.5% (World Bank, 2024–25). Implied measured TFP growth s_L × g = 2.65%. |
| λ; 1 − φ | Research returns; fishing-out | 1; 3.1 | 1; 3.1 | Kept. The research share of GDP drops out of the growth gap, so India's 0.84% R&D/GDP does not enter. |

## B. Labour market in normal times

| Symbol | Meaning | India | US (paper) | Basis |
|---|---|---|---|---|
| Ū | Normal unemployment pool, share of labour force | 0.043 | 0.038 | PLFS current weekly status, all-India 15+, Jan–Mar 2026: 4.3% ([MoSPI quarterly bulletin](https://www.mospi.gov.in/uploads/PressRelease/Press_note%20_Jan_March_2026%20PLFS_QB.pdf)). Usual status is 3.1% ([PLFS AR 2025](https://www.mospi.gov.in/uploads/latestReleases/latest_release_1774607827733_3e8964a9-268b-4cc9-ad65-cfc8a9e32f08_Press_note_AR_PLFS_2025_23032025_V2.1_26032026_final.pdf)); weekly status is closer to the CPS reference-week concept the paper uses. |
| q̄_C / q̄; q̄_N / q̄ | Relative separation rates by group | 1.216; 0.935 | 0.69; 1.52 | Set so the steady-state pool implies cognitive-origin unemployment of 6.6% and other-origin 3.6%. India's unemployment is concentrated among the educated (graduate unemployment 11–13%, youth 10%), the reverse of the US pattern. **Assumption**; see sensitivities. |
| f̄ | Job-finding rate, per month | 0.15 | 0.23 | **Assumption.** PLFS panel evidence (Bhattacharya, [Indian Urban Workers' Labour Market Transitions](https://arxiv.org/pdf/2110.05482)) shows very slow transitions into salaried work and long spells for educated job seekers. Implies a quit rate q̄ = f̄·Ū/(1−Ū) ≈ 0.08 a year (US 0.11). A value of 0.10 is in the sensitivity table and barely changes the results. |
| q^T / q̄ | Share of quits responding to job prospects | 0.55 | 0.55 | Kept |
| μ̄ | Search discount in normal times | 0.17 | 0.17 | Kept; no Indian estimate of cross-group occupational switching |
| ι; π̄ | Matching curvature; mean filling rate | 1.27; 0.65 | 1.27; 0.65 | Kept |
| ξ | Rigidity of the cognitive wage, per year | 0.5 | 0.5 | Kept; ξ = 0 and 0.9 in sensitivities |

## C. AI anchors, mid-2026 (measured)

| Symbol | Meaning | India | US (paper) | Basis |
|---|---|---|---|---|
| m₂₀₂₆ | Affected task mass | 0.051 | 0.14 | The paper's observed-exposure measure averages 0.22 within cognitive occupations. We apply the same 0.22 to India's cognitive share: 0.22 × 0.23. |
| d₂₀₂₆ | Diffusion share | 0.05 | 0.10 | [Anthropic Economic Index, India brief](https://www.anthropic.com/research/india-brief-economic-index) (Feb 2026): India is 2nd in global Claude use (5.8%) but 101st of 116 per capita; usage per cognitive worker is roughly a quarter to a third of the US. Large IT firms report near-universal Copilot deployment; 47% of large enterprises have GenAI in production ([EY-CII](https://www.ey.com/en_in/newsroom/2025/11/india-s-ai-shift-from-pilots-to-performance-47-percent-of-enterprises-have-multiple-ai-use-cases-live-in-production-ey-cii-report)); the SME and informal economy is near zero. Set at half the US anchor. **Judgment call.** |

## D. Scenario objects, 2030 (kept)

| Symbol | Meaning | Modest | Substantial | Extreme | Note |
|---|---|---|---|---|---|
| f | Fraction of cognitive work affected | 0.32 | 0.48 | 0.80 | = paper's m₂₀₃₀ (0.2 / 0.3 / 0.5) ÷ 0.624 |
| m₂₀₃₀ | Affected mass, India | 0.074 | 0.111 | 0.184 | = f × 0.230 |
| d₂₀₃₀ | Diffusion | 0.2 | 0.4 | 0.6 | Kept |
| a₂₀₂₆; a₂₀₃₀ | Log gain per instance | 0.30; 0.30 | 0.35; 0.45 | 0.45; 0.80 | Kept |
| ψ | Automation share | 0.5 | 0.75 | 0.9 | Kept |
| ρ | Reinstatement ratio | 0.5 | 0.25 | 0 | Kept |
| μ | Search discount on the path | 0.17 | 0.08 | 0.04 | Kept |
| θ_H | Posting speed, per month | 0.10 | 0.25 | 0.50 | Kept |

## E. Context figures used on the page (not model inputs)

| Figure | Value | Source |
|---|---|---|
| Nominal GDP FY2025-26 | ₹346.4 lakh crore (≈ $4.0 tn) | MoSPI Provisional Estimates |
| No-AI GDP 2030 at FY26 prices | ≈ ₹449 lakh crore | ₹346 × e^(0.065 × 4) |
| Employment by sector, 2025 | Agriculture 43.0%, manufacturing 12.1%, construction 12.0%, services ≈ 32.5% | PLFS AR 2025 |
| Status of employment, 2025 | Self-employed 56.2%, regular salaried 23.6%, casual 20.2% | PLFS AR 2025 |
| Earnings, 2025 | Regular salaried (male) ₹24,217 a month; casual (male) ₹455 a day | PLFS AR 2025 via [PIB](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2246009&reg=3&lang=1) |
| Food share of household spending | 47.0% rural, 39.7% urban | [HCES 2023-24](https://www.mospi.gov.in/sites/default/files/publication_reports/HCES%20FactSheet%202023-24.pdf) |
| Private consumption, % of GDP | ≈ 61% | World Bank WDI, 2024 |
| IT-BPM revenue, exports, employment | $297 bn (FY25), $246 bn exports (FY26E, 84% of revenue), 5.95 mn employees, net hiring 133,000 (FY25) | NASSCOM via [Dataquest](https://www.dqindia.com/news/nasscom-outlook-indias-tech-industry-to-grow-61-to-315-bn-in-fy26-11151228) |
| TCS, Infosys headcount | TCS ≈ 12,000 roles cut in FY26; Infosys −8,440 in Q4 FY26 | [Gulf News](https://gulfnews.com/business/markets/ai-overhaul-indias-tcs-to-cut-12000-jobs-this-year-after-growth-slows-in-q1-1.500212931), [Business Today](https://www.businesstoday.in/technology/story/infosys-headcount-falls-by-over-8400-in-q4-workforce-at-328594-527161-2026-04-23) |
| Graduate and youth unemployment | 11–13%; 9.9% (15–29) | PLFS 2023-24, 2025 |
| Urban unemployment, Apr–Jun 2020 | 20.8% | PLFS quarterly bulletin |
| Centre's gross tax revenue | ≈ 12% of GDP | Union Budget 2026-27 |
| Compensation arithmetic, extreme | Cognitive wage bill = 0.53 × 0.23 = 12.2% of GDP; −48% of that = 5.9% of GDP against a 9.3% GDP gain | Model output |

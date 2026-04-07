# Market Risk Dynamics: 2025 Tariff Shock Analysis
**Comparative Risk Assessment of S&P500, Dow Jones, and Nasdaq using Backtested VaR & Expected Shortfall.**

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Key Features](#2-key-features)
3. [Technical Methodology](#3-technical-methodology)
4. [Main Results](#4-main-results)
5. [Conclusions & Limitations](#5-conclusions--limitations)

---

## 1. Executive Summary
This analysis examines the systemic impact of the April 2nd, 2025 tariff announcement on volatility and tail-risk structures of major US indices. Using an **Event Study** methodology, we quantify the breakdown in predictive capacity of historical risk models during a significant macroeconomic structural shift.

## 2. Key Features
- **Multi-Index Pipeline:** Automated data retrieval via `yfinance` and vectorized log-return processing.
- **Dynamic Data Slicing:** Implementation of rolling windows for calibration (Estimation Window) and backtesting (Event Window).
- **Non-Parametric Risk Metrics:** Calculation of Historical Value-at-Risk ($VaR$) and Conditional VaR / Expected Shortfall ($ES$).
- **Statistical Validation:** Backtesting performed via **Kupiec’s POF (Proportion of Failures) Test** to verify model robustness.

## 3. Technical Methodology
- **Estimation Window:** 600 observations (pre-event volatility regime).
- **Gap Period:** 15 days to isolate the announcement effect from short-term noise.
- **Event/Distress Window:** 240 post-event observations.
- **Confidence Levels:** $\alpha = 0.01, 0.05$.
- **Hypothesis Testing:** Kupiec's Test calibrated at a 99% confidence level to identify systematic **Model Drift**.

## 4. Main Results
Empirical evidence shows an asymmetric risk increase across indices. While NASDAQ (^IXIC) and S&P500 (^GSPC) maintained statistical validity (p-value > 0.01), the Dow Jones (^DJI) exhibited a **critical model failure** (p-value = 0.001028).

### Kupiec Test Results
| **Ticker** | **^DJI** | **^GSPC** | **^IXIC** |
|:--- |:--- |:--- |:--- |
| **Violations** | 9.00 | 7.00 | 6.00 |
| **p-value** | 0.001028 | 0.01535 | 0.049737 |

The divergence between indices is critical. The 0.001 p-value for the Dow Jones suggests that the tariff shock disproportionately affected the **Industrial Sector** and **Blue Chips**, which are historically less volatile, leading to a number of violations (9) statistically incompatible with a 99% confidence level.

### Risk Metric Variations (Δ)

#### VaR Change Comparison
| **#** | **Ticker** | **0.01** | **0.05** |
|:--- |:--- |:--- |:--- |
| 1 | ^DJI | 0.425531 | 0.455642 |
| 2 | ^GSPC | 0.522981 | 0.159383 |
| 3 | ^IXIC | 0.430110 | 0.217884 |

#### Expected Shortfall (ES) Change Comparison
| **#** | **Ticker** | **0.01** | **0.05** |
|:--- |:--- |:--- |:--- |
| 1 | ^DJI | 0.826864 | 0.557829 |
| 2 | ^GSPC | 0.880754 | 0.544965 |
| 3 | ^IXIC | 0.588299 | 0.443745 |

---

### Data Visualization & Analysis

![VaR Comparison Chart](immagini/change_comparison_VaR.png)
*Figure 1: Comparison of VaR levels across scenarios.*

The chart highlights a **structural risk shift**. The 99% VaR increase is systematically higher than the 95% increase, confirming that the tariff shock impacted **tail events** more severely than average volatility. This suggests a mutation in return distributions towards higher **leptokurtosis**.

![Log Returns Distributions](immagini/log_returns.png)
*Figure 2: Shift from Normality to Distress Window distributions.*

**Distributional Analysis:** The transition from the "Normality" to "Distress" window clearly shows the emergence of **fat tails**. While the pre-event distribution approximates normality, the post-event period presents **extreme outliers** (up to -6% daily returns) that the historical model fails to capture effectively.

## 5. Conclusions & Limitations
The analysis confirms that the 2025 tariff announcement represented a **regime shift** for US markets. The statistical failure of the model on the Dow Jones highlights the intrinsic limitations of purely historical approaches during exogenous shocks.

### Model Limitations (Historical VaR)
1. **Echo Effect:** Historical VaR is sensitive to the chosen time window; past extreme events remain in the calculation until they drop out of the window, potentially inflating current risk estimates.
2. **Equally Weighted Returns:** The model lacks a weighted memory. It treats a return from 600 days ago with the same importance as yesterday's, resulting in a slow reaction to sudden **volatility clustering**.
3. **Loss Magnitude:** As VaR is not a "coherent risk measure," it fails to capture the severity of losses beyond the threshold—a task successfully delegated to **Expected Shortfall** in this study.

### Future Extensions
- **Filtered Historical Simulation (FHS):** Combining GARCH models to standardize returns and capture volatility dynamics.
- **Extreme Value Theory (EVT):** Specifically modeling distribution tails using Generalized Pareto Distribution (GPD).
- **Monte Carlo Simulation (MCS):** Generating predictive scenarios based on stochastic processes (e.g., Geometric Brownian Motion).
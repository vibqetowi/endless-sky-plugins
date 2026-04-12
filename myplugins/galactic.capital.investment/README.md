# Galactic Capital Investments

Galactic Capital Investments (GCI) became the largest bank in human space thanks to combination of attractive financial products, personalized service and... innovation. Perhaps unsurprisingly, the Syndicate is their biggest customer.

They control over 40% of financial infrastructure in Human, Hai and Quarg space while also hosting the Galactic Stock Exchanges where investors make and lose fortunes. Their recent public filings show daily revenue in the Trillions.

## Purpose

This plugin fixes the useless passive income system to improve vanilla gameplay and provide a smooth transition to plugin content. Players experience a faster path to a combat fleet, a more engaging midgame, and a rewarding endgame economy (including a legitimate path to the [Quaernan](https://github.com/AvianGeneticist/QuaernanHardpointsCarries)).

## Features

In addition to **a mission chain unlocking absolutely ludicrous returns**, the system replicates real-world US financial instruments to create a layered economic experience:
*   **Bonds Portfolio:** A high-yield savings account providing a risk-free return equivalent to Treasury Bonds.
*   **Trust Funds:** Family trust shared between all pilots (0% annualized return).
*   **Public Markets Investments:** Realistic stock trading with 10 stocks and monthly dividend payouts.
*   **Private Markets Perpetuities:** Investment missions providing salaries managed by GCI.
*   **Liquidation:** Optional conversion of investment salary back into cash (at a capital loss).

## Design Around Endless Sky Meta

*   **Time Compression:** Taking a human working lifetime of 40 years and scaling it down to the vanilla game's soft content limit of roughly 8 in-game years represents a 5x time compression. 
*   **Bank Loans & Interest Rates:** Vanilla's loan rates establish a minimum 0.20% daily interest (107% APY). By taking this 107% APY as the in-universe prime rate and mapping it to the US long-term average prime rate (6.87%), we establish a strict **15.6x macroeconomic multiplier**.
*   **Violence Meta:** Ship capturing is the most efficient way to earn capital in vanilla Endless Sky. This system supports that reality by bootstrapping your first combat ship and covering operational expenses in the mid/end game so you can play aggressively.
*   **Post-Vanilla Meta:** All income becomes obsolete for plugin-scale assets (1B+ ships). The system's ROI architecture specifically shortens payback periods as you invest more, becoming the primary economic engine for trillion-credit fleets.

---

## Appendix A: US Market Equivalency Table

**Anchor:** 0.2% daily = 6.87% (US Long-Term Prime Average).
**Multiplier:** 15.6x.

| Game Product | Game Daily Rate | Game APY | US Market Equivalent (Target Rate) |
| :--- | :--- | :--- | :--- |
| Bonds Portfolio | 0.15% | 71.7% | 4.6% (10Y Treasury / Risk-Free) |
| Prime Loan | 0.20% | 107.2% | 6.87% (Prime Rate) |
| Private Credit (Perpetuity)| 0.25% | 148.2% | 9.5% (outsttanding Private Credit Fund) |
| Dividend Stocks | 0.29% | 187.2% | 12.0% (Good year for the S&P index) |
| High-Interest Loan | 0.40% | 324.5% | 20.8% (Subprime Loan, near Credit Card) |
| Growth Stocks | 0.42% | 358.8% | 23.0% (Growth/Tech Stocks) |
| Penalty Loan | 0.6% | 787% | 50.45% (Loan shark) |

---

## Appendix B: Private Market Yield Schedules

The player is purchasing an annuity from GCI. GCI uses the player's capital to fund high-growth ventures, absorbing the risk and paying the player a guaranteed daily perpetuity (after fees).

*Note 1: The 100k non repeatable Angel Entry intentionally yields higher than the base formula to whet the player's appetite for the plugin's mechanics.*
*Note 2: Tiers above 1B deliberately break the 15.6x macroeconomic model, defaulting to a flat 1.00% daily yield to accelerate access to post-vanilla plugin content.*

### Investment Jobs (Repeatable)

| Tier | Principal | Daily Yield | Rate | Payback Period |
| :--- | :--- | ---: | :--- | ---: |
| Angel Entry (one time)| 100k | 500 | 0.50% | 200 days |
| Seed Venture | 1M | 2,500 | 0.25% | 400 days |
| IPO Invitation | 10M | 25,000 | 0.25% | 400 days |
| Corporate Takeover | 100M | 250,000 | 0.25% | 400 days |
| Planetary Terraforming| 1B | 10,00,000 | 1% | 100 days |
| Forbidden R&D | 10B | 100,000,000 | 1.00% | 100 days |
| War Bonds | 100B | 1,000,000,000 | 1.00% | 100 days |
| Sovereign Wealth Fund| 1T | 10,000,000,000 | 1.00% | 100 days |


### Mission-Chain Investments

*   **Intro Investment (1M principal):** 2,500 daily yield, 400-day payback.
*   **Colonization Chain Reward (1B total principal):** 10,00,000 daily yield, 100-day payback.

---

## Appendix C: Math (Stochastic Market Simulation)

The correct engine would use Geometric Brownian Motion with drift to simulate stock prices. Given the constraints of the game engine, we must use log functions and discrete probability buckets to approximate the desired returns and volatility.

### Explaining Stock Design Decisions

**1. Choosing a 15.6x Multiplier Over Real Stock Markets**
*   **Private Market Baseline:** The GCI 100M Perpetuity pays out 250k/day (148% APY), a highly attractive risk-free return.
*   **Public Market Requirement:** Public stocks carry the risk of total loss. To compel a player to choose the stock market over the private perpetuity, the expected compounding return must map strictly to the 15.6x macroeconomic multiplier to establish a mathematically sound risk premium.

**2. Simulating Black Swan Events**
*   **IRL Baseline:** SPY experiences a 15-20% drop roughly every 8 years. 
*   **In-Game Frequency:** A 1% daily chance = an average of 3.65 Black Swans per year.
*   **Event Magnitude:** The Black Swan event must be a **-25% drop** (multiplier of 0.75), occurring exactly 1% of the time. This scales macroeconomic crashes into the game engine's probability limits.

**3. Target 1: Dividend Stocks**
*   **List:** Southbound, Syndicate, Kraz, Lovelace, Betelgeuse.
*   **Goal:** Based on IRL S&P 500 data (approx. 11% price growth + 1% dividend = **12% total US APY**).
*   **Dividend Mapping:** The in-game dividend is **1.3% monthly**, targeting a `1% * 15.6 = 15.6%` annualized yield.
*   **Price Drift Mapping:** The price must grow at `11% * 15.6 = 171.6%` APY. The RNG buckets generate a 2.71x geometric drift to hit this target.

**4. Target 2: High Growth Stocks**
*   **List:** Lionheart, Deep Sky, Delta V, Tarazed, Megaparsec.
*   **Goal:** Based on IRL Tech Growth data (**23% total US APY**).
*   **Dividend:** 0%.
*   **Price Drift Mapping:** The price must grow at `23% * 15.6 = 358.8%` APY. The RNG buckets use higher volatility to generate a 4.58x geometric drift.

### Return Probability Matrices

**Asset A: Dividend Stocks**
*Target: ~2.71x Annual Price Growth + 1.3% Monthly Dividend = ~187% Total APY.*

| Scenario | Roll | Multiplier ($X$) | $\ln(X)$ | Prob ($P$) | Expected Log ($P \times \ln(X)$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Black Swan | 1 | 0.75 | -0.28768 | 0.01 | -0.002877 |
| Lose Big | 2-8 | 0.98 | -0.02020 | 0.07 | -0.001414 |
| Lose Small | 9-23 | 0.99 | -0.01005 | 0.15 | -0.001507 |
| Flat | 24-38 | 1.00 | 0.00000 | 0.15 | 0.000000 |
| Win Small | 39-76 | 1.01 | 0.00995 | 0.38 | +0.003781 |
| Win Big | 77-100 | 1.02 | 0.01980 | 0.24 | +0.004752 |
*   **Sum $E[\ln(X)]$:** $\mathbf{0.002735}$
*   **Annual Price Drift:** $e^{(0.002735 \times 365)} = \mathbf{2.71x}$

Dividend stocks get a 1.3% dividend paid as cash every 1st of the month. 

**Asset B: High-Growth Stocks**
*Target: ~4.58x (358.8%) Total APY. High Volatility. Zero Dividend.*

| Scenario | Roll | Multiplier ($X$) | $\ln(X)$ | Prob ($P$) | Expected Log ($P \times \ln(X)$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Black Swan | 1 | 0.75 | -0.28768 | 0.01 | -0.002877 |
| Lose Big | 2-11 | 0.96 | -0.04082 | 0.10 | -0.004082 |
| Lose Small | 12-27 | 0.98 | -0.02020 | 0.16 | -0.003232 |
| Flat | 28-41 | 1.00 | 0.00000 | 0.14 | 0.000000 |
| Win Small | 42-88 | 1.02 | 0.01980 | 0.47 | +0.009306 |
| Win Big | 89-100 | 1.04 | 0.03922 | 0.12 | +0.004706 |
*   **Sum $E[\ln(X)]$:** $\mathbf{0.003821}$
*   **Annual Price Drift:** $e^{(0.003821 \times 365)} = \mathbf{4.03x}$


*A price floor is hardcoded at 100 credits to avoid bankruptcy loops.*

For some damn reason this code sets a floor properly

```txt
				"stock value Lionheart Shipyards" >= 100
			action
				"stock value Lionheart Shipyards" = 100
			label "updated Lionheart Shipyards"
```

while this sets a ceiling

```txt
				"stock value Lionheart Shipyards" <= 100
			action
				"stock value Lionheart Shipyards" = 100
			label "updated Lionheart Shipyards"
```

I don't get it either
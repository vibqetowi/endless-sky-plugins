# Galactic Capital Investments

Galactic Capital Investments (GCI) became the largest bank in human space thanks to a combination of attractive financial products, personalized service and... innovative practices. Perhaps unsurprisingly, the Syndicate is their biggest customer.

In addition to the Galactic Stock Exchange, they control over 40% of financial infrastructure in Human, Hai and Quarg space. Their recent public filings show daily transaction volume in the trillions.


## Table of Contents

- [Purpose](#purpose)
- [Features](#features)
- [Design Around Endless Sky Meta](#design-around-endless-sky-meta)
- [Appendix 1: US Market Equivalency Table](#appendix-1-us-market-equivalency-table)
- [Appendix 2: Private Market Yield Schedules](#appendix-2-private-market-yield-schedules)
- [Appendix 3: Stock Math (Stochastic Market Simulation)](#appendix-3-stock-math-stochastic-market-simulation)
- [Appendix 4: Market Impact Model (Price Democracy)](#appendix-4-market-impact-model-price-democracy)


## Purpose

This plugin massively improves the vanilla finance system and provides a smooth transition to plugin content. Players experience a faster path to a combat fleet, a more engaging midgame, and a rewarding endgame economy (including a legitimate path to the  [Quaernan](https://github.com/AvianGeneticist/QuaernanHardpointsCarries)).

## Features

In addition to a mission chain unlocking absolutely ludicrous returns, the system replicates real-world US financial instruments to create a layered economic experience:
*   **Bonds Portfolio:** A high-yield savings account providing a risk-free return equivalent to 10Y Treasury Bonds.
*   **Trust Funds:** Family trust shared between all pilots (0% annualized return).
*   **Public Markets Investments:** Realistic stock trading with 10 stocks and monthly dividend payouts.
*   **Private Markets Perpetuities:** Investment missions providing salaries managed by GCI.
*   **Liquidation:** Optional conversion of investment salary back into cash (at a capital loss).
*   **Financial Responsibility:** Pay your workers or else.

## Design Around Endless Sky Meta

*   **Time Compression**: We use the in-universe loan rate as our tangible anchor for the rest of the math. The lowest one in vanilla is 0.2% daily or 107.357% APY, reserved for credit scores of 800. Mapping it to the US long-term average prime rate (6.87%), we establish a strict **15.627x macroeconomic multiplier**.
*   **Violence Meta:** Ship capturing is the most efficient way to earn capital in vanilla Endless Sky. This system supports that reality by bootstrapping your first combat ship and covering operational expenses in the mid/end game so you can play aggressively.
*   **Post-Vanilla Meta:** All income becomes obsolete for plugin-scale assets (1B+ ships). The system's ROI architecture specifically shortens payback periods as you invest more, becoming the primary economic engine for trillion-credit fleets.


## Appendix 1: US Market Equivalency Table

| Game Product | Game Daily Interest | Game Yearly Interest | Yearly IRL Interest | US Market Equivalent |
| :--- | :--- | :--- | :--- |  :--- |
| Bonds Portfolio | 0.149% | 71.884% | 4.6%|  10Y Treasury Bonds / Risk-Free |
| Prime Loan | 0.2% | 107.357% | 6.87% | Prime Lending Rate |
| Private Credit | 0.25% | 148.456% | 9.5% | Private Credit Fund |
| Dividend Stocks | 0.29% | 187.523% | 12% | S&P 500 Index (good year) |
| High-Interest Loan | 0.4% | 329.344% | 21.075% | Subprime / Credit Card |
| Growth Stocks | 0.419% | 359.419% | 23% | Tech Stocks (GOOGL) |
| Penalty Loan | 0.6% | 787.693% | 50.406% | Loan shark |


## Appendix 2: Private Market Yield Schedules

GCI uses the player's capital to fund private high-growth ventures, absorbing the risk and paying the player a guaranteed daily perpetuity (after fees). 

We're basically conflating Private Credit, Venture Capital and Private Equity.


### Contents

1. [Investment Jobs (Repeatable)](#31-investment-jobs-repeatable)
2. [Mission-Chain Investments](#32-mission-chain-investments)

*Note: Tiers above 1B deliberately break the 15.627x macroeconomic model, defaulting to a flat 1% daily yield to accelerate access to post-vanilla plugin content. They might look ridiculous using real world logic, but are extremely realistic in game. See Appendix 4*

### 2.1 Investment Jobs (Repeatable)

| Tier | Principal | Daily Yield | Rate | Payback Period |
| :--- | :--- | ---: | :--- | ---: |
| Angel Entry | 100k | 500 | 0.5% | 200 days |
| Seed Venture | 1M | 2,500 | 0.25% | 400 days |
| IPO Invitation | 10M | 25k | 0.25% | 400 days |
| Corporate Takeover | 100M | 250k | 0.25% | 400 days |
| Planetary Terraforming| 1B | 10M | 1% | 100 days |
| Forbidden R&D | 10B | 100M | 1% | 100 days |
| War Bonds | 100B | 1B | 1% | 100 days |
| Sovereign Wealth Fund| 1T | 10B | 1% | 100 days |

The penalty for early selling is 30% of the principal which is on the high end of real Private Credit. To balance the 1% daily returns, selling is disabled after the terraforming mission chain.


### 2.2 Mission-Chain Investments

*   **Intro Investment (1M principal):** 2,500 daily yield, 400-day payback. Unlocks 1M to 100M repeatable investment missions.
*   **Terraforming/Blood Money Reward (1B total principal):** 10,000,000 daily yield, 100-day payback. Unlocks the post-vanilla 1B+ repeatable investment missions.

A fair warning: the terraforming chain mission is very much a dark story, but so is the ES combat system. Most pirates are canonically downtrodden teenagers.
## Appendix 3: Stock Math (Stochastic Market Simulation)

### Contents

1. [Theory](#31-theory)
2. [Engine Limitations](#32-engine-limitations)
3. [Backcalculating Probabilities](#33-backcalculating-probabilities)
4. [Application: The Probability Matrices](#34-application-the-probability-matrices)
5. [Stock Splitting](#35-stock-splitting)

### 3.1 Theory

To simulate a realistic market, we start with the standard continuous-time models.

**1. Geometric Brownian Motion (GBM)** <br>
The standard model for asset prices. It assumes price changes are proportional to the current price.
*   **Formula:** $dS_t = \mu S_t dt + \sigma S_t dW_t$
    *   $S_t$: Price at time $t$.
    *   $\mu$: Drift (expected return).
    *   $\sigma$: Volatility.
    *   $dW_t$: Random noise (Wiener process).

**2. Jump-Diffusion (Merton, 1976)** <br>
Real markets experience "Black Swan" events (15-20% drops) roughly once every 8 years. Standard GBM underestimates this **Tail Risk**, it must be added manually.
*   **Concept:** A standard random walk plus a Poisson process (rare, discrete events).

**3. Log Returns**
We use log returns ($r = \ln(X)$) instead of simple percentage returns because they allow us to **solve for probabilities**.
*   **The Problem:** Simple returns compound multiplicatively ($X_{total} = X_1 \times X_2 \dots$). Distributing a total return across daily outcomes creates a non-linear system that conflicts with the requirement that probabilities must sum to 1 ($\sum P_i = 1$).
*   **The Solution:** Log returns convert multiplication into addition ($r_{total} = r_1 + r_2 \dots$).
*   **Application:** This linearity allows us to set up a solvable linear equation:
    $$ \sum (P_i \times \ln(X_i)) = \text{Target Daily Log Return} $$
    Subject to the constraint: $\sum P_i = 1$.
    This lets us reverse-engineer the exact probabilities ($P_i$) for our arbitrary daily multipliers ($X_i$) to hit a specific annual target.

### 3.2 Engine Limitations

The *Endless Sky* engine prevents us from solving the differential equations above.
1.  **No SDE Execution:** The engine only runs discrete arithmetic on "landing." We cannot simulate continuous time ($dt \to 0$).
2.  **Integer Truncation:** All values are `int64_t`. Division truncates toward zero. There are no decimals.
3.  **No Floating Point State:** We cannot store volatility ($\sigma$) or drift ($\mu$) as continuous variables.

### 3.3 Backcalculating Probabilities

Since the engine cannot run a continuous simulation, we reverse-engineer the daily probabilities to match known annual targets.

**Step 1: Define Asset Targets** <br>
We map real-world assets to the game using the 15.627x macro multiplier (see *Appendix 1*).
*   **Dividend Stocks (SPY):** From a rounded 11% + 1% dividends annualized returns, we target 171.896% APY (2.719x drift) + 1.217% monthly dividend. 
*   **Growth Stocks (GOOGL):** From a rounded 23% annualized returns, we target  359.419% APY (4.594x drift). Zero dividend.

**Step 2: Inject the Black Swan** <br>
We must backcalculate the log impact to match IRL tail risk (a 15–20% drop roughly every 8 years).
*   **Frequency:** Since the game rolls 0-99, the smallest frequency is **1% daily probability** (approx. 3.65 crashes/year).
*   **Deriving the Jump Size ($J$):**
    $$ \text{Daily Log Drag} = \frac{1}{8 \text{ years}} \times \ln(0.8) \times 15.627 \div 365 \text{ days} = -0.001194 $$
    Since this drag comes from a 1% probability event ($P=0.01$):
    $$ 0.01 \times \ln(J) = -0.001194 $$
    $$ \ln(J) = -0.1194 \implies J = e^{-0.1194} \approx 0.8874 $$
    **Result:** A **-11.26%** drop occurs exactly when the random roll is `0`. This multiplier is **fixed** for both asset classes.

**Step 3: Define Arbitrary Multipliers**
We define 5 additional arbitrary daily price movement bins (e.g., "Lose Big" = 0.98, "Win Small" = 1.01). These are **designer choices**, not derived from a model. They serve as the "buckets" for the random roll.

**Step 4: Solve for Probabilities**
With the Black Swan fixed and the 5 arbitrary multipliers chosen, we use a Python script to solve for the remaining probabilities ($P_i$) such that:
1.  The sum of expected log returns equals the **Target Daily Log Return** (from Step 1).
2.  The sum of all probabilities equals 1 ($\sum P_i = 1$).

$$ \sum (P_i \times \ln(X_i)) = \text{Target Daily Log Return} $$

### 3.4 Daily Probability Matrices

**Dividend Stocks**
*Target: 2.719x Annual Price Drift + 1.217% Monthly Dividend.*

| Scenario | Roll | Multiplier ($X$) | $\ln(X)$ | Prob ($P$) | Expected Log ($P \times \ln(X)$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Black Swan | 0 | 0.8874 | -0.1195 | 0.01 | -0.0012 |
| Lose Big | 1–6 | 0.98 | -0.0202 | 0.06 | -0.0012 |
| Lose Small | 7–21 | 0.99 | -0.0101 | 0.15 | -0.0015 |
| Flat | 22–44 | 1.00 | 0.0000 | 0.23 | 0.0000 |
| Win Small | 45–87 | 1.01 | 0.0099 | 0.43 | 0.0043 |
| Win Big | 88–99 | 1.02 | 0.0198 | 0.12 | 0.0024 |
| **Sum** | | | | **1.00** | **0.0027** |

*Calculation:* $e^{0.0027 \times 365} \approx 2.719\times$ (Matches Target).

**Growth Stocks**
*Target: 4.594x Annual Price Drift.*

| Scenario | Roll | Multiplier ($X$) | $\ln(X)$ | Prob ($P$) | Expected Log ($P \times \ln(X)$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Black Swan | 0 | 0.8874 | -0.1195 | 0.01 | -0.0012 |
| Lose Big | 1–6 | 0.96 | -0.0408 | 0.15 | -0.0061 |
| Lose Small | 7–21 | 0.98 | -0.0202 | 0.23 | -0.0046 |
| Flat | 22–44 | 1.00 | 0.0000 | 0.04 | 0.0000 |
| Win Small | 45–75 | 1.02 | 0.0198 | 0.32 | 0.0063 |
| Win Big | 76–99 | 1.04 | 0.0392 | 0.25 | 0.0098 |
| **Sum** | | | | **1.00** | **0.0042** |

*Calculation:* $e^{0.0042 \times 365} \approx 4.594\times$ (Matches Target).

### 3.5 Stock Splitting

The `int64_t` engine disallows fractional trading and creates two specific problems:
1.  **Divide-by-Zero:** If a stock hits price `0`, return calculations crash.
2.  **UX Degradation:** Without fractional shares, a high price (e.g., 10,000 credits) forces players to sell massive positions to access small amounts of cash, creating a frustrating experience.

**The Fix: Neutral Stock Splits**
We force the price back to a ~1,000 credit anchor. Market Cap remains constant; only Share Count and Price per Share change.
*   **Forward Split (Price $\ge 10,000$):** `Price = Price / 10`, `UserShares = UserShares * 10`.
*   **Reverse Split (Price $\le 100$):** `Price = Price * 10`, `UserShares = UserShares / 10`.

**Real-World Parallel:**
This mirrors the **Trading Range Hypothesis** (Fama et al., 1969). In real markets, companies split shares to keep prices in a "tradable" range for investors who cannot buy fractions.

**Note:** Because the engine truncates decimals, the remainder is lost during reverse splits (e.g., 9 shares / 10 = 0 shares). This un-modeled negative drift destroys up to 9 × 100 credits per split, which is basically a rounding error and can be safely ignored.

## Appendix 4: Market Impact Model (Price Democracy)

### Contents

### Contents

1. [From Stock Simulation to Trading Simulation](#41-from-stock-simulation-to-trading-simulation)
2. [Modelling Friction](#42-modelling-friction)
3. [Math Calibration](#43-math-calibration)
4. [Procedural Execution](#44-procedural-execution)
5. [Alpha Calibration Strategy](#45-alpha-calibration-strategy)
6. [ROI Table: Velocity Calibration](#46-roi-table-velocity-calibration)


### 4.1 From Stock Simulation to Trading Simulation

**Appendix 3** created a mathematically correct *Stock Simulator*. It generates random price movements based on historical data. However, it does not yet simulate the *trading* experience. In real markets, your trades affect the price. This is called **Market Impact**.

This section implements **Liquidity Friction** so that large trades become progressively more expensive, preventing infinite money glitches and simulating the reality of market depth.

### 4.2 Modelling Market Impact for Block Trades

The critical design decision here is driven by **Appendix 3 (Stock Splits)**.

If we calculated friction based on **Share Count**, a stock split would instantly break the math (e.g., a 10:1 split would make the friction constant 10x too weak).

The solution is to calculate friction based on **Notional Flow** (Total Credits Traded). 1 Billion credits traded is 1 Billion credits traded, regardless of whether that buys 1 million shares at $1,000 or 10 million shares at $100.

The game engine processes trades as instantaneous, discrete blocks. To model the market impact of these block trades, we use the industry-standard framework: Kyle's Lambda (Kyle, 1985) which provides a direct, linear formula for the permanent price shift caused by a single trade.

$$\Delta P = \lambda \cdot Q$$
*(Where $\Delta P$ is Price Change, $Q$ is Notional Flow, and $\lambda$ is the market's depth/sensitivity).*

Because $\lambda$ is a tiny decimal, we invert the metric to create a whole-number Friction Constant ($C = \frac{1}{\lambda}$). This translates the academic theory into a functioning integer rule: 'For every $C$ credits traded ($Q$), change the price by 1.'


### 4.3 Math Calibration

Since we cannot derive numbers from in game logic, we constructed a "Sense of Scale" using real-world ratios and arbitrary caps.

**Scale Anchor**
We needed a maximum corporate size to ground the simulation.
*   **Player Cap:** Chose **8 Trillion Credits** arbitrarily (roughly 2x the cost of the Quaernan).
*   **Corporate Ratio:** Applied the real-world ratio of **NVIDIA's Market Cap** ($4.82T$) to **Elon Musk's Net Worth** ($800B$) $\approx 6.025$.
*   **Result:** The largest interstellar shipyard is modeled as $8T \times 6.025 = \mathbf{48.2\text{ Trillion Credits}}$.
*   **Derived Metrics:**
    *   **Total Shares (TSO):** $48.2T / 1,000 \text{ (anchor price)} = 48.2 \text{ Billion shares}$.
    *   **Daily Average Volume (ADV):** Assumed **0.2%** of Market Cap (standard for large caps) $\to \mathbf{96.4 \text{ Billion Credits}}$.

**Friction Constant**
*   **Axiom:** Trading 100% of Average Daily Volume (ADV) shall move the price by 31.254% (the macro-multiplied equivalent of a 2% real-world move, institutional heuristic).
*   **Unit Move:** At anchor price ($1,000$), a 31.254% move is $312.54$ credits.
*   **Calculation:** $C = \text{ADV} / \text{Unit Move} = 96,400,000,000 / 312.54 \approx \mathbf{308,440,520}$.
*   **Meaning:** Trading **308,440,520 credits** in a single day permanently moves the price by **1 credit**.

**Bid-Ask Spread**
Because we use a **Reactive** approach (price updates *after* the trade), a player could infinitely push the price up, and sell immediately for a profit (Pump-and-Dump). We implement another real life tool, the **Bid-Ask Spread** (Market Maker profit) to control this exploit to a carefully tuned level (See 4.6).

### 4.4 Procedural Execution

The system maintains state variables for the daily notional volume per stock, reset on landing. To bypass PEMDAS and maintain integer integrity, the logic executes as a linear sequence.

#### 4.4.1 Buy Logic
The buy process calculates the price impact before executing the trade:
1. Calculate the current volume index: `BEFORE = {abbr}_daily_notional_volume / 308440520`.
2. Apply the spread to the current price to get the Ask: `ASK = price * SPREAD / 10000`.
3. Determine the total value of the trade: `VALUE = ASK * shares`.
4. Check remaining liquidity capacity: `CAP = 96400000000 - {abbr}_daily_notional_volume`.
5. **UI Constraint:** The engine checks if the transaction value exceeds `CAP`. If it does, the transaction button is disabled.
6. Update the daily volume: `{abbr}_daily_notional_volume = {abbr}_daily_notional_volume + VALUE`.
7. Calculate the new volume index: `AFTER = {abbr}_daily_notional_volume / 308440520`.
8. Determine the price impact: `IMPACT = AFTER - BEFORE`.
9. Update the price: `price = price + IMPACT`.

#### 4.4.2 Sell Logic
The sell process mirrors the buy logic but reduces the price:
1. Calculate the current volume index: `BEFORE = {abbr}_daily_notional_volume / 308440520`.
2. Apply the spread to the current price to get the Bid: `BID = price * SPREAD / 10000`.
3. Determine the total value of the trade: `VALUE = BID * shares`.
4. Check remaining liquidity capacity: `CAP = 96400000000 - {abbr}_daily_notional_volume`.
5. **UI Constraint:** The engine checks if the transaction value exceeds `CAP`. If it does, the transaction button is disabled.
6. Update the daily volume: `{abbr}_daily_notional_volume = {abbr}_daily_notional_volume + VALUE`.
7. Calculate the new volume index: `AFTER = {abbr}_daily_notional_volume / 308440520`.
8. Determine the price impact: `IMPACT = AFTER - BEFORE`.
9. Update the price: `price = price - IMPACT`.

*Note: Players can exploit this mechanic by preventing price drop during dumping thus generating ~20% more alpha. This is not patched because I respect the grind.*

### 4.5 Alpha Calibration Strategy

The Market Impact Model is calibrated for a **22-day transition** from 1 Trillion Credits to the 4 Trillion Credit endgame cap. This velocity is achieved by tuning the **Bid-Ask Spread ($S$)** against the fixed friction of the market.

#### 4.5.1 Defining Alpha
In finance, **Alpha ($\alpha$)** represents the "active return" on an investment—the performance of a strategy above and beyond a market benchmark or a risk-adjusted expected return. It is the primary metric used to evaluate the skill of a fund manager or the effectiveness of a specific trading strategy.

In game, **Alpha** is the return earned in excess of the stock's natural stochastic movement (**Drift**) using the market impact model.

**The Formula:**
$$\text{Alpha} = \frac{1 + \text{I}}{D} - 1$$

The maximum practical alpha is achieved as follows:
1.  **Day 1 (Buy):** Purchase 100% of a stock's ADV ($96.4\text{B}$ credits). This creates **Impact ($I$)**, raising the price for the next day.
2.  **Overnight (Hold):** Hold the position through the daily stochastic move (**Drift**).
3.  **Day 2 (Sell):** Liquidate the entire position at the new higher price.

#### 4.5.2 Deriving Spread S
The **Spread ($S$)** is the only remaining tunable variable. It is calculated by working backward from the 22-day wealth progression target, using the fixed Market Drift and Friction constants.

**Underlying Drift D**

The expected daily movement is derived from the expected log returns ($E[\ln(X)]$) calculated in the stochastic probability matrices (Section 4.4):
*   **Dividend:** $E[\ln(X)] = 0.0027 \implies M_D = e^{0.0027} \approx \mathbf{1.002704}$
*   **Growth:** $E[\ln(X)] = 0.0042 \implies M_G = e^{0.0042} \approx \mathbf{1.004209}$
*   **Market Drift ($D$):** For a 10-stock market (5 of each), the average overnight move is:
    $$D = (5 \cdot 1.002704 + 5 \cdot 1.004209) \div 10 = \mathbf{1.003456}$$

**Target Velocity**
To scale from **1 Trillion to 4 Trillion Credits** in **22 days**:
*   **Daily Profit:** $3,000\text{B} \div 22 = \mathbf{136.36 \text{ Billion/Day}}$.
*   **Required Cycle ROI ($R_t$):** A trade cycle is 2 days. The total market ($964\text{B}$ ADV) must yield:
    $$R_t = (136.36\text{B} \times 2) \div 964\text{B} = \mathbf{28.291\% \text{ ROI per cycle}}.$$

**Solving for the Tunable Friction ($S$)**
We align the **Potential Return** (Pump + Drift) with the **Target Velocity** ($R_t$) by solving for the **Spread ($S$)**:
*   **Potential Return:** $(P_0 + I) \div P_0 \times D = 1.312 \times 1.003456 = \mathbf{1.316534}$
*   **Equation:** $1.282912 = 1.316534 \times \frac{1 - S}{1 + S}$
*   **Solution:** **$S = 1.30\%$** half spread ($130$ bps) which is 2.60% total.

### 4.6 ROI Table: Velocity Calibration

*Averaged across 10 Stocks | $S = 1.30\%$ | $C = 308,440,520$*

| Buy Volume (% of ADV) | Budget Required | Expected Total ROI (2-Day) | Manipulation Alpha |
| :--- | :--- | :--- | :--- |
| 1% | $964\text{M}$ | **-1.92%** | **-2.26%** |
| 8.5% | **$8.2\text{B}$** | **+0.35%** | **0.00%** |
| 25% | $24.1\text{B}$ | **5.39%** | **5.03%** |
| 100% | **$96.4\text{B}$** | **28.32%** | **27.88%** |

**Summary:** The market manipulation mechanics unlock at 8.2 billion credits, which is significantly beyond the vanilla game economy.
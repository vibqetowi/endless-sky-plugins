# Galactic Capital Investments

Galactic Capital Investments (GCI) became the largest bank in human space thanks to a combination of attractive financial products, personalized service and... innovative practices. Perhaps unsurprisingly, the Syndicate is their biggest customer.

In addition to the Galactic Stock Exchange, they control over 40% of financial infrastructure in Human, Hai and Quarg space. Their recent public filings show daily transaction volume in the trillions.

## Table of Contents

- [Purpose](#purpose)
- [Features](#features)
- [Design Around Endless Sky Meta](#design-around-endless-sky-meta)
- [Appendix A: US Market Equivalency Table](#appendix-a-us-market-equivalency-table)
- [Appendix B: Private Market Yield Schedules](#appendix-b-private-market-yield-schedules)
- [Appendix C: Stock Math (Stochastic Market Simulation)](#appendix-c-stock-math-stochastic-market-simulation)
- [Appendix D: Liquidity Friction Model](#appendix-d-liquidity-friction-model)
- [Appendix E: Lore for Nerds](#appendix-e-lore-for-nerds)

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

## Appendix A: Game Engine Limitation
* allows basic arithmetic +, - , *, /, and  % (modulo) 
* allows an prng from 0 to 99
* as far as i know does not support PEMDAS, so order of operations is strictly left to right. 
* prefers stateless operations
* used 64 bit signed ints
* integer only, rounds down

## Appendix A: US Market Equivalency Table

**Anchor:** 0.2% daily = 107.357% APY.
**Multiplier:** 15.627x.

| Game Product | Game Daily Interest | Game Yearly Interest | US Market Equivalent |
| :--- | :--- | :--- | :--- |
| Bonds Portfolio | 0.149% | 71.884% | 4.6% (10Y Treasury / Risk-Free) |
| Prime Loan | 0.2% | 107.357% | 6.87% (Prime Rate) |
| Private Credit | 0.25% | 148.456% | 9.5% (Private Credit Fund) |
| Dividend Stocks | 0.29% | 187.523% | 12% (S&P 500 Index) |
| High-Interest Loan | 0.4% | 329.344% | 21.075% (Subprime / Credit Card) |
| Growth Stocks | 0.419% | 359.419% | 23% (Tech / Growth Stocks) |
| Penalty Loan | 0.6% | 787.693% | 50.406% (Loan shark) |


## Appendix B: Private Market Yield Schedules

GCI uses the player's capital to fund private high-growth ventures, absorbing the risk and paying the player a guaranteed daily perpetuity (after fees). 

Finance people may now crucify me for conflating Private Credit, Venture Capital and Private Equity.

*Note: Tiers above 1B deliberately break the 15.627x macroeconomic model, defaulting to a flat 1% daily yield to accelerate access to post-vanilla plugin content. They might look ridiculous using real world logic, but are extremely realistic in game. See appendix D*

### Investment Jobs (Repeatable)

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

### Mission-Chain Investments

*   **Intro Investment (1M principal):** 2,500 daily yield, 400-day payback. Unlocks 1M to 100M repeatable investment missions.
*   **Terraforming/Blood Money Reward (1B total principal):** 10,000,000 daily yield, 100-day payback. Unlocks the post-vanilla 1B+ repeatable investment missions.

A fair warning: the terraforming chain mission is very much a dark story, but so is the ES combat system. Most pirates are canonically downtrodden teenagers.

## Appendix C: Stock Math (Stochastic Market Simulation)

The correct engine would use Geometric Brownian Motion with drift to simulate stock prices. Given the constraints of the game engine, we must use logarithms to precalculate probilities and approximate the desired returns and volatility.

### Explaining Stock Design Decisions

**Simulating Black Swan Events**
*   **IRL Baseline:** Capital markets (proxied by the S&P 500) experience a 15-20% drop roughly every 8 years. 
*   **In-Game Frequency:** A 1% daily chance = an average of 3.65 Black Swans per year.
*   **Event Magnitude:** The Black Swan event must be an -11.26% drop (multiplier of 0.8874), occurring exactly 1% of the time.
*   **Derivation of 0.8874:** $\frac{1 \text{ event}}{8 \text{ years}} \times \ln(0.8) \times 15.627 \div 365 \text{ days} = -0.001194$ required daily log drag. To achieve this expected value at a 1% probability, the required multiplier is $e^{\frac{-0.001194}{0.01}} = 0.8874$

**Target 1: Dividend Stocks**
*   **Goal:** Based on IRL S&P 500 data (10.58% price growth + 1.09% dividend).
*   **Dividend Mapping:** 1.217% monthly, targeting a 15.627% annualized yield.
*   **Price Drift Mapping:** Target 171.896% APY via a 2.719x geometric drift.

**Target 2: High Growth Stocks**
*   **Goal:** Based on IRL NVIDIA/Tech data (approx. 22.8% yearly price growth).
*   **Price Drift Mapping:** Target 359.419% APY via a 4.594x geometric drift.

### Return Probability Matrices

**Asset A: Dividend Stocks**
*Target: ~2.719x Annual Price Growth + 1.217% Monthly Dividend = ~187.523% Total APY.*

| Scenario | Roll | Multiplier ($X$) | $\ln(X)$ | Prob ($P$) | Expected Log ($P \times \ln(X)$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Black Swan | 0 | 0.8874 | -0.1195 | 0.01 | -0.0012 |
| Lose Big | 1-6 | 0.98 | -0.0202 | 0.06 | -0.0012 |
| Lose Small | 7-21 | 0.99 | -0.0101 | 0.15 | -0.0015 |
| Flat | 22-44 | 1 | 0 | 0.23 | 0 |
| Win Small | 45-87 | 1.01 | 0.01 | 0.43 | 0.0043 |
| Win Big | 88-99 | 1.02 | 0.0198 | 0.12 | 0.0024 |
*   **Sum $E[\ln(X)]$:** **0.0027**
*   **Annual Price Drift:** **2.719x**


**Asset B: High-Growth Stocks**
*Target: ~4.594x (359.419%) Total APY. High Volatility. Zero Dividend.*

| Scenario | Roll | Multiplier ($X$) | $\ln(X)$ | Prob ($P$) | Expected Log ($P \times \ln(X)$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Black Swan | 0 | 0.8874 | -0.1195 | 0.01 | -0.0012 |
| Lose Big | 1-6 | 0.96 | -0.0408 | 0.15 | -0.0061 |
| Lose Small | 7-21 | 0.98 | -0.0202 | 0.23 | -0.0046 |
| Flat | 22-44 | 1 | 0 | 0.04 | 0 |
| Win Small | 45-75 | 1.02 | 0.0198 | 0.32 | 0.0063 |
| Win Big | 76-99 | 1.04 | 0.0392 | 0.25 | 0.0098 |
*   **Sum $E[\ln(X)]$:** **0.0042**
*   **Annual Price Drift:** **4.594x**

### Stock splitting

Since the engine truncates integers, we cannot do fracitonal trading, this creates 2 problems:
1) divide by zero when calculating returns from a stock that has dropped to 0 value
2) liquidity. Prices that exceed 10k impact flexicility and locks out small investment

To solve this the system simulates **Neutral Stock Splits** (*Fama et al., 1969*) to a target price of 1000 credit/stock. This means market cap doesnt change but the UX is betetr. This very much happens IRL, for example Apple has done 5 stock splits in its history. 

Implementation:

On landing, the system checks if any stock price is above 10,000 or below 100. If so, it applies the appropriate split and adjusts the user's shares accordingly.This is done only on landing not live as you trade because its more realistic and also would be a bitch to code otherwise.

*   **Forward Split (Trigger: Price $\ge 10,000$):**
    *   `Price = Price % 10`
    *   `UserShares = UserShares * 10`
*   **Reverse Split (Trigger: Price $\le 100$):**
    *   `Remainder = UserShares % 10` 
    *   `Price = Price * 10`
    *   `UserShares = UserShares / 10`

TThe engine rounding down craetes capital losses every time a split occurs, forward or backwards. This simulates administration fees (read: the developper is coping).

## Appendix D: Liquidity Friction Model

This model simulates the reality that every transaction physically alters the stock market by consuming liquidity and shifting the price. This extra bit ensures the player has different experiences at different wealth scales

Because the engine lacks a floating-point unit and rtracking TSO is stateful annoyance, we employ a **Cumulative Notional Linear Friction** model based on the permanent impact component of the Almgren-Chriss framework.  In Layman's terms: stocks usually only trade a certain dolalr volume per day (notional value) on the entire market, the more of that daily limit you trade the more you move the price against yourself. Thie code uses a scaling factor this is resistant to the share splitting mechanic above because it uses notional value (credits traded) rather than shares traded as the input for the price impact calculation.

### The Musk-NVIDIA Anchor

To ground the simulation in real-world wealth concentration while adhering to the **8 Trillion Credit** (2 Quaernans) individual soft wealth cap, we apply a real world ratio:

*   **Richest man On Earth (2026):** Elon Musks's net worth is estimated at $800 Billion USD.
*   **Company with the largest market cap (2026):** NVIDIA at $4.82 Trillion USD. 
*   **The Ratio:** $4.82T / 0.8T = \mathbf{6.025}$. The largest interstellar shipyard is roughly 6x wealthier than the wealthiest human.
*   **Galactic Application:** $8\text{ Trillion Credits} \times 6.025 = \mathbf{48.2\text{ Trillion Credits}}$.
*   **Equity Baseline:** At 1,000 credits per share, a Large Corp has **48,20,000,000 (48.2 Billion) Total Shares Outstanding (TSO).**
| **Daily Average Vol (ADV)** | $96,400,000,000$ | **0.2% Liquidity-to-Cap Ratio**. Standard for IRL hufge companies

I chose $8T arbitrarily but to be honest there is literally no reason to buy 2 Quaernans. One is enough to destroy the entire galaxy multiple times over.

### Friction Constant Derivation

The Almgren-Chriss model (*Almgren & Chriss, 2000*) defines the permanent price impact of a trade equal to 100% of the ADV as **2% (200 bps)**. this means if you somehow traded the entire daily volume of a stock in one go, you would move the price by 2%. 

Applying the Macroeconimic Multiplier ($15.627$):
$$\text{Target Impact} = 0.02 \times 15.627 = \mathbf{31.254\%}\text{ (31254 bps)}$$

At the simulation’s anchor price of $1,000$ credits:
$$\text{Unit Move} = 1,000 \times 0.31254 = \mathbf{312.54 \text{ units}}$$

$C$ represents the Credits required per $1$ unit of price movement:
$$C = \text{ADV} / \text{Unit Move} = 96,400,000,000 / 312.54 \approx \mathbf{308,440,520}$$
**Engine Implementation Value:** **$308,440,520$**.

TLDR: trading 308 million credits of stock on a single day will move its price by 1 credit. this works in both directions regardless of split

### Way too much math

We implement a bastard cousin of the **Permanent Impact Component ($\gamma$)** of **Kyle’s Lambda** (*Kyle, 1985*) and **Almgren-Chriss** (*2000*), adapted for Notional Value. To properly model market dynamics.

Combiunation of reactive and practive appprach The price updates via friction after the trade to keep in simple(reactive approach) this does open up a prtentila pump and dump exploit but the proactive spread is a bitch to code 

Engine limitations also actively forbid the elastic component of Kyle, in real life, large trades experience slip, which is a fancy way to say that the price changes as the trade executes obviously I can't code any of that or more accurately can't be bothered to.

simpler is better. We just need to apply a hardcoded bid ask spread and call it a day. this tansform an exzploit to something we intended irl the difference means the delta between the buy and sell price of a stock. MArket makers like GCI make bank just by executing the trade and pocketing that difference.

The system maintains state variables per stock, reset at the start of each simulated day (on landing):
*   `{abbr)_daily_traded_volume` (Initial: 0 credits)
*   `bid_ask_spread` = **2.51%** (Multiplier for proactive cost)

To bypass PEMDAS and maintain integer integrity, the logic must be executed as a linear sequence of single operations.

### **PROCEDURAL EXECUTION (BUY)**
1. `BEFORE = {abbr)_daily_traded_volume / 308440520`
2. `ASK = price * 10251`
3. `ASK = ASK / 10000`
4. `VALUE = ASK * shares`
5. `CAP = 96400000000 - {abbr)_daily_traded_volume`
6. IF VALUE > CAP: VALUE = CAP
7. `{abbr)_daily_traded_volume = {abbr)_daily_traded_volume + VALUE`
8. `AFTER = {abbr)_daily_traded_volume / 308440520`
9. `IMPACT = AFTER - BEFORE`
10. `price = price + IMPACT`


### **PROCEDURAL EXECUTION (SELL)**
1. `BEFORE = {abbr)_daily_traded_volume / 308440520`
2. `BID = price * 9749`
3. `BID = BID / 10000`
4. `VALUE = BID * shares`
5. `CAP = 96400000000 - {abbr)_daily_traded_volume`
6. IF VALUE > CAP: VALUE = CAP
7. `{abbr)_daily_traded_volume = {abbr)_daily_traded_volume + VALUE`
8. `AFTER = {abbr)_daily_traded_volume / 308440520`
9. `IMPACT = AFTER - BEFORE`
10. `price = price - IMPACT`




### **7. BID-ASK SPREAD DERIVATION & PROFITABILITY**
the diference betweeb the buy and sell prioce was carefully chosen so that the max you can return in a single day via market manipulation is 5%

numbers were derived using a python script

| Daily ROI Target | Budget Required (Credits) | % of Daily ADV |  
| :--- | :--- | :--- | 
| **-24.8%** | $925,321,559$ | 0.96% | *|
| **0.0% (Break-even)** | **$77,418,570,423$** | 80.31% |  
| **1.0% ROI** | **$80,502,975,619$** | 83.51% |  
| **2.0% ROI** | **$83,587,380,815$** | 86.71% | 
| **3.0% ROI** | **$86,671,786,011$** | 89.91% | 
| **4.0% ROI** | **$89,756,191,208$** | 93.11% | 
| **5.0% ROI** | **$92,840,596,404$** | 96.31% | 

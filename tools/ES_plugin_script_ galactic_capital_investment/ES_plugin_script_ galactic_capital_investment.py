import os

STOCKS =[
	{'name': 'Southbound Shipyards', 'init': 1322, 'type': 'Dividend', 'abbr': 'sb'},
	{'name': 'Lionheart Shipyards', 'init': 976, 'type': 'Growth', 'abbr': 'li'},
	{'name': 'Megaparsec Shipyards', 'init': 1110, 'type': 'Growth', 'abbr': 'me'},
	{'name': 'Syndicate Shipyards', 'init': 1692, 'type': 'Dividend', 'abbr': 'sy'},
	{'name': 'Kraz Cybernetics', 'init': 1451, 'type': 'Dividend', 'abbr': 'kz'},
	{'name': 'Deep Sky', 'init': 837, 'type': 'Growth', 'abbr': 'ds'},
	{'name': 'Lovelace Labs', 'init': 1791, 'type': 'Dividend', 'abbr': 'll'},
	{'name': 'Delta V', 'init': 788, 'type': 'Growth', 'abbr': 'dv'},
	{'name': 'Betelgeuse Shipyards', 'init': 1224, 'type': 'Dividend', 'abbr': 'be'},
	{'name': 'Tarazed Corporation', 'init': 676, 'type': 'Growth', 'abbr': 'ta'}
]

DIVIDEND_TIERS =[1000000000, 100000000, 10000000, 1000000, 100000, 10000, 1000, 100, 10, 1]
STOCK_TIERS =[10000000000, 1000000000, 100000000, 10000000, 1000000, 100000, 10000, 1000, 100, 10, 1]
MONEY_TIERS =[1000000000000, 100000000000, 10000000000, 1000000000, 100000000, 10000000, 1000000, 100000, 10000, 1000, 100, 10, 1]

def fmt(n):
	mapping = {	
		1000000000000: "1 trillion",
		100000000000: "100 billion",
		10000000000: "10 billion",
		1000000000: "1 billion",
		100000000: "100 million",
		10000000: "10 million",
		1000000: "1 million",
		100000: "100,000",
		10000: "10,000",
		1000: "1,000",
		100: "100",
		10: "10",
		1: "1"
	}
	return mapping.get(n, str(n))

base_indent="\t\t\t\t"

def gen_fluctuation(stock):		
	name = stock['name']
	is_div = stock['type'] == 'Dividend'
	m_base = "10200" if is_div else "10400"
	r2 = "7" if is_div else "16"
	r3 = "22" if is_div else "39"
	r4 = "45" if is_div else "43"
	r5 = "88" if is_div else "75"
	m2 = "9800" if is_div else "9600"
	m3 = "9900" if is_div else "9800"
	m5 = "10100" if is_div else "10200"
	lbl = "dividend" if is_div else "growth"
	
	return f"""{base_indent[:-1]}action
{base_indent}"stock roll {name}" = "roll: 100"
{base_indent}"stock multiplier {name}" = {m_base}
{base_indent[:-1]}branch "{lbl} roll 1 {name}"
{base_indent}"stock roll {name}" == 1
{base_indent[:-1]}branch "{lbl} roll 2 {name}"
{base_indent}"stock roll {name}" <= {r2}
{base_indent[:-1]}branch "{lbl} roll 3 {name}"
{base_indent}"stock roll {name}" <= {r3}
{base_indent[:-1]}branch "{lbl} roll 4 {name}"
{base_indent}"stock roll {name}" <= {r4}
{base_indent[:-1]}branch "{lbl} roll 5 {name}"
{base_indent}"stock roll {name}" <= {r5}
{base_indent[:-1]}branch "apply {name}"
{base_indent[:-1]}label "{lbl} roll 1 {name}"
{base_indent[:-1]}action
{base_indent}"stock multiplier {name}" = 8874
{base_indent[:-1]}branch "apply {name}"
{base_indent[:-1]}label "{lbl} roll 2 {name}"
{base_indent[:-1]}action
{base_indent}"stock multiplier {name}" = {m2}
{base_indent[:-1]}branch "apply {name}"
{base_indent[:-1]}label "{lbl} roll 3 {name}"
{base_indent[:-1]}action
{base_indent}"stock multiplier {name}" = {m3}
{base_indent[:-1]}branch "apply {name}"
{base_indent[:-1]}label "{lbl} roll 4 {name}"
{base_indent[:-1]}action
{base_indent}"stock multiplier {name}" = 10000
{base_indent[:-1]}branch "apply {name}"
{base_indent[:-1]}label "{lbl} roll 5 {name}"
{base_indent[:-1]}action
{base_indent}"stock multiplier {name}" = {m5}
{base_indent[:-1]}label "apply {name}"
{base_indent[:-1]}action
{base_indent}"stock value {name}" = "stock value {name}" * "stock multiplier {name}" / 10000
{base_indent[:-1]}branch "floor check {name}"
{base_indent}"stock value {name}" >= 100
{base_indent[:-1]}action
{base_indent}"stock value {name}" *= 10
{base_indent}"stock amount {name}" /=  10
{base_indent[:-1]}label "floor check {name}"
{base_indent[:-1]}branch "ceil check {name}"
{base_indent}"stock value {name}" <= 10000
{base_indent[:-1]}action
{base_indent}"stock value {name}" /= 10
{base_indent}"stock amount {name}" *= 10
{base_indent[:-1]}label "ceil check {name}"
\n"""

BASE_TEMPLATE = """# See ES_plugin_script_galactic_capital_investment.py for the code that generates this script.

mission "gci init"
	non-blocking
	invisible
	landing
	repeat
	to offer
		or
			"stock value Delta V = 0"
			not "gci init: failed"
	on offer
		lastvisit = "days since start"
		"stock last day" = "days since start"
%SETUP_VARS%
		fail

mission "gci banking account update"
	non-blocking
	invisible
	repeat
	landing
	to offer
		has "gci init: failed"
	on offer
		datedifference = "days since start" - lastvisit
		lastvisit = "days since start"
		dailyincome = deposit * 149 / 100000 - "salary: Galactic Capital Transfer"
		deposit += datedifference * dailyincome
		fail

mission "gci stock dividends"
	entering
	invisible
	repeat
	non-blocking
	destination "Earth"
	to offer
		"day" == 1
		or
%DIVIDEND_OFFER_CONDITIONS%
	on offer
		conversation
			label "start"
			action
				"passed days" = "days since start" - "stock last day"
			``
			label "days loop"
			branch "end"
				"passed days" == 0
%DIVIDEND_FLUCTUATIONS%
			action
				"passed days" -= 1
			branch "days loop"
			label "end"
			action
				"stock last day" = "days since start"
			branch "monthly anchor update"
				"day" == 1
			branch "monthly anchor update end"
			label "monthly anchor update"
			action
%DIVIDEND_ANCHORS%
			label "monthly anchor update end"
			action
%DIVIDEND_MATH%
%DIVIDEND_WATERFALL%
			label "dividends payment done"
			scene "scene/stock_chart_analysis"
			`This is your monthly stock report and dividend payout.`
%DIVIDEND_DISPLAY%
			``
			`All dividend payouts: &[stock all dividends]`
				decline

mission "gci banking terminal"
	name "Galactic Capital Investment"
	color selected "gci job: selected"
	color unselected "gci job: unselected"
	description "Smart Captains invest their money."
	job
	repeat
	"apparent payment" 99999999999999999999999999999999
	"offer precedence" 9999999
	priority
	to offer
		has "gci init: failed"
	on accept
		conversation
			action
				"passed days" = "days since start" - "stock last day"
			label "calculations loop"
			branch "calculations end"
				"passed days" == 0
%TERMINAL_FLUCTUATIONS%
			action
				"passed days" -= 1
			branch "calculations loop"
			label "calculations end"
			action
				"stock last day" = "days since start"
			label singleline
				goto menu
			label menu
			action
				bankroute = 1
			goto "calc bank values"
			label "calc bank values return menu"
			scene scene/gci_terminal
			action
				stockroute = 1
			goto "calc stocktotal"
			label "calc stocktotal return menu"
			action		
%TOTAL_PRINCIPAL_ACTIONS%
				"current_val_total" = "stocktotalvalue"
			branch "calc total roi"
				"total_principal" > 0
			action
				"total_up_alltime" = 0
			branch "calc total roi end"
			label "calc total roi"
			action
				"total_roi" = "current_val_total" * 100 / "total_principal"
				"total_up_alltime" = "total_roi" - 100
			label "calc total roi end"

			`Welcome to "Galactic Capital Investment Service"! Your last visit is &[datedifference] day/s ago.`
			``
			`Cash chip balance:`
			`	&[credits] credits`
			`Savings account balance:`
			`	&[deposit] credits`
			`	&[dailyincome] credits daily interest + &[salary: Galactic Capital Transfer] credits daily cash withdrawals`
			``
			`Daily investment salary to your cash chip: &[salary: GCI Private Markets] credits`
			`Stock Portfolio value: &[stocktotalvalue] credits (up &[total_up_alltime]% all-time)`
			`Family trust: &[global: familytrust] credits (0% monthly, for all pilots)`
			``
			choice
				`	[access to your savings account]`
					goto linebankaccount
				`	[access to your family trust]`
					goto linefamilytrust
				`	[access to your daily cash withdrawal]`
					goto linecashtransfer
				`	[access to the stock exchange]`
					goto linestockexchange
				`	[sell investments]`
					to display
						"salary: Galactic Capital" > 0
					goto linesellinvestment
				`	[enable GCI missions and private investments]`
					to display
						not "global: gcijobs active"
					goto setjobs1
				`	[disable GCI missions and private investments]`
					to display
						has "global: gcijobs active"
					goto setjobs0
				`	[leave]`
					goto end

%BANK_MENUS%

			label "calc bank values"
			action
				dailyincome = deposit * 149 / 100000 - "salary: Galactic Capital Transfer"
				available = "salary: Galactic Capital Transfer" * 100000
				available /= 149
				available *= -1
				available += deposit
			branch "calc bank values return menu"
				bankroute == 1
			branch "calc bank values return bankaccount"
				bankroute == 2
			branch "calc bank values return bankaccountD"
				bankroute == 3
			branch "calc bank values return bankaccountW"
				bankroute == 4
			branch "calc bank values return cashtransfer"
				bankroute == 5
			branch "calc bank values return transfert"
				bankroute == 6
			branch "calc bank values return transferb"
				bankroute == 7
			branch "menu"

			label "calc stocktotal"
			%CALC_STOCKTOTAL_BLOCK%
			branch "calc stocktotal return menu"
				stockroute == 1
			branch "calc stocktotal return stockoverview"
				stockroute == 2
%CALC_STOCKTOTAL_BRANCHES%
			branch "stockoverview"

			label linestockexchange
			``
				goto stockoverview
			label "linestockoverview"
			``
			label "stockoverview"
			action
				stockroute = 2
			goto "calc stocktotal"
			label "calc stocktotal return stockoverview"
			scene "scene/stock_chart_analysis"
			`Welcome to Galactic Stock Exchange`
			``
			`Cash chip balance: &[credits]`
			`Portfolio Value: &[stocktotalvalue] credits (up &[total_up_alltime]% all-time)`
			``
			`Stock Categories:`
			`  Dividend Stocks: These companies pay you a steady 1.22% cash dividend every month based on your share value.`
			`  Growth Stocks: These companies do not pay dividends in exchange for potentially higher returns in share price.`
			``
			choice
%STOCK_OVERVIEW_CHOICES%
				`	[back]`
					goto clearscreen

%INDIVIDUAL_STOCK_PAGES%

%STOCK_WATERFALLS%

			label setjobs0
			action
				clear "global: gcijobs active"
			`Job board investments/missions are hidden now.`
				goto menu
			label setjobs1
			action
				set "global: gcijobs active"
			`Job board investments/missions are shown now.`
				goto menu

			label clearscreen
			``
				goto menu
			label end
			``
			scene scene/gci_terminal
			`Thank you for being a valued customer at Galactic Capital Investments!`
				decline
		fail
"""

def build_script():
	# 1. SETUP_VARS
	setup_vars = ""
	for s in STOCKS:
		setup_vars += f'{base_indent[:-2]}"stock value {s["name"]}" = {s["init"]}\n'
		setup_vars += f'{base_indent[:-2]}"{s["abbr"]}_anchor_monthly" = {s["init"]}\n'
		setup_vars += f'{base_indent[:-2]}"stock amount {s["name"]}" = 0\n'
		setup_vars += f'{base_indent[:-2]}"{s["abbr"]}_avg_price" = 0\n'
		setup_vars += f'{base_indent[:-2]}"{s["abbr"]}_daily_notional_volume" = 0\n'

	# 2. DIVIDENDS
	div_cond = ""
	for s in STOCKS:
		if s['type'] == 'Dividend':
			div_cond += f'{base_indent[:-1]}"stock amount {s["name"]}" > 0\n'
		
	div_fluc = ""
	for s in STOCKS:
		div_fluc += gen_fluctuation(s)

	div_anchors = ""
	for s in STOCKS:
		div_anchors += f'{base_indent}"{s["abbr"]}_anchor_monthly" = "stock value {s["name"]}"\n'

	div_math = ""
	div_adds =[]
	for s in STOCKS:
		if s['type'] == 'Dividend':
			div_math += f'{base_indent}"dividend {s["name"]}" = "stock amount {s["name"]}" * "stock value {s["name"]}" * 1217 / 100000\n'
			div_adds.append(f'"dividend {s["name"]}"')
		else:
			div_math += f'{base_indent}"dividend {s["name"]}" = 0\n'
			div_adds.append(f'"dividend {s["name"]}"')

	div_math += f'{base_indent}"stock dividends addi" = {" + ".join(div_adds)}\n'
	div_math += f'{base_indent}"stock all dividends" = "stock dividends addi"\n'

	div_wf = ""
	for i in range(len(DIVIDEND_TIERS)):
		tier = DIVIDEND_TIERS[i]
		next_lbl = DIVIDEND_TIERS[i+1] if i + 1 < len(DIVIDEND_TIERS) else "done"
		div_wf += f'{base_indent[:-1]}label "dividends payment {tier}"\n'
		div_wf += f'{base_indent[:-1]}branch "dividends payment {next_lbl}"\n'
		div_wf += f'{base_indent}"stock dividends addi" < {tier}\n'
		div_wf += f'{base_indent[:-1]}action\n'
		div_wf += f'{base_indent}payment {tier}\n'
		div_wf += f'{base_indent}"stock dividends addi" -= {tier}\n'
		div_wf += f'{base_indent[:-1]}branch "dividends payment {tier}"\n\n'

	div_disp = ""
	for s in STOCKS:
		rate = "1.22%" if s['type'] == 'Dividend' else "0%"
		div_disp += f'{base_indent[:-1]}`You hold &[stock amount {s["name"]}] "{s["name"]}" stocks at &[stock value {s["name"]}] credits each. Monthly dividend ({rate}): &[dividend {s["name"]}]`\n'
		div_disp += f'{base_indent}to display\n'
		div_disp += f'{base_indent}\t"stock amount {s["name"]}" > 0\n'

	# 3. TERMINAL FLUCTUATIONS
	term_fluc = ""
	for s in STOCKS:
		term_fluc += f'{base_indent}"{s["abbr"]}_daily_notional_volume" = 0\n'
	for s in STOCKS:
		term_fluc += gen_fluctuation(s)

# 4. MATH TOTALS
	total_principal_actions = f'{base_indent}"total_principal" = 0\n'
	for s in STOCKS:
		abbr = s['abbr']
		name = s['name']
		total_principal_actions += f'{base_indent}"{abbr}_cost_basis" = "{abbr}_avg_price" * "stock amount {name}"\n'
		total_principal_actions += f'{base_indent}"total_principal" += "{abbr}_cost_basis"\n'

	# 5. BANK MENUS (Omitted generic builders for brevity, preserving exact UI string)
	bank_menus = ""
	# Bank Deposit
	bank_menus += """			label linebankaccount
			``
			label bankaccount
			action
				bankroute = 2
			goto "calc bank values"
			label "calc bank values return bankaccount"
			scene scene/gci_terminal
			`Your savings accounts generates 4.6% risk-free interest every month via Republic Treasury Bonds.`
			`The displayed daily interest is lowered by your cash withdrawals.`
			``
			`Cash chip:`
			`	&[credits] credits`
			`Account balance:`
			`	&[deposit] credits`
			`	&[dailyincome] credits daily interest + &[salary: Galactic Capital Transfer] credits daily cash withdrawals`
			``
			``
			choice
				`	[deposit credits]`
					goto linebankaccountD
				`	[withdraw credits]`
					goto linebankaccountW
				`	[back]`
					goto clearscreen

			label linebankaccountD
			``
			label bankaccountD
			action
				bankroute = 3
			goto "calc bank values"
			label "calc bank values return bankaccountD"
			scene scene/gci_terminal
			`Your savings accounts generates 4.6% risk-free interest every month via Republic Treasury Bonds.`
			`The displayed daily interest is lowered by your cash withdrawals.`
			``
			`Cash chip:`
			`	&[credits] credits`
			`Account balance:`
			`	&[deposit] credits`
			`	&[dailyincome] credits daily interest + &[salary: Galactic Capital Transfer] credits daily cash withdrawals`
			``
			``
			choice\n"""
	for tier in MONEY_TIERS:
		bank_menus += f'{base_indent}`\t[deposit {fmt(tier)} credits]`\n'
		bank_menus += f'{base_indent}\tto display\n'
		bank_menus += f'{base_indent}\t\t"credits" >= {tier}\n'
		bank_menus += f'{base_indent}\tgoto d{tier}\n'
	bank_menus += f'{base_indent}`\t[back]`\n{base_indent}\tgoto linebankaccount\n'

	for tier in MONEY_TIERS:
		bank_menus += f'''			label d{tier}
			action
				payment -{tier}
				deposit += {tier}
				dailyincome = deposit * 149 / 100000 - "salary: Galactic Capital Transfer"
			``
				goto bankaccountD\n'''

	# Bank Withdraw
	bank_menus += """			label linebankaccountW
			``
			label bankaccountW
			action
				bankroute = 4
			goto "calc bank values"
			label "calc bank values return bankaccountW"
			scene scene/gci_terminal
			`Your savings accounts generates 4.6% risk-free interest every month via Republic Treasury Bonds.`
			`The displayed daily interest is lowered by your cash withdrawals.`
			``
			`Cash chip:`
			`	&[credits] credits`
			`Account balance:`
			`	&[deposit] credits`
			`	&[dailyincome] credits daily interest + &[salary: Galactic Capital Transfer] credits daily cash withdrawals`
			`	(to withdraw more credits, reduce your daily cash withdrawals)`
			``
			choice\n"""
	for tier in MONEY_TIERS:
		bank_menus += f'{base_indent}`\t[withdraw {fmt(tier)} credits]`\n'
		bank_menus += f'{base_indent}\tto display\n'
		bank_menus += f'{base_indent}\t\tavailable >= {tier}\n'
		bank_menus += f'{base_indent}\tgoto w{tier}\n'
	bank_menus += f'{base_indent}`\t[back]`\n{base_indent}\tgoto linebankaccount\n'

	for tier in MONEY_TIERS:
		bank_menus += f'''			label w{tier}
			action
				payment {tier}
				deposit -= {tier}
				dailyincome = deposit * 149 / 100000 - "salary: Galactic Capital Transfer"
			``
				goto bankaccountW\n'''

	# Family Trust
	bank_menus += """			label linefamilytrust
			``
			label familytrust
			scene scene/gci_terminal
			`Access to your family trust. This is an account shared between all pilots in your family.`
			``
			`Cash chip:`
			`	&[credits] credits`
			`Family trust:`
			`	&[global: familytrust] credits`
			``
			choice
				`	[deposit credits]`
					goto linefamilytrustD
				`	[withdraw credits]`
					goto linefamilytrustW
				`	[back]`
					goto clearscreen

			label linefamilytrustD
			``
			label familytrustD
			scene scene/gci_terminal
			`Access to your family trust. This is an account shared between all pilots in your family.`
			``
			`Cash chip:`
			`	&[credits] credits`
			`Family trust:`
			`	&[global: familytrust] credits`
			``
			choice\n"""
	for tier in MONEY_TIERS:
		bank_menus += f'{base_indent}`\t[deposit {fmt(tier)} credits]`\n'
		bank_menus += f'{base_indent}\tto display\n'
		bank_menus += f'{base_indent}\t\t"credits" >= {tier}\n'
		bank_menus += f'{base_indent}\tgoto td{tier}\n'
	bank_menus += f'{base_indent}`\t[back]`\n{base_indent}\tgoto linefamilytrust\n'

	for tier in MONEY_TIERS:
		bank_menus += f'''			label td{tier}
			action
				payment -{tier}
				"global: familytrust" += {tier}
			``
				goto familytrustD\n'''

	bank_menus += """			label linefamilytrustW
			``
			label familytrustW
			scene scene/gci_terminal
			`Access to your family trust. This is an account shared between all pilots in your family.`
			``
			`Cash chip:`
			`	&[credits] credits`
			`Family trust:`
			`	&[global: familytrust] credits`
			``
			choice\n"""
	for tier in MONEY_TIERS:
		bank_menus += f'{base_indent}`\t[withdraw {fmt(tier)} credits]`\n'
		bank_menus += f'{base_indent}\tto display\n'
		bank_menus += f'{base_indent}\t\t"global: familytrust" >= {tier}\n'
		bank_menus += f'{base_indent}\tgoto tw{tier}\n'
	bank_menus += f'{base_indent}`\t[back]`\n{base_indent}\tgoto linefamilytrust\n'

	for tier in MONEY_TIERS:
		bank_menus += f'''			label tw{tier}
			action
				payment {tier}
				"global: familytrust" -= {tier}
			``
				goto familytrustW\n'''

	# Cash Transfer
	bank_menus += """			label linecashtransfer
			``
				goto cashtransfer
			label cashtransfer
			action
				bankroute = 5
			goto "calc bank values"
			label "calc bank values return cashtransfer"
			scene scene/gci_terminal
			`Set up daily withdrawals of credits, from you savings account to your cash chip. It must be equal or lower than your daily interest.`
			``
			`Cash chip:`
			`	&[credits] credits`
			`Account balance:`
			`	&[deposit] credits`
			`	&[dailyincome] credits daily interest  + &[salary: Galactic Capital Transfer] credits daily cash withdrawals`
			``
			choice
				`	[transfer credits from daily interest to daily cash withdrawals]`
					to display
						"dailyincome" >= 100
					goto "linetransfert"
				`	[transfer credits from daily cash withdrawals to daily interest]`
					to display
						"salary: Galactic Capital Transfer" >= 100
					goto "linetransferb"
				`	[back]`
					goto clearscreen

			label linetransfert
			``
				goto transfert
			label transfert
			action
				bankroute = 6
			goto "calc bank values"
			label "calc bank values return transfert"
			scene scene/gci_terminal
			`Set up daily withdrawals of credits, from you savings account to your cash chip. It must be equal or lower than your daily interest.`
			``
			`Cash chip:`
			`	&[credits] credits`
			`Account balance:`
			`	&[deposit] credits`
			`	&[dailyincome] credits daily interest  + &[salary: Galactic Capital Transfer] credits daily cash withdrawals`
			``
			choice\n"""
	for tier in MONEY_TIERS:
		bank_menus += f'{base_indent}`\t[transfer {fmt(tier)} credits of your daily interest]`\n'
		bank_menus += f'{base_indent}\tto display\n'
		bank_menus += f'{base_indent}\t\t"dailyincome" >= {tier}\n'
		bank_menus += f'{base_indent}\tgoto t{tier}\n'
	bank_menus += f'{base_indent}`\t[back]`\n{base_indent}\tgoto linecashtransfer\n'

	bank_menus += """			label linetransferb
			``
				goto transferb
			label transferb
			action
				bankroute = 7
			goto "calc bank values"
			label "calc bank values return transferb"
			scene scene/gci_terminal
			`Set up daily withdrawals of credits, from you savings account to your cash chip. It must be equal or lower than your daily interest.`
			``
			`Cash chip:`
			`	&[credits] credits`
			`Account balance:`
			`	&[deposit] credits`
			`	&[dailyincome] credits daily interest  + &[salary: Galactic Capital Transfer] credits daily cash withdrawals`
			``
			choice\n"""
	for tier in MONEY_TIERS:
		bank_menus += f'{base_indent}`\t[transfer {fmt(tier)} credits back to your daily interest]`\n'
		bank_menus += f'{base_indent}\tto display\n'
		bank_menus += f'{base_indent}\t\t"salary: Galactic Capital Transfer" >= {tier}\n'
		bank_menus += f'{base_indent}\tgoto b{tier}\n'
	bank_menus += f'{base_indent}`\t[back]`\n{base_indent}\tgoto linecashtransfer\n'

	for tier in MONEY_TIERS:
		bank_menus += f'''			label t{tier}
			action
				"salary: Galactic Capital Transfer" += {tier}
				dailyincome = deposit * 149 / 100000 - "salary: Galactic Capital Transfer"
			``
				goto transfert\n'''
	for tier in MONEY_TIERS:
		bank_menus += f'''			label b{tier}
			action
				"salary: Galactic Capital Transfer" -= {tier}
				dailyincome = deposit * 149 / 100000 - "salary: Galactic Capital Transfer"
			``
				goto transferb\n'''

# Sell Investment
	bank_menus += """			label linesellinvestment
			``
				goto sellinvestment
			label sellinvestment
			scene scene/gci_terminal
			branch "blood_money_lock"
				has "GCI blood money"
			`Sell your private market equities at a loss for some emergency funds (cannot be reverted).`
			``
			`Cash chip:`
			`	&[credits] credits`
			`Private market annuities:`
			`	&[salary: GCI Private Markets]`
			``
			choice\n"""
	
	for tier in MONEY_TIERS:
		val = int(tier * 70)
		bank_menus += f'{base_indent}`\t[sell investment of {fmt(tier)} daily credits for {fmt(val)} credits]`\n'
		bank_menus += f'{base_indent}\tto display\n'
		bank_menus += f'{base_indent}\t\t"salary: Galactic Capital" >= {tier}\n'
		bank_menus += f'{base_indent}\tgoto si{tier}\n'
	bank_menus += f'{base_indent}`\t[back]`\n{base_indent}\tgoto menu\n'

	bank_menus += """			label "blood_money_lock"
			`I wouldn't do that if I were you, Captain <last>.`
			choice
				`	[back]`
					goto menu\n"""

	for tier in MONEY_TIERS:
		val = int(tier * 70)
		bank_menus += f'''			label si{tier}
			action
				payment {val}
				"salary: Galactic Capital" -= {tier}
			``
				goto sellinvestment\n'''
		
	# 6. CALC STOCKTOTAL
	calc_stocktotal_block = f'{base_indent[:-1]}action\n'
	calc_stock_math_simple = ""
	for s in STOCKS:
		abbr = s['abbr']
		name = s['name']
		calc_stocktotal_block += f'{base_indent}"val {abbr}" = "stock amount {name}" * "stock value {name}"\n'
		calc_stock_math_simple += f'{base_indent}"val {abbr}" = "stock amount {name}" * "stock value {name}"\n'
		calc_stocktotal_block += f'{base_indent[:-1]}branch "calc up monthly zero {abbr}"\n'
		calc_stocktotal_block += f'{base_indent}"{abbr}_anchor_monthly" == 0\n'
		calc_stocktotal_block += f'{base_indent[:-1]}branch "calc up monthly div {abbr}"\n'
		calc_stocktotal_block += f'{base_indent[:-1]}action\n'
		calc_stocktotal_block += f'{base_indent}"{name} up monthly" = 0\n'
		calc_stocktotal_block += f'{base_indent[:-1]}branch "calc up monthly done {abbr}"\n'
		calc_stocktotal_block += f'{base_indent[:-1]}label "calc up monthly div {abbr}"\n'
		calc_stocktotal_block += f'{base_indent[:-1]}action\n'
		calc_stocktotal_block += f'{base_indent}"{name} up monthly" = "stock value {name}" * 100 / "{abbr}_anchor_monthly"\n'
		calc_stocktotal_block += f'{base_indent}"{name} up monthly" -= 100\n'
		calc_stocktotal_block += f'{base_indent[:-1]}label "calc up monthly done {abbr}"\n'
	calc_stocktotal_block += f'{base_indent[:-1]}action\n'
	calc_stocktotal_block += f'{base_indent}stocktotalvalue = ' + ' + '.join([f'"val {s["abbr"]}"' for s in STOCKS]) + '\n'
	calc_stock_math_simple += f'{base_indent}stocktotalvalue = ' + ' + '.join([f'"val {s["abbr"]}"' for s in STOCKS]) + '\n'
	
	calc_stock_branches = ""
	for i, s in enumerate(STOCKS):
		calc_stock_branches += f'{base_indent[:-1]}branch "calc stocktotal return {s["name"]}"\n{base_indent}stockroute == {i+3}\n'

	# 7. STOCK OVERVIEW
	stock_overview_choices = ""
	for s in STOCKS:
		div_txt = "Dividend"
		if s['type'] == 'Growth':
			div_txt = "Growth"
			
		stock_overview_choices += f'{base_indent}`	[{s["name"]} ({div_txt}), price &[stock value {s["name"]}], up &[{s["name"]} up monthly]% this month.]`\n'
		stock_overview_choices += f'{base_indent}\tgoto "line{s["name"]}"\n'

# 8. INDIVIDUAL STOCK PAGES
	stock_pages = ""
	for i, s in enumerate(STOCKS):
		name = s['name']
		abbr = s['abbr']
		
		ui_precalc = ""
		ui_precalc += f'{base_indent}"buy price {name}" = "stock value {name}" * 10130 / 10000\n'
		ui_precalc += f'{base_indent}"sell price {name}" = "stock value {name}" * 9870 / 10000\n'
		ui_precalc += f'{base_indent}"liquidity {name}" = 96400000000\n'
		ui_precalc += f'{base_indent}"liquidity {name}" -= "{abbr}_daily_notional_volume"\n'
		for tier in STOCK_TIERS:
			mult_str = f" {tier}" if tier > 1 else ""
			ui_precalc += f'{base_indent}"buy val {name}{mult_str}" = "buy price {name}" * {tier}\n'
			ui_precalc += f'{base_indent}"sell val {name}{mult_str}" = "sell price {name}" * {tier}\n'

		stock_pages += f'''			label "line{name}"
			``
			label "{name}"
			action
{ui_precalc}
			action
				stockroute = {i+3}
			goto "calc stocktotal"
			label "calc stocktotal return {name}"
			branch "{abbr} alltime zero"
				"{abbr}_avg_price" == 0
			label "{abbr} alltime calc"
			action
				"stock_roi" = "stock value {name}" * 100 / "{abbr}_avg_price"
				"stock_up_alltime" = "stock_roi" - 100
			branch "{abbr} monthly check"
			label "{abbr} alltime zero"
			action
				"stock_up_alltime" = 0
			label "{abbr} monthly check"
			branch "{abbr} monthly zero"
				"{abbr}_anchor_monthly" == 0
			label "{abbr} monthly calc"
			action
				"stock_mtd_roi" = "stock value {name}" * 100 / "{abbr}_anchor_monthly"
				"stock_up_monthly" = "stock_mtd_roi" - 100
			branch "{abbr} monthly done"
			label "{abbr} monthly zero"
			action
				"stock_up_monthly" = 0
			label "{abbr} monthly done"
			scene "scene/stock_chart_analysis"
			`{name}`
			``
			`Cash chip balance: &[credits] credits`
			`Value of all owned stocks: &[stocktotalvalue] credits`
			``
			`You hold: &[stock amount {name}] shares at &[{abbr}_avg_price] credits on average.`
			`Your Position: Up &[stock_up_alltime]% All-Time`
			`Market Trend: Up &[stock_up_monthly]% This Month`
			choice
				`	Buy {name} shares`
					to display
						"credits" >= "buy val {name}"
						"liquidity {name}" >= "buy val {name}"
					goto "lineBuy {name}"
				`	Sell {name} shares`
					to display
						"stock amount {name}" > 0
						"liquidity {name}" >= "sell val {name}"
					goto "lineSell {name}"
				`	[back]`
					goto "linestockoverview"

			label "lineBuy {name}"
			``
			label "Buy {name}"
			action
{ui_precalc}{calc_stock_math_simple}			scene "scene/stock_chart_analysis"
			`{name}`
			``
			`Cash chip balance: &[credits] credits`
			`Value of all owned stocks: &[stocktotalvalue] credits`
			``
			`You hold: &[stock amount {name}] shares at &[{abbr}_avg_price] credits on average.`
			branch "Buy liquidity open {name}"
				"liquidity {name}" >= "buy val {name}"
			`No more sellers today for this stock.`
			choice
				`	[back]`
					goto "line{name}"
			label "Buy liquidity open {name}"
			choice\n'''
		for tier in STOCK_TIERS:
			txt_amt = fmt(tier)
			mult = f" {tier}" if tier > 1 else ""
			stock_pages += f'{base_indent}`	Buy {txt_amt} shares for &[buy val {name}{mult}] credits.`\n'
			stock_pages += f'{base_indent}\tto display\n'
			stock_pages += f'{base_indent}\t\t"credits" >= "buy val {name}{mult}"\n'
			stock_pages += f'{base_indent}\t\t"liquidity {name}" >= "buy val {name}{mult}"\n'
			stock_pages += f'{base_indent}\tgoto "Buy {tier} {name}"\n'
		stock_pages += f'{base_indent}`	[back]`\n{base_indent}\tgoto "line{name}"\n\n'

		stock_pages += f'''			label "lineSell {name}"
			``
			label "Sell {name}"
			action
{ui_precalc}{calc_stock_math_simple}			scene "scene/stock_chart_analysis"
			`{name}`
			``
			`Cash chip balance: &[credits] credits`
			`Value of all owned stocks: &[stocktotalvalue] credits`
			``
			`You hold: &[stock amount {name}] shares at &[{abbr}_avg_price] credits on average.`
			branch "Sell liquidity open {name}"
				"liquidity {name}" >= "sell val {name}"
			`No more buyers today for this stock.`
			choice
				`	[back]`
					goto "line{name}"
			label "Sell liquidity open {name}"
			choice\n'''
		for tier in STOCK_TIERS:
			txt_amt = fmt(tier)
			mult = f" {tier}" if tier > 1 else ""
			stock_pages += f'{base_indent}`	Sell {txt_amt} shares for &[sell val {name}{mult}] credits.`\n'
			stock_pages += f'{base_indent}\tto display\n'
			stock_pages += f'{base_indent}\t\t"stock amount {name}" >= {tier}\n'
			stock_pages += f'{base_indent}\t\t"liquidity {name}" >= "sell val {name}{mult}"\n'
			stock_pages += f'{base_indent}\tgoto "Sell {tier} {name}"\n'
		stock_pages += f'{base_indent}`	[back]`\n{base_indent}\tgoto "line{name}"\n\n'
		
	# 9. STOCK WATERFALLS
	stock_wfs = ""
	for s in STOCKS:
		name = s['name']
		abbr = s['abbr']

		for tier in STOCK_TIERS:
			stock_wfs += f'			label "Buy {tier} {name}"\n'
			stock_wfs += f'			action\n'
			mult_str = f" {tier}" if tier > 1 else ""
			stock_wfs += f'{base_indent}"actual_cost" = "buy val {name}{mult_str}"\n'
			stock_wfs += f'{base_indent}"BEFORE" = "{abbr}_daily_notional_volume"\n'
			stock_wfs += f'{base_indent}"BEFORE" /= 308440520\n'
			stock_wfs += f'{base_indent}"{abbr}_daily_notional_volume" += "actual_cost"\n'
			stock_wfs += f'{base_indent}"AFTER" = "{abbr}_daily_notional_volume"\n'
			stock_wfs += f'{base_indent}"AFTER" /= 308440520\n'
			stock_wfs += f'{base_indent}"IMPACT" = "AFTER"\n'
			stock_wfs += f'{base_indent}"IMPACT" -= "BEFORE"\n'
			stock_wfs += f'{base_indent}"stock value {name}" += "IMPACT"\n'
			stock_wfs += f'{base_indent}"temp_hist" = "{abbr}_avg_price" * "stock amount {name}"\n'
			stock_wfs += f'{base_indent}"temp_hist" += "actual_cost"\n'
			stock_wfs += f'{base_indent}"temp_vol" = "stock amount {name}" + {tier}\n'
			stock_wfs += f'{base_indent[:-1]}branch "avg price zero {abbr} {tier}"\n'
			stock_wfs += f'{base_indent}"temp_vol" == 0\n'
			stock_wfs += f'{base_indent[:-1]}branch "avg price div {abbr} {tier}"\n'
			stock_wfs += f'{base_indent[:-1]}action\n'
			stock_wfs += f'{base_indent}"{abbr}_avg_price" = 0\n'
			stock_wfs += f'{base_indent[:-1]}branch "avg price done {abbr} {tier}"\n'
			stock_wfs += f'{base_indent[:-1]}label "avg price div {abbr} {tier}"\n'
			stock_wfs += f'{base_indent[:-1]}action\n'
			stock_wfs += f'{base_indent}"{abbr}_avg_price" = "temp_hist" / "temp_vol"\n'
			stock_wfs += f'{base_indent[:-1]}label "avg price done {abbr} {tier}"\n'
			stock_wfs += f'{base_indent[:-1]}action\n'
			stock_wfs += f'{base_indent}"stock amount {name}" += {tier}\n'
			stock_wfs += f'{base_indent}"waterfall_cost" = "actual_cost"\n'
			stock_wfs += f'{base_indent[:-1]}`Bought {fmt(tier)} {name}`\n'
			stock_wfs += f'{base_indent}goto "buy stocks {name}"\n\n'

		for tier in STOCK_TIERS:
			stock_wfs += f'			label "Sell {tier} {name}"\n'
			stock_wfs += f'			action\n'
			mult_str = f" {tier}" if tier > 1 else ""
			stock_wfs += f'{base_indent}"actual_cost" = "sell val {name}{mult_str}"\n'
			stock_wfs += f'{base_indent}"BEFORE" = "{abbr}_daily_notional_volume"\n'
			stock_wfs += f'{base_indent}"BEFORE" /= 308440520\n'
			stock_wfs += f'{base_indent}"{abbr}_daily_notional_volume" += "actual_cost"\n'
			stock_wfs += f'{base_indent}"AFTER" = "{abbr}_daily_notional_volume"\n'
			stock_wfs += f'{base_indent}"AFTER" /= 308440520\n'
			stock_wfs += f'{base_indent}"IMPACT" = "AFTER"\n'
			stock_wfs += f'{base_indent}"IMPACT" -= "BEFORE"\n'
			stock_wfs += f'{base_indent}"stock value {name}" -= "IMPACT"\n'
			stock_wfs += f'{base_indent[:-1]}branch "friction floor done {abbr} {tier}"\n'
			stock_wfs += f'{base_indent}"stock value {name}" >= 100\n'
			stock_wfs += f'{base_indent[:-1]}action\n'
			stock_wfs += f'{base_indent}"stock value {name}" = 100\n'
			stock_wfs += f'{base_indent[:-1]}label "friction floor done {abbr} {tier}"\n'
			stock_wfs += f'{base_indent[:-1]}action\n'
			stock_wfs += f'{base_indent}"stock amount {name}" -= {tier}\n'
			stock_wfs += f'{base_indent}"waterfall_cost" = "actual_cost"\n'
			stock_wfs += f'{base_indent[:-1]}`Sold {fmt(tier)} {name}`\n'
			stock_wfs += f'{base_indent}goto "sell stocks {name}"\n\n'

		stock_wfs += f'			label "buy stocks {name}"\n'
		for i in range(len(MONEY_TIERS)):
			tier = MONEY_TIERS[i]
			next_tier = MONEY_TIERS[i+1] if i + 1 < len(MONEY_TIERS) else "end"
			stock_wfs += f'''			label "buy stocks {tier} {name}"
			branch "buy stocks {next_tier} {name}"
				"waterfall_cost" < {tier}
			action
				payment -{tier}
				"waterfall_cost" -= {tier}
			branch "buy stocks {tier} {name}"\n'''
		
		stock_wfs += f'''			label "buy stocks end {name}"
			branch "Buy {name}"\n\n'''

		stock_wfs += f'			label "sell stocks {name}"\n'
		for i in range(len(MONEY_TIERS)):
			tier = MONEY_TIERS[i]
			next_tier = MONEY_TIERS[i+1] if i + 1 < len(MONEY_TIERS) else "end"
			stock_wfs += f'''			label "sell stocks {tier} {name}"
			branch "sell stocks {next_tier} {name}"
				"waterfall_cost" < {tier}
			action
				payment {tier}
				"waterfall_cost" -= {tier}
			branch "sell stocks {tier} {name}"\n'''
			
		stock_wfs += f'''			label "sell stocks end {name}"
			branch "Sell {name}"\n\n'''

	# INJECT INTO TEMPLATE
	output = BASE_TEMPLATE
	output = output.replace('%SETUP_VARS%', setup_vars)
	output = output.replace('%DIVIDEND_OFFER_CONDITIONS%', div_cond)
	output = output.replace('%DIVIDEND_FLUCTUATIONS%', div_fluc)
	output = output.replace('%DIVIDEND_ANCHORS%', div_anchors)
	output = output.replace('%DIVIDEND_MATH%', div_math)
	output = output.replace('%DIVIDEND_WATERFALL%', div_wf)
	output = output.replace('%DIVIDEND_DISPLAY%', div_disp)
	
	output = output.replace('%TERMINAL_FLUCTUATIONS%', term_fluc)
	output = output.replace('%TOTAL_PRINCIPAL_ACTIONS%', total_principal_actions)
	
	output = output.replace('%BANK_MENUS%', bank_menus)
	output = output.replace('%CALC_STOCKTOTAL_BLOCK%', calc_stocktotal_block)
	output = output.replace('%CALC_STOCKTOTAL_BRANCHES%', calc_stock_branches)
	output = output.replace('%STOCK_OVERVIEW_CHOICES%', stock_overview_choices)
	output = output.replace('%INDIVIDUAL_STOCK_PAGES%', stock_pages)
	output = output.replace('%STOCK_WATERFALLS%', stock_wfs)

	with open('gci_banking.txt', 'w') as f:
		f.write(output)

if __name__ == "__main__":
	build_script()
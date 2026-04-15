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

FRICTION = {
	10000000000: {"buy": 1636644, "sell": 363356},
	1000000000:  {"buy": 1201325, "sell": 798675},
	100000000:   {"buy": 1063664, "sell": 936336},
	10000000:	{"buy": 1020132, "sell": 979868},
	1000000:	 {"buy": 1006366, "sell": 993634},
	100000:	  {"buy": 1002013, "sell": 997987},
	10000:	   {"buy": 1000637, "sell": 999363},
	1000:	   {"buy": 1000201, "sell": 999799}
}

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

def gen_fluctuation(stock, indent="\t\t\t\t"):		
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
	
	return f"""{indent[:-1]}action
{indent}"stock roll {name}" = "roll: 100"
{indent}"stock multiplier {name}" = {m_base}
{indent[:-1]}branch "{lbl} roll 1 {name}"
{indent}"stock roll {name}" == 1
{indent[:-1]}branch "{lbl} roll 2 {name}"
{indent}"stock roll {name}" <= {r2}
{indent[:-1]}branch "{lbl} roll 3 {name}"
{indent}"stock roll {name}" <= {r3}
{indent[:-1]}branch "{lbl} roll 4 {name}"
{indent}"stock roll {name}" <= {r4}
{indent[:-1]}branch "{lbl} roll 5 {name}"
{indent}"stock roll {name}" <= {r5}
{indent[:-1]}branch "apply {name}"
{indent[:-1]}label "{lbl} roll 1 {name}"
{indent[:-1]}action
{indent}"stock multiplier {name}" = 8874
{indent[:-1]}branch "apply {name}"
{indent[:-1]}label "{lbl} roll 2 {name}"
{indent[:-1]}action
{indent}"stock multiplier {name}" = {m2}
{indent[:-1]}branch "apply {name}"
{indent[:-1]}label "{lbl} roll 3 {name}"
{indent[:-1]}action
{indent}"stock multiplier {name}" = {m3}
{indent[:-1]}branch "apply {name}"
{indent[:-1]}label "{lbl} roll 4 {name}"
{indent[:-1]}action
{indent}"stock multiplier {name}" = 10000
{indent[:-1]}branch "apply {name}"
{indent[:-1]}label "{lbl} roll 5 {name}"
{indent[:-1]}action
{indent}"stock multiplier {name}" = {m5}
{indent[:-1]}label "apply {name}"
{indent[:-1]}action
{indent}"stock value {name}" = "stock value {name}" * "stock multiplier {name}" / 10000
{indent[:-1]}branch "floor check {name}"
{indent}"stock value {name}" >= 100
{indent[:-1]}action
{indent}"stock value {name}" = "stock value {name}" = 1000
{indent}"stock amount {name}" = "stock amount {name}" % 10
{indent[:-1]}label "floor check {name}"
{indent[:-1]}branch "ceil check {name}"
{indent}"stock value {name}" <= 10000
{indent[:-1]}action
{indent}"stock value {name}" = "stock value {name}" = 1000
{indent}"stock amount {name}" = "stock amount {name}" * 10
{indent[:-1]}label "ceil check {name}"
\n"""

BASE_TEMPLATE = """# See ES_plugin_script_galactic_capital_investment.py for the code that generates this script.
	mission "gci banking account initial"
	non-blocking
	invisible
	landing
	on offer
		lastvisit = "days since start"
		fail

mission "gci banking account update"
	non-blocking
	invisible
	repeat
	landing
	to offer
		has "gci banking account initial: failed"
	on offer
		datedifference = "days since start" - lastvisit
		lastvisit = "days since start"
		dailyincome = deposit * 149 / 100000 - "salary: Galactic Capital Transfer"
		deposit += datedifference * dailyincome
		fail

mission "gci stock setup"
	landing
	invisible
	repeat
	to offer
		"stock value Delta V" = 0
	on offer
		action
			"stock last day" = "days since start"
%SETUP_VARS%
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
	description "Access to your savings account, family trust, cash withdrawals, and investments."
	job
	repeat
	"apparent payment" 99999999999999999999999999999999
	"offer precedence" 9999999
	priority
	to offer
		has "gci banking account initial: failed"
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
			`Daily investment salary to your cash chip: &[salary: Galactic Capital] credits`
			`Stock portfolio value: &[stocktotalvalue] credits`
			`Family trust: &[global: familytrust] credits (0% monthly, for all pilots)`
			`GCI Portfolio Performance: Up &[total_up_alltime]% All-Time`
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
			action
%CALC_STOCKTOTAL_MATH%
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
			`Value of all owned stocks: &[stocktotalvalue] credits`
			`Stock portfolio Performance: Up &[total_up_alltime]% All-Time`
			``
			`Stock Categories:`
			`  Dividend Stocks: These companies pay you a steady 1.22% cash dividend every month based on your share value.`
			`  Growth Stocks: These companies do not pay dividends, but their share prices are more volatile. High risk, high reward.`
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
		setup_vars += f'\t\t\t"stock value {s["name"]}" = {s["init"]}\n'
		setup_vars += f'\t\t\t"{s["abbr"]}_anchor_monthly" = {s["init"]}\n'
		setup_vars += f'\t\t\t"stock amount {s["name"]}" = 0\n'
		setup_vars += f'\t\t\t"{s["abbr"]}_avg_price" = 0\n'

	# 2. DIVIDENDS
	div_cond = ""
	for s in STOCKS:
		if s['type'] == 'Dividend':
			div_cond += f'\t\t\t"stock amount {s["name"]}" > 0\n'
		
	div_fluc = ""
	for s in STOCKS:
		div_fluc += gen_fluctuation(s, "\t\t\t\t")

	div_anchors = ""
	for s in STOCKS:
		div_anchors += f'\t\t\t\t"{s["abbr"]}_anchor_monthly" = "stock value {s["name"]}"\n'

	div_math = ""
	div_adds =[]
	for s in STOCKS:
		if s['type'] == 'Dividend':
			div_math += f'\t\t\t\t"dividend {s["name"]}" = "stock amount {s["name"]}" * "stock value {s["name"]}" * 1217 / 100000\n'
			div_adds.append(f'"dividend {s["name"]}"')
		else:
			div_math += f'\t\t\t\t"dividend {s["name"]}" = 0\n'
			div_adds.append(f'"dividend {s["name"]}"')

	div_math += f'\t\t\t\t"stock dividends addi" = {" + ".join(div_adds)}\n'
	div_math += '\t\t\t\t"stock all dividends" = "stock dividends addi"\n'

	div_wf = ""
	for i in range(len(DIVIDEND_TIERS)):
		tier = DIVIDEND_TIERS[i]
		next_lbl = DIVIDEND_TIERS[i+1] if i + 1 < len(DIVIDEND_TIERS) else "done"
		div_wf += f'\t\t\tlabel "dividends payment {tier}"\n'
		div_wf += f'\t\t\tbranch "dividends payment {next_lbl}"\n'
		div_wf += f'\t\t\t\t"stock dividends addi" < {tier}\n'
		div_wf += f'\t\t\taction\n'
		div_wf += f'\t\t\t\tpayment {tier}\n'
		div_wf += f'\t\t\t\t"stock dividends addi" -= {tier}\n'
		div_wf += f'\t\t\tbranch "dividends payment {tier}"\n\n'

	div_disp = ""
	for s in STOCKS:
		rate = "1.22%" if s['type'] == 'Dividend' else "0%"
		div_disp += f'\t\t\t`You hold &[stock amount {s["name"]}] "{s["name"]}" stocks at &[stock value {s["name"]}] credits each. Monthly dividend ({rate}): &[dividend {s["name"]}]`\n'
		div_disp += f'\t\t\t\tto display\n'
		div_disp += f'\t\t\t\t\t"stock amount {s["name"]}" > 0\n'

	# 3. TERMINAL FLUCTUATIONS
	term_fluc = ""
	for s in STOCKS:
		term_fluc += gen_fluctuation(s, "\t\t\t\t")

	# 4. MATH TOTALS
	total_principal_actions = '\t\t\t\t\t"total_principal" = 0\n'
	for s in STOCKS:
		abbr = s['abbr']
		name = s['name']
		total_principal_actions += f'\t\t\t\t\t"{abbr}_cost_basis" = "{abbr}_avg_price" * "stock amount {name}"\n'
		total_principal_actions += f'\t\t\t\t\t"total_principal" += "{abbr}_cost_basis"\n'

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
		bank_menus += f'\t\t\t\t`\t[deposit {fmt(tier)} credits]`\n'
		bank_menus += f'\t\t\t\t\tto display\n'
		bank_menus += f'\t\t\t\t\t\t"credits" >= {tier}\n'
		bank_menus += f'\t\t\t\t\tgoto d{tier}\n'
	bank_menus += '\t\t\t\t`\t[back]`\n\t\t\t\t\tgoto linebankaccount\n'

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
		bank_menus += f'\t\t\t\t`\t[withdraw {fmt(tier)} credits]`\n'
		bank_menus += f'\t\t\t\t\tto display\n'
		bank_menus += f'\t\t\t\t\t\tavailable >= {tier}\n'
		bank_menus += f'\t\t\t\t\tgoto w{tier}\n'
	bank_menus += '\t\t\t\t`\t[back]`\n\t\t\t\t\tgoto linebankaccount\n'

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
		bank_menus += f'\t\t\t\t`\t[deposit {fmt(tier)} credits]`\n'
		bank_menus += f'\t\t\t\t\tto display\n'
		bank_menus += f'\t\t\t\t\t\t"credits" >= {tier}\n'
		bank_menus += f'\t\t\t\t\tgoto td{tier}\n'
	bank_menus += '\t\t\t\t`\t[back]`\n\t\t\t\t\tgoto linefamilytrust\n'

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
		bank_menus += f'\t\t\t\t`\t[withdraw {fmt(tier)} credits]`\n'
		bank_menus += f'\t\t\t\t\tto display\n'
		bank_menus += f'\t\t\t\t\t\t"global: familytrust" >= {tier}\n'
		bank_menus += f'\t\t\t\t\tgoto tw{tier}\n'
	bank_menus += '\t\t\t\t`\t[back]`\n\t\t\t\t\tgoto linefamilytrust\n'

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
		bank_menus += f'\t\t\t\t`\t[transfer {fmt(tier)} credits of your daily interest]`\n'
		bank_menus += f'\t\t\t\t\tto display\n'
		bank_menus += f'\t\t\t\t\t\t"dailyincome" >= {tier}\n'
		bank_menus += f'\t\t\t\t\tgoto t{tier}\n'
	bank_menus += '\t\t\t\t`\t[back]`\n\t\t\t\t\tgoto linecashtransfer\n'

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
		bank_menus += f'\t\t\t\t`\t[transfer {fmt(tier)} credits back to your daily interest]`\n'
		bank_menus += f'\t\t\t\t\tto display\n'
		bank_menus += f'\t\t\t\t\t\t"salary: Galactic Capital Transfer" >= {tier}\n'
		bank_menus += f'\t\t\t\t\tgoto b{tier}\n'
	bank_menus += '\t\t\t\t`\t[back]`\n\t\t\t\t\tgoto linecashtransfer\n'

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
			`	&[salary: Galactic Capital]`
			``
			choice\n"""
	
	for tier in MONEY_TIERS:
		val = int(tier * 70)
		bank_menus += f'\t\t\t\t`\t[sell investment of {fmt(tier)} daily credits for {fmt(val)} credits]`\n'
		bank_menus += f'\t\t\t\t\tto display\n'
		bank_menus += f'\t\t\t\t\t\t"salary: Galactic Capital" >= {tier}\n'
		bank_menus += f'\t\t\t\t\tgoto si{tier}\n'
	bank_menus += '\t\t\t\t`\t[back]`\n\t\t\t\t\tgoto menu\n'

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
	calc_stock_math = ""
	for s in STOCKS:
		calc_stock_math += f'\t\t\t\t"val {s["abbr"]}" = "stock amount {s["name"]}" * "stock value {s["name"]}"\n'
		calc_stock_math += f'\t\t\t\t"{s["name"]} up monthly" = "stock value {s["name"]}" * 100 / "{s["abbr"]}_anchor_monthly"\n'
		calc_stock_math += f'\t\t\t\t"{s["name"]} up monthly" -= 100\n'
	calc_stock_math += '\t\t\t\tstocktotalvalue = ' + ' + '.join([f'"val {s["abbr"]}"' for s in STOCKS]) + '\n'
	
	calc_stock_branches = ""
	for i, s in enumerate(STOCKS):
		calc_stock_branches += f'\t\t\tbranch "calc stocktotal return {s["name"]}"\n\t\t\t\tstockroute == {i+3}\n'

	# 7. STOCK OVERVIEW
	stock_overview_choices = ""
	for s in STOCKS:
		div_txt = "Dividend"
		if s['type'] == 'Growth':
			div_txt = "Growth"
			
		stock_overview_choices += f'\t\t\t\t`	[{s["name"]} ({div_txt}), price &[stock value {s["name"]}], up &[{s["name"]} up monthly]% this month.]`\n'
		stock_overview_choices += f'\t\t\t\t\tgoto "line{s["name"]}"\n'

# 8. INDIVIDUAL STOCK PAGES
	stock_pages = ""
	for i, s in enumerate(STOCKS):
		name = s['name']
		abbr = s['abbr']
		
		ui_precalc = ""
		for tier in STOCK_TIERS:
			mult_str = f" {tier}" if tier > 1 else ""
			if tier >= 10000:
				b_mult = FRICTION[tier]['buy']
				s_mult = FRICTION[tier]['sell']
				ui_precalc += f'\t\t\t\t"buy val {name}{mult_str}" = "stock value {name}" * {b_mult} / 1000000 * {tier}\n'
				ui_precalc += f'\t\t\t\t"sell val {name}{mult_str}" = "stock value {name}" * {s_mult} / 1000000 * {tier}\n'
			else:
				ui_precalc += f'\t\t\t\t"buy val {name}{mult_str}" = "stock value {name}" * {tier}\n'
				ui_precalc += f'\t\t\t\t"sell val {name}{mult_str}" = "stock value {name}" * {tier}\n'

		stock_pages += f'''			label "line{name}"
			``
			label "{name}"
			action
{ui_precalc}
			action
				stockroute = {i+3}
			goto "calc stocktotal"
			label "calc stocktotal return {name}"
			branch "{abbr} alltime calc"
				"{abbr}_avg_price" > 0
			action
				"stock_up_alltime" = 0
			branch "{abbr} monthly calc"
			label "{abbr} alltime calc"
			action
				"stock_roi" = "stock value {name}" * 100 / "{abbr}_avg_price"
				"stock_up_alltime" = "stock_roi" - 100
			label "{abbr} monthly calc"
			action
				"stock_mtd_roi" = "stock value {name}" * 100 / "{abbr}_anchor_monthly"
				"stock_up_monthly" = "stock_mtd_roi" - 100
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
					goto "lineBuy {name}"
				`	Sell {name} shares`
					to display
						"stock amount {name}" > 0
					goto "lineSell {name}"
				`	[back]`
					goto "linestockoverview"

			label "lineBuy {name}"
			``
			label "Buy {name}"
			action
{ui_precalc}{calc_stock_math}			scene "scene/stock_chart_analysis"
			`{name}`
			``
			`Cash chip balance: &[credits] credits`
			`Value of all owned stocks: &[stocktotalvalue] credits`
			``
			`You hold: &[stock amount {name}] shares at &[{abbr}_avg_price] credits on average.`
			choice\n'''
		for tier in STOCK_TIERS:
			txt_amt = fmt(tier)
			mult = f" {tier}" if tier > 1 else ""
			stock_pages += f'\t\t\t\t`	Buy {txt_amt} shares for &[buy val {name}{mult}] credits.`\n'
			stock_pages += f'\t\t\t\t\tto display\n'
			stock_pages += f'\t\t\t\t\t\t"credits" >= "buy val {name}{mult}"\n'
			stock_pages += f'\t\t\t\t\tgoto "Buy {tier} {name}"\n'
		stock_pages += f'\t\t\t\t`	[back]`\n\t\t\t\t\tgoto "line{name}"\n\n'

		stock_pages += f'''			label "lineSell {name}"
			``
			label "Sell {name}"
			action
{ui_precalc}{calc_stock_math}			scene "scene/stock_chart_analysis"
			`{name}`
			``
			`Cash chip balance: &[credits] credits`
			`Value of all owned stocks: &[stocktotalvalue] credits`
			``
			`You hold: &[stock amount {name}] shares at &[{abbr}_avg_price] credits on average.`
			choice\n'''
		for tier in STOCK_TIERS:
			txt_amt = fmt(tier)
			mult = f" {tier}" if tier > 1 else ""
			stock_pages += f'\t\t\t\t`	Sell {txt_amt} shares for &[sell val {name}{mult}] credits.`\n'
			stock_pages += f'\t\t\t\t\tto display\n'
			stock_pages += f'\t\t\t\t\t\t"stock amount {name}" >= {tier}\n'
			stock_pages += f'\t\t\t\t\tgoto "Sell {tier} {name}"\n'
		stock_pages += f'\t\t\t\t`	[back]`\n\t\t\t\t\tgoto "line{name}"\n\n'
		
	# 9. STOCK WATERFALLS
	stock_wfs = ""
	for s in STOCKS:
		name = s['name']
		abbr = s['abbr']

		for tier in STOCK_TIERS:
			stock_wfs += f'			label "Buy {tier} {name}"\n'
			stock_wfs += f'			action\n'
			if tier >= 10000:
				b_mult = FRICTION[tier]['buy']
				stock_wfs += f'\t\t\t\t"stock value {name}" = "stock value {name}" * {b_mult} / 1000000\n'
			
			stock_wfs += f'\t\t\t\t"actual_cost" = "stock value {name}" * {tier}\n'
			stock_wfs += f'\t\t\t\t"temp_hist" = "{abbr}_avg_price" * "stock amount {name}"\n'
			stock_wfs += f'\t\t\t\t"temp_hist" += "actual_cost"\n'
			stock_wfs += f'\t\t\t\t"temp_vol" = "stock amount {name}" + {tier}\n'
			stock_wfs += f'\t\t\t\t"{abbr}_avg_price" = "temp_hist" / "temp_vol"\n'
			stock_wfs += f'\t\t\t\t"stock amount {name}" += {tier}\n'
			stock_wfs += f'\t\t\t\t"waterfall_cost" = "actual_cost"\n'
			stock_wfs += f'\t\t\t`Bought {fmt(tier)} {name}`\n'
			stock_wfs += f'\t\t\t\tgoto "buy stocks {name}"\n\n'

		for tier in STOCK_TIERS:
			stock_wfs += f'			label "Sell {tier} {name}"\n'
			stock_wfs += f'			action\n'
			if tier >= 10000:
				s_mult = FRICTION[tier]['sell']
				stock_wfs += f'\t\t\t\t"stock value {name}" = "stock value {name}" * {s_mult} / 1000000\n'
				stock_wfs += f'\t\t\tbranch "friction floor {abbr} {tier}"\n'
				stock_wfs += f'\t\t\t\t"stock value {name}" >= 100\n'
				stock_wfs += f'\t\t\taction\n'
				stock_wfs += f'\t\t\t\t"stock value {name}" = 100\n'
				stock_wfs += f'\t\t\tlabel "friction floor {abbr} {tier}"\n'
				stock_wfs += f'\t\t\taction\n'
			
			stock_wfs += f'\t\t\t\t"actual_cost" = "stock value {name}" * {tier}\n'
			stock_wfs += f'\t\t\t\t"stock amount {name}" -= {tier}\n'
			stock_wfs += f'\t\t\t\t"waterfall_cost" = "actual_cost"\n'
			stock_wfs += f'\t\t\t`Sold {fmt(tier)} {name}`\n'
			stock_wfs += f'\t\t\t\tgoto "sell stocks {name}"\n\n'

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
	output = output.replace('%CALC_STOCKTOTAL_MATH%', calc_stock_math)
	output = output.replace('%CALC_STOCKTOTAL_BRANCHES%', calc_stock_branches)
	output = output.replace('%STOCK_OVERVIEW_CHOICES%', stock_overview_choices)
	output = output.replace('%INDIVIDUAL_STOCK_PAGES%', stock_pages)
	output = output.replace('%STOCK_WATERFALLS%', stock_wfs)

	with open('gci_banking.txt', 'w') as f:
		f.write(output)

if __name__ == "__main__":
	build_script()
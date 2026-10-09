# Sophia's published "people-first" positions on key votes (rubric v2.0). Drafted Oct 8, 2026 for Ron's review.
# Each stance names the documented basis. Votes with no stance are shown on pages but not scored.
import json
C = {
 'cbo_hr1_dist': ('CBO — Distributional effects of H.R. 1 (2025)', 'https://www.cbo.gov/publication/61387'),
 'scotus_ieepa': ('U.S. Supreme Court strikes down IEEPA tariffs — Steptoe (2026)', 'https://www.steptoe.com/en/news-publications/global-trade-and-investment-law-blog/us-supreme-court-strikes-down-ieepa-tariffs.html'),
 'kff_aca': ('KFF projections on the enhanced ACA subsidy lapse (via MEXC News)', 'https://www.mexc.com/news/91669'),
 'sophia_t2': ('Sophia — Trump Second-Term Promise Ledger (t01 OBBBA, t02 tariffs, t05 ACA subsidies, t_crypto)', 'https://bit.ly/sophia-v3#sim/trump2'),
 'aclu_aaa': ('ACLU opposes the Antisemitism Awareness Act — ACLU', 'https://www.aclu.org/documents/aclu-opposes-antisemitism-awareness-act'),
}
S = {
 # pocketbook
 'h118_hjres45_2023': ('no', 'pocketbook', 'Would have overturned the student-loan relief rule and ended the payment pause for borrowers.'),
 's118_hjres45_2023': ('no', 'pocketbook', 'Would have overturned the student-loan relief rule and ended the payment pause for borrowers.'),
 'h118_hr7024_2024': ('yes', 'pocketbook', 'Expanded the refundable child tax credit for lower-income families, alongside business tax breaks.'),
 's118_hr7024_2024': ('yes', 'pocketbook', 'Expanded the refundable child tax credit for lower-income families, alongside business tax breaks.'),
 'h118_hr82_2024': ('yes', 'pocketbook', 'Restored full Social Security benefits to teachers, police, firefighters and others with public pensions.'),
 's118_hr82_2024': ('yes', 'pocketbook', 'Restored full Social Security benefits to teachers, police, firefighters and others with public pensions.'),
 'h119_hr1834_aca_2026': ('yes', 'pocketbook', 'Extends the enhanced ACA premium credits; KFF projects the lapse raises premiums about 75% on average and leaves 4 million more uninsured.', ['kff_aca', 'sophia_t2']),
 's119_aca_ext_2025': ('yes', 'pocketbook', 'Extends the enhanced ACA premium credits; KFF projects the lapse raises premiums about 75% on average and leaves 4 million more uninsured.', ['kff_aca', 'sophia_t2']),
 # taxes
 'h119_hr1_2025': ('no', 'taxes', 'CBO’s distributional table: resources fall for the lowest-income households and rise for the top; adds about $3.4 trillion to deficits.', ['cbo_hr1_dist', 'sophia_t2']),
 's119_hr1_2025': ('no', 'taxes', 'CBO’s distributional table: resources fall for the lowest-income households and rise for the top; adds about $3.4 trillion to deficits.', ['cbo_hr1_dist', 'sophia_t2']),
 # corporate
 'h118_hr4763_2024': ('no', 'corporate', 'Moved most crypto oversight from the SEC to a lighter-touch regime the industry lobbied for.'),
 's118_hjres109_2024': ('no', 'corporate', 'Overturned an SEC accounting rule that protected customers whose crypto is held by custodians.'),
 'h119_s1582_2025': ('no', 'corporate', 'Stablecoin framework written with heavy industry backing; the President’s family holds a stablecoin business that benefits from it.', ['sophia_t2']),
 's119_s1582_2025': ('no', 'corporate', 'Stablecoin framework written with heavy industry backing; the President’s family holds a stablecoin business that benefits from it.', ['sophia_t2']),
 # tariffs
 'h119_hjres72_2026': ('yes', 'tariffs_trade', 'Ends the emergency used for the Canada tariffs; courts later ruled the emergency tariffs illegal and they raised prices paid by Americans.', ['scotus_ieepa', 'sophia_t2']),
 's119_sjres37_2025': ('yes', 'tariffs_trade', 'Ends the emergency used for the Canada tariffs; courts later ruled the emergency tariffs illegal and they raised prices paid by Americans.', ['scotus_ieepa', 'sophia_t2']),
 # israel
 'h118_hr8034_2024': ('no', 'israel', 'About $26.4 billion in military and related aid to Israel, with no added conditions, during the Gaza war.'),
 's118_sjres111_2024': ('yes', 'israel', 'Would have blocked a weapons sale to Israel during the Gaza war.'),
 's119_sjres41_2025': ('yes', 'israel', 'Would have blocked a sale of rifles to Israel’s national police.'),
 'h119_hr23_2025': ('no', 'israel', 'Sanctions the International Criminal Court for investigating the U.S. or allies such as Israel.'),
 's119_hr23_2025': ('no', 'israel', 'Sanctions the International Criminal Court for investigating the U.S. or allies such as Israel.'),
 'h118_hr6090_2024': ('no', 'israel', 'Writes the IHRA definition of antisemitism into civil-rights enforcement; the ACLU warned it would chill protected criticism of Israel.', ['aclu_aaa']),
 's119_sres852_2026': ('yes', 'israel', 'Requests a State Department report on Israel’s human-rights practices before more security aid.'),
 # war
 'h119_hconres86_2026': ('yes', 'foreign_aid_war', 'Asserts Congress’s constitutional power over war by directing U.S. forces out of hostilities with Iran.'),
 's119_hconres86_2026': ('yes', 'foreign_aid_war', 'Asserts Congress’s constitutional power over war by directing U.S. forces out of hostilities with Iran.'),
 's119_sjres59_2025': ('yes', 'foreign_aid_war', 'Asserts Congress’s constitutional power over war by directing U.S. forces out of hostilities with Iran.'),
}
out = {'version': '2.0-draft', 'rule': 'Sophia takes a published position only on key votes whose documented effects on households, on industry, on Israel policy or on Congress’s war powers are clear from the record. Every other key vote is shown on candidate pages but not scored. The same positions apply to every member of every party.',
       'cites': {k: {'t': t, 'u': u} for k, (t, u) in C.items()},
       'stances': {k: {'pos': v[0], 'cat': v[1], 'why': v[2], 'c': (v[3] if len(v) > 3 else [])} for k, v in S.items()}}
json.dump(out, open('/home/claude/el26/research/stances.json', 'w'), ensure_ascii=False, indent=1)
print(len(S))

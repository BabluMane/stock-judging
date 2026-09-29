#!/usr/bin/env python3
"""Disjointness check for the v3.10 OOS pre-registration set.

Pure name/date-membership check — no price/EPS/fundamental data is touched,
no valuation or backtest is run. Checks the 25 v3.10 name-dates (13
companies) against all prior name-dates: in-sample 25 companies (50
name-dates), v3.8 OOS 13 companies (25 name-dates), v3.9 OOS 13 companies
(25 name-dates). Overlap is tested at BOTH company level (strict) and
name-date level.
"""

INSAMPLE = """aplapollo_2016-03-31 aplapollo_2018-03-31 astral_2016-03-31 astral_2018-03-31
bajajcon_2016-03-31 bajajcon_2018-03-31 bajfin_2015-12-31 bajfin_2017-12-29
bhel_2015-03-31 bhel_2017-03-31 brightcom_2018-08-22 brightcom_2020-08-21
deepak_2016-03-31 deepak_2018-03-31 dhfl_2014-06-04 dhfl_2016-06-03
hero_2016-03-31 hero_2018-03-31 itc_2015-03-31 itc_2017-03-31
lichf_2016-03-31 lichf_2018-03-31 lupin_2015-03-31 lupin_2017-03-31
manpasand_2015-07-09 manpasand_2016-05-20 mnm_2016-03-31 mnm_2018-03-31
navin_2016-03-31 navin_2018-03-31 persistent_2019-03-29 persistent_2021-03-31
piind_2016-03-31 piind_2018-03-31 safari_2018-03-31 safari_2020-03-31
suntv_2017-03-31 suntv_2019-03-29 symphony_2016-03-31 symphony_2018-03-31
tataelxsi_2017-03-31 tataelxsi_2019-03-31 trent_2019-03-29 trent_2021-03-31
vakrangee_2013-06-03 vakrangee_2015-06-01 wipro_2015-03-31 wipro_2017-03-31
yesbank_2015-03-05 yesbank_2017-03-03""".split()

V3_8 = """titan_2016-03-31 titan_2018-03-31 divislab_2016-03-31 divislab_2018-03-31
pageind_2015-03-31 pageind_2017-03-31 dmart_2018-03-31 dmart_2019-03-31
polycab_2020-03-31 polycab_2021-03-31 colpal_2016-03-31 colpal_2018-03-31
ashokley_2016-03-31 ashokley_2018-03-31 cipla_2016-03-31 cipla_2018-03-31
coalindia_2016-03-31 coalindia_2018-03-31 gail_2016-03-31 gail_2018-03-31
pcjeweller_2017-03-31 pcjeweller_2018-03-31 fretail_2017-03-31 fretail_2019-03-31
cgpower_2016-03-31""".split()

V3_9 = """asianpaint_2014-03-31 asianpaint_2016-03-31 hdfcbank_2014-03-31 hdfcbank_2016-03-31
nestleind_2015-03-31 nestleind_2017-03-31 britannia_2015-03-31 britannia_2017-03-31
havells_2014-03-31 havells_2016-03-31 bhartiartl_2016-03-31 bhartiartl_2018-03-31
tatasteel_2015-03-31 tatasteel_2017-03-31 ntpc_2015-03-31 ntpc_2017-03-31
tatamotors_2015-03-31 tatamotors_2017-03-31 bankbaroda_2015-03-31 bankbaroda_2017-03-31
zeel_2017-03-31 zeel_2018-03-31 relcapital_2016-03-31 relcapital_2018-03-31
ilfstransport_2017-03-31""".split()

V3_10 = """dixon_2019-03-31 dixon_2021-03-31 hal_2019-03-31 hal_2021-03-31
bel_2019-03-31 bel_2021-03-31 coforge_2019-03-31 coforge_2021-03-31
tatapower_2020-03-31 tatapower_2021-03-31
hul_2021-03-31 hul_2022-03-31 bajajauto_2019-03-31 bajajauto_2021-03-31
petronet_2019-03-31 petronet_2021-03-31 bpcl_2019-03-31 bpcl_2021-03-31
powergrid_2019-03-31 powergrid_2021-03-31
coffeeday_2019-03-31 coffeeday_2020-03-31 gensol_2023-03-31 gensol_2024-03-31
lvb_2019-03-31""".split()

co = lambda nds: {n.rsplit("_", 1)[0] for n in nds}


def main():
    assert len(V3_10) == len(set(V3_10)) == 25
    assert len(co(V3_10)) == 13
    assert len(co(INSAMPLE)) == 25 and len(INSAMPLE) == 50
    assert len(co(V3_8)) == 13 and len(V3_8) == 25
    assert len(co(V3_9)) == 13 and len(V3_9) == 25
    assert all(n.rsplit("_", 1)[1] >= "2019-03-31" for n in V3_10)
    for label, prior in (("in-sample", INSAMPLE), ("v3.8", V3_8), ("v3.9", V3_9)):
        print(f"prior {label}: {len(co(prior))} companies / {len(prior)} name-dates")
        print(f"  company overlap:   {sorted(co(V3_10) & co(prior))}")
        print(f"  name-date overlap: {sorted(set(V3_10) & set(prior))}")
    allc = co(INSAMPLE) | co(V3_8) | co(V3_9)
    allnd = set(INSAMPLE) | set(V3_8) | set(V3_9)
    print(f"union company overlap:   {sorted(co(V3_10) & allc)}")
    print(f"union name-date overlap: {sorted(set(V3_10) & allnd)}")
    print(f"min v3.10 scoring date: {min(n.rsplit('_',1)[1] for n in V3_10)}")
    print(f"DISJOINT: {not (co(V3_10) & allc) and not (set(V3_10) & allnd)}")


if __name__ == "__main__":
    main()

# Alfredo Garcia - Bitshares core developer

Author: oxarbitrage

https://github.com/oxarbitrage/

## Background

I had been working hired by the bitshares blockchain for the last 6 months mainly as a core developer but also in lot of different areas from client side applications, proof of concepts and documentation.

Most of that work(but not all) can be found in the links inside the worker proposal thread https://bitsharestalk.org/index.php/topic,24540.0.html that it is about to expire.

This worker proposal is a renew of the previous one at very similar rate and scope.

## Worker Scope:

This is an all terrain worker that will review and test code submitted by others but that enjoys doing stuff himself. I try to keep focus in `bitshares-core` as it is the most needed and most challenge part of the project but also contribute in many other areas of the whole.

* **bitshares-core issues and maintenance:**
New issues are added to the github every day. Worker job is to close the most possible, get the needed people together, review code from others, create bug fixes and all related to maintenance inside the core repo. 

- **bitshares-core api:**
Always looking to add, fix, make new api calls for client applications to connect to the core and get data in more effienient ways, key factors for any business that want to run on top of the chain.
The coordination with the `bitshares-ui` to create the calls they need to make user experience in the DEX better is included in this point.

- **the cli wallet:**
The command line wallet is where other programs and individuals connect to interact with the chain. This new period i plan to extend trading capabilities of the cli_wallet to make it a full trading command line workstation.

- **big improvements and BSIPs **:
In this period the worker will at least implement 1 BSIP(not decided witch one yet). It will participate and help any other dev working in a BSIP with testing, code review, etc. The worker will also write at least 1 BSIP more and participate in the BSIP discussions with implementation teams or individuals. 

- **release and hardfork planning:**
With the last hardfork the worker was able to learn the process to plan a new one when needed. Releases are already being made by this worker, we had made a plan to add code to our repos that this worker applies and instruct new devs do adapt to this rules.
This point include witnesses help at hardfork and coordination. 

- **bitshares documentation:**
Always improving documentation in the bitshares wiki pages, in docs.bitshares.org and any other sources. The worker takes note of everything while developing so new documentation naturally evolve from this notes. As changes are added to the different pats of the project the documentation need to be constantly updated. 

- **tools for other devs / integration:**
In the last time i made different wrapper tools to help the integration of bitshares with other apps. This kind of tools are very needed as they speed up the work of developers that want to make business on top of the chain. It is important that new application developers can get started as soon as possible with the use of this tools.

- **review and help with third party open source tools related to bitshares**
When developers are creating new tools that will contribute with the grow of the ecosystem this worker will help them reviewing their work, helping to get the data they need from the chain, make their learning curve a bit easier when starting with bitshares.

- **client side applications:**
When the community need a feature(certain data from the chain, chart/stats of something, etc) the worker will create a client side application for them. The open source explorer was born this way and so other tools made in the last time like the account history csv exporter. Tools of this kind will be developed by popular demand.

### Note about hosting

In the last year i had been using hosting provided by @lin9uxis to do almost all the development needed and to put applications and proof of concepts live. A machine with specifications needed cost 100/usd per month(same rate as infrastructure worker machines).

@lin9uxis hosted my work for free and he can keep doing but i think it is fair that the chain can compensate him for his services by hiring 2 machines from him at 200 usd per month.


## Worker payment and duration:

I am asking for the same rate as the previous contract plus 200 usd per month for hosting as detailed above.

This is a full time contract, 8 hours per day, 5 days a week of development.

8 h/day * 5 days a week = 40 hs a month * 40 usd/h = 6400 usd + 200 usd of hosting = 6600 usd per month.

Duration of the worker is 6 months(180 days). 

The worker account(`alfredo-worker`) and the escrow group is already formed and it will remain the same with the following bitshares users:

```
chainsquad
dev.bitsharesblocks
elmato
fox
lin9uxis
```

Current worker ends on Jan 8th. I am taking some small vacations from Jan 13th to Jan 21th so the new worker will start Monday Jan 22th and end Saturday 22 of July.

Calculation:

1.3 = settlement price of bitusd/bts at the moment of writing.(2018-01-03)

2.5 = multiplier to cover market fluctuations and borrow at 2.5x collateral if needed.

6600 usd/month * 1.3 = 8580 * 2.5 = 21450 BTS/month

31845 / 30 = 715 bts per day

**Note:** worker will not receive 21450 bts per month but exactly 6600 bitusd with the escrow setup. Remaining bts(if any) will be burned back to the network or keeped in the worker escrow account if there is a plan to renew in 6 months.
If at some point the escrow can't buy enough bitusd to make the payment the worker will submit a new worker proposal that the stakeholders will need to approve.


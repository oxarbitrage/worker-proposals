Bitshares Core Developer Worker proposal
========================================

Intro.
------

My name is Alfredo Garcia and I had been working in the bitshares community as a core developer since the end of January of 2017.
For this work I was hired by Bitshares Munich who was in charge of adding a worker proposal for me, link can be found here:

https://bitsharestalk.org/index.php/topic,23698.0.html

This was a 6 months contract paid in BTS. As the price of BTS increased considerable the worker was voted out among with other workers before natural end. Fair enough. To avoid this situation this new worker is in bitusd. This will be explained in detail in the "The worker payment." section.

Since the very beginning, discovering how the bitshares community operates, I had plans to add a new worker proposal myself after the first one expires. Several personal reasons for this, the main ones are:

- I love to work in the bitshares core, graphene code is my passion. I want to spend my full time working in this project without the need of going somewhere else for more income. The intellectual challenge is for me here at bitshares, if I can make a living from it then there is no better place for me to be.
- I like the idea of not having a single boss/company, I prefer to be driven by the shareholders in the direction the Bitshares DAC needs.
- I have good relation with all the community members I ever met, never a problem since I started apart from normal technical discussions and exchange of different opinions. It is real fun and exiting to be in this community every day.
- I am a strong defender of the blockchain technology as a way to change the world in pretty much every aspect for better.

Background.
-----------

Initially hired to work in 190 github issues that were open at the time the original worker started. This  number is at around 90 now(https://github.com/bitshares/bitshares-core/issues). New issues are opened all the time so there was a lot of work done. This reduction in the open issues was by no mean caused by me alone working on them; I resolved what I was able to do, requested help to others, participated in the discussions, but this only was possible because there were a lot of other devs involved.

Measuring worker performance by the number of github issues that were closed is a bit unfair for both sides(the shareholders and the worker).One single issue can take weeks of research, discussion and coding while a related group of 2 or 3 issues could be closed in hours just with small changes or in minutes with a single reply. It is simply statistics that don't reflect the whole reality.

Worker tasks.
-------------

Worker will move in every aspect of the technical spectrum where he will get required, main focus will be at the following areas:

###1- Github issues:

It is extremly important to be after this issues all the time. Any serious technical problem/suggestion is added to github issues of the bitshares core. As new clients dapps are developed - more features/api calls are needed from the core, as the blockchain increases in size - alternative ways are needed to run nodes with less resources, as more business uses bitshares as a backend - more bugs are discovered and so on.

This issues are in my opinion the most important channel of technical discussion of the bitshares community and they must be a priority. My work will be the same in this stage as it was before, try to resolve them, organize them by priority, bring other devs more specialized in a particular issue, join the parts to get consensus, etc.

The difference between now and my first period is the experience, when I started every issue was a huge challenge. Without previous graphene experience it was a lot of work to make every test, new feature, understand single concepts. This time, I am  a lot more mature, I have developed a method to work on core code, I know where is everything, I know all the terminology, I am doing better code, etcetera. All this allows me get into the problem a lot faster and more efficiently than before.

###2- BSIPS

The next front for the worker will be at the bsips(https://github.com/bitshares/bsips). This proposals are not so immediate as issues, they require more planning and implementation is most of the time a lot longer than issues in general. 
This are extremely important as this could be real changers of the community, a whole new industry can be included into bitshares after a good bsip. 
Worker will participate in the discussions of new bsips and do the implementation of new features described in the this proposals if needed. If another dev is in charge of the changes I will help and support with all my knowledge and dedication.

As an example there a few ideas being discussed by the community where the worker will participate like the possible EOS integration of bitshares, the dividend feature to coins, bitasset recovery, just to name a few of currently discussed.

###3- Client side applications and the explorer.

In order to know what the core needs there are 2 options. One is to check the github issues, bsips, forum threads and chats and solve problems other users are facing. Good enough but there is also another way more active, this is, develop relative simple client side applications that interact to the bitshares backend to see what is needed, bugs, improvements from first hand.

For this reason and by the popular community demand of a bitshares explorer I decided to start the project. It is located at:

http://bitshares-explorer.io

Please note this is under development, expect the explorer to be down, full of bugs, with fake data and such in this stage.

Follow the progress of the explorer on this thread:

https://bitsharestalk.org/index.php/topic,24508.0.html

Worker will be in charge of finishing and maintaining the explorer. Release all code involved under MIT. A roadmap for it will be created, documentation on how to install, use, etc.

The explorer will be the first of other client side applications, this can go from trading strategies, wallets, interfaces and any kind of dapp the community decide we must have.

###4- Help and documentation

I take notes of everything i do, this is very valuable to add wiki pages into bitshares:

https://github.com/bitshares/bitshares-core/wiki

And to help other community members in setups, solutions, questions in general. The different communication channels(telegram, forum) of the bitshares community will be attended by this worker in everything possible while writing new documents to the wiki that can help new devs, new nodemasters and other enthusiasts achieve different tasks that without documentation may be very hard and misleading.

###5- Hardfork planning

Some issues and changes will require a hardfork in the bitshares chain. In my first phase I avoided all kind of issues that required hardfork. In this new phase all the changes needing hardfork will be grouped and discussed in order to have a roadmap on the exact steps we will have to consider in the next hardfork.

###6- Basic maintence.

When first worker was voted out, the worker from @vikram was also voted down. He was in charge of basic maintenance of the bitshares core. This included approving pull requests made by all the devs that submitted changes to the bitshares core repo.
His work was very important. By now, he will be focusing on other project outside bitshares. I don't have his skills and I but I could be handling some of his tasks until at least some other worker gets approved for this admin task.


The proposal.
-------------

Due to the worker proposal nature it is hard to simply write a roadmap with timeframes. Some guidance can be followed but the worker will react on demand. For example, if a new security bug is discovered it is possible that the full attention will be on resolving that issue while other tasks will be delayed. 

The flexibility of the worker demands full time commitment to the community.

- Full time worker proposal. 8 hours per day Monday to Friday. 40 hs per week.
- 40 usd per hour. 320 usd per day. 1600 usd per week.
- Duration.  6 months.

The worker payment.
-------------------

Payment will be in usd with method developed by @xeroc:

https://github.com/xeroc/worker-proposals/blob/master/2017-02.md#worker


1600 USD/4 weeks/40 h = 40 usd/h

4.10 = settlement price at the moment of writting.
2.5 = to cover market fluctuations.

6400 * 4.10 = 26240.0 

26240 * 2.5 = 65600 

65600 / 30 = 2186.6667 

Worker payment per day: 2187 bts

Money to worker will be sent only in bitusd at the specified price(of 1600 usd / week) and the rest will be burned back to the chain.

My list of escrows will be:

- Xeroc.
- …
- …
- …
- …

Scripts used for claim, burn, etc will be posted into this repo. 

Worker Updates.
---------------

Worker updates will be posted to bitshares talk forum every weekend with previous week work.






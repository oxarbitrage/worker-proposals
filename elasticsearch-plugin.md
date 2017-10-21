# ElasticSearch Plugin v0.1

The document explains motivations, rationale and technical aspects of a new plugin created for bitshares to store account history data into an elasticsearch database.

## Motivation

There are 2 main problems this plugin tries to solve

- The amount of RAM needed to run a full node. Current options for this are basically store account history: yes/no, store some of the account history, track history for specific accounts only. Plugin allows to have a full node without the amount of RAM required in current implementation.
- The number of requests in regards to new api calls to search account history. Elasticsearch plugin will allow users to search anything quering directly into the database without the need of developing API calls for every case.

More details on how we overcame this 2 points will be explained throw the docs.

## The database selection

So shy elasticsearch ? When i started coding this solution i had not enough arguments to answer this, it was recommended by one of our core developers(@peter conrad). My initial thinking was actually that any database will work to remove history from RAM so i didn't worried too much about what will be. 
After i was already over i started to see the benefits of elasticsearch and was able to convkience myself this is a great choice, here are some key points about why it suits perfect for our needs:

- Elasticsearch(ES) index json objects. Graphene technology use json objects for operations, blocks, all kind of data and elasticsearch works naturally with them(with osme exeptions as we may see later). This is a great advantage, a database that can index json objects.
- The database is fast, speed and industrial oriented, this is great for our project.
- ES can scale by the use of syncronized nodes. I had no chance yet to study the details of this as they were not needed yet to build the plugin but this can be of great use in the future.
- ES is easy to install and to start indexing. Indexing can be done by rpc by calling endpoints with data. We made the coice of doing this with curl.
- Is open source.
- ES recomments a flatworld philosofy and recommends to store everything in a single line to speed indexing and searching. This is exactly what we need.
- others ?

## Technical

The elasticsearch plugin is a copy of account_history_plugin where not needeed stuff was removed and indexation to boost indexes were replaced by indexing into elastic.

Here is how the current account_history plugin works basically:
- with every signed block arraiving to the plugin the ops are extracted from it.
- each op is added to ohi(operation history index) and to ath(account transaction history index).
- both indexes keep growing as new block gets in.
- with the memory reduction techniques currently available the 2 indexes can remove early ops by account reducing ram size.

And now what elasticsearch plugin attempts to do:

- with every signed block arraiving to the plugin the ops are extracted from it, just as in account_history.
- create indexes ohi and ath and store current op there just as account history do. this a temp indexation of 1 op only that is done to remain compatible with the previous numbers used as id(1.11.X and 2.9.X).
- send ath and ohi plus additional block data into elasticsearch(actually we send them in bulks not one by one, ill explain that in the next section).
- remove everything in the compatibility temporal indexes expect for current operation. This way the indexes always have just 1 item and dont waste any ram.

### Replay and bulks

As mentioned we dont send to elasticsearch the operations one by one, this is because in a replay the number of ops will be so big that performance will decrease drastically and time to be in sync will be too much.
For this reason we use the elasticsearch bulk api and send by default 5000 lines when we are in replay and downgrade this to 10 lines after we are in sync.

ES bulk format is one line of metadata and the line of data itself, so 5000 is actually 2500 operations we send on every bulk and 10 is actually 5. We could be doing it 1 by 1 after sync but keep going with the bulk will allow to change the values to increase performance sacrificing some real time.

This values are available as plugins options to the user to change, so if a change in ....
[add data and plugin options]

The name of the index for us will be `graphene`

### Differences from SQL and other relational databases - Why a flatworld ?

When i first looked at elasticsearch one of the first thing i had to figure out was how to relate one data with the other. Coming mainly from a sql world i was first atracted to make several containers and relate them. To my surprise the recommendation in ES is to actually store everything alltogether like in a huge table. 
This makes sense, iun a real world application when saving lets say users data some may have a cell phone while others don't; in our case some ops may have for example an  `issuer` fields while others just don't. It doesn't matter, the number of "columns" will be big and each op will fill where it correspond.

Another very good feature of elasticsearch is that it just index anything you send without previous step, as new fields/columns are sent to index elasticsearch just add them to the "table" without the need of preporocessing(creating tables).

Es encourage the denormalization(https://www.elastic.co/guide/en/elasticsearch/guide/current/denormalization.html) as the best opption to store data, this clearly suit our case.


The optimal number of

Two main problems were found:

- Inde

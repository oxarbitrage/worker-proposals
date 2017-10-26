# ElasticSearch Plugin v1

The document explains motivations, rationale and technical aspects of a new plugin created for bitshares to store account history data into an elasticsearch database.

## Motivation

There are 2 main problems this plugin tries to solve

- The amount of RAM needed to run a full node. Current options for this are basically store account history: yes/no, store some of the account history, track history for specific accounts, etc. Plugin allows to have all the account history data without the amount of RAM required in current implementation.
- The number of github issues in regards to new api calls to lookup account history in different ways. Elasticsearch plugin will allow users to search account history quering directly into the database without the need of developing API calls for every case.

Additionally we are after a secure way to store error free full account data. The huge amount of operations data involved in bitshares blockchain and the way it is serialized makes this a big challenge.

## The database selection

Elastic search was selected for the main following reasons:

- open source.
- fast.
- index oriented.
- easy to install and start using.
- send data from c++ using curl.
- scalability and decentralized nodes of data.

## Technical

The elasticsearch plugin is a copy of account_history_plugin skeleton where not needeed stuff was removed saving to objects(to RAM) was replaced by saving into elastic.

Here is how the current account_history plugin works basically:
- with every signed block arraiving to the plugin the ops are extracted from it.
- each op is added to ohi(operation history index) and to ath(account transaction history index).
- both indexes keep growing as new block gets in.
- with the memory reduction techniques currently available the 2 indexes can remove early ops of accounts reducing ram size.

And now what elasticsearch plugin attempts to do:

- with every signed block arraiving to the plugin the ops are extracted from it, just as in account_history.
- create indexes ohi and ath and store current op there just as account history do. this a temp indexation of 1 op only that is done to remain constant with the previous numbers used as id(1.11.X and 2.9.X).
- send ath and ohi plus additional block data and visitor data(lini to visitor data) into elasticsearch(actually we send them in bulks not one by one - replay and bulk links).
- remove everything in the compatibility temporal indexes expect for current operation. This way the indexes always have just 1 item and dont waste any ram.

### Replay and _bulk

As mentioned we dont send to elasticsearch the operations one by one, this is because in a replay the number of ops will be so big that performance will decrease drastically and time to be in sync will be too much.
For this reason we use the elasticsearch bulk api and send by default 5000 lines when we are in replay and downgrade this to 10 lines after we are in sync.

ES bulk format is one line of metadata and the line of data itself, so 5000 is actually 2500 operations we send on every bulk and 10 is actually 5. We could be doing it 1 by 1 after sync but keep going with the bulk will allow to change the values to increase performance sacrificing some real time.

This values are available as plugins options to the user to change, so if a change in ....
[add data and plugin options]

The optimal number of docs to bulk is hardware dependent this is why we added it as an option for changing it at start time.

The name of the index for us will be `graphene`

### Accessing data inside operations

There are cases where data coming from account transaction history index, operation history index and block data is not enough. We may want to index fields inside operations themselves like the fees the asset id or the amount of transfer to make fast queries into them. 

Data inside operations is saved as a text fields into elasticsearch, this means that we can't fast search into them as the data is not indexed, we can, still search by other data and filter converting the op text to json i nclient side.

To workaround the limitation it is available a visitor that can be turned on/off by the command line. Something in common all ops have is a fee field with asset_id and amount. In current plugin version when visitor is on this 2 values will be saved meaning clients can know total chain fees collected in real time, total fees in asset, fees by op among other things. This will be explained in the EXAMPLES section.

As a poc we also added amount and asset_id of transfer operations to ilustrate how easy is to index more data for any competent graphene developer.

## Installation

Basically there are 2 things you need: elasticsearch and curl for c++. elasticsearch need java so those are the 3 things you will need to have. The following are instructions tested in debian(ubuntu - mint) based linux versions.

### Install java:

download the jre, add sudo to the start of the commands if installing from a non root user:

`apt-get install default-jre`

we are going to need the jdk too:

`apt-get install default-jre`

add repository to install oracle java8:

in ubuntu:

`add-apt-repository ppa:webupd8team/java` 

in debian:

`add-apt-repository "deb http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main"`

then:
`apt-get update`

if you don't have add-apt-repository command you can install it by: 

`apt-get install software-properties-common`

install java 8:

`apt-get install oracle-java8-installer`

### Install ES:

Get the last version zip file at: https://www.elastic.co/downloads/elasticsearch

Please do this as a non root user as ES will not run as root.

download as: 

`wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.3.zip`

unzip:

`unzip elasticsearch-5.6.3.zip`

and run:

```
cd elasticsearch-5.6.3/
./bin/elasticsearch
```

You can put this as a service, the binary haves a `--deamon` option, can run inside `screen` or any other option that suits you in order to keep the database running. 

### Install curl

We need curl to send requests from the c++ plugin into the ES database:

`apt-get install libcurl4-openssl-dev`

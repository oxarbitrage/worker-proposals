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

`apt-get install default-jdk`

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

## Running

Make sure ES is running, can start it by:

`./elasticsearch --daemonize`

ES will listen on localhost port 9200 `127.0.0.1:9200`

Clone repo with elasticsearch plugin and install bitshares:

```
git clone https://github.com/oxarbitrage/bitshares-core
cd bitshares-core
git checkout -t origin/elasticsearch
git submodule update --init --recursive
cmake -DBOOST_ROOT="$BOOST_ROOT" -DCMAKE_BUILD_TYPE=RelWithDebInfo .
make
```

### Arguments

The ES plugin have the following parameters passed by command line:

- `elasticsearch-node-url` - The url od elasticsearch - default: `http://localhost:9200/`
- `elasticsearch-bulk-replay` - The number of lines(ops * 2) to send to database in replay state - default: `10000`
- `elasticsearch-bulk-sync` - The number of lines(ops * 2) to send to database at syncronized state - default: `100` 
- `elasticsearch-logs` - Save logs to database - default: `true`
- `elasticsearch-visitor` - Index visitor additional inside op data - default: `true`

### Starting node

ES plugin is not active by default, we need to start it with the `plugins` parameter. An example of starting a node with ES plugin may be:

`programs/witness_node/witness_node --data-dir data/my-blockprod --rpc-endpoint "127.0.0.1:8090" --plugins "witness elasticsearch market_history" --elasticsearch-bulk-replay 10000 --elasticsearch-logs true --elasticsearch-visitor true`

### Checking if it is working

A few minutes after the node start the first batch of 5000 ops will be inserted to the database. If you are in a desktop linux you may want to install https://github.com/mobz/elasticsearch-head and see the database from the web browser to make sure if it is working. This is optional.

If you only have command line available you can query the database directly throw curl as:

```
root@NC-PH-1346-07:~/bitshares/elastic/bitshares-core# curl -X GET 'http://localhost:9200/graphene/data/_count?pretty=true' -d '
{
    "query" : {
        "bool" : { "must" : [{"match_all": {}}] }
    }
}
'
{
  "count" : 360000,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "skipped" : 0,
    "failed" : 0
  }
}
root@NC-PH-1346-07:~/bitshares/elastic/bitshares-core# 
```

360000 records are inserted at this point in ES, means it is working.

**Important: Replay with ES plugin will be always slower than the "save to ram" `account_history_plugin` so expect to wait more to be in sync than usual.**

## Usage

After your node is in sync you are in posesion of a full node without the ram issues. A syncronized witness_node with ES will be using around X gigs of ram:

[free command here with the witness to show]

What client side apps can do with this new data is kind of unlimited to client developer imagination but lets check some real world examples to see the benefits of this new feature.

### Get operations by account, time and operation type

References:
https://github.com/bitshares/bitshares-core/issues/358
https://github.com/bitshares/bitshares-core/issues/413
https://github.com/bitshares/bitshares-core/pull/405
https://github.com/bitshares/bitshares-core/pull/379
https://github.com/bitshares/bitshares-core/pull/430
https://github.com/bitshares/bitshares-ui/issues/68

This is one of the issues that has been requested constantly. It can be easily queried with ES plugin by calling the _search endpoint doing:

```
root@NC-PH-1346-07:~/bitshares/elastic/bitshares-core# curl -X GET 'http://localhost:9200/graphene/data/_search?pretty=true' -d '
{
    "query" : {
        "bool" : { "must" : [{"term": { "account_history.account.keyword": "1.2.282"}}, {"range": {"block_data.block_time": {"gte": "2015-10-26T00:00:00", "lte": "2
015-10-29T23:59:59"}}}] }
    }
}
'
{
  "took" : 99,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : 3,
    "max_score" : 9.865524,
    "hits" : [
      {
        "_index" : "graphene",
        "_type" : "data",
        "_id" : "2.9.121234",
        "_score" : 9.865524,
        "_source" : {
          "account_history" : {
            "id" : "2.9.121234",
            "account" : "1.2.282",
            "operation_id" : "1.11.114383",
            "sequence" : 11,
            "next" : "2.9.113951"
          },
          "operation_history" : {
            "trx_in_block" : 0,
            "op_in_trx" : 0,
            "operation_results" : "[0,{}]",
            "virtual_op" : 14811,
            "op" : "[0,{'fee':{'amount':4210936,'asset_id':'1.3.0'},'from':'1.2.89940','to':'1.2.282','amount':{'amount':2000000,'asset_id':'1.3.535'},'memo':{'from
':'BTS8LWkZLmsnWjgtT1PNHT5XGAu1z1ueQkBHBQTVfECFVQfD3s7CF','to':'BTS5TPTziKkLexhVKsQKtSpo4bAv5RnB8oXcG4sMHEwCcTf3r7dqE','nonce':'370147387190899','message':'559c6966
ccf3db2583f9636489c7be0339a88c1703f3b60dde9f165825720486'},'extensions':[]}]"
          },
          "operation_type" : 0,
          "block_data" : {
            "block_num" : 375534,
            "block_time" : "2015-10-26T19:37:18",
            "trx_id" : ""
          },
          "fee_data" : {
            "fee_asset" : "1.3.0",
            "fee_amount" : "4210936"
          },
          "transfer_data" : {
            "transfer_asset_id" : "1.3.535",
            "transfer_amount" : "2000000"
          }
        }
      },
      {
        "_index" : "graphene",
        "_type" : "data",
        "_id" : "2.9.143682",
        "_score" : 9.720996,
        "_source" : {
          "account_history" : {
            "id" : "2.9.143682",
            "account" : "1.2.282",
            "operation_id" : "1.11.136390",
            "sequence" : 13,
            "next" : "2.9.126760"
          },
          "operation_history" : {
            "trx_in_block" : 0,
            "op_in_trx" : 0,
            "operation_results" : "[0,{}]",
            "virtual_op" : 36818,
            "op" : "[0,{'fee':{'amount':4335936,'asset_id':'1.3.0'},'from':'1.2.376','to':'1.2.282','amount':{'amount':1010000,'asset_id':'1.3.535'},'memo':{'from':
'BTS6zT2XD7YXJpAPyRKq8Najz4R5ut3tVMEfK8hqUdLBbBRjTjjKy','to':'BTS5TPTziKkLexhVKsQKtSpo4bAv5RnB8oXcG4sMHEwCcTf3r7dqE','nonce':'370212206009967','message':'02b9072a43
b3e1ed960e7710b227984600b17fa3d6837bed56fba07e69c6e2793eac9ea7d3851eb48b04e9ab48933900996b00016d2f145808d30dc81e61232f1b29afb38caf1361e46927d8749826a26435bd9a227533
d5f1b181bfca5e26ac'},'extensions':[]}]"
          },
          "operation_type" : 0,
          "block_data" : {
            "block_num" : 459202,
            "block_time" : "2015-10-29T17:57:18",
            "trx_id" : ""
          },
          "fee_data" : {
            "fee_asset" : "1.3.0",
            "fee_amount" : "4335936"
          },
          "transfer_data" : {
            "transfer_asset_id" : "1.3.535",
            "transfer_amount" : "1010000"
          }
        }
      },
      {
        "_index" : "graphene",
        "_type" : "data",
        "_id" : "2.9.126760",
        "_score" : 9.720996,
        "_source" : {
          "account_history" : {
            "id" : "2.9.126760",
            "account" : "1.2.282",
            "operation_id" : "1.11.119823",
            "sequence" : 12,
            "next" : "2.9.121234"
          },
          "operation_history" : {
            "trx_in_block" : 0,
            "op_in_trx" : 0,
            "operation_results" : "[0,{}]",
            "virtual_op" : 20251,
            "op" : "[0,{'fee':{'amount':4000000,'asset_id':'1.3.0'},'from':'1.2.96086','to':'1.2.282','amount':{'amount':78970118,'asset_id':'1.3.0'},'extensions':[
]}]"
          },
          "operation_type" : 0,
          "block_data" : {
            "block_num" : 394952,
            "block_time" : "2015-10-27T11:51:30",
            "trx_id" : ""
          },
          "fee_data" : {
            "fee_asset" : "1.3.0",
            "fee_amount" : "4000000"
          },
          "transfer_data" : {
            "transfer_asset_id" : "1.3.0",
            "transfer_amount" : "78970118"
          }
        }
      }
    ]
  }
}
root@NC-PH-1346-07:~/bitshares/elastic/bitshares-core# 
```

more samples here ...

### Get operations by account and block

References:
https://github.com/bitshares/bitshares-core/issues/61

### Get operations by transaction hash

Refs: https://github.com/bitshares/bitshares-core/pull/373

## New stats

After we solve some of the issues needed by the community and generating a framework for future issues of the same kind lets go a bit beyond and explore how rich is to have account data operations stored in ES in regards to stats. This are just a few samples.

### Get total ops

- get total ops by type.
- get total ops in a period of time. 
- get total ops by type inside a range of blocks.

### Get speed data

- ops per second
- trxs per second

### Get fee data

- total collected fee
- total colected fee for op type
- total fees collected this month
- total fee collected in asset

### Transfer data

- get amount transfered from account.
- get 

### More visitor code = more indexed data = more filters to use

Just as an example, it will be easy to index asset of trading operations by extending the visitor code of them. point 3 of https://github.com/bitshares/bitshares-core/issues/358 reqquest trading pair, can be solved by indexing the asset of the trading ops as mentioned.

Remember ES already have all the needed info in the `op` text field of the `operation_history` object. Client can get all the ops of an account, loop throw them and convert the `op` string into json being able to filter by the asset or any other field needed. There is no need to index everything but it is possible.

## Duplicates

By using the `op_type` = `create` on each bulk line we send to the database and as we use an unique ID(ath id(2.9.X)) the plugin will not index any operation twice. If the node is on a replay, the plugin will start adding to database when it find a new record and never before. 

## The future

Plugin aims to be included and be part bitshares-core project as a cheaper ram full node alternative to `account_history_plugin` while obtaining the benefits in quering the huge amounts of data present in the blockchain in a new way.

Plugin should be improved in speed and performance by the dev community and active workers, some basic maintence will be needed if a new operation cames in(we need to add it to the visitor). Interested third parties can improve it for their own needs but i think Bitshares should do the basic maintence of this. 





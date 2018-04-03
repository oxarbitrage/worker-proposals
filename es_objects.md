# Elastic Search Objects Plugin V0.1

The document explains motivations, technical challenges and and some examples of a new plug-in created for bitshares to store blockchain object data into an elasticsearch database(ES).


## Motivations

`bitshares-core` stores all blockchain data in objects, this are usually sorted in boost indexes. This is an efficient way to keep consensus fast and the chain functional. API calls that need this objects are done by iterating throw the mentioned indexes. 

The `bitshares-core` team directives are to only store the data needed for consensus to save valuable RAM, some objects are deleted after they expire, changes in objects are not recorded,  some data of the past will not be available but only current state, etc.

`es_objects`  plugin will make some preselected objects persist in time to get history snapshots at any time in the blockchain life.

## Installation:

In order to install elasticsearch and dependencies please refer to here: 

https://github.com/bitshares/bitshares-core/wiki/ElasticSearch-Plugin#installation

## Arguments:

`es_objects` haves its own set of arguments:


- `es-objects-elasticsearch-url`  - The database url(default: `http://localhost:9200/`)
- `es-objects-logs` - Log bulk events to database(default: true)
- `es-objects-bulk-replay` - Number of bulk documents to index on replay(default: 5000)
- `es-objects-bulk-sync`  - Number of bulk documents to index on a  synchronized chain(default: 2)
- `es-objects-proposals` - Store proposal objects(default: true)
- `es-objects-accounts` - Store account objects(default: true)
- `es-objects-assets` - Store asset objects(default: true)
- `es-objects-balances` - Store balances objects(default: true)
- `es-objects-limit-orders` - Store limit order objects(default: true)
- `es-objects-asset-bitasset`  - Store feed data(default: true)

## Starting node:

Make sure your ES database is up and running by:

`curl 'http://localhost:9200/?pretty'`

That should response with some database information, if that is the case your ES is ready to start receiving data so we can start the witness node with the `es-objects` plugin.

 To start the node with all the default plugin options use:


    programs/witness_node/witness_node --data-dir blockchain --rpc-endpoint "127.0.0.1:8090" --plugins "es_objects"

Tip: If you already have data in ES and want to start fresh you can delete all indexes by:

 `curl -XDELETE localhost:9200/_all`

To start with some custom options; lets suppose we only want to track the proposal objects and nothing more: 


    programs/witness_node/witness_node --data-dir blockchain --rpc-endpoint "127.0.0.1:8090" --plugins "es_objects" --es-objects-accounts false --es-objects-assets false --es-objects-balances false --es-objects-limit-orders false --es-objects-asset-bitasset false es-objects-bulk-replay 100

Note that above we also changed the number of bulks in replay to 100. We did this just to start getting results inserted to the database faster as proposals alone is not an object updated so often.

This plugin can be used in combination with the former account history `elasticsearch` plugin so you will have full account history and objects in the same ES database:


    programs/witness_node/witness_node --data-dir blockchain --rpc-endpoint "127.0.0.1:8090" --plugins "es_objects elasticsearch"

It is recommended to don't track bitasset objects if not needed, so, you can start your node as:


    programs/witness_node/witness_node --data-dir blockchain --rpc-endpoint "127.0.0.1:8090" --plugins "es_objects" --es-objects-asset-bitasset false --es-objects-bulk-replay 1000

Avoid tracking limit orders if you don't need them as:


    programs/witness_node/witness_node --data-dir blockchain --rpc-endpoint "127.0.0.1:8090" --plugins "es_objects" --es-objects-asset-bitasset false --es-objects-limit-orders false --es-objects-bulk-replay 1000

## Checking if it is working:

There are several ways to visualize data from ES, the most common is simply by executing curl requests against the database:


    curl -X GET 'http://localhost:9200/bitshares-*/data/_count?pretty=true' -H 'Content-Type: application/json' -d '
    {
        "query" : {
            "bool" : { "must" : [{"match_all": {}}] }
        }
    }
    '

In the response, the `count` field must be a positive number, indicating records are being inserted.

## Indexes:

When running with all the objects the indexes created will be the followings:


    $ curl -X GET 'http://localhost:9200/_cat/indices' 
    yellow open bitshares-proposal   HeL9iJyEQuSZftcPUM0sQQ 5 1     7   5  76.4kb  76.4kb
    yellow open bitshares-account    PSPTWSrQQo294DaAl5-RIw 5 1  4604  28   3.5mb   3.5mb
    yellow open bitshares-limitorder 5BNcA7yJQpKbhDUGhCR4Cw 5 1   712   7 316.5kb 316.5kb
    yellow open bitshares-balance    5EVcBDBVQkudp8l0XquHEQ 5 1  2407  34 763.7kb 763.7kb
    yellow open objects_logs         wczACN4sQP2vP-jIavcZnQ 5 1    89   0   3.2mb   3.2mb
    yellow open bitshares-bitasset   ZD4aG2V5RMaZQs98KuSH5Q 5 1 18389   0   3.7mb   3.7mb
    yellow open bitshares-asset      FEpl_FAYRpWuWEdFal1LtQ 5 1    31 697 132.6kb 132.6kb
    $


## Meta Data:

All objects tracked will have 3 meta data fields that will help you to easy sort and get data inside time or block ranges.


- `object_id`
- `block_time`
- `block_number`

Plugin creates new record with the same `object_id` if the object changed. For this reason there will be multiple records of for example account object `1.2.0` in `bitshares-account` index.
You need  to pull the most recent to get current snapshot while you need to search in the past to get a history snapshot.


## Use Cases:

It is unlikely that you will be using raw curl queries to get data from ES, most probably you will use some wrapper to make the task easier. 
Currently a Bitshares ES Wrapper exist and its code is located at: https://github.com/oxarbitrage/bitshares-es-wrapper

The wrapper(`es-wrapper`)  provides the following calls to interact with the objects stored in the ES database:


- `get_object_history` - by knowing an object_id you will be able to get history of changes of this object.
- `search_object` - will allow  to search for an object by any field.

In this document we are going to use raw curl calls to ES as it will probably work for everybody. The same can be done with the `es-wrapper` or others but it will not be explained here.

Only queries are provided in the samples as results will make the document too big.

### Proposal Tracking:

https://github.com/bitshares/bitshares-core/issues/115

If `es-objects-proposals` is set to `true`  then proposal objects will be saved and never deleted into the ES database. Changes in this object across time will be available, this will allow to query historical proposal not possible to retrieve with current available API calls.

Historical proposal data(expired or executed) is discarded by the `bitshares-core` as it is not needed for consensus, this is the perfect candidate to store in ES.

Nodes with this feature enabled will be able to make queries into historical proposals. Lets get for example all the proposals made by an account by using raw curl:

`curl -X GET 'http://localhost:9200/bitshares-*/data/_search?pretty=true' -H 'Content-Type: application/json' -d '{"query":{"bool":{"must":[{"term":{"proposer.keyword":"1.2.152768"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"aggs":{}}'` 

Or lets get a proposal by id:

`curl -X GET 'http://localhost:9200/bitshares-*/data/_search?pretty=true' -H 'Content-Type: application/json' -d '{"query":{"bool":{"must":[{"term":{"object_id.keyword":"1.10.4626"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"aggs":{}}'`


### Account tracking:

https://github.com/bitshares/bitshares-core/issues/452

Currently, the `bitshares-core` does not maintain an index with referrer data. This make the task of getting referrers a matter of looping throw the entire account_index and checking the referrer fields. This is extremely inefficient to do client side. An index can be added, in fact there is already one created but not being populated as it is not needed for consensus.

If the option `es-objects-accounts` is `true` all  account data will be saved to elastic. This brings the benefit of have an index on each of the important fields of an account including referrer data.

Please remember that you will have duplicates of each account as a new record is added when data changes. For this reason you need to use extra `aggs` for grouping the newest occurrence of an object to get current snapshot.

This query will get all the up to date referrers from `committee-account`:

    curl -XGET 'http://localhost:9200/bitshares-account/data/_search?pretty=true' -d '
    {
        "query":{"bool":{"must":[{"term":{"referrer.keyword":"1.2.0"}}]}},
        "aggs": {
            "group": {
                "terms": {
                    "field": "object_id.keyword"
                },
                "aggs": {
                    "group_docs": {
                        "top_hits": {
                            "size": 1,
                            "sort": [
                                {
                                    "block_time": {
                                        "order": "desc"
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
    '

Pagination is easy by adding from and size fields as:


    curl -XGET 'http://localhost:9200/bitshares-account/data/_search?pretty=true' -d '
    {
        "query":{"bool":{"must":[{"term":{"referrer.keyword":"1.2.0"}}]}},
        "from": 20,
        "size": 10,
        "aggs": {
            "group": {
                "terms": {
                    "field": "object_id.keyword"
                },
                "aggs": {
                    "group_docs": {
                        "top_hits": {
                            "size": 1,
                            "sort": [
                                {
                                    "block_time": {
                                        "order": "desc"
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
    '

Another similar issue with the referrers is reported in the UI: https://github.com/bitshares/bitshares-ui/issues/661

### Limit orders tracking:

https://github.com/bitshares/bitshares-core/issues/556

When a fill or cancel order is executed it currently not possible to get the original limit order creating the trade. 

Lets take for example the following 2 fill orders:

http://open-explorer.io/#/operations/1.11.476244 - Order ID: 1.7.9126
http://open-explorer.io/#/operations/1.11.476024 - Order ID: 1.7.9109

A `get_objects` against  this 2 ids will return empty results from the blockchain.

This plugin will make this orders to persist, so a simple search by the id to the limit orders index will return the original limit create order:

`curl -XGET 'http://localhost:9200/bitshares-limitorder/data/1.7.9126?pretty=true'`

Note: When the limit order is created and filled in the same block the original limit order will not be saved! This will be fixed in the next plugin upgrade.


### Track feeds:

https://github.com/bitshares/bitshares-core/issues/690

The bitasset object for each MPA is updated with new feeds all the time. The core simply updates the object while loosing historical records on price settlements. Basically we cant know the historical settlement price for a market but only the current one.

By saving the bitasset object on each settlement change we can have this track record available.

For instance if i want to check the settlement price of market CNY(1.3.113) in a range of the blockchain history, we know CNY bitasset object is 2.4.13(http://open-explorer.io/#/objects/1.3.113), so we do:

`curl -XGET 'http://localhost:9200/bitshares-bitasset/data/_search?pretty=true' -d '{"query":{"bool":{"must":[{"term":{"object_id.keyword":"2.4.13"}},{"range":{"current_feed_publication_time":{"gt":"2016-05-24T11:36:34","lt":"2016-05-24T18:48:34"}}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}'`

Sorting and filtering will allow to get for example the settlement price in an exact time in 
the past by getting the last feed of that range, something as:

`curl -XGET 'http://localhost:9200/bitshares-bitasset/data/_search?pretty=true' -d '{"query":{"bool":{"must":[{"term":{"object_id.keyword":"2.4.13"}},{"range":{"current_feed_publication_time":{"gt":"2016-05-24T11:36:34","lt":"2016-05-24T18:48:34"}}}],"must_not":[],"should":[]}},"from":0,"size":1,"sort":[{"current_feed_publication_time": {"order" : "desc"}}],"aggs":{}}'`

Note: Several feeds came in the same second, need to make sure we are actually getting the last result, maybe need to add a seq number to the table.

### Asset tracking:

https://github.com/bitshares/bitshares-core/issues/688

When `es-objects-assets` is  `true` when all assets will be saved into elasticsearch and the most important fields of it will be available for indexing.

To get the total count of assets simply do:

`curl -XGET 'http://localhost:9200/bitshares-asset/_count?pretty=true'`

To get the total count of mpa assets do:

`curl -XGET 'http://localhost:9200/bitshares-asset/_count?pretty=true' -d '{"query":{"bool":{"must":[{"term":{"is_market_issued":"true"}}],"must_not":[],"should":[]}}}'`

Get me the count of assets issued by account 1.2.0:

c`url -XGET 'http://localhost:9200/bitshares-asset/_count?pretty=true' -d '{"query":{"bool":{"must":[{"term":{"issuer.keyword":"1.2.0"}}],"must_not":[],"should":[]}}}'`

To get actual assets instead of count change the api endpoint from _count to _search, apply from, size, etc if needed.

### Balance tracking:

Under development. Need to save `account_balance` instead of `balance`.


## Future:

Not all objects available are stored by `es_objects`, this is because not all of them are needed, the plugin was mainly done to satisfy some well known issues. more objects can be added with ease. The list of all available objects on bitshares is available at:
http://docs.bitshares.org/development/blockchain/objects.html
All of them can be added with ease to the plugin.

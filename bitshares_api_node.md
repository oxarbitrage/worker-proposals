# Running a bitshares api node

## Introduction

An Bitshares API Node is a `witness_node` instance specially configured to serve applications with data endpoints. Any bitshares application(gateway, explorer, wallet, trading program, etc) interacts with the decentralized network(blockchain) by connecting to one or many api nodes.

If you plan to run a business on top of bitshares you will probably want one or several api nodes of your property. You can use public nodes but they are very busy and most of the time running old versions, the most api nodes around the better for the network and final users.

This tutorial is for users that already have `witness_node` compiled successfully.

## Running a basic api node

We have `witness_node` executable and we know we can run it by terminal. First thing is to check the options available:

`./programs/witness_node/witness_node --help`

It is important to know what version you are using to know what to expect from a node. Get the version of the node by using the `--version` flag:

`./programs/witness_node/witness_node --version`

The basic api node will run by:

`./programs/witness_node/witness_node --rpc-endpoint "127.0.0.1:8090"`

With the above command you are starting a node that will listen for api calls at port 8090, only at localhost. This can be changed to listen in the internet, local area network or any IP address you own.

By default, the blockchain directory will be `witness_node_data_dir` unless you specify a data directory, for example:

`./programs/witness_node/witness_node --rpc-endpoint "127.0.0.1:8090" --data-dir data/my-blockprod`

Depending on your hardware and use purposes of your api node, you will start it with some custom parameters, enabling and disabling plugins. This will be explained as we go.

Options to the witness_node binary can be added to the config file or passed by command line as we did above. Check the default `config.ini` created when started the node by the first time to make an idea on how you can customize it.
 
A typical node start command can be something like:

`programs/witness_node/witness_node --data-dir data/my-blockprod --rpc-endpoint "127.0.0.1:8090" --max-ops-per-account 10000 --partial-operations true`

Above we limit the operations per account to 1000 to save RAM. This is the default behaviour for newest versions of `witness_node` as a full node needs more than 80 gigs of ram to run.

We call full node to an api node that haves all the account history from all the accounts in the bitshares blockchain. As the amount of RAM needed is so big and increasing this kind of nodes are each time more rare.

Look in the terminal for messages like:

```
1256186ms th_a       application.cpp:499           handle_block         ] Got block: #10000 time: 2015-10-13T23:15:42 latency: 73184714186 ms from: cyrano  irreversible: 9976 (-24)
1267475ms th_a       application.cpp:499           handle_block         ] Got block: #20000 time: 2015-10-14T07:37:33 latency: 73154614475 ms from: bitcube  irreversible: 19975 (-25)
```

If you see this, the blockchain is synchronizing ok. Complete the sync is a long process that depends a lot in your hardware. While you see the blocks coming in the witness node terminal you are in good track.

## Running a production api node

For a production api node there are several options depending in your OS, a few of them are:

### GNU screen

This is the easier way, start a `screen` terminal and run your node on it as: https://github.com/bitshares/bitshares-core/wiki/Manage-your-nodes-by-using-gnu-screen

This works but it is  not the most recommended, in a reboot the node admin will need to run everything again.

### As linux service

In order to run a node by service you need to ...

get documentation

### Docker

get documentation

### Others?

get documentation

## Performance tip

Improve performance for API nodes (do it before starting a node):

```
sudo sysctl -w net.core.somaxconn=65535
```

## Secure your websocket connection

get help

## Full classic node

In bitshares a full node is a node that haves all the account history for all the network users. This setup uses a lot of RAM so nodes by default dont run this way anymore. If you want to run a full node start it by:

`command`

## Elasticsearch node

Another way to have all the account history plus improved capability to search throw it than the classic node you can run your node with elasticsearch plugin.

Elasticsearch installation guide can be found at:

https://github.com/bitshares/bitshares-core/wiki/ElasticSearch-Plugin

To start a node with elasticsearch plugin activated use:

`command`

## Run python wrappers

Add something.

NGINX.

## Connecting to your api node

There are 2 ways to connect to your api node:

- By RPC calls.
- By Websocket.

The 2 of them will send back the response in JSON format.

### RPC

RPC calls are one time calls made to the api node each time, this is you send a command, server returns something and connection end there.

The easiest way to make this calls is by curl command line, for example:

`curl command`

Curl can also make calls authenticated, this is for wallet type applications that need to be logged to access restricted account data.

Here is how this is done:

`command authenticated curl call`

Curl is not the only option to make rpc calls to the api server, in fact almost all programming languages will offer a built in library or third party addons to make this calls.
It is possible to make rpc calls with php, python, javascript just to name a few.

### Websocket

From the command line bitshares developers use wscat tool to connect to an api node. The main difference with the websocket against the rpc calls is that the websocket can sendback updates in real time if you are subscribed to an event. Lets see how that works with an example:

```
example for wscat receiving real time data
```

The same as with the rpc calls almost all languages will have a built in or addon to work with a websocket.

#### Connect the cli wallet

The `cli_wallet` is part of the `bitshares-core` project and use a websocket address to connect to a node and send/receive data.

Connect the `cli_wallet` to your node with a command like:

`cli wallet start basic command`

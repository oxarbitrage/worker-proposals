from pprint import pprint
from bitshares import BitShares
from bitshares.instance import set_shared_bitshares_instance
from bitshares.vesting import Vesting
from bitshares.price import Price
from bitshares.market import Market
from bitshares.amount import Amount

from getpass import getpass

account = "alfredo-worker"
proposer = "oxarbitrage.a699"
vesting_id = "1.13.1608"

bitshares = BitShares(
    nobroadcast=False,
    bundle=True,
    proposer=proposer,
    proposal_expiration=60 * 60 * 24 * 2,
)
set_shared_bitshares_instance(bitshares)
market = Market("USD:BTS")
price = market.ticker()["quoteSettlement_price"]

bitshares.wallet.unlock(getpass())
vesting = Vesting(vesting_id)

print("Claiming Vesting Balance: %s" % vesting.claimable)
bitshares.vesting_balance_withdraw(
    vesting["id"],
    amount=vesting.claimable,
    account=account
)

pprint(bitshares.broadcast())

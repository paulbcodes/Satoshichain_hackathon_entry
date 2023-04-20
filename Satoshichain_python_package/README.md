# Satoshichain python package
A python package for easily interacting with the satochichain blockchain and its ecosystem.

This will be altered for the rpc and addresses in mainnet after June 1st and uploaded to Pypi for pip installation(once it has full functionality).

There is still work to be done with this which should be completed bbefore the launch of mainnet.
Presently satoshix is being added to the package and one function is included in this entry as proof of concept.
Other work to be implemented prior to mainnet is nft creation and adding any other relevent third party contract interfaces.

### Useage
After June 1st when mainnet launces this will available through Pypi for pip installation. Until then ....
Clone this repository 

Then either use satoshichain.py to just use its functionality or place the file in same directory as your project and import at the top of your file.

pub_key = public key of sender wallet
priv_key = private key of sender wallet

##### Functions - Send
acc_to = the account to send sats to(string)
send_amount = amount of sats to send(integer)
Send.sats(pub_key, priv_key, acc_to, send_amount)

send_amount = amount of sats to send(integer)
address_list = list of addresses to send to(list)
Send.satsMulti(pub_key, priv_key, send_amount, address_list = [])


##### Functions - Create
address = the address to find the balance of(string)
Create.balance(address)

tx_hash = the transaction hash to find details of(string)
Create.transaction(tx_hash)

block_number = the block number to find details of(integer)
Create.block(block_number)

##### Functions - Create
name = the name of the token(string)
ticker = the ticker / identifier of the token(string)
token_supply = the amount of tokens to mint(integer)
burnable & mintable = bolean value
Create.ERC20(pub_key, priv_key, name, ticker, token_supply, burnable=False, mintable=False)

##### Functions - Wallets
Wallets.single()

number to create = the number of wallets / addreses to create
Wallets.multiple(number_to_create)


##### Functions - Satoshix
token_address = token address of the token you want to swap for(string)
send_amount = amount of SAT to swap for the token(integer)
Satoshix.swapExactSATForTokens(pub_key, priv_key, token_address, send_amount)


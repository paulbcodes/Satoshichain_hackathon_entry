from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
import secrets
import time

web3 = Web3(Web3.HTTPProvider("https://rpc.satoshichain.io"))
	
class Send():
    
     def sats(pub_key, priv_key, acc_to, send_amount):
            global tx_hash
            nonce = web3.eth.getTransactionCount(pub_key)
            tx = {
                    'nonce': nonce,
                    'to': acc_to,
                    'value': web3.toWei(send_amount, 'ether'),
                    'gas': 25000,
                    'gasPrice': web3.toWei('0.001', 'ether'),
                }
            signed_tx = web3.eth.account.signTransaction(tx, priv_key)

            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            tx_hash = web3.toHex(tx_hash)
            return tx_hash
     
     ######  Function to send to multiple addresses
     def satsMulti(pub_key, priv_key, send_amount, address_list = []):
          global tx_list
          tx_list = []
          nonce = web3.eth.getTransactionCount(pub_key)
          print(len(address_list))
          for i in range(0, len(address_list)):
              tx = {
                  'nonce': nonce,
                  'to': address_list[i],
                  'value': web3.toWei(send_amount, 'ether'),
                  'gas': 25000,
                  'gasPrice': web3.toWei('0.001', 'ether'),
              }
              signed_tx = web3.eth.account.signTransaction(tx, priv_key)

              tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
              tx_hash = web3.toHex(tx_hash)
              tx_list.append(tx_hash)
              nonce += 1
          return tx_list
     
class Accounts():
      ######  Function to create account
      def single():
          global wallet
          priv = secrets.token_hex(32)
          acct = Account.from_key(priv)
          acct = acct.address
          wallet = [acct, priv]
          return wallet

      ######  Function to create multiple wallets / accounts
      def multiple(number_to_create):
          global wallets
          wallets = []
          for i in range(1, number_to_create):
              priv = secrets.token_hex(32)
              acct = Account.from_key(priv)
              acct = acct.address
              wallets += [acct, priv]
          return wallets
      
class Query():
     ######  Function to chaeck wallets balance
    def balance(address):
        global balance_wei 
        balance_wei = web3.eth.getBalance(address)
        return balance_wei
    
    ######  Function to get transaction details
    def transaction(tx_hash):
        global result
        result = web3.eth.getTransactionReceipt(tx_hash)
        return result
     
     ######  Function to get block data
    def block(block_number):
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        global block_data
        block_data = web3.eth.getBlock(block_number)
        return block_data
    
###### Object to create tokens
class Tokens():
    def ERC20(pub_key, priv_key, name, ticker, token_supply, burnable=False, mintable=False):
          global tx_hash
          web3 = Web3(Web3.HTTPProvider("https://rpc.satoshichain.io"))
          erc20abi = '''[
          {
            "anonymous": false,
            "inputs": [
              {
                "indexed": false,
                "internalType": "string",
                "name": "_name",
                "type": "string"
              },
              {
                "indexed": false,
                "internalType": "string",
                "name": "_symbol",
                "type": "string"
              },
              {
                "indexed": false,
                "internalType": "string",
                "name": "_tokenType",
                "type": "string"
              },
              {
                "indexed": false,
                "internalType": "address",
                "name": "_tokenAddress",
                "type": "address"
              }
            ],
            "name": "Created",
            "type": "event"
          },
          {
            "inputs": [
              {
                "internalType": "string",
                "name": "name_",
                "type": "string"
              },
              {
                "internalType": "string",
                "name": "symbol_",
                "type": "string"
              },
              {
                "internalType": "bool",
                "name": "isBurnable_",
                "type": "bool"
              },
              {
                "internalType": "bool",
                "name": "isMintable_",
                "type": "bool"
              },
              {
                "internalType": "uint256",
                "name": "initialSupply_",
                "type": "uint256"
              }
            ],
            "name": "create",
            "outputs": [
              {
                "internalType": "bool",
                "name": "",
                "type": "bool"
              }
            ],
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "inputs": [],
            "name": "getAll",
            "outputs": [
              {
                "components": [
                  {
                    "internalType": "string",
                    "name": "name",
                    "type": "string"
                  },
                  {
                    "internalType": "string",
                    "name": "symbol",
                    "type": "string"
                  },
                  {
                    "internalType": "string",
                    "name": "tokenType",
                    "type": "string"
                  },
                  {
                    "internalType": "bool",
                    "name": "isBurnable",
                    "type": "bool"
                  },
                  {
                    "internalType": "bool",
                    "name": "isMintable",
                    "type": "bool"
                  },
                  {
                    "internalType": "address",
                    "name": "tokenAddress",
                    "type": "address"
                  }
                ],
                "internalType": "struct Token[]",
                "name": "",
                "type": "tuple[]"
              }
            ],
            "stateMutability": "view",
            "type": "function"
          }
      ]'''

          erc20address = '0xb9F5F06f2ea258Cb4e1cD6B08EF85983211999b6' 
          contract = web3.eth.contract(erc20address, abi=erc20abi) 
          nonce = web3.eth.getTransactionCount(pub_key) 
          func = contract.functions.create(
          name,
          ticker,
          burnable,
          mintable,
          token_supply,
          )
          tx = func.buildTransaction({
          'from': pub_key,
          'nonce': nonce,
          'value': web3.toWei(0, 'ether'),
          'gas': 2500000,
          'gasPrice': web3.toWei('0.001', 'ether'),
          })
          signed_tx = web3.eth.account.signTransaction(tx, priv_key)
          emitted = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
          tx_hash = web3.toHex(emitted)
          return tx_hash

class Satoshix():
     def swapExactSATForTokens(pub_key, priv_key, token_address, send_amount):
          global tx_hash
          satoshix_abi = '''[{"type":"constructor","stateMutability":"nonpayable","inputs":[{"type":"address","name":"_factory","internalType":"address"},{"type":"address","name":"_WETH","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"WETH","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountA","internalType":"uint256"},{"type":"uint256","name":"amountB","internalType":"uint256"},{"type":"uint256","name":"liquidity","internalType":"uint256"}],"name":"addLiquidity","inputs":[{"type":"address","name":"tokenA","internalType":"address"},{"type":"address","name":"tokenB","internalType":"address"},{"type":"uint256","name":"amountADesired","internalType":"uint256"},{"type":"uint256","name":"amountBDesired","internalType":"uint256"},{"type":"uint256","name":"amountAMin","internalType":"uint256"},{"type":"uint256","name":"amountBMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"payable","outputs":[{"type":"uint256","name":"amountToken","internalType":"uint256"},{"type":"uint256","name":"amountETH","internalType":"uint256"},{"type":"uint256","name":"liquidity","internalType":"uint256"}],"name":"addLiquidityETH","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"amountTokenDesired","internalType":"uint256"},{"type":"uint256","name":"amountTokenMin","internalType":"uint256"},{"type":"uint256","name":"amountETHMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"factory","inputs":[]},{"type":"function","stateMutability":"pure","outputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"}],"name":"getAmountIn","inputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"},{"type":"uint256","name":"reserveIn","internalType":"uint256"},{"type":"uint256","name":"reserveOut","internalType":"uint256"}]},{"type":"function","stateMutability":"pure","outputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"}],"name":"getAmountOut","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"uint256","name":"reserveIn","internalType":"uint256"},{"type":"uint256","name":"reserveOut","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"getAmountsIn","inputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"getAmountsOut","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"}]},{"type":"function","stateMutability":"pure","outputs":[{"type":"uint256","name":"amountB","internalType":"uint256"}],"name":"quote","inputs":[{"type":"uint256","name":"amountA","internalType":"uint256"},{"type":"uint256","name":"reserveA","internalType":"uint256"},{"type":"uint256","name":"reserveB","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountA","internalType":"uint256"},{"type":"uint256","name":"amountB","internalType":"uint256"}],"name":"removeLiquidity","inputs":[{"type":"address","name":"tokenA","internalType":"address"},{"type":"address","name":"tokenB","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountAMin","internalType":"uint256"},{"type":"uint256","name":"amountBMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountToken","internalType":"uint256"},{"type":"uint256","name":"amountETH","internalType":"uint256"}],"name":"removeLiquidityETH","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountTokenMin","internalType":"uint256"},{"type":"uint256","name":"amountETHMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountETH","internalType":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountTokenMin","internalType":"uint256"},{"type":"uint256","name":"amountETHMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountToken","internalType":"uint256"},{"type":"uint256","name":"amountETH","internalType":"uint256"}],"name":"removeLiquidityETHWithPermit","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountTokenMin","internalType":"uint256"},{"type":"uint256","name":"amountETHMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"},{"type":"bool","name":"approveMax","internalType":"bool"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountETH","internalType":"uint256"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountTokenMin","internalType":"uint256"},{"type":"uint256","name":"amountETHMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"},{"type":"bool","name":"approveMax","internalType":"bool"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountA","internalType":"uint256"},{"type":"uint256","name":"amountB","internalType":"uint256"}],"name":"removeLiquidityWithPermit","inputs":[{"type":"address","name":"tokenA","internalType":"address"},{"type":"address","name":"tokenB","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountAMin","internalType":"uint256"},{"type":"uint256","name":"amountBMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"},{"type":"bool","name":"approveMax","internalType":"bool"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}]},{"type":"function","stateMutability":"payable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapETHForExactTokens","inputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"payable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapExactETHForTokens","inputs":[{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"payable","outputs":[],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","inputs":[{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapExactTokensForETH","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapExactTokensForTokens","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapTokensForExactETH","inputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"},{"type":"uint256","name":"amountInMax","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapTokensForExactTokens","inputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"},{"type":"uint256","name":"amountInMax","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"receive","stateMutability":"payable"}]'''

          satoshix_address   = "0x1c3d90C09978db72e40BCB67B0409aABA3E3126F"
          nonce = web3.eth.getTransactionCount(pub_key)
          contract = web3.eth.contract(satoshix_address, abi=satoshix_abi)
          swap_path = ['0xba338C3a779B3a60D54A7f953c41cD7fCa4AF480', '0xa43b79Df334a19ce89838e7062f0390E012E69D8', token_address]
          amount_out_min = 0
          deadline = int(time.time() + 60)
          func = contract.functions.swapExactETHForTokens(
          amount_out_min,
          swap_path,
          pub_key,
          deadline
          )
          tx = func.buildTransaction({
          'from': pub_key,
          'nonce': nonce,
          'value': web3.toWei(send_amount, 'ether'),
          'gas': 250000,
          'gasPrice': web3.toWei('0.001', 'ether'),
          })
          signed_tx = web3.eth.account.signTransaction(tx, priv_key)
          emitted = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
          tx_hash = web3.toHex(emitted)
          return tx_hash
    

#Tokens.ERC20('0xe68ca8D09816CDa4C44D818Bdb8625cDbD481C33', 'c7e64df4b232c0be26389401a980757d8bb5088b4c9bfd6206552778b4980a8c', 'thur3000', 'thur', 3000, True, False)
Satoshix.swapExactSATForTokens('0xe68ca8D09816CDa4C44D818Bdb8625cDbD481C33', 'c7e64df4b232c0be26389401a980757d8bb5088b4c9bfd6206552778b4980a8c', '0x20420c2d841442c248e57B506079dF3C408e9541', 100)



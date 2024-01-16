import json
import web3
import datetime
from WapsClient.logger import logger

class Uniswap():

    @staticmethod
    def convert_wei_to_eth(wei):
        return web3.Web3.fromWei(wei, 'ether')

    @staticmethod
    def convert_eth_to_wei(wei):
        return web3.Web3.toWei(wei, 'ether')

    @staticmethod
    def get_default_deadline():
        return int(datetime.datetime.now().timestamp() + 1200)

    def get_asset_out_qnty_from_tx(self,tx,token_addr):
        # for the transaction, we are looking for the number of coins that were ultimately withdrawn from the uniswap contract
        err=0
        while err==0:
            print(1)
            try:
                tx_rec=self.provider.eth.getTransactionReceipt(tx)
                err=1
            except:
                err=0
        for i in tx_rec['logs']:
            if i['address']==token_addr and any([j.hex().endswith(tx_rec['from'].lower()[2:]) for j in i['topics'] ]):
                amount=int(i['data'],0)
                return int(amount)
        return None

    def get_erc_contract_by_addr(self,addr):
        # if addr==self.waps_addr:
        #     from WapsClient.models import w3_mainnet
        #     contr = w3_mainnet.eth.contract(address=w3_mainnet.toChecksumAddress(addr),
        #                                        abi=self.erc_20_abi)
        # else:
        contr = self.provider.eth.contract(address=self.provider.toChecksumAddress(addr),
                                           abi=self.erc_20_abi)
        return contr

    def __init__(self, addr, key, provider: web3, weth_address, router_addr, net_type, mainnet=False, slippage=0.05):

        # the address from which we are doing something
        self.addr = addr

        # the key to this wallet
        self.key = key

        # allowable drawdown in price - odds 0-1
        self.slippage = slippage

        # the web3 object through which to connect
        self.provider = provider

        # for all the shit in the world we take abi contract erc20
        with open("erc20.abi") as f:
            self.erc_20_abi = json.load(f)
        #chainnet setting
        if mainnet:
            self.weth_addr = self.provider.toChecksumAddress(weth_address)
        else:
            self.weth_addr = self.provider.toChecksumAddress(weth_address)

        # the contract is dilapidated so that the balance and all that
        self.weth_contr = provider.eth.contract(self.weth_addr, abi=self.erc_20_abi)

        # self.waps_addr='0x0c79b8f01d6f0dd7ca8c98477ebf0998e1dbaf91'
        # self.waps_contr=self.get_erc_contract_by_addr(self.waps_addr)

        # uniswap router address
        self.uni_adr = router_addr

        # abi
        abi_path =''
        if net_type   == "0":
            abi_path = 'Net/KOVAN/router.abi'
        elif net_type == "1":
            abi_path = 'Net/BSC/router.abi'
        elif net_type == "2":
            abi_path = 'Net/ETH/router.abi'
        elif net_type == "3":
            abi_path = 'Net/POL/router.abi'
            
        with open(abi_path) as f:
            self.abi = json.load(f)

        # контракт юнисвопа, через который уже можно шо то делать
        self.uni_contract = provider.eth.contract(self.uni_adr, abi=self.abi)


    def get_out_qnty_by_path(self, amount, path):
        # the amount of path [-1] tokens that we get by giving the amount of path [0] tokens
        # like how many tokens we will get if we exchange a certain amount along the way
        # SwapExactTokensForTokens
        try:
            return self.uni_contract.functions.getAmountsOut(int(amount),
                                                         path).call()[-1]
        except Exception as ex:
            print(ex)
            logger.info("get_out_qnty_by_path exception")
            return None
    def get_in_qnty_by_path(self, amount, path):
        # the amount of path [0] tokens we need to get the amount of path [-1] tokens
        # like how many tokens a do we need to get a specific number of tokens b along the path
        # SwapTokensForExactTokens

        return self.uni_contract.functions.getAmountsIn(int(amount),
                                                        path).call()[0]

    def get_min_out_tokens(self, price,slippage):
        # the minimum amount of tokens we will receive with slippage
        return int(price / (1 + slippage))

    def get_max_in_tokens(self, price,slippage):
        # the maximum number of tokens we need to buy with slippage
        return int(price / (1 - slippage))

    def _create_exact_token_for_token_tx(self, in_token_amount, min_out_token_amount, path, deadline,fee_support=True ):
         # create a transaction to exchange a specific amount of token for ether
         # all arguments are required, since this function is at the very bottom of the calls, only another method can be called here
        # create a transaction through the router contract function
        if fee_support==False:
            tx = self.uni_contract.functions.swapExactTokensForTokens(int(in_token_amount), int(min_out_token_amount), path,
                                                                  self.addr,
                                                                  deadline, )
        else:
            tx=self.uni_contract.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(int(in_token_amount), int(min_out_token_amount), path,
                                                                  self.addr,
                                                                  deadline, )
        return tx

    def _create_token_for_exact_token_tx(self, max_in_token_amount, out_token_amount, path, deadline,):
        # create a transaction to exchange a token for a specific amount of another token


        # create a transaction through the router contract function
        tx = self.uni_contract.functions.swapTokensForExactTokens(int(out_token_amount), int(max_in_token_amount), path,
                                                                  self.addr,
                                                                  deadline, )
        return tx


    def swap_exact_token_for_token(self, in_token_amount, path, min_out_token_amount,
                                   deadline=None, gas=320000,
                                   gas_price=None,fee_support=True):
        # send a transaction to exchange a specific amount of Ether for a token
        # set deadline
        try:
            if deadline is None:
                deadline = self.get_default_deadline()

            # create a transaction
            tx = self._create_exact_token_for_token_tx(in_token_amount, min_out_token_amount, path,
                                                       deadline=deadline,fee_support=fee_support )

            # add all kinds of nonce, gas, etc.
            b_tx = self.build_tx(tx, gas=gas, gas_price=gas_price)

            # signed the transaction with a key
            signed_tx = self.sign_row_tx(b_tx)
            # performed
            return self.send_signed_raw_tx(signed_tx)
        except Exception as ex:
            logger.exception(ex)
            raise ex


    def swap_token_for_exact_token(self, out_token_amount, path, max_in_token_amount=None,
                                   deadline=None, gas=320000,
                                   gas_price=None):
        # send a transaction to exchange a specific amount of Ether for a token
        # set deadline
        if deadline is None:
            deadline = self.get_default_deadline()

        # create a transaction
        tx = self._create_token_for_exact_token_tx(max_in_token_amount, out_token_amount, path,
                                                   deadline=deadline, )

        # add all kinds of nonce, gas, etc.
        b_tx = self.build_tx(tx, gas=gas, gas_price=gas_price)

        signed_tx = self.sign_row_tx(b_tx)

        our_tx =  self.send_signed_raw_tx(signed_tx)
        
        return our_tx

    def build_tx(self, tx, gas, gas_price):
        # add required fields to the transaction

        b_tx = tx.buildTransaction({'from': self.addr, 'gas': gas,
                                    'gasPrice': gas_price,
                                    'nonce': self.provider.eth.getTransactionCount(self.addr,"pending"),
                                    })
        return b_tx

    def sign_row_tx(self, tx):
        
        s_tx = self.provider.eth.account.sign_transaction(tx,
                                                          private_key=self.key)
        return s_tx

    def send_signed_raw_tx(self, tx):
       
        tx_hash =  self.provider.eth.sendRawTransaction(tx.rawTransaction)
        tx = tx_hash.hex()
        self.provider.eth.waitForTransactionReceipt(tx)
        return tx_hash

    def get_allowance(self, contr_addr):
        contr = self.get_erc_contract_by_addr(contr_addr)
        return contr.functions.allowance(self.addr, self.uni_adr).call()

    def approve(self, contr_addr,gas_price,value=None):
        contr = self.get_erc_contract_by_addr(contr_addr)
        if value is None:
            value=115792089237316195423570985008687907853269984665640564039457584007913129639935
        tx = contr.functions.approve(self.uni_adr, value)
        b_tx = self.build_tx(tx,gas= 300000,gas_price=gas_price)
        signed_tx = self.sign_row_tx(b_tx)
        return self.send_signed_raw_tx(signed_tx).hex()

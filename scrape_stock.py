# API Key = 9908a58b-eeb0-4b93-8cc2-818b98c73ce5
from stocksymbol import StockSymbol

api_key = '9908a58b-eeb0-4b93-8cc2-818b98c73ce5'
ss = StockSymbol(api_key)

symbol_list_id = ss.get_symbol_list(market="indonesia")
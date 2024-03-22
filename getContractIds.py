import datetime
from ib_insync import *

import csv

ib = IB()
ib.connect('localhost', 4002, clientId=3)
ib.reqMarketDataType(4)
#god forbid they give you live dividend data so you must switch to delayed


original = open('haus.csv')
wrangled = open('haus_conid.csv', 'w')

with original as f1, wrangled as f2:
    reader = csv.reader(f1)
    writer = csv.writer(f2)
    writer.writerow(next(reader))
    for row in reader:
        ticker = row[13]
        venue = row[8]
        currency = row[7]
        # print(currency)
        contract = Stock(ticker, venue, currency)
        cntData = ib.reqContractDetails(contract)


        mktData = ib.reqMktData(contract, '456') #456 is ib api's **convoluted*** dividend enumerated param for getting dividend data. 
        ib.sleep(1) # give the api time fetch the data. ideally would figure out async way  #TODO
        # print(contract)
        # print(cntData[0].contract.conId)
        # print(mktData.dividends)


        if not cntData:
            row[6] = "none"
            writer.writerow(row)
            continue


        row[14] = contId = cntData[0].contract.conId
        row[15] = industry = cntData[0].industry
        row[16] = cntData[0].category
        row[17] = cntData[0].subcategory
        
        row[18] = primaryExchange = cntData[0].contract.primaryExchange
        if hasattr(mktData, 'dividends'):
            row[19] = next_dividend_date = getattr(mktData.dividends, 'nextDate', 'badData')
            row[20] = next_dividend_amount = getattr(mktData.dividends, 'nextAmount', 'badData')
            row[21] = next_12_month_total_dividends = getattr(mktData.dividends, 'next12Months', 'badData')
            row[22] = previous_12_month_dividends_total = getattr(mktData.dividends, 'past12Months', 'badData')

        writer.writerow(row)

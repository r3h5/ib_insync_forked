import datetime
from ib_insync import *

import csv

ib = IB()
ib.connect('localhost', 7497, clientId=3)


original = open('haus.csv')
wrangled = open('haus_conid.csv', 'w')

with original as f1, wrangled as f2:
    reader = csv.reader(f1)
    writer = csv.writer(f2)
    writer.writerow(next(reader))
    for row in reader:
        ticker = row[2]
        contract = Stock(ticker, 'SMART', 'USD')
        cntData = ib.reqContractDetails(contract)

        mktData = ib.reqMktData(contract, '456') #456 is ib api's **convoluted*** dividend enumerated param for getting dividend data. 
        ib.sleep(1.5) # give the api time fetch the data. ideally would figure out async way  #TODO
        print(contract)
        print(cntData[0].contract.conId)
        print(mktData.dividends)

        row[3] = industry = cntData[0].industry+'/ '+cntData[0].category+'/ '+cntData[0].subcategory
        
        row[6] = contId = cntData[0].contract.conId
        row[7] = primaryExchange = cntData[0].contract.primaryExchange
        if hasattr(mktData, 'dividends'):
            row[8] = next_dividend_date = getattr(mktData.dividends, 'nextDate', 'badData')
            row[9] = next_dividend_amount = getattr(mktData.dividends, 'nextAmount', 'badData')
            row[10] = next_12_month_total_dividends = getattr(mktData.dividends, 'next12Months', 'badData')
            row[11] = previous_12_month_dividends_total = getattr(mktData.dividends, 'past12Months', 'badData')

        writer.writerow(row)

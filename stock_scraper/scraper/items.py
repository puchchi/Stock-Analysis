'''This module will help in saving data through item
    field to database
'''

from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, Join
from scraper import utility


class StockOptionItem(Item):
    # This class will contains Option(Call/Put) values only
    Date = Field(
                 input_processor=MapCompose(utility.dateEncoding),
                 output_processor=Join(),
                 )  # DDMMYYYY
    Expiry = Field(
                   input_processor=MapCompose(utility.expiryEncoding),
                   output_processor=Join(''),
                   )  # DDMMYYYY+OptionType+StrikePrice   
    Open = Field(
                 input_processor=MapCompose(utility.strToFloatNumber),
                 output_processor=Join(),
                 )# '7,500.00' to '7500.00'
    High = Field(
                 input_processor=MapCompose(utility.strToFloatNumber),
                 output_processor=Join(),
                 )# '7,500.00' to '7500.00'
    Low = Field(
                input_processor=MapCompose(utility.strToFloatNumber),
                output_processor=Join(),
                )# '7,500.00' to '7500.00'
    Close = Field(
                  input_processor=MapCompose(utility.strToFloatNumber),
                  output_processor=Join(),
                  )# '7,500.00' to '7500.00'
    NoOfContracts = Field(
                          input_processor=MapCompose(utility.strToIntNumber),
                          output_processor=Join(),
                          )# '7,500.00' to '7500'
    Turnover = Field(
                     input_processor=MapCompose(utility.strToFloatNumber),
                     output_processor=Join(),
                     )  # '7,500.00' to '7500.00'# In lacks
    OpenInterest = Field(
                         input_processor=MapCompose(utility.strToIntNumber),
                         output_processor=Join(),
                         )# '7,500.00' to '7500'
    ChangeInOI = Field(
                       input_processor=MapCompose(utility.strToIntNumber),
                       output_processor=Join(),
                       )# '7,500.00' to '7500'


class kHistoricIndexItem(Item):
    Date = Field(input_processor=MapCompose(utility.dateEncoding),output_processor=Join(),)  
    Open = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500.00'
    High = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500.00'
    Low = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500.00'
    Close = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500.00'
    SharesTraded = Field(input_processor=MapCompose(utility.strToIntNumber),output_processor=Join(),)# '7,500.00' to '7500.00'
    Turnover = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500.00'  # In lacks
    DatabaseTableName = Field(output_processor=Join())


class kHistoricEquityItem(Item):
    Date = Field(input_processor=MapCompose(utility.dateEncoding),output_processor=Join(),)  
    Open = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500.00'
    High = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500.00'
    Low = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500.00'
    Close = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500.00'
    SharesTraded = Field(input_processor=MapCompose(utility.strToIntNumber),output_processor=Join(),)# '7,500.00' to '7500.00'
    Turnover = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500.00'  # In lacks
    DatabaseTableName = Field(output_processor=Join())
    

class kHistoricOptionItem(Item):
    # This class will contains Option(Call/Put) values only
    Date = Field(input_processor=MapCompose(utility.dateEncoding),output_processor=Join(),)  # DDMMYYYY
    Expiry = Field()
    OptionType = Field()
    StrikePrice = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500.00'
    Open = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join(), )# '7,500.00' to '7500.00'
    High = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join(),)# '7,500.00' to '7500.00'
    Low = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500.00'
    Close = Field( input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join(),)# '7,500.00' to '7500.00'
    NoOfContracts = Field(input_processor=MapCompose(utility.strToIntNumber),output_processor=Join(),)# '7,500.00' to '7500'
    Turnover = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)  # '7,500.00' to '7500.00'# In lacks
    OpenInterest = Field(input_processor=MapCompose(utility.strToIntNumber),output_processor=Join(),)# '7,500.00' to '7500'
    ChangeInOI = Field(input_processor=MapCompose(utility.strToIntNumber),output_processor=Join(),)
    DatabaseTableName = Field()


class kLiveOptionItem(Item):
        OpenInterestCall = Field(input_processor=MapCompose(utility.strToIntNumber),)
        ChangeInOICall = Field(input_processor=MapCompose(utility.strToIntNumber),)
        VolumeCall = Field(input_processor=MapCompose(utility.strToIntNumber),)
        ImpliedVolatilityCall = Field(input_processor=MapCompose(utility.strToFloatNumber),)
        LTPCall = Field(input_processor=Join(), output_processor=MapCompose(utility.strToFloatNumber),)
        NetChangeCall = Field(input_processor=MapCompose(utility.strToFloatNumber),)
        StrikePrice = Field(input_processor=MapCompose(utility.strToIntNumber),)
        NetChangePut = Field(input_processor=MapCompose(utility.strToFloatNumber),)
        LTPPut = Field(input_processor=Join(), output_processor=MapCompose(utility.strToFloatNumber),)
        ImpliedVolatilityPut = Field(input_processor=MapCompose(utility.strToFloatNumber),)
        VolumePut = Field(input_processor=MapCompose(utility.strToIntNumber),)
        ChangeInOIPut = Field(input_processor=MapCompose(utility.strToIntNumber),)
        OpenInterestPut = Field(input_processor=MapCompose(utility.strToIntNumber),)
        DatabaseTableName = Field()
        Symbol = Field()
        Expiry = Field()
        TimeStamp = Field(output_processor=Join())


class kLiveEquityItem(Item):

    Symbol = Field(output_processor=Join()) 
    Open = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join(), )# '7,500.00' to '7500.00'
    High = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join(),)# '7,500.00' to '7500.00'
    Low = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500.00'
#    PrevClose = Field( input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join(),)# '7,500.00' to '7500.00'
    LTP = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500'
    TotalChange = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)  # '7,500.00' to '7500.00'# In lacks
    PerChange = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500'
    Volume = Field(input_processor=MapCompose(utility.strToIntNumber),output_processor=Join(),)
    Turnover = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)  # '7,500.00' to '7500.00'# In lacks
#    TotalBuyQuantity = Field(input_processor=MapCompose(utility.strToIntNumber),output_processor=Join(),)# '7,500.00' to '7500'
 #   TotalSellQuantity = Field(input_processor=MapCompose(utility.strToIntNumber),output_processor=Join(),)
    DatabaseTableName = Field(output_processor=Join())
    TimeStamp = Field(output_processor=Join())


class kLiveFutureItem(Item):
    StockIdentifier_f = Field(output_processor=Join())
    Open = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join())
    High = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join())
    Low = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join())
    PrevClose = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join())
    LastTradedPrice = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join())
    Volume = Field(input_processor=MapCompose(utility.strToIntNumber), output_processor=Join())
    Turnover = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join())
    UnderlyingValue = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join()) 
    AnnualisedVolatility = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join())
    DailyVolatility = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join())
    OpenInterest = Field(input_processor=MapCompose(utility.strToIntNumber), output_processor=Join())
    ChangeInOI = Field(input_processor=MapCompose(utility.strToIntNumber), output_processor=Join())
    PerChangeInOI = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join())

    
class kLiveIndexItem(Item):

    Symbol = Field(output_processor=Join()) 
    Open = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join(), )# '7,500.00' to '7500.00'
    High = Field(input_processor=MapCompose(utility.strToFloatNumber), output_processor=Join(),)# '7,500.00' to '7500.00'
    Low = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500.00'
    LTP = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500'
    TotalChange = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)  # '7,500.00' to '7500.00'# In lacks
    PerChange = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)# '7,500.00' to '7500'
    Volume = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)
    Turnover = Field(input_processor=MapCompose(utility.strToFloatNumber),output_processor=Join(),)  # '7,500.00' to '7500.00'# In lacks
    DatabaseTableName = Field(output_processor=Join())
    TimeStamp = Field(output_processor=Join())
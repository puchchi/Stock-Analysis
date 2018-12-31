import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import pandas as pd

class kAverageDirectionalIndex():

    def __init__(self):
        print "In kADI class"

    def CalculateTrPlusDmMinusDm(self, i):
        tr = max( (self.high[i] - self.low[i]), abs(self.high[i] - self.close[i-1]), abs(self.low[i] - self.close[i-1]))

        plusDM = 0
        if (self.high[i] - self.high[i-1]) > (self.low[i-1] - self.low[i]) and (self.high[i] - self.high[i-1]) > 0:
            plusDM = (self.high[i] - self.high[i-1])
            
        minusDM = 0
        if (self.low[i-1] - self.low[i]) >= (self.high[i] - self.high[i-1]) and (self.low[i-1] - self.low[i]) > 0:
            minusDM = (self.low[i-1] - self.low[i])

        return tr, plusDM, minusDM


    def Calculate14RollingWindow(self, col, i):
        # Subsequent Values = Prior TR14 - (Prior TR14/14) + Current TR1
        col14 = col + "14"
        return self.adiDF[col14][i-1] - (self.adiDF[col14][i-1]/14) + self.adiDF[col][i]

    
    def CalculateTrPlusDmMinusDm14(self, i):
        tr14 = self.Calculate14RollingWindow("TR", i)
        plusDM14 = self.Calculate14RollingWindow("+DM", i)
        minusDM14 = self.Calculate14RollingWindow("-DM", i)

        return tr14, plusDM14, minusDM14


    def calculate(self, dataframe):
        #####  ALGORITHM #####
        # Calculate the True Range (TR), Plus Directional Movement (+DM) and Minus Directional Movement (-DM) for each period.
        # Smooth these periodic values using Wilder's smoothing techniques. These are explained in detail in the next section.
        # Divide the 14-day smoothed Plus Directional Movement (+DM) by the 14-day smoothed True Range to find the 14-day Plus Directional Indicator (+DI14). Multiply by 100 to move the decimal point two places. This +DI14 is the green Plus Directional Indicator line (+DI) that is plotted along with the ADX line.
        # Divide the 14-day smoothed Minus Directional Movement (-DM) by the 14-day smoothed True Range to find the 14-day Minus Directional Indicator (-DI14). Multiply by 100 to move the decimal point two places. This -DI14 is the red Minus Directional Indicator line (-DI) that is plotted along with the ADX line.
        # The Directional Movement Index (DX) equals the absolute value of +DI14 less -DI14 divided by the sum of +DI14 and -DI14. Multiply the result by 100 to move the decimal point over two places.
        # After all these steps, it is time to calculate the Average Directional Index (ADX) line. The first ADX value is simply a 14-day average of DX. Subsequent ADX values are smoothed by multiplying the previous 14-day ADX value by 13, adding the most recent DX value, and dividing this total by 14.

        #####  FORMULA of TR #####
        # max( (Current High - current Low), abs(Current High - previous Close), abs(Current Low - previous Close))

        #####  FORMULA of Plus Directial Indicator(+DM) & Minus Directional Movement (-DM) #####
        # +DM = (Cur High - Prev High) > (Prev Low - Cur Low) ? (Cur High - Prev High) : 0
        # -DM = (Prev Low - Cur Low) > (Cur High - Prev High) ? (Prev Low - Cur Low) : 0
        # A negative value would simply be entered as zero in case of +DM and -DM 

        #####  FORMULA of TR14, +DM14 & -DM14 #####
        # First TR14 = Sum of first 14 periods of TR1 
        # Subsequent Values = Prior TR14 - (Prior TR14/14) + Current TR1


        self.date = dataframe.index
        self.high = dataframe["High"]
        self.close = dataframe["Close"]
        self.low = dataframe["Low"]

        self.adiDF = pd.DataFrame(columns=("Date","TR", "+DM", "-DM", "TR14", "+DM14", "-DM14", "+DI14", "-DI14","DI14Diff", "DI14Sum", "DX", "ADX"))

        # Inserting 0th value.
        self.adiDF.loc[0] = [self.date[0],0,0,0,0,0,0,0,0,0,0,0,0]
        
        #inserting rest 13 value.
        for i in range(1, 14):
            tr, plusDM, minusDM = self.CalculateTrPlusDmMinusDm(i)            
            self.adiDF.loc[i] = [self.date[i], tr, plusDM, minusDM, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Inserting 14th value
        tr, plusDM, minusDM = self.CalculateTrPlusDmMinusDm(14)
        tr14 = self.adiDF["TR"].sum() + tr
        plusDM14 = self.adiDF["+DM"].sum() + plusDM
        minusDM14 = self.adiDF["-DM"].sum() + minusDM
        plusDI14 = plusDM14 / tr14 * 100
        minusDI14 = minusDM14 / tr14 * 100
        di14Diff = abs(plusDI14 - minusDI14)
        di14Sum = abs(plusDI14 + minusDI14)
        dx = 0
        if (di14Sum):
            dx = di14Diff / di14Sum * 100

        self.adiDF.loc[14] = [self.date[14], tr, plusDM, minusDM, tr14, plusDM14, minusDM14, plusDI14, minusDI14, di14Diff, di14Sum, dx, 0]

        # Now inserting next 13(till 27th) value
        for i in range(15, 28):
            tr, plusDM, minusDM = self.CalculateTrPlusDmMinusDm(i)
            self.adiDF.loc[i] = [self.date[i], tr, plusDM, minusDM, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            tr14, plusDM14, minusDM14 = self.CalculateTrPlusDmMinusDm14(i)

            plusDI14 = plusDM14 / tr14 * 100
            minusDI14 = minusDM14 / tr14 * 100
            di14Diff = abs(plusDI14 - minusDI14)
            di14Sum = abs(plusDI14 + minusDI14)
            if di14Sum:
                dx = di14Diff / di14Sum * 100
            self.adiDF.loc[i] = [self.date[i], tr, plusDM, minusDM, tr14, plusDM14, minusDM14, plusDI14, minusDI14, di14Diff, di14Sum, dx, 0]

        # Now inserting 28th value(First ADX value)
        tr, plusDM, minusDM = self.CalculateTrPlusDmMinusDm(i)
        self.adiDF.loc[28] = [self.date[28], tr, plusDM, minusDM, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        tr14, plusDM14, minusDM14 = self.CalculateTrPlusDmMinusDm14(28)

        plusDI14 = plusDM14 / tr14 * 100
        minusDI14 = minusDM14 / tr14 * 100
        di14Diff = abs(plusDI14 - minusDI14)
        di14Sum = abs(plusDI14 + minusDI14)
        dx = di14Diff / di14Sum * 100

        adx = self.adiDF["DX"].sum() / 14
        self.adiDF.loc[28] = [self.date[28], tr, plusDM, minusDM, tr14, plusDM14, minusDM14, plusDI14, minusDI14, di14Diff, di14Sum, dx, adx]

        # Now inserting rest of the value value
        for i in range(29, self.close.count()):
            tr, plusDM, minusDM = self.CalculateTrPlusDmMinusDm(i)
            self.adiDF.loc[i] = [self.date[i], tr, plusDM, minusDM, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            tr14, plusDM14, minusDM14 = self.CalculateTrPlusDmMinusDm14(i)

            plusDI14 = plusDM14 / tr14 * 100
            minusDI14 = minusDM14 / tr14 * 100
            di14Diff = abs(plusDI14 - minusDI14)
            di14Sum = abs(plusDI14 + minusDI14)
            dx = di14Diff / di14Sum * 100

            adx = (self.adiDF["ADX"][i-1]*13 + dx) / 14
            self.adiDF.loc[i] = [self.date[i], tr, plusDM, minusDM, tr14, plusDM14, minusDM14, plusDI14, minusDI14, di14Diff, di14Sum, dx, adx]


        self.adiDF = self.adiDF.set_index("Date")
        self.adiDF = self.adiDF.drop(["TR", "+DM", "-DM", "TR14", "+DM14", "-DM14", "DI14Diff", "DI14Sum", "DX"], axis=1)
        #print self.adiDF

        return self.adiDF

        
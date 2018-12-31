import MySQLdb

def connectDB():
    mysql = MySQLdb.connect('localhost', 'StockUser', 'StockPass', 'StockDB', charset="utf8", use_unicode=True)
    cursor = mysql.cursor()
    SQL = """
        select Close from SpotValueOfNifty50 where Date= 12012014;
    """
    cursor.execute(SQL)
    
    print int(cursor.fetchone()[0])
    
    mysql.close()
    
if __name__=='__main__':
    connectDB()



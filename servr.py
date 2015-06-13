import sqlite3
import serial

con=sqlite3.connect('server.db')
if con:
	print 'Connected to Data base succesfully'
else :
	print 'failed Database connection cahnge permission to read and write'
if con.execute(''' CREATE TABLE Datas
	        (SNO INTEGER PRIMARY KEY AUTOINCREMENT,
	         TIME TEXT,
	         TEMP INTEGER,
	         HUMID INTEGER,
	         MOIST INTEGER,
	         LIGHT INTEGER,
	         WATER INTEGER,
	         RTIME INTEGER
	        	);'''):
	        	print "Table created succesfully"		
else:
	print "Table already exist"
	
port=serial.Serial("/dev/ttyACM0",9600)
if port:
	print "opened port succesfully"
	while 1:
		k=con.execute(''' SELECT RTIME FROM Datas WHERE SNO=(SELECT MAX(SNO)  FROM Datas)''')
		
		if(k):
			port.write(k)
			

		print 'waiting...'
		rcv=port.readline()
		rcv=rcv.strip()
		print "recieved data :",rcv
		if len(rcv)>0:
			temptr=int(rcv[1:2])
			humidt=int(rcv[3:4])
			moistr=int(rcv[5:6])
			lite=int(rcv[7:8]) 
			wc=int(rcv[9])
			rtime=datetime.datetime.now()
			con.execute('''' INSERT INTO Datas
				(TIME,TEMP,HUMID,MOIST,LIGHT,WATER)
				VALUES (?,?,?,?,?,?);''',(rtime,temptr,humidt,moistr,lite,wc))
			con.commit()
con.close()
port.close()			

		
			
		
	
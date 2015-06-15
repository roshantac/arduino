import sqlite3
import serial
import datetime

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
	         SURFTEMP INTEGER,
	         LEAFMOIST INTEGER,
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
			snd="x" + str (k) + "y"  #this is the recieving format kp want
			port.write(snd)


		print 'waiting...'
		rcv=port.readline()
		rcv=rcv.strip()
		print "recieved data :",rcv
		if len(rcv)>0:
			temptr=int(rcv[0:1])
			humidt=int(rcv[2:3])
			moistr=int(rcv[4:5])
			lite=int(rcv[6:7]) 
			srft=int(rcv[8:9]) #surface temp
			lifm=int(rcv[10:11])   #leaf moisture

			rtime=datetime.datetime.now()
			con.execute('''' INSERT INTO Datas
				(TIME,TEMP,HUMID,MOIST,LIGHT,SURFTEMP,LEAFMOIST)
				VALUES (?,?,?,?,?,?,?);''',(rtime,temptr,humidt,moistr,lite,srft,lifm))
			con.commit()
con.close()
port.close()			

		
			
		
	
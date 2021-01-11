#
#
# For testing SQL Server connection in CSIL through pyodbc connection (using Windows Authentication)
#
# Author: Johnny Zhang
#
# You should run this program on a CSIL Windows system. (verified with Python 3.6.2 64bit)
#
# Last modified @ 2018.03.27
#
#
# There is no need to modify this program before using.
#
# (the default database has been setup for you)
#
#

import pyodbc
import random


conn = pyodbc.connect('driver={SQL Server};Server=cypress.csil.sfu.ca;Trusted_Connection=yes;')

cur = conn.cursor()
book_id = 0
print('What do you want to do? 1:searching 2.Write review 3.Terminate')
option = input("Your choice?")
while option != 3:
    if option == 2:
       #need to print error message
        guest_name = raw_input('Please tell me your name ')
      
        
        cur.execute('SELECT * \
                        FROM [dbo].[Bookings] \
                        WHERE guest_name = ?', guest_name )
        
        row = cur.fetchone() 
        while row:
            print ("id: "  +str(row[0]))
            print ('listing_id: ' + str(row[1]))
            print ('stay_from: ' + str(row[3]))
            print ('stary_from: '+ str(row[4]))
            print(" ")
            row = cur.fetchone()

        select_id = raw_input('Please select the id you had booked ')
        select_listing_id = raw_input('Please select the listing_id you had booked ')
        review = raw_input('Please type in your review after your stay ')
        try:
            cur.execute('INSERT INTO [dbo].[Reviews](id,listing_id,comments,guest_name)\
                                VALUES(?,?,?,?)', select_id,select_listing_id,review,guest_name)
    
            conn.commit()

        except:
            print('Fail to write review due to date or name')
    if option == 1:
        min_price = input("Input the minium price ")
        max_price = input("Input the maximum price ")
        num_bed = input("Input number of bedroom needed ")
        start_year =str(raw_input("Input starting year YYYY "))
        start_month = str(raw_input("Input starting month MM "))
        start_day = str(raw_input("Input starting day DD "))
        start_date = start_year+"-"+start_month+"-"+start_day
        print("start_date: "+ start_date)
    
        end_year =str(raw_input("Input ending year YYYY "))
        end_month = str(raw_input("Input ending month MM "))
        end_day = str(raw_input("Input ending day DD "))
        end_date = end_year+"-"+end_month+"-"+end_day
        print("end_date: "+ end_date)
        cur.execute('SELECT COUNT(*) \
                    FROM [dbo].[Listings] \
                        WHERE number_of_bedrooms=? AND id IN(SELECT listing_id\
                        FROM [dbo].[Calendar]\
                        WHERE price>=? AND price <=?\
                        AND date>=? AND date< ? AND available = 1)', num_bed,min_price,max_price,start_date,end_date )
        count_result = cur.fetchone()
        print('Total result: '+ str(count_result[0]))
        continue_search = raw_input('continue? Y/N ')
        if continue_search == "Y" and count_result[0]!=0:
        
            cur.execute('SELECT listing_id,name,SUBSTRING(description,1,25),number_of_bedrooms,price \
                        FROM [dbo].[Listings] L INNER JOIN dbo.Calendar C on L.id = C.listing_id \
                        WHERE number_of_bedrooms=? AND  price>=? AND price <=?\
                        AND date>=? AND date< ? AND available = 1', num_bed,min_price,max_price,start_date,end_date )
        
            row = cur.fetchone() 
            while row:
                print ("id: "  +str(row[0]))
                print ('Name: ' + row[1])
                print ('Description: ' + row[2])
                print ('Number_of_bedrooms: ' + str(row[3]))
                print ('Price: '+ str(row[4]))
                print(" ")
                row = cur.fetchone()
        
            continue_book = raw_input('continue for booking? Y/N ')
            if continue_book =="Y":
                
                
                room_num = raw_input('Please input the id you want to book ')
                cur.execute('SELECT COUNT(*) \
                        FROM [dbo].[Listings], [dbo].[Calendar] \
                        WHERE number_of_bedrooms=? AND price>=? AND price <=?\
                        AND date>=? AND date< ? AND available = 1 AND listing_id = ?'\
                        , num_bed,min_price,max_price,start_date,end_date,room_num )
                legit_check = cur.fetchone()
                
                if legit_check[0] == 0:
                   print('The room is not available for booking')
                
                
                
                else:
                    guest_name = raw_input('Please tell me your name ')
                    guest_num = input('How many guests? ')
                    print('Booking success')
                    book_id+=random.randint(1,100000000)
                    cur.execute('INSERT INTO [dbo].[Bookings](id,listing_id,guest_name,stay_from,stay_to,number_of_guests)\
                                VALUES(?,?,?,?,?,?)', book_id,room_num,guest_name,start_date,end_date,guest_num)
    
                    conn.commit()

        
        else:
            print("No result")





        
    print('What else do you want to do? 1:searching 2.Write review 3.Terminate')
    option = input("Your choice?")


# id, name, first 25 characters of description, number of bedrooms, price



    
# to validate the connection, there is no need to change the following line
#cur.execute('SELECT username,password from dbo.helpdesk')
#row = cur.fetchone()

#while row:
 #   print ('SQL Server standard login name = ' + row[0])
  #  print ('The password for this login name = ' + row[1])
   # row = cur.fetchone()

conn.close()

#  This program will output your CSIL SQL Server standard login,
#  If you see the output as s_<yourusername>, it means the connection is a success.
#  
#  You can now start working on your assignment.
# 

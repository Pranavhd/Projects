#!/usr/bin/python2.7
#
# Interface for the assignement
#

import psycopg2

DATABASE_NAME = 'dds_assgn1'


def getopenconnection(user='postgres', password='1234', dbname='postgres'):
    return psycopg2.connect("dbname='" + dbname + "' user='" + user + "' host='localhost' password='" + password + "'")


def loadratings(ratingstablename, ratingsfilepath, openconnection):
    cur = openconnection.cursor()

    cur.execute("DROP TABLE IF EXISTS " + ratingstablename)
    cur.execute("CREATE TABLE " + ratingstablename + " (row_id serial primary key,UserID INT, semicol1 VARCHAR(10),  MovieID INT , semicol3 VARCHAR(10),  Rating REAL, semicol2 VARCHAR(10), Timestamp INT)")
    path_to_file = open(ratingsfilepath, 'r')
    # get path details of the file

    cur.copy_from(path_to_file, ratingstablename, sep=':',columns=('UserID', 'semicol1', 'MovieID', 'semicol3', 'Rating', 'semicol2', 'Timestamp'))
    cur.execute("ALTER TABLE " + ratingstablename + " DROP COLUMN semicol1, DROP COLUMN semicol3,DROP COLUMN semicol2, DROP COLUMN Timestamp")
    #cur.execute("INSERT INTO " + ratingstablename + " VALUES (100,1,1);")
    #cur.execute("SELECT setval(" + ratingstablename_row_id_seq + ", (SELECT MAX(id)  from " + ratingstablename + "));")

    # meta-tables store specific data related to each of the tables
    cur.execute("DROP TABLE IF EXISTS META_RANGE")
    cur.execute("DROP TABLE IF EXISTS META_ROUND")
    cur.execute("CREATE TABLE META_RANGE (NUM_PART INT NOT NULL);")
    cur.execute("CREATE TABLE META_ROUND (LAST_PART INT NOT NULL);")

    # finally close the connection
    cur.close()

def rangepartition(ratingstablename, numberofpartitions, openconnection):
    cur = openconnection.cursor()

    '''
    # Uncomment to delete tables in this name format
    cur.execute("SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE 'range_part%';")
    del_list = []
    for row in cur:
        del_list.append(row[0])
    for ele in del_list:
        cur.execute("DROP TABLE IF EXISTS " + ele)
    '''

    boundary = 5.0/numberofpartitions
    start = 0
    part_num = 1
    cur.execute("INSERT INTO META_RANGE(NUM_PART) VALUES (" + str(numberofpartitions) + ");")

    # create the table accordingly
    cur.execute("CREATE TABLE range_part" + str(part_num-1) + " AS SELECT USERID, MOVIEID, RATING FROM " + ratingstablename + " WHERE Rating>=" + str(
        start) + " AND Rating<=" + str(start + boundary) + ";")
    part_num = part_num + 1
    start = start + boundary

    while start < 5.0:
        cur.execute(
            "CREATE TABLE range_part" + str(part_num-1) + " AS SELECT USERID, MOVIEID, RATING FROM " + ratingstablename + " WHERE Rating>" + str(
                start) + " AND Rating<=" + str(start + boundary) + ";")
        part_num = part_num + 1
        start = start + boundary

    # finally close the connection
    cur.close()



def roundrobinpartition(ratingstablename, numberofpartitions, openconnection):
    cur = openconnection.cursor()

    '''
    # Uncomment to delete tables in this name format
    cur.execute("SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE 'rrobin_part%';")
    del_list = []
    for row in cur:
        del_list.append(row[0])
    for ele in del_list:
        cur.execute("DROP TABLE IF EXISTS " + ele)
    '''

    #select row_id from test order by row_id desc limit 1;
    cur.execute("select row_id from " + ratingstablename + " order by row_id desc limit 1;")
    temp_part = 0
    for row in cur:
        temp_part = row[0]
    last_part = int(int(temp_part)%int(numberofpartitions))

    cur.execute("INSERT INTO META_ROUND(LAST_PART) VALUES (" + str(last_part) + ");")
    list_part_nums = list(range(1,numberofpartitions+1))

    for num in list_part_nums:
        cur.execute("CREATE TABLE rrobin_part" + str(num-1) + " AS SELECT * FROM " + ratingstablename + " WHERE row_id % " + str(numberofpartitions) + " = " + str(num%numberofpartitions))

    # finally close the connection
    cur.close


def roundrobininsert(ratingstablename, userid, itemid, rating, openconnection):
    cur = openconnection.cursor()

    temp = 0
    cur.execute("SELECT LAST_PART FROM META_ROUND")
    for row in cur:
        temp = row[0]

    # create the table accordingly
    cur.execute("INSERT INTO rrobin_part" + str(temp) + " (UserID,MovieID,Rating) VALUES (%s, %s, %s)",(userid, itemid, rating))
    cur.execute("UPDATE META_ROUND SET LAST_PART = " + str((int(temp)+1)%5) + ";")

    cur.execute("select row_id from " + ratingstablename + " order by row_id desc limit 1;")
    temp_part = 0
    for row in cur:
        temp_part = row[0]
    cur.execute("INSERT INTO " + ratingstablename + " VALUES (" + str(temp_part+1) + ",%s,%s,%s)",(userid, itemid, rating))

    # finally close the connection
    cur.close()

def rangeinsert(ratingstablename, userid, itemid, rating, openconnection):
    cur = openconnection.cursor()

    temp = 0
    cur.execute("SELECT NUM_PART FROM META_RANGE")
    for row in cur:
        temp = row[0]

    numberofpartitions = int(temp)
    boundary = 5.0 / numberofpartitions
    start = 1

    # keep checking where the rating boundary is
    while start*boundary < rating:
        start += 1
    cur.execute("INSERT INTO range_part" + str(start-1) + " (UserID,MovieID,Rating) VALUES (%s, %s, %s)",(userid, itemid, rating))

    # find the maximum row_id
    cur.execute("select row_id from " + ratingstablename + " order by row_id desc limit 1;")
    temp_part = 0
    for row in cur:
        temp_part = row[0]
    cur.execute("INSERT INTO " + ratingstablename + " VALUES (" + str(temp_part+1) + ",%s,%s,%s)",(userid, itemid, rating))

    # finally close the connection
    cur.close()


def create_db(dbname):
    """
    We create a DB by connecting to the default user and database of Postgres
    The function first checks if an existing database exists for a given name, else creates it.
    :return:None
    """
    # Connect to the default database
    con = getopenconnection(dbname='postgres')
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()

    # Check if an existing database with the same name exists
    cur.execute('SELECT COUNT(*) FROM pg_catalog.pg_database WHERE datname=\'%s\'' % (dbname,))
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute('CREATE DATABASE %s' % (dbname,))  # Create the database
    else:
        print 'A database named {0} already exists'.format(dbname)

    # Clean up
    cur.close()
    con.close()

if __name__ == '__main__':
    try:

        with getopenconnection() as con:

            #loadratings('Ratings', '/home/user/Desktop/DDS/ml-10M100K/ratings.dat', con)
            loadratings('Test', '/home/user/Desktop/DDS/ml-10M100K/test_data.dat', con)
            #rangepartition(ratingstablename='Ratings', numberofpartitions=10, openconnection=con)
            rangepartition(ratingstablename='Test', numberofpartitions=2, openconnection=con)
            roundrobinpartition(ratingstablename='Test', numberofpartitions=5, openconnection=con)
            rangeinsert(ratingstablename='Test', userid=2, itemid=2, rating=5, openconnection=con)
            roundrobininsert(ratingstablename='Test', userid=1, itemid=2, rating=5, openconnection=con)
            rangeinsert(ratingstablename='Test', userid=6, itemid=2, rating=5, openconnection=con)
            #rangepartition(ratingstablename = 'Ratings', numberofpartitions = 2, openconnection = con)
            #roundrobinpartition(ratingstablename = 'Ratings', numberofpartitions = 5, openconnection = con)
            #roundrobininsert(ratingstablename = 'Ratings', userid = 1, itemid = 2, rating = 5, openconnection = con)
            #rangeinsert(ratingstablename = 'Ratings', userid = 2, itemid = 2, rating = 4, openconnection = con)
            #rangeinsert(ratingstablename = 'Ratings', userid = 3, itemid = 3, rating = 3, openconnection = con)

    except Exception as e:
        print e
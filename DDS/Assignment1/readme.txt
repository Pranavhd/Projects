The required task is to simulate data partitioning approaches on-top of an open source relational database
management system (i.e., PostgreSQL). You must generate a set of Python functions that load the
input data into a relational table, partition the table using different horizontal fragmentation approaches,
and insert new tuples into the rightfragment.
Input Data. The input data is a Movie Rating data set collected from the MovieLens web site
(http://movielens.org). The raw data is available in the file ratings.dat.
The rating.dat file contains 10 million ratings and 100,000 tag applications applied to 10,000 movies by
72,000 users. Each line of this file represents one rating of one movie by one user, and has the following
format:
UserID::MovieID::Rating::Timestamp
Ratings are made on a 5-star scale, with half-star increments. Timestamps represent seconds since
midnight Coordinated Universal Time (UTC) of January 1, 1970. A sample of the file contents is given
below:
1::122::5::838985046
1::185::5::838983525
1::231::5::838983392
Required Task. Below are the steps you need to follow to fulfill this assignment:
1. Download the virtual machine that has the same environment with the grading machine. This is highly
recommended. You can use your own machine. But it is not ensured that you code can work in the grading
machine. If you use the provided machine, then skip Step 2. Virtual Machine setting: Python 2.7.x. Ubuntu
16.04.
2. Install PostgreSQL.
3. Download rating.dat file from the MovieLens website,
http://files.grouplens.org/datasets/movielens/ml-10m.zip
You can use partial data for testing. One testing data file is given on blackboard
4. Implement a Python function LoadRatings() that takes a file system absolute path that contains the
rating.dat file as input. LoadRatings() then loads the rating.dat content into a table (saved in
PostgreSQL) named Ratings that has the following schema
UserID (int) – MovieID (int) – Rating (float)
5. Implement a Python function Range_Partition() that takes as input: (1) the Ratings table stored in
PostgreSQL and (2) an integer value N; that represents the number of partitions. Range_Partition()
then generates N horizontal fragments of the Ratings table and store them in PostgreSQL. The
algorithm should partition the ratings table based on N uniform ranges of the Rating attribute.
6. Implement a Python function RoundRobin_Partition() that takes as input: (1) the Ratings table
stored in PostgreSQL and (2) an integer value N; that represents the number of partitions. The
function then generates N horizontal fragments of the Ratings table and stores them in PostgreSQL.
Thealgorithmshouldpartitiontheratings tableusingthe roundrobinpartitioningapproach(explained
in class).
7. Implement a Python function RoundRobin_Insert() that takes as input: (1) Ratings table stored in
PostgreSQL, (2) UserID, (3) ItemID, (4) Rating. RoundRobin_Insert() then inserts a new tuple to the
Ratings table and the right fragment based on the round robinapproach.
8. Implement a Python function Range_Insert() that takes as input: (1) Ratings table stored in PostgreSQL
(2) UserID, (3) ItemID, (4) Rating. Range_Insert() then inserts a new tuple to the Ratings
table and the correct fragment (of the partitioned ratings table) based upon the Rating value.


The number of partitions here refer to the number of tables to be created.
For rating values in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
Case N = 1,
One table containing all the values.
Case N = 2,
Two tables,
Partition 0 has values [0, 2.5]
Partition 1 has values (2.5, 5]
Case N = 3,
Three tables,
Partition 0 has values [0, 1.67]
Partition 1 has values (1.67, 3.34]
Partition 2 has values (3.34, 5]
Uniform ranges means a region is divided uniformly.

--------------------------------------------------------------------------------------------------

Other details:
Necessary software such as postgres and python have been installed on it. Pycharm has also been installed but feel free to use other IDE. 

1. Download all the files from the link: https://drive.google.com/open?id=1_efzBidI7waVEjVxJw2OJ3kv2PZO-dNm. Put all three files in your local directory.

2. Load files into either VMWare or VirtualBox.

VMWare (recommended).  It provides a free trail for CIDSE student for one year. The link is https://e5.onthehub.com/WebStore/OfferingsOfMajorVersionList.aspx?pmv=e7d3dd90-8b51-e511-940f-b8ca3a5db7a1&cmi_mnuMain=16a020b5-ed3c-df11-b4ab-0030487d8897&cmi_mnuMain_child=aafc5891-884f-e511-940f-b8ca3a5db7a1&cmi_mnuMain_child_child=6130e417-ad1a-e511-940d-b8ca3a5db7a1&ws=dbcd06b7-86b0-e411-9408-b8ca3a5db7a1&vsro=.  Use File->Open to load the .ovf file.
VirtualBox. It can be downloaded online. Use File->Import Appliance to load the .ovf file.
 The default setting up of the machine is: Memory: 4GB, Processor: 4, Disk: 15GB. You can modify them in the settings for your purpose.

3. Start the machine and log into the default user "cse512assignment".  The login password: user

3. Write your code in Interface.py. Do not change anything in the test file except for the import file name of your file name. It is commented in the test file and you check it for guidance.
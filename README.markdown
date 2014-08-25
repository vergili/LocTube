# INTRODUCTION

LocTube is a video finder via google map  coordinates system. 
To find a video you just need to drag marker to a location. If a video crawled by admin related to that location
you gonna see a list on google map. 



## SETUP  (Please do not forget to fix below BUG for geoalchemy package)

	Clone:
    git clone https://github.com/vergili/loctube loctube
    
    $ virtualenv env 
    $ source env/bin/activate 
    $ pip install -U pip 
    $ pip install -U distribute 
    $ pip install -r requirements.txt
    
    
change path for INSTANCE_FOLDER_PATH  in loctube/utils.py  
    
  
### Create database and your admin account:

Change SQLALCHEMY_DATABASE_URI for your database connection  in loctube/config.py

    python manage.py initdb
 
### Start: 
    
	python manage.py run

Open:http://127.0.0.1:5000  

   
## BUG in the geoalchemy package
    geoalchmy package has a bug  to fix it please find   base.py  and apply belowe change. 

    path to base.py  for geoalchemy package
    env/lib/python2.7/site-packages/geoalchemy/base.py
    open it  and change  
    ColumnProperty.ColumnComparator  with  ColumnProperty.Comparator 
    

## CRAWLING TRAIN DATA from wikipedia for ancient cities 

	run: 

	python CrawlWiki.py  # in the /crawler directory

it will create a LocationsList txt files for every 30 location from 
http://en.wikipedia.org/wiki/List_of_archaeological_sites_by_country

this page includes many ancient cities information with coordinates 

Note: This process is very slow  ones a list done you can start to use it for video crawling. 

## CRAWLING youtube videos 

Connect to the site  http://127.0.0.1:5000  and  login with admin account:  admin:123456
click on admin on top right 3. link  and  then crawler tab 
Then copy and paste PART of LocationsList which we generate from previous section,  in the text area then click send button. 
It will start crawling and ones it done  it will give you a flash message  with  id number of location and number of crawled entries.

Note: Each of LocationList  entry  should be in below format  otherwise crawler will cancel it
	
	id, PlaceName, latitude, longitude, Link 
	4, Balkh, 36.773056,66.873611, http://en.wikipedia.org/wiki/Balkh


	
# INTRODUCTION

LocTube is a video finder via google map  coordinates system. 
To find a video you just need to drag marker to a location. If a video crawled by admin related to that location
you gonna see a list on google map. 



## SETUP  (Please do not forget to fix below BUG for geoalchemy package)

Clone.
    git clone https://github.com/vergili/loctube loctube
    
    $ virtualenv env 
    $ source env/bin/activate 
    $ pip install -U pip 
    $ pip install -U distribute 
    $ pip install -r requirements.txt
    
    
    change path for INSTANCE_FOLDER_PATH  in loctube/utils.py  
    
    change SQLALCHEMY_DATABASE_URI for your database connection  in loctube/config.py
  
create database and your admin account
    python manage.py initdb
 
Start 
    python manage.py run

Open
    http://127.0.0.1:5000  
   
## BUG in the geoalchemy package
    geoalchmy package has a bug  to fix it please find   base.py  and apply belowe change. 

    path to base.py  for geoalchemy package
    env/lib/python2.7/site-packages/geoalchemy/base.py
    open it  and change  
    ColumnProperty.ColumnComparator  with  ColumnProperty.Comparator 
    

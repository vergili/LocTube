from sys import argv
from pyquery import PyQuery
from lxml import etree
import urllib

#crawl wikipedia list of archaelogical sites and get available geo coordinates from wmflabs.org

sitesHtml = PyQuery(url='http://en.wikipedia.org/wiki/List_of_archaeological_sites_by_country');


allLinks = sitesHtml("ul li a");


listOfCity = [];

for a in allLinks:
    if '#' not in a.attrib['href']:  
        listOfCity.append("http://en.wikipedia.org" + a.attrib['href']);               
    


LocationFile = open("LocationsList.txt", "w")
CoordinateList=[];
i=1;
for a in listOfCity:

    try : 
        siteHtml =PyQuery(url=a);

        link1 = siteHtml("#coordinates .plainlinks.nourlexpansion a").attr['href'];
        link1 = "http:" + link1;

        cityCountry = siteHtml(".label:eq(0)").text();

        siteHtml2 =PyQuery(url=link1);

        test3 = str(i) + ", " + a.split('/')[-1].replace("_", " ").replace("-", " ");

        test3 = test3 + ", " + siteHtml2("a.external.free").text().replace("geo:", "").replace("geo", "");

        test3 = test3  + ", " + a;

        CoordinateList.append(test3);

        LocationFile.write(test3+"\n")
        i+=1

   
    except Exception: 
        pass
LocationFile.close()


x = raw_input('stop?')

print "yeni"+x


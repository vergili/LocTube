# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required

from ..extensions import db
from ..decorators import admin_required

from ..user import User
from loctube.admin.forms import UserForm, CrawlerForm, VideoForm
from loctube.admin.models import Video
import requests
import json
from flask import jsonify
from flask_wtf import csrf
from geoalchemy.base import WKTSpatialElement, WKBSpatialElement

from geoalchemy import (GeometryColumn, Point, Polygon, LineString,GeometryDDL, WKTSpatialElement, 
                        DBSpatialElement, GeometryExtensionColumn,WKBSpatialElement)
from geoalchemy.functions import functions
from nose.tools import ok_, eq_, raises, assert_almost_equal
from sqlalchemy import and_
  
from geoalchemy.mysql import MySQLComparator, mysql_functions
import random
import re
import sys
from random import randrange

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template('admin/index.html', users=users, active='index')


@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users, active='users')


@admin.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    form = UserForm(obj=user, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        flash('User updated.', 'success')
         
    return render_template('admin/user.html', user=user, form=form)


@admin.route('/videos')
@login_required
@admin_required
def videos():
    videos = Video.query.all()
    return render_template('admin/videos.html', videos=videos, active='videos')


@admin.route('/video/<int:video_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def video(video_id):
    video = Video.query.filter_by(id=video_id).first_or_404()
    form = VideoForm(obj=video, next=request.args.get('next'))

    if form.is_submitted():
        form.populate_obj(video)

        db.session.add(video)
        db.session.commit()

        flash('Video updated.', 'success')

    return render_template('admin/video.html', video=video, form=form)


@admin.route('/delete_video/<int:video_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_video(video_id):
    video = Video.query.filter_by(id=video_id).first_or_404()

    db.session.delete(video)
    db.session.commit()

    message = "Video ID="+ str(video_id) + " has been deleted"
    flash( message, 'success')

    return redirect(url_for('admin.videos'))


@admin.route('/crawler', methods=['GET', 'POST'])
@login_required
@admin_required
def crawler():
    form = CrawlerForm()
    error = None
    if request.method == 'GET':
        return render_template( "admin/crawler.html", form=form)

    
    if request.method == 'POST':

        loc_info_list = form.location_list.data.split('\r\n')
        
        message1 = ""
        message2 = ""
        for loc_info in loc_info_list:

            try: 
                if regex_compare("[0-9]+,[\w]+,[-0-9.]+,[-0-9.]+", loc_info) == False: continue

                location = loc_info.split(',')
               

                googlemap_url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + location[2] + "," + location[3]

                googlemap_json = requests.get(googlemap_url) 
                # Convert it to a Python dictionary
                googlemap_data = json.loads(googlemap_json.text)

                if 'ZERO_RESULTS' in str(googlemap_data['status']): continue
          
                googlemap_country = googlemap_data['results'][0]['address_components'][-1]['long_name'] + " " + googlemap_data['results'][0]['address_components'][-2]['long_name']
            
                #since last 2 element can be country name or zip code  get both and reject numbers via regEx
                country_regex = regex_find(r'[a-zA-Z]+', googlemap_country)

                youtube_url = "http://gdata.youtube.com/feeds/api/videos?alt=json&max-results=50" + "&q=" + location[1] +" " + country_regex
        
                # Get the youtube json
                youtube_json = requests.get(youtube_url)

                # Convert it to a Python dictionary
                youtube_data = json.loads(youtube_json.text)

                res = youtube_data['feed']['openSearch$totalResults']['$t']

                if int(res) != 0: 

                    tot_entry=0
                    for item in youtube_data['feed']['entry']:

                        title = (item['title']['$t'])

                        if location[1].strip().lower() in title.lower(): 

                            video = Video()

                            video.title = unicode(item['title']['$t'])

                            video.description = unicode(item['media$group']['media$description']['$t'])

                            video.video_url   = (item['link'][0]['href'].encode('utf-8'))

                            video.image_url1  = (item['media$group']['media$thumbnail'][0]['url'].encode('utf-8'))
                            video.image_url2  = (item['media$group']['media$thumbnail'][1]['url'].encode('utf-8'))


                            video.location_lat = location[2]
                            video.location_lng = location[3]
                            video.location_link = location[4]

                            wkt_spot = "POINT(" + location[2] + " " + location[3] +")"
                            video.location_lat_lng = WKTSpatialElement(wkt_spot)

                            db.session.add(video)

                            db.session.commit()
                            tot_entry=tot_entry+1

                    message1 = message1+ location[0] + "-"+ str(tot_entry) +" "

            except Exception as inst:
                message2 += str(inst) + " - "
                pass


        flash(message1 + ' has been crawled [Id-NumberofIndexed] ' + " .... " + message2 , 'has been crawled')

        return render_template( "admin/crawler.html",form=form, active='crawler')


@admin.route('/video_search', methods=['GET', 'POST'])
def video_search():


    # this method is temporary  since geoalchemy  has problem with sqlite  video can not be found by distance between to coordinates. 
    if request.method == 'POST':


        #db.session.query(Video).filter()

        #test3 = db.session.scalar(functions._within_distance(Video.location_lat_lng, 'POINT(-88.9139332929936 35.5082802993631)', 10))
        
        posted_corr = 'POINT(' + request.data.replace('"','').replace(',',' ') + ')'

        geo_data_list = db.session.query(Video.video_url).filter(functions._within_distance(Video.location_lat_lng, posted_corr, 0.6))[:30]

        #test2 = session.scalar(functions._within_distance('POINT(-88.9139332929936 42.5082802993631)', 'POINT(-88.9139332929936 35.5082802993631)', 10)) 

        geo_data_dict ={}
        for i in range(len(geo_data_list)):
            geo_data_dict[i] = geo_data_list[i][0]




        #youtube_link = "http://gdata.youtube.com/feeds/api/videos?v=2&alt=json&prettyprint=true&location=" + request.data.replace('"','') + "!&location-radius=6mi&max-results=12";
    
        #youtube_request = requests.get(youtube_link)

        ## Convert it to a Python dictionary
        #youtube_data = json.loads(youtube_request.text)

        #test = request.data

        #coor = request.data.split(',')


        return jsonify(geo_data_dict)

def find_by_geo(event):
    radius = 20000

    #geog = WKTElement('POINT({} {})'.format(lng, lat))

    distance_query = Video.location_lat_lng.ST_Distance(event.geog).label('distance')
    nearby_query = Video.location_lat_lng.ST_DWithin(event.geog,radius)

    city_query = db.session.query(Video, distance_query)

    city_query = city_query.filter(nearby_query)

    videos = city_query.all()

    return videos




def regex_find(pat,text):
     match = re.search(pat,text)
     if match: 
        return match.group()
     else: 
         return None


def regex_compare(pat,text):

     text = text.replace(" ", "")
     match = re.search(pat,text)
     if match: 
        return True
     else: 
        return False



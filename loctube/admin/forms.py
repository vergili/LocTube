# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import HiddenField, SubmitField, RadioField, DateField, TextField, TextAreaField
from wtforms.validators import (Required, Length, EqualTo, Email, NumberRange,  URL, AnyOf, Optional)
from ..user import USER_ROLE, USER_STATUS


class UserForm(Form):
    next = HiddenField()
    role_code = RadioField(u"Role", [AnyOf([str(val) for val in USER_ROLE.keys()])],
            choices=[(str(val), label) for val, label in USER_ROLE.items()])
    status_code = RadioField(u"Status", [AnyOf([str(val) for val in USER_STATUS.keys()])],
            choices=[(str(val), label) for val, label in USER_STATUS.items()])
    # A demo of datepicker.
    created_time = DateField(u'Created time')
    submit = SubmitField(u'Save')

class CrawlerForm(Form):
    location_list = TextAreaField(u'Location List')
    submit = SubmitField(u'Save')

class VideoForm(Form):
    multipart        = False
    next             = HiddenField()
    title            = TextAreaField(u'Title')
    description      = TextAreaField(u'Description')
    video_url        = TextField(u'Video URL', [Length(max=250)])
    country          = TextField(u'Country', [Length(max=80)])
    country_code     = TextField(u'Country Code', [Length(max=5)])
    category         = TextField(u'Category', [Length(max=120)])
    category_code    = TextField(u'CategoryCode', [Length(max=120)])
    save_date        = DateField(u'Created time')
    local_rank       = TextField(u'Local Rank', [Length(max=120)])
    global_rank      = TextField(u'Global Rank', [Length(max=120)])
    image_url1       = TextField(u'Image Url-1')
    image_url2       = TextField(u'Image Url-2')
    origin_id        = TextField(u'OriginID', [Length(max=120)])
    publish_date     = DateField(u'Publish Date')
    location_lat     = TextField(u'Location Lat', [Length(max=120)])
    location_lng     = TextField(u'Location Lng', [Length(max=120)])
    #location_lat_lng = TextField(u'Location LatLng', [Length(max=120)])
    location_country = TextField(u'Location Country', [Length(max=120)])
    location_state   = TextField(u'Location State', [Length(max=120)])
    location_city    = TextField(u'Location City', [Length(max=120)])
    location_zip     = TextField(u'Location Zip', [Length(max=120)])
    location_link    = TextField(u'Location Link')
    location_visit   = TextField(u'Location Visit', [Length(max=120)])
    submit           = SubmitField(u'Save')



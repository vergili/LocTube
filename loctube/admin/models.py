# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
import requests


from ..extensions import db
from ..utils import get_current_time, SEX_TYPE, STRING_LEN
from geoalchemy import *

from geoalchemy.base import SpatialComparator, PersistentSpatialElement,GeometryBase
from geoalchemy.dialect import SpatialDialect 
from geoalchemy.functions import functions, BaseFunction, check_comparison, BooleanFunction
from geoalchemy.geometry import LineString, MultiLineString, GeometryCollection,Geometry
from geoalchemy.base import WKTSpatialElement, WKBSpatialElement
  

class Video(db.Model):

    __tablename__ = 'videos'

    id               = Column(db.Integer, primary_key=True)
    title            = Column(db.Text)
    description      = Column(db.Text)
    video_url         = Column(db.String(250))
    country          = Column(db.String(80))
    country_code      = Column(db.String(5))
    category         = Column(db.String(120))
    category_code     = Column(db.String(120))
    save_date         = Column(db.DateTime, default=get_current_time)
    local_rank        = Column(db.String(120))
    global_rank       = Column(db.String(120))
    image_url1        = Column(db.Text)
    image_url2        = Column(db.Text)
    origin_id         = Column(db.String(120))
    publish_date      = Column(db.DateTime)
    location_lat      = Column(db.String(120))
    location_lng      = Column(db.String(120))
    location_lat_lng  = GeometryColumn(Point(2))
    location_country  = Column(db.String(120))
    location_state    = Column(db.String(120))
    location_city     = Column(db.String(120))
    location_zip      = Column(db.String(120))
    location_link     = Column(db.Text)
    location_visit    = Column(db.String(120))
    
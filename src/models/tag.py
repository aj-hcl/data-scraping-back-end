from db import db, MAX_LEN

from sqlalchemy.orm import validates


class URL_Model(db.Model):
    __tablename__ = 'Web-scraper-URLs'
    __table_args__ = {'schema': 'nsds'}
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.VARCHAR(length=MAX_LEN), primary_key=True)
    children = db.relationship('TagModel', lazy = 'dynamic')

    @validates('url')
    def validate_tag(self, key, value):
        value = str(value)
        if len(value) > MAX_LEN:
            return value[:MAX_LEN]
        return value

    def __init__(self, url):
        self.url = url


    @classmethod
    def find_by_url(cls, url):
        return cls.query.filter_by(url=url).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class TagModel(db.Model):
    __tablename__ = 'Web-scraper-data'
    __table_args__ = {'schema': 'nsds'}
    url_id = db.Column(db.Integer, db.ForeignKey('nsds.Web-scraper-URLs.uid'))
    tag_name = db.Column(db.VARCHAR(length=MAX_LEN), primary_key=True)
    tag_data = db.Column(db.VARCHAR(length=MAX_LEN))
    tag_key = db.Column(db.VARCHAR(length=MAX_LEN), primary_key=True)
    parent = db.relationship('URL_Model', primaryjoin=url_id == URL_Model.uid)

    def json(self):
        return {"tag_name":self.tag_name, "tag_data": self.tag_data, "tag_key": self.tag_key}


    def __init__(self, url_id, tag_name, tag_data, tag_key):
        self.url_id = url_id
        self.tag_name = tag_name
        self.tag_data = tag_data
        self.tag_key = tag_key


    @classmethod
    def find_tag(cls, url_id, tag_name, tag_key):
        return cls.query.filter_by(url_id=url_id, tag_name=tag_name, tag_key=tag_key).first()

    @classmethod
    def find_all_by_url_id(cls, url_id):
         return cls.query.filter_by(url_id=url_id)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def save_list_to_db(cls, lst):
        try:
            for i in lst:
                db.session.add(i)
        except:
            db.session.rollback()
            raise Exception('Error saving to database')
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


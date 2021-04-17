from db import db

class ExternalDataModel(db.Model):
    __tablename__ = 'API_data'
    __table_args__ = {'schema': 'nsds'}
    login = db.Column(db.VARCHAR(length=200), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.Text)
    url = db.Column(db.Text)
    avatar_url = db.Column(db.Text)
    description = db.Column(db.Text)


    def __init__(self, login, _id, node_id, url, avatar_url, description):
        self.login = login
        self.id = _id
        self.node_id = node_id
        self.url = url
        self.avatar_url = avatar_url
        self.description = description

    def json(self):
        return {"login": self.login, "id":self.id, "node_id": self.node_id, "url": self.url, "avatar_url": self.avatar_url, "description": self.description}

    @classmethod
    def find_by_login(cls, login):
        return cls.query.filter_by(login=login).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def save_list_to_db(cls, lst):
        try:
            for i in lst:
                db.session.add(i)
        except:
            session.rollback()
            raise Exception('Error saving to database')
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

from app import app, db


class Lread(db.Model):
    __tablename__ = "lread"

    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.VARCHAR(32))
    auth = db.Column(db.VARCHAR(32))
    novel_type = db.Column(db.VARCHAR(32))
    art_title = db.Column(db.VARCHAR(32), unique=True)
    art_num = db.Column(db.BIGINT)
    text = db.Column(db.Text)


    def __init__(self, title, auth, novel_type, art_title, text):
        self.title = title
        self.auth = auth
        self.novel_type = novel_type
        self.art_title = art_title
        self.text = text


class User(db.Model):
    __tablename__ = "novel_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.VARCHAR(32), unique=True)
    password = db.Column(db.VARCHAR(32))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return e
        finally:
            return 0

    def isExisted(self):
        tempUser = User.query.filter_by(username=self.username, password=self.password).first()
        if tempUser is None:
            return 0
        else:
            return 1


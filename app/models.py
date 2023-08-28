from flask_sqlalchemy import SQLAlchemy

from .app import search_app

db = SQLAlchemy(search_app)


class Source(db.Model):
    __tablename__ = "sources"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    url = db.Column(db.String(50))

    def __repr__(self):
        return f'<Source "{self.name}">'


class Manga(db.Model):
    __tablename__ = "mangas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    link = db.Column(db.String(150))

    def __repr__(self):
        return f'<Manga "{self.name}">'


class Chapter(db.Model):
    __tablename__ = "chapters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    number = db.Column(db.Integer)
    link = db.Column(db.String(150))

    def __repr__(self):
        return f'<Chapter "{self.number}: {self.name}">'


class Page(db.Model):
    __tablename__ = "pages"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    link = db.Column(db.String(150))


class Panel(db.Model):
    # TODO: use composite key
    __tablename__ = "panels"
    id = db.Column(db.Integer, primary_key=True)
    dhash = db.Column(db.String)
    phash = db.Column(db.String)

    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"))
    manga_id = db.Column(db.Integer, db.ForeignKey("mangas.id"))
    page_id = db.Column(db.Integer, db.ForeignKey("pages.id"))

    chapter = db.relationship("Chapter", backref=db.backref("Panel", uselist=False))
    manga = db.relationship("Manga", backref=db.backref("Panel", uselist=False))
    page = db.relationship("Page", backref=db.backref("Panel", uselist=False))

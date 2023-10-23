from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()


class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    url = Column(String(50))

    def __repr__(self):
        return f'<Source "{self.name}">'


class Manga(Base):
    __tablename__ = "mangas"
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    link = Column(String(150))

    def __repr__(self):
        return f'<Manga "{self.name}">'


class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    number = Column(Integer)
    link = Column(String(150))

    def __repr__(self):
        return f'<Chapter "{self.number}: {self.name}">'


class Page(Base):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    link = Column(String(150))


class Panel(Base):
    # TODO: use composite key
    __tablename__ = "panels"
    id = Column(Integer, primary_key=True)
    dhash = Column(String)
    phash = Column(String)

    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    manga_id = Column(Integer, ForeignKey("mangas.id"))
    page_id = Column(Integer, ForeignKey("pages.id"))

    chapter = relationship("Chapter", backref="Panel")
    manga = relationship("Manga", backref="Panel")
    page = relationship("Page", backref="Panel")


def connect():
    username = "postgres"
    password = ""
    schema = "panels"

    connection_string = f"postgresql+psycopg2://{username}:{password}@localhost:5432/{schema}"
    engine = create_engine(connection_string)

    if not database_exists(engine.url):
        create_database(engine.url)
    #
    # Manga.panels = relationship("Panel", order_by=Panel.id, back_populates="manga")
    # Chapter.panels = relationship("Panel", order_by=Panel.id, back_populates="chapter")
    # Page.panels = relationship("Panel", order_by=Panel.id, back_populates="page")

    Base.metadata.create_all(engine)
    return engine

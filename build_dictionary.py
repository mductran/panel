import os
from image import extract_panels, generate_hash
from models import Panel, Page, Chapter, Manga, connect

from sqlalchemy.orm import sessionmaker

import re


def build_dump(engine):
    base_dir = "dump"
    session = sessionmaker(bind=engine)()

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            _, manga_name, chapter_name = root.split("/")
            page_number = int(re.findall(r'\d+', file)[0])
            path = os.path.join(root, file)
            panels = extract_panels(path=path)
            manga = Manga(name=manga_name, link="")
            chapter = Chapter(name=chapter_name, number=0, link="")
            page = Page(number=page_number, link="")
            for panel in panels:
                phash, dhash = generate_hash(panel)
                panel = Panel(dhash=dhash, phash=phash)
                panel.manga = manga
                panel.chapter = chapter
                panel.page = page
                session.add(manga)
                session.add(chapter)
                session.add(page)
                session.add(panel)
            session.commit()


if __name__ == "__main__":
    engine = connect()

    build_dump(engine)

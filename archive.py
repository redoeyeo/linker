from datetime import datetime

import requests
from sqlalchemy.orm import sessionmaker

from src.models import WebPageArchive, engine


def archive_webpage(url):
    response = requests.get(url)
    response.raise_for_status()

    Session = sessionmaker(bind=engine)
    session = Session()

    archive = WebPageArchive(
        url=url,
        html=response.text
    )

    # Сохраняем в базу данных
    session.add(archive)
    session.commit()
    session.close()

    print(f"Успешно архивирована страница: {url}")


if __name__ == "__main__":
    test_url = "https://basic.bearblog.dev/turn-off-and-journal-instead/"
    success = archive_webpage(test_url)

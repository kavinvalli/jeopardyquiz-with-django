import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('db.sqlite3')
db = scoped_session(sessionmaker(bind=engine))

def main():
    b = open("level.csv")
    reader = csv.reader(b)
    for level_name, image_url, negative_marking in reader:
        db.execute("INSERT INTO polls_level (level_name, image_url, negative_marking) VALUES (:level_name, :image_url, :negative_marking)",
                    {"level_name": level_name, "image_url": image_url, "negative_markingnegative_marking":negative_marking})
        print(f"Added {level_name}")
    db.commit()

if __name__ == "__main__":
    main()        
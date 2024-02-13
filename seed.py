from models import Pet, connect_db, db
from app import app

db.drop_all()
db.create_all()

opi = Pet(name="Optimus Prime", species="cat", age=1, photo_url="https://media.discordapp.net/attachments/905483886635659345/1185249803488198707/IMG_7594.jpg?ex=65d8c0e6&is=65c64be6&hm=4e36a3cebbc0543379f8fb1e7943c236357b052640ad1d58a228472e3d66d825&=&format=webp&width=762&height=1016", notes="Tuxedo")
alice = Pet(name="Alice", species="dog", notes="A good girl", photo_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7yrsnIMehvA9gjRTHIXUBMUwj-q4727y13w&usqp=CAU", available=False)

db.session.add_all([opi, alice])

db.session.commit()
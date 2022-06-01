"""

TODO use wordnet
https://www.nltk.org/howto/wordnet.html
https://github.com/goodmami/wn
"""
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Word(Base):
     __tablename__ = "words"

     id = Column(Integer, primary_key=True)
     word = Column(String(50))


     def __repr__(self):
         return f"Word(id={self.id!r}, word={self.word!r})"


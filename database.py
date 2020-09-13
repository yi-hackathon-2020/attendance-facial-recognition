import threading
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    UnicodeText,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

DB_URI = "sqlite:///studentdb.db"


def start() -> scoped_session:
    engine = create_engine(DB_URI, encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()


class Students(BASE):
    __tablename__ = "students"
    roll_num = Column(Integer, primary_key=True, nullable=False)
    name = Column(UnicodeText)

    def __init__(self, roll_num: int, name: str):
        self.roll_num = roll_num
        self.name = name

    def __repr__(self):
        return "<Student {} ({})>".format(self.roll_num, self.name)


# Generate 31 days' attributes
for i in range(1, 32):
    setattr(Students, f"day{i}", Column(Boolean))

Students.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def update_student_attendance(roll_num: int, day: int):
    """ Update student's attendance for a given day. Marks them present. """

    with INSERTION_LOCK:
        student = SESSION.query(Students).get(roll_num)
        setattr(student, f"day{day}", True)
        SESSION.commit()


def mark_remaining_absent(day: int):
    """ Marks remaining students for given day. """

    with INSERTION_LOCK:
        students = (
            SESSION.query(Students).filter(getattr(Students, f"day{day}") == None).all()
        )
        for student in students:
            setattr(student, f"day{day}", False)

        SESSION.commit()


def get_name_by_rollnum(roll_num: int) -> str:
    """ Returns student name for given roll number. """
    try:
        return (
            SESSION.query(Students).filter(Students.roll_num == roll_num).first().name
        )
    finally:
        SESSION.close()

# -*- coding: utf-8 -*-

# BUSSINESS SCHOOL SYSTEM

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import exists

engine = create_engine('sqlite:///:memory:')

Base = declarative_base()

print('WELCOME TO THE BUSSINESS SCHOOL')
print('-------------------------------------------------------------------')

class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, Sequence('course_id_seq'), primary_key=True)
    coursename = Column(String)

    teachers = relationship("Teacher", order_by="Teacher.id", back_populates="course")
    
    students = relationship("Student", order_by="Student.id", back_populates="course")

    def __repr__(self):
        return "{}".format(self.coursename)

class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, Sequence('teacher_id_seq'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    schedule = Column(String)
    course_id = Column(Integer, ForeignKey('course.id'))

    course = relationship("Course", back_populates="teachers")

    def __repr__(self):
        return "{} {}".format(self.firstname, self.lastname)

class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, Sequence('student_id_seq'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    schedule = Column(String)
    course_id = Column(Integer, ForeignKey('course.id'))

    course = relationship("Course", back_populates="students")

    def __repr__(self):
        return "{} {}".format(self.firstname, self.lastname)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

market = Course(coursename='Portfolio Diversified')

market.teachers = [Teacher(firstname='Mark',
                        lastname='Cuban / ',
                        schedule='Tuesday & Friday; from 9:00 to 11:30'),
                   Teacher(firstname='Kevin',
                        lastname='Oleary / ',
                        schedule='Monday & Thursday; from 9:00 to 11:30')]

print('(Course: Market) Teachers & Schedules:')
print(market.teachers[0], market.teachers[0].schedule)
print(market.teachers[1], market.teachers[1].schedule)

market.students = [Student(firstname='Pepito',
                        lastname='Perez / ',
                        schedule='Monday & Thursday; from 9:00 to 11:30'),
                   Student(firstname='Maria',
                        lastname='Paz / ',
                        schedule='Tuesday & Friday; from 9:00 to 11:30')]

print('(Course: Market) Students & Schedules:')
print(market.students[0], market.students[0].schedule)
print(market.students[1], market.students[1].schedule)
print('-------------------------------------------------------------------')

bussiness = Course(coursename='risky investments')

bussiness.teachers = [Teacher(firstname='Mark',
                        lastname='Cuban / ',
                        schedule='Saturday & Sunday; from 13:00 to 16:00'),
                      Teacher(firstname='Lori',
                        lastname='Greiner / ',
                        schedule='Wednesday & Sunday; from 17:00 to 20:00')]

print('(Course: Bussiness) Teachers & Schedules:')
print(bussiness.teachers[0], bussiness.teachers[0].schedule)
print(bussiness.teachers[1], bussiness.teachers[1].schedule)

bussiness.students = [Student(firstname='Rafael',
                        lastname='Nadal / ',
                        schedule='Wednesday & Sunday; from 17:00 to 20:00'),
                      Student(firstname='Serena',
                        lastname='Williams / ',
                        schedule='Saturday & Sunday; from 13:00 to 16:00')]

print('(Course: Bussiness) Students & Schedules:')
print(bussiness.students[0], bussiness.students[0].schedule)
print(bussiness.students[1], bussiness.students[1].schedule)
print('-------------------------------------------------------------------')

sales = Course(coursename='supply chain')

sales.teachers = [Teacher(firstname='Barbara',
                          lastname='Corcoran / ',
                          schedule='Wednesday & Saturday; from 18:00 to 21:00'),
                  Teacher(firstname='Kevin',
                          lastname='Oleary / ',
                          schedule='Wednesday & Saturday; from 17:00 to 20:00'),
                  Teacher(firstname='Lori',
                          lastname='Greiner / ',
                          schedule='Tuesday & Thursday; from 19:00 to 22:00')]

print('(Course: Sales) Teachers & Schedules:')
print(sales.teachers[0], sales.teachers[0].schedule)
print(sales.teachers[1], sales.teachers[1].schedule)
print(sales.teachers[2], sales.teachers[2].schedule)

sales.students = [Student(firstname='Rafael',
                        lastname='Nadal / ',
                        schedule='Tuesday & Thursday; from 19:00 to 22:00'),
                      Student(firstname='Serena',
                        lastname='Williams / ',
                        schedule='Wednesday & Saturday; from 17:00 to 20:00'),
                      Student(firstname='Pepito',
                        lastname='Perez / ',
                        schedule='Wednesday & Saturday; from 17:00 to 20:00'),
                      Student(firstname='Maria',
                        lastname='Paz / ',
                        schedule='Wednesday & Saturday; from 18:00 to 21:00')]

print('(Course: Sales) Students & Schedules:')
print(sales.students[0], sales.students[0].schedule)
print(sales.students[1], sales.students[1].schedule)
print(sales.students[2], sales.students[2].schedule)
print(sales.students[3], sales.students[3].schedule)
print('-------------------------------------------------------------------')

session.add(market)
session.add(bussiness)
session.add(sales)
session.commit()

# Query
print('QUERY')

print('QUERY #1 --> Market course: Teachers')
market = session.query(Course).filter_by(coursename='Portfolio Diversified').one()
print(market.teachers)
print('-------------------------------------------------------------------')

print('QUERY #2--> Market course: Students')
market = session.query(Course).filter_by(coursename='Portfolio Diversified').one()
print(market.students)
print('-------------------------------------------------------------------')

print("QUERY #3 --> Active Teachers")
for name, in session.query(Teacher.firstname).filter(Course.teachers.any()):
    print(name)
print('-------------------------------------------------------------------')

print("QUERY #4 --> Active Students")
for name, in session.query(Student.firstname).filter(Course.students.any()):
    print(name)
print('-------------------------------------------------------------------')

print("QUERY #5 --> Active Courses")
for name, in session.query(Course.coursename).filter(Course.teachers.any()):
    print(name)
print('-------------------------------------------------------------------')

print("QUERY #6 --> Teachers Schedules")
for name, in session.query(Teacher.schedule).filter(Course.teachers.any()):
    print(name)
print('-------------------------------------------------------------------')

print("QUERY #7 --> Students Schedules")
for name, in session.query(Student.schedule).filter(Course.students.any()):
    print(name)
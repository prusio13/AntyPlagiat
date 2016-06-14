# -*- coding: utf-8 -*-
# modul dodaje pliki z katalogu import_dir do bazy danych do tabeli raw_reports
import os
from _mysql import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
import pymysql

pymysql.install_as_MySQLdb()


class RawReport(declarative_base()):
    __tablename__ = 'raw_reports'
    added = Column(TIMESTAMP(timezone=True), default=func.now())
    filename = Column(String(50), primary_key=True)
    text = Column(MEDIUMTEXT)

    def __repr__(self):
        return "<raw_report(added='%s', filename='%s', text='%s')>" % (
            self.added, self.filename, self.text)

import_dir = "data/reports/import/"
debug = True
connect_string = 'mysql+mysqldb://antyplagiat_user:antyplagiat1@db4free.net:3306/antyplagiat_db?charset=utf8mb4'
engine = create_engine(connect_string, echo=debug)
Session = sessionmaker()
try:
    conn = engine.connect()
except OperationalError:
    if debug:
        print("nie mozna polaczyc")

# tworzenie tabeli - przerobic tak zeby wykorzystac istniejaca klase
metadata = MetaData()
raw_reports = Table('raw_reports', metadata,
                    Column('added', TIMESTAMP(timezone=True), default=func.now()),
                    Column('filename', String(50), primary_key=True),
                    Column('text', MEDIUMTEXT),
                    )
raw_reports.create(engine, checkfirst=True)  # tworzy tabele jezeli taka nie istnieje

files_in_dir = list(os.listdir(import_dir))
Session.configure(bind=engine)
sess = Session()

for file_in_dir in files_in_dir:
    f2path = import_dir + file_in_dir
    file = open(f2path, "r", encoding='iso-8859-2')
    text = file.read()
    # sprawdzam czy istnieje raport o tej nazwie pliku
    report = sess.query(RawReport).filter_by(filename=file_in_dir).first()
    report_to_import = RawReport(added=func.now(), filename=file_in_dir, text=text)
    if not report:  # no bike in DB
        sess.add(report_to_import)
        sess.commit()
        if debug:
            print("dodano", file_in_dir)
            # usunac/przeniesc plik z to_import do innego katalogu np. 2016-
    else:
        if debug:
            print("nie dodano - duplikat nazwy pliku", file_in_dir)
# zrobic timestamp z milisekundami

# wypisuje wszystkie pliki z bazy
for report in sess.query(RawReport).order_by(RawReport.filename):
    print(report.filename, report.added)

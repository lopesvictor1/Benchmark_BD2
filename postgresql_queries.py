import psycopg2 as pg2
from psycopg2 import sql
import datetime
import random
import time
from threading import Thread
from subprocess import check_output

import sys
import os
import argparse
import logging
import subprocess
import shlex


DEFAULT_SUPPLIERS = 100
DEFAULT_PARTS = 100

parts_colors = ["red", "green", "blue", "black", "white"]

class Database:
    def __init__(self):
        self.conn = pg2.connect(
            host="localhost",
            database="stock",
            user="postgres",
            password="123")

        #cursor
        cur = self.conn.cursor()

        #drop previous tables
        query = sql.SQL("drop table if exists Suppliers cascade")
        cur.execute(query)
        query = sql.SQL("drop sequence if exists Suppliers_sid_seq cascade")
        cur.execute(query)
        query = sql.SQL("drop table if exists Parts cascade")
        cur.execute(query)
        query = sql.SQL("drop sequence if exists Parts_pid_seq cascade")
        cur.execute(query)
        query = sql.SQL("drop table if exists Catalog cascade")
        cur.execute(query)
        query = sql.SQL("drop sequence if exists Catalog_siq_seq cascade")
        cur.execute(query)

        #insert tables (again) from scratch
        query = sql.SQL("create table if not exists Suppliers \
        (sid SERIAL NOT NULL, sname VARCHAR, address VARCHAR, PRIMARY KEY(sid))")
        cur.execute(query)

        query = sql.SQL("create table if not exists Parts \
        (pid SERIAL NOT NULL, pname VARCHAR, color VARCHAR, PRIMARY KEY(pid))")
        cur.execute(query)

        query = sql.SQL("create table if not exists Catalog \
        (sid SERIAL NOT NULL, pid INT NOT NULL, cost INT, PRIMARY KEY(sid, pid), \
        FOREIGN KEY(sid) REFERENCES Suppliers(sid), FOREIGN KEY(pid) REFERENCES Parts(pid))")
        cur.execute(query)

        self.conn.commit()
        cur.close()

    
    #insertion
    def insert_suppliers(self, suppliers):
        cur = self.conn.cursor()

        data = []
        for i in range(suppliers):
            sid = i
            sname = "Supplier {}".format(i)
            address = "Av {}, number {}".format(random.randint(0, suppliers), random.randint(0, 1000))
            row = [sid, sname, address]
            data.append(row)
        args_str = ','.join(cur.mogrify("(%s,%s,%s)", x).decode("utf-8") for x in data)
        start = time.time() * 1000
        cur.execute("INSERT INTO Suppliers VALUES " + args_str)
        end = time.time() * 1000
        self.conn.commit()
        cur.close()

        return (end - start) #time in ms



    def insert_parts(self, parts):
        cur = self.conn.cursor()

        data = []
        for i in range(parts):
            pid = i
            pname = "Part {}".format(i) 
            color = parts_colors[random.randint(0, len(parts_colors)-1)]
            row = [pid, pname, color]
            data.append(row)
        args_str = ','.join(cur.mogrify("(%s,%s,%s)", x).decode("utf-8") for x in data)
        start = time.time() * 1000
        cur.execute("INSERT INTO Parts VALUES " + args_str)
        end = time.time() * 1000
        self.conn.commit()
        cur.close()

        return (end - start) #time in ms


    def insert_catalog(self, parts, suppliers):
        cur = self.conn.cursor()

        data = []
        for i in range(parts):
            for j in range(suppliers):
                sid = i
                pid = j
                cost = random.randint(0, 1000)
                row = [sid, pid, cost]
                data.append(row)
        args_str = ','.join(cur.mogrify("(%s,%s,%s)", x).decode("utf-8") for x in data)
        start = time.time() * 1000
        cur.execute("INSERT INTO Catalog VALUES " + args_str)
        end = time.time() * 1000
        self.conn.commit()
        cur.close()

        return (end - start) #time in ms


    def update_catalog(self, parts, suppliers):
        cur = self.conn.cursor()

        data = []
        sid = suppliers // 2

        start = time.time() * 1000 
        for i in range(parts):
            pid = i
            cur.execute("UPDATE Catalog SET cost = 1 WHERE pid = " + str(pid) + " AND sid = " + str(sid) + ";")
            #cur.execute("UPDATE Catalog SET cost = 1 WHERE pid = 1 AND sid = 1;")
            self.conn.commit()
        end = time.time() * 1000

        return (end - start)
        
            
    def delete_catalog(self):
        cur = self.conn.cursor()

        data = []
        start = time.time() * 1000
        cur.execute("DELETE FROM Catalog")
        end = time.time() * 1000

        return (end - start)

def main():
    parser = argparse.ArgumentParser(description='InfluxDB queries script')
    parser.add_argument("--suppliers", "-s", help="Number of suppliers", default=DEFAULT_SUPPLIERS, type=int)
    parser.add_argument("--parts", "-p", help="Number of parts", default=DEFAULT_PARTS, type=int)

    args = parser.parse_args()
    catalog_insertions = args.parts*args.suppliers

    db = Database()
    db.insert_parts(args.parts)
    db.insert_suppliers(args.suppliers)
    time_insertion = db.insert_catalog(args.parts, args.suppliers)
    #time_update = db.update_catalog(args.parts, args.suppliers)
    #time_delete = db.delete_catalog()

    #x = "X"
    #print("PostgreSQL;{};{};{};{};{};".format(catalog_insertions, time_insertion, time_update, time_delete, x))


if __name__ == "__main__":
    main()

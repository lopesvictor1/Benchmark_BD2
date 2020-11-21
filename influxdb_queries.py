from influxdb import InfluxDBClient
import random
import time
from datetime import datetime

import sys
import os
import argparse
import logging
import subprocess


DEFAULT_SUPPLIERS = 100
DEFAULT_PARTS = 100
DEFAULT_BATCH_SIZE = 5000


parts_colors = ["red", "green", "blue", "black", "white"]

def insert_suppliers(client, b, suppliers):
    data = []
    for i in range(suppliers):
        sname = "Supplier {}".format(i)
        address = "Av {}, number {}".format(random.randint(0, suppliers), random.randint(0, 1000))
        di_data = {"measurement": "Suppliers",
                    "tags": {"sid" : i},
                    "time":0,
                    "fields" : {"sname":sname, "address": address}}
        data.append(di_data)
    start = time.time()*1000
    client.write_points(data, batch_size=b)
    end = time.time()*1000

    return (end - start)


def insert_parts(client, b, parts):
    data = []
    for i in range(parts):
        pname = "Part {}".format(i)
        for j in range(3):
            color = parts_colors[random.randint(0, len(parts_colors)-1)]
            di_data = {"measurement": "Parts",
                        "tags": {"pid" : i},
                        "time":0,
                        "fields" : {"pname":pname, "color": color}}
            data.append(di_data)
    start = time.time()*1000
    client.write_points(data, batch_size=b)
    end = time.time()*1000
    
    return (end - start)


def insert_catalog(client, b, parts, suppliers):
    print("insert_catalog: entrei aqui")
    data = []
    for i in range(parts):
        for j in range(suppliers):
            pid = i
            sid = j
            cost = random.randint(0, 1000)
            di_data = {"measurement": "Catalog",
                        "tags": {"sid" : sid, "pid" : pid},
                        "time":0,
                        "fields" : {"cost":cost}}
            data.append(di_data)
    start = time.time()*1000
    client.write_points(data, batch_size=b)
    end = time.time()*1000
    
    return (end - start)


def update_catalog(client):
    x = 10


def main():
    print("main: teste")
    parser = argparse.ArgumentParser(description='InfluxDB queries script')
    parser.add_argument("--suppliers", "-s", help="Number of suppliers", default=DEFAULT_SUPPLIERS, type=int)
    parser.add_argument("--parts", "-p", help="Number of parts", default=DEFAULT_PARTS, type=int)
    parser.add_argument("--batch_size", "-b", help="Batch size of insertions", default=DEFAULT_BATCH_SIZE, type=int)

    args = parser.parse_args()

    client = InfluxDBClient(host='localhost', port=8086)

    #overwrites old database
    client.drop_database("ProbeMon")
    client.create_database("ProbeMon")

    #use recreated database
    client.switch_database("ProbeMon")

    time_insertion_supplier = insert_suppliers(client, args.suppliers, args.batch_size)
    time_insertion_parts = insert_parts(client, args.parts, args.batch_size)
    time_insertion_catalog = insert_catalog(client, args.batch_size, args.parts, args.suppliers)
    
    
    time_insertion = time_insertion_supplier + time_insertion_parts + time_insertion_catalog
    print(time_insertion)



if __name__ == '__main__':
    sys.exit(main())

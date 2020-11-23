from influxdb import InfluxDBClient
import random
import time
from datetime import datetime

import sys
import os
import argparse
import logging
import subprocess


DEFAULT_SUPPLIERS = 5000
DEFAULT_PARTS = 1000


parts_colors = ["red", "green", "blue", "black", "white"]

def insert_suppliers(client, suppliers, b):
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


def insert_parts(client, parts, b):
    data = []
    for i in range(parts):
        pname = "Part {}".format(i)
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


def insert_catalog(client, parts, suppliers, b):
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


def update_catalog(client, parts, suppliers, b):
    sid = suppliers // 2
    start = time.time()*1000
    data = []
    i = 0
    for i in range(parts):
        query = client.query("SELECT cost FROM Catalog WHERE pid = '{}' AND sid = '{}'".format(i, sid))
        x = list(query.get_points())
        if x:
            cost = x[0]['cost'] + 1
            di_data = {"measurement": "Catalog",
                        "tags": {"sid" : sid, "pid" : i},
                        "time": 0,
                        "fields" : {"cost" : cost}}
            data.append(di_data)
    client.write_points(data, batch_size=b)
    end = time.time()*1000
    return (end - start)

def delete_catalog(client):
    start = time.time() * 1000
    client.delete_series(database='stock', measurement='Catalog')
    end = time.time() * 1000
    return (end - start)


def main():
    parser = argparse.ArgumentParser(description='InfluxDB queries script')
    parser.add_argument("--suppliers", "-s", help="Number of suppliers", default=DEFAULT_SUPPLIERS, type=int)
    parser.add_argument("--parts", "-p", help="Number of parts", default=DEFAULT_PARTS, type=int)
    #parser.add_argument("--batch_size", "-b", help="Batch size of insertions", default=DEFAULT_BATCH_SIZE, type=int)

    args = parser.parse_args()

    client = InfluxDBClient(host='localhost', port=8086)

    #overwrites old database
    client.drop_database("stock")
    client.create_database("stock")

    #use recreated database
    client.switch_database("stock")

    #time_insertion_supplier = insert_suppliers(client, args.suppliers, args.batch_size)
    #time_insertion_parts = insert_parts(client, args.parts, args.batch_size)
    #time_insertion_catalog = insert_catalog(client, args.batch_size, args.parts, args.suppliers)
    #time_insertion = time_insertion_supplier + time_insertion_parts + time_insertion_catalog
    catalog_insertions = args.parts*args.suppliers
    if catalog_insertions > 50000:
        batch_size = catalog_insertions // 50
    else:
        batch_size = catalog_insertions // 25

    insert_suppliers(client, args.suppliers, batch_size)
    insert_parts(client, args.parts, batch_size)

    time_insertion = insert_catalog(client, args.parts, args.suppliers, batch_size)

    time_update = update_catalog(client, args.parts, args.suppliers, batch_size)

    time_delete = delete_catalog(client)

    print("InfluxDB;{};{};{};{};{};".format(catalog_insertions, time_insertion, time_update, time_delete, batch_size))


if __name__ == '__main__':
    sys.exit(main())
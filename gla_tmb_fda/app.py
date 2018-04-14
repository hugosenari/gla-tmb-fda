import csv
import zipfile
from io import TextIOWrapper
from flask import Flask, jsonify
from toolz.itertoolz import first
from toolz.functoolz import curry, excepts, compose
from os import path

app = Flask('gla-tmb-fda')
file_path = path.join(path.dirname(__file__), 'gtf')
gtf = zipfile.ZipFile(file_path, 'r')

as_json = lambda fn: compose(jsonify, fn)

class OpenFileInZipAsCSV():
    def __init__(self, zipfile, filename):
        self.filename = filename
        self.zipfile = zipfile
        self.stream = None
    
    def __enter__(self):
        self.stream = self.zipfile.open(self.filename)
        ustream = TextIOWrapper(self.stream, 'utf-8')
        return csv.reader(ustream, quotechar='"')
    
    def __exit__(self, *exc_info):
        self.stream.close()

open_as_csv = curry(OpenFileInZipAsCSV, gtf)
by_nth = curry(lambda nth, uid, obj: obj[nth] == str(uid)) 
list_first = curry(lambda it: [first(it)])
list_first_or_empty = excepts(StopIteration, list_first, lambda _: [])
filter_by_nth = curry(lambda nth, uid, stream: filter(by_nth(nth, uid), stream))
filter_by_uid = filter_by_nth(0)

@curry
def swap (i, j, arr):
    arr[i], arr[j] = arr[j], arr[i]
    return arr

def list_file(name):
    with open_as_csv(name) as stream:
        return list(stream)

@curry
def first_nth(nth, file_name, uid):
    with open_as_csv(file_name) as stream:
        match = filter_by_nth(nth, uid, stream)
        return list_first_or_empty(match)

first_uid = first_nth(0)

@curry
def list_nth(nth, file_name, uid):
    with open_as_csv(file_name) as stream:
        match = filter_by_nth(nth, uid, stream)
        return list(match)

list_uid = list_nth(0)

@app.route('/agency')
@as_json
def agency():
    return list_file('agency.txt')

@app.route('/agency/<uid>')
@as_json
def agency_get(uid):
    return first_uid('agency.txt', uid)

@app.route('/calendar')
@as_json
def calendar():
    return list_file('calendar.txt')

@app.route('/calendar/<uid>')
@as_json
def calendar_get(uid):
    return first_uid('calendar.txt', uid)

@app.route('/fare_attribute')
@as_json
def fare_attribute():
    return list_file('fare_attributes.txt')

@app.route('/fare_attribute/<uid>')
@as_json
def fare_attribute_get(uid):
    return first_uid('fare_attributes.txt', uid)

@app.route('/frequency')
@as_json
def frequency():
    return list_file('frequencies.txt')

@app.route('/frequency/<uid>')
@as_json
def frequency_get(uid):
    return list_uid('frequencies.txt', uid)

@app.route('/route')
@as_json
def route():
    return list_file('routes.txt')

@app.route('/route/<uid>')
@as_json
def route_get(uid):
    return first_uid('routes.txt', uid)

@app.route('/shape')
@as_json
def shape():
    return list_file('shape.txt')

@app.route('/shape/<uid>')
@as_json
def shape_get(uid):
    return list_uid('shape.txt', uid)

@app.route('/stop_time')
@as_json
def stop_time():
    return list_file('stop_times.txt')

@app.route('/stop_time/<uid>')
@as_json
def stop_time_get(uid):
    return list_uid('stop_times.txt', uid)

@app.route('/stop')
@as_json
def stop():
    return list_file('stops.txt')

@app.route('/stop/<uid>')
@as_json
def stop_get(uid):
    return first_uid('stops.txt', uid)

@app.route('/trip')
@as_json
def trip():
    return list_file('trips.txt')

@app.route('/trip/<uid>')
@as_json
def trip_get(uid):
    return list_uid('trips.txt', uid)

@app.route('/stop_trip')
@as_json
def stop_trip():
    return swap(0, 3, list_file('stop_times.txt'))

@app.route('/stop_trip/<uid>')
@as_json
def stop_trip_get(uid):
    return list_nth(3, 'stop_times.txt', uid)

@app.route('/')
@as_json
def index():
    endpoint = lambda rule: rule.endpoint\
        .replace('jsonify_of_', '')\
        .replace('_get', '/id')
    
    return list(map(endpoint, app.url_map.iter_rules()))
from django.http import HttpResponse, HttpResponseNotFound
from json import dumps
from csv import DictReader
from os import path

# FIXME https://docs.djangoproject.com/en/4.0/howto/static-files/
# https://stackoverflow.com/questions/40066199/django-filenotfounderror-in-a-view-when-returning-html-using-codecs
FILE = path.dirname(path.realpath(__file__)) + '/congressional-candidate-totals.csv'

def index(request):
    result = []
    with open(FILE) as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            result.append(row)
    return HttpResponse(dumps(result))

def election(request, state, year):
    result = []
    with open(FILE) as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            if row['election_id'].startswith(state) and row['election_id'].endswith(year):
                result.append(row)
    if result:
        return HttpResponse(dumps(result))
    return HttpResponseNotFound('no election found for {} in {}'.format(state, year))

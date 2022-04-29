from django.http import HttpResponse, HttpResponseNotFound
from json import dumps
from csv import DictReader
from os import path

# TODO https://docs.djangoproject.com/en/4.0/howto/static-files/
# https://stackoverflow.com/questions/40066199/django-filenotfounderror-in-a-view-when-returning-html-using-codecs
FILE = path.dirname(path.realpath(__file__)) + "/congressional-candidate-totals.csv"


def index(request):
    result = []
    with open(FILE) as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            result.append(row)

    sort = request.GET.get("sort")
    # https://stackoverflow.com/questions/18411560/sort-list-while-pushing-none-values-to-the-end
    if sort:
        key, direction = sort.split(":")
        result.sort(
            key=lambda candidate: (candidate[key] != "NA", candidate[key]),
            reverse=direction.startswith("d"),
        )

    return HttpResponse(dumps(result))


def election(request, state, year):
    result = []
    with open(FILE) as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            if row["election_id"].startswith(state) and row["election_id"].endswith(
                year
            ):
                result.append(row)

    sort = request.GET.get("sort")
    # https://stackoverflow.com/questions/18411560/sort-list-while-pushing-none-values-to-the-end
    if sort:
        key, direction = sort.split(":")
        result.sort(
            key=lambda candidate: (candidate[key] != "NA", candidate[key]),
            reverse=direction.startswith("d"),
        )

    if result:
        return HttpResponse(dumps(result))
    return HttpResponseNotFound("no election found for {} in {}".format(state, year))

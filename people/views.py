import inspect

from django.shortcuts import render

from people.get_people import (
    get_people_naive,
    get_people_select_related_only,
    get_people_select_related,
    get_people_qs_only,
    get_people_values,
)


def index(request):
    return render(request, "people/index.html")


def list_people_naive(request):
    """List person/observatory/site using "naive" iteration of Person QuerySet"""
    people = get_people_naive()
    return render(
        request,
        "people/list_people_fastest.html",
        {
            "people": people,
            "title": r"Naive QuerySet.all()",
            "description": "get_people_naive",
            "func_source": inspect.getsource(get_people_naive),
        },
    )


def list_people_select_related_only(request):
    people = get_people_select_related_only()
    return render(
        request,
        "people/list_people_fastest.html",
        {
            "people": people,
            "title": r"Using QuerySet.select_related()",
            "description": "get_people_select_related_only",
            "func_source": inspect.getsource(get_people_select_related_only),
        },
    )


def list_people_select_related(request):
    """List person/observatory/site via iteration of QuerySet using select_related"""
    people = get_people_select_related()
    return render(
        request,
        "people/list_people_fastest.html",
        {
            "people": people,
            "title": r"Using QuerySet.only()",
            "description": "get_people_select_related",
            "func_source": inspect.getsource(get_people_select_related),
        },
    )


def list_people_qs_only(request):
    """List person/observatory/site via iteration of QuerySet.only()"""
    people = get_people_qs_only()
    return render(
        request,
        "people/list_people_fastest.html",
        {
            "people": people,
            "title": r"Using QuerySet.select_related() <i>and</i> QuerySet.only()",
            "description": "get_people_qs_only",
            "func_source": inspect.getsource(get_people_qs_only),
        },
    )


def list_people_values(request):
    """List person/observatory/site using explict retrieval of relevant values"""
    people = get_people_values()
    return render(
        request,
        "people/list_people_fastest.html",
        {
            "people": people,
            "title": r"Using QuerySet.values()",
            "description": "get_people_values",
            "func_source": inspect.getsource(get_people_values),
        },
    )

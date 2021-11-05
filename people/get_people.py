from people.models import Person

def get_people_naive(people):
    """List person/observatory/site using "naive" iteration of Person QuerySet"""
    return [
        (person, person.site.observatory, person.site)
        for person in people
    ]


def get_people_select_related_only(people):
    return [
        (person, person.site.observatory, person.site)
        for person in people.select_related("site__observatory")
        .only("name", "site_id")
        .all()
    ]


def get_people_select_related(people):
    """List person/observatory/site via iteration of QuerySet using select_related"""
    return [
        (person, person.site.observatory, person.site)
        for person in people.select_related("site__observatory").all()
    ]


def get_people_qs_only(people):
    """List person/observatory/site via iteration of QuerySet.only()"""
    return [
        (person, person.site.observatory, person.site)
        for person in people.only("name", "site_id").all()
    ]


def get_people_values(people):
    """List person/observatory/site using explict retrieval of relevant values"""
    return [
        (name, observatory, site)
        for name, site, observatory in people.values_list(
            "name", "site__name", "site__observatory__name"
        )
    ]

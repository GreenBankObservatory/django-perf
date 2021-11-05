import logging
import os
import random
import string

from faker import Faker
from tqdm import tqdm

from django.core.management.base import BaseCommand
from django.apps import apps


fake = Faker()

LOGGER = logging.getLogger(__name__)

import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


class Command(BaseCommand):
    skip_checks = True

    def add_arguments(self, parser):
        parser.add_argument("num_people", type=int)
        parser.add_argument("--notes-length", type=int, default=1000)

    def handle(self, *args, **kwargs):
        Observatory = apps.get_model("people", "Observatory")
        gbo = Observatory.objects.get(name="Green Bank Observatory")
        nrao = Observatory.objects.get(name="National Radio Astronomy Observatory")

        Site = apps.get_model("people", "Site")
        gb_site = Site.objects.get(observatory=gbo, name="Green Bank")
        soc_site = Site.objects.get(observatory=nrao, name="Socorro")
        cv_site = Site.objects.get(observatory=nrao, name="Charlottesville")

        site_ids = [gb_site.id, soc_site.id, cv_site.id]
        Person = apps.get_model("people", "Person")
        people = [
            Person(
                name=fake.name(),
                notes = fake.paragraph(kwargs["notes_length"]),
                site_id=site_ids[random.randint(0, len(site_ids) - 1)],
            )
            for __ in tqdm(range(kwargs["num_people"]))
        ]
        print("Creating people in DB...")
        Person.objects.bulk_create(
            people,
            batch_size=10_000,
        )

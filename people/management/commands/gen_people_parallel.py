from functools import partial
import concurrent.futures
import logging
import os
import random

from faker import Faker
from tqdm import tqdm

from django.core.management.base import BaseCommand
from django.apps import apps


fake = Faker()

LOGGER = logging.getLogger(__name__)


Person = apps.get_model("people", "Person")


def gen_people(num_people, notes_length, site_ids):
    people = [
        Person(
            name=fake.name(),
            notes=fake.paragraph(notes_length),
            site_id=site_ids[random.randint(0, len(site_ids) - 1)],
        )
        for __ in range(num_people)
    ]
    Person.objects.bulk_create(
        people,
        batch_size=10_000,
    )


class Command(BaseCommand):
    skip_checks = True

    def add_arguments(self, parser):
        parser.add_argument("num_people", type=int)
        parser.add_argument("--notes-length", type=int, default=10)

    def handle(self, *args, **kwargs):
        Observatory = apps.get_model("people", "Observatory")
        gbo = Observatory.objects.get(name="Green Bank Observatory")
        nrao = Observatory.objects.get(name="National Radio Astronomy Observatory")

        Site = apps.get_model("people", "Site")
        gb_site = Site.objects.get(observatory=gbo, name="Green Bank")
        soc_site = Site.objects.get(observatory=nrao, name="Socorro")
        cv_site = Site.objects.get(observatory=nrao, name="Charlottesville")

        site_ids = [gb_site.id, soc_site.id, cv_site.id]

        with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
            chunk_size = kwargs["num_people"] // os.cpu_count()
            futures = [
                executor.submit(
                    gen_people,
                    chunk_size,
                    notes_length=kwargs["notes_length"],
                    site_ids=site_ids,
                )
                for __ in range(os.cpu_count())
            ]
            for future in concurrent.futures.as_completed(futures):
                future.result()
        print("Creating people in DB...")

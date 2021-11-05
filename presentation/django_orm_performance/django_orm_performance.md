# Django ORM Performance Optimization

Thomas Chamberlin | Wed 17 Nov 2021 2PM EST

### ...what's an ORM

**Object Relational Mapper (ORM)**: a tool that maps **tables** in a relational database schema to **objects** in a programming language

[In Django](https://docs.djangoproject.com/en/3.2/topics/db/models/), the objects being mapped are **models**:

> A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.

---
# Django at GBO

- Django is used for _all_ of GBO SDD's "dynamic" websites
    - **DSS**: Dynamic Scheduling System
    - **GBORS**: GBO Reservation System
    - **QZAT**: NRQZ Administration Tool
    - **Alda**: GBT Archive POC

---
# ...what's Django

https://docs.djangoproject.com

> With Django, you can take web applications from concept to launch in a matter of hours. Django takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.

- Python web framework
- Allows you to:
    - Query database via ORM
    - Handle HTTP requests/return HTTP responses
    - Render templates

---
# ...what's Django

### The ORM

Let's say we have a database. It has a `person` database table:

```plain
                         Table "public.people_person"
 Column  |  Type  |                         Modifiers                          
---------+--------+------------------------------------------------------------
 id      | bigint | not null default nextval('people_person_id_seq'::regclass)
 name    | text   | not null
 notes   | text   | not null
 site_id | bigint | not null
Indexes:
    "people_person_pkey" PRIMARY KEY, btree (id)
    "people_person_site_id_4c070efc" btree (site_id)
Foreign-key constraints:
    "people_person_site_id_4c070efc_fk_people_site_id" FOREIGN KEY (site_id)
      REFERENCES people_site(id) DEFERRABLE INITIALLY DEFERRED
```

---
# ...what's Django

### The ORM

And here is the `Person` model. This was used to generate the above schema, and is also used to interact with it at runtime.

```python
class Person(models.Model):
    name = models.TextField()
    site = models.ForeignKey("Site", on_delete=models.CASCADE)
    notes = models.TextField()
```

---
# ...what's Django

Let's try a query:

```python
In [1]: p = Person.objects.first()
In [2]: print(p)
Catherine Barry
```

This is the query that was performed:

```sql
SELECT "people_person"."id",
       "people_person"."name",
       "people_person"."site_id",
       "people_person"."notes"
  FROM "people_person"
 ORDER BY "people_person"."id" ASC
 LIMIT 1
```

---
# The Full Model Layer


```python
class Person(models.Model):
    """An individual Person"""
    name = models.TextField()
    site = models.ForeignKey("Site", on_delete=models.CASCADE)
    notes = models.TextField()

    def __str__(self): return self.name

class Observatory(models.Model):
    """e.g. Green Bank Observatory, NRAO"""
    name = models.TextField()

    def __str__(self): return self.name

class Site(models.Model):
    """e.g. Green Bank, Charlottesville, Socorro"""
    name = models.TextField()
    observatory = models.ForeignKey("Observatory", on_delete=models.CASCADE)

    def __str__(self): return self.name

```

---
# The Full Model Layer

### Model Layer Entity-Relationship Diagram


.mermaid-diagram[
  erDiagram
    Person }o--|| Site : "works at"
    Site }o--|| Organization : within
]

---
# Let's Do Some Queries

### Count People

The `Manager.count()` method will generate a SQL `COUNT` query for you:

```python
In []: Person.objects.count()
SELECT COUNT(*) AS "__count"
  FROM "people_person"

Execution time: 0.002128s [Database: default]
Out[]: 10000
```

---
# Let's Do Some Queries
### Count People at Green Bank Site

`Manager.filter()` will generate `WHERE` clauses for you, and will _also_ generate `JOIN`s for you!

```python
In []: Person.objects.filter(site__name="Green Bank").count()
SELECT COUNT(*) AS "__count"
  FROM "people_person"
 INNER JOIN "people_site"
    ON ("people_person"."site_id" = "people_site"."id")
 WHERE "people_site"."name" = 'Green Bank'

Execution time: 0.006917s [Database: default]
Out[]: 3360
```

---
# Let's Do Some Queries
### Which Sites Contain Someone Named Thomas?

Get site names by filtering the `Person` `Model`:

```python
In [xx]: Person.objects.filter(name__startswith="Thomas").values_list("site__name", flat=True).distinct()
Out[xx]: SELECT DISTINCT "people_site"."name"
  FROM "people_person"
 INNER JOIN "people_site"
    ON ("people_person"."site_id" = "people_site"."id")
 WHERE "people_person"."name"::text LIKE 'Thomas%'
 LIMIT 21

Execution time: 0.003907s [Database: default]
<QuerySet ['Charlottesville', 'Green Bank', 'Socorro']>
```

---
# Let's Do Some Queries
### Which Sites Contain Someone Named Thomas?

Another method (this one gets you `Site` instances):

```python
In [xx]: Site.objects.filter(person__name__startswith="Thomas").distinct()
Out[xx]: SELECT DISTINCT "people_site"."id",
       "people_site"."name",
       "people_site"."observatory_id"
  FROM "people_site"
 INNER JOIN "people_person"
    ON ("people_site"."id" = "people_person"."site_id")
 WHERE "people_person"."name"::text LIKE 'Thomas%'
 LIMIT 21

Execution time: 0.004253s [Database: default]
<QuerySet [<Site: Green Bank>, <Site: Socorro>, <Site: Charlottesville>]>
```


---
# Demo Time

- `django_orm_perf`
- `nell_orm_perf`



---
# The Curse of Abstraction

- "If I learn an ORM, I won't have to learn SQL"
- "Why isn't the ORM doing what I want it to do?"
- "...what _is_ the ORM doing?"
- "What do I _want_ it to do?"
- [write the SQL yourself]
- [Figure out how to make the ORM generate that SQL]
- Now you've learned _two_ things: the ORM _and_ SQL

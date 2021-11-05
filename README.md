# Django Performance Optimization Demo

Demo Django project that explore the following performance issues:

- The N+1 Queries Problem
- Over-querying
- Doing too much "in Python"


1. Start with [the introductory slides](https://www.gb.nrao.edu/~tchamber/presentations/django_orm_performance) (source code is in `./presentation`)
2. Look at [the introductory Jupyter notebook](https://nbviewer.org/github/GreenBankObservatory/django-perf/blob/main/django_orm_performance.ipynb). This uses the `people` app from this repo to explore mitigations to the N+1 problem
3. Look at [the DSS Jupyter notebook](https://nbviewer.org/github/GreenBankObservatory/django-perf/blob/main/nell_orm_performance.ipynb). This explores some advanced real-world optimizations from the `nell` repository of the GBO Dynamic Scheduling System

from dagster import job, op

import os

@op
def ingest():
    os.system("python pipeline/ingest.py")

@op
def validate(context, after_ingest=None):
    os.system("python pipeline/validate.py")

@op
def transform(context, after_validate=None):
    os.system("cd dbt_pipeline && dbt run --profiles-dir .")

@op
def test_data(context, after_transform=None):
    os.system("cd dbt_pipeline && dbt test --profiles-dir .")

@job
def ventes_pipeline():
    i = ingest()
    v = validate(after_ingest=i)
    t = transform(after_validate=v)
    test_data(after_transform=t)

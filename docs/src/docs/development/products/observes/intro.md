---
id: intro
title: Observes
sidebar_label: Introduction
slug: /development/observes
---

Observes is the product responsible
for company-wide data analytics.

Observes follows the
[Data Warehouse](https://en.wikipedia.org/wiki/Data_warehouse)
architecture,
which means that most of what it does
is _Extract_ data
from different sources,
_Transform_ that into a relational model,
and _Upload_ the results to a Data Warehouse.
This process is usually known as an ETL.
Once the data is in the Warehouse,
data can be consumed for creating dashboards
and info-graphics that End Users consume.

Observes also provides a few services
outside of the Data Warehouse architecture,
for example:
Generating billing information,
and stopping stuck [GitLab](/development/stack/gitlab) jobs.

## Public Oath

1. Data in the Warehouse is consistent, correct, and reasonably up-to-date.

1. When deciding between correctness and speed,
   correctness will be given priority.

## Architecture

1. The Data Warehouse is a
   [Redshift cluster on Amazon Web Services](/development/stack/aws/redshift)
   deployed on many subnets provided
   by the [VPC component of Common](/development/common/vpc)
   for High Availability.

1. [Grow](https://www.grow.com/)
   is the solution we use for Business Intelligence (BI).

1. ETL tasks are scheduled
   using the [Compute component of Common](/development/common/compute).

1. ETLs fetch data from their corresponding service and
   transports it into a target location,
   commonly to the warehouse.

:::note
For simplicity, each ETL is not shown in the diagram and instead a
generic ETL is used. For a particular ETL refer to its docs subsection
or check the source-code at `./observes/etl`
:::

:::tip
You can right-click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Observes](./arch.dot.svg)

:::caution
The diagram arrows represents a dependency relation, not data flow.
i.e. arrow tail is the dependent and head is the dependency
:::

## Generic ETL

1. Fetch: The ETL fetch data from the source. e.g. API endpoint.
1. Get schema: Then the ETL determines the schema (metadata of the data).
   This can be done by various means:
  - SDKs hardcoded typings
  - auto determination by raw data analysis.
  Both methods with pros and cons.
1. Target transform: with data correctly typed, then it is transformed
   into the expected types for the target. For redshift the most common
   transform is Flattering.
  - Flattering: nested/complex fields (e.g. list, dictionaries) are mapped
  into flat, primitive (as defined by the target) collections of fields.
  i.e. For redshift list and dictionaries are mapped into separate tables.

1. Load: having transformed the data into the data type that the
   target expects, load commands are triggered for saving the data.
   i.e. in redshift this corresponds to SQL queries.

## Particular Cases

For almost all ETLs:

- target is set to Redshift.
- source is an API endpoint exposed on the internet.
- schema is hardcoded on the SDK or auto determined on each trigger.
- **all** data is erased and re-uploaded into the target.
- the etl job triggers the full ETL procedure from start to finish.
- the [Compute component of Common](/development/common/compute) triggers the ETL.

A few exceptions exist though:

- [S3 bucket](/development/stack/aws/s3) target: They emit data into
  a bucket rather than to Redshift. i.e.
  - `/observes/etl/timedoctor/backup` into `fluidanalytics/backup_timedoctor`
  - `/observes/etl/code/compute-bills` into `integrates/continuous-data/bills`
  - dynamo_etl emits first to `observes.etl-data` and latter into Redshift.

- Differential ETLs: they do not erase and re-upload all data.
  They store the current streaming state in the `observes.state` bucket.
  i.e. gitlab_etl, checkly_etl

- Cached schema: They do not have hardcoded schema nor auto determination.
  They extract the schema previously saved in the `observes.cache` bucket.
  i.e. dynamo_etl (another job auto determines the schema and saves it on the bucket).

- Fractioned ETL phases:
  - Zoho ETL:Has two jobs separating ETL phases i.e.
  `/observes/etl/zoho-crm/fluid/prepare` and `/observes/etl/zoho-crm/fluid`
  - Dynamo ETL: start phase is triggered into multiple concurrent jobs,
    but final phase is manually triggered.

## Jobs

- `/observes/job/batch-stability`:
  Whose task is to monitor the
  [Compute component of Common](/development/common/compute).

- `/observes/job/cancel-ci-jobs`:
  Whose task is to cancel old CI jobs on [GitLab](/development/stack/gitlab)
  that got stuck.

## Contributing

Please read the
[contributing](/development/contributing) page first.

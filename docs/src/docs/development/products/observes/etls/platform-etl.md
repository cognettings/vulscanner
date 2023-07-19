---
id: platform-etl
title: Fluid Attacks' platform ETL
sidebar_label: Platform
slug: /development/platform-etl
---

This ETL process extracts data from the Fluid Attacks'
platform database (dynamo) and sends it to
the warehouse (redshift).

:::note
Local execution and sending of jobs will require to
[setup your terminal](/talent/engineering/onboarding#terminal)
and have access to the
`prod_observes` role and the `CACHIX_AUTH_TOKEN` environment variable.
:::

## Architecture

The ETL has two core procedures:

- Data-schema determination

    where the schema of the data is inferred.

- Data refresh (the ETL)

    where all data is updated from dynamodb to redshift

The ETL has four phases:

1. Segment ETL (dynamo -> s3)

    where the ETL is executed over a segment of the dynamo data and saves it on s3.

1. Preparation

    where a pristine staging (a.k.a. loading) redshift-schema is created for
    temporal store of the new data.

1. Upload ETL (s3 -> redshift)

    where the codified s3 data is uploaded to the corresponding tables on
    the staging redshift-schema.

1. Replacement

    where the staging schema becomes the new source of truth.

:::caution
Do not confuse: _redshift-schema_ is an entity that groups a collection of
tables (like a folder), instead, data-schema is the metadata of some data
(e.g. their column names and types)
:::

## Data refresh

### Segment ETL

The segment ETL is a multi-node job (on various machines) that is executed on aws-batch.
Internally the procedure consist of:

1. Segment extraction

    The data is extracted using a
    [parallel scan](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html#Scan.ParallelScan)
    over one specific segment.

1. Data transform

    By using the auto generated data-schemas, the data is adjusted.

1. S3 upload

    Data is transformed into a csv file (one for each data-schema)
    and uploaded into the _observes.etl-data_ bucket.

:::info
Data is uploaded first to s3 and then to redshift due to performance issues.
The custom redshift load query from s3 is more efficient than direct upload
queries.
:::

### Upload ETL

The upload ETL is a multi-node job executed on aws-batch, that coincides on
the number of machines (total segments) as for the _Segment ETL_.
It can be locally triggered with:

:::info
This job performance depends mostly on the redshift cluster number of nodes.
:::

## Data-schema determination

This process infer data-schema from raw data and stores the determined
data-schemas into _observes.cache_ s3 bucket for serving as a cache.

This process is triggered by an schedule. It has a frequency of execution
of one week.

## Manual Trigger

Each ETL phase and the data-schema determination can be manually triggered
using dynamo etl binary. These jobs commonly run at aws-batch.

```bash
m . /observes/etl/dynamo/jobs/run --help
```

## Manual Retry

If a segment job fails (a job from PHASE_1) it can be retried on aws-batch with:

```bash
m . /computeOnAwsBatch/observesDynamoRetryPhase1 "{total_segments}" "{segment_number}"
```

If a upload job fails (a job from PHASE_3) it can be retried on aws-batch with:

```bash
m . /computeOnAwsBatch/observesDynamoRetryPhase3 "{segment_number}"
```

## Issues

ETL jobs are unstable because of redshift or aws unhandled errors,
but the retry procedure makes them stable.
For the record, this were the most common issues before enabling the
retry procedure:

### CannotInspectContainerError

- Reason: the job finish in an unknown state from aws batch perspective

- Resolution: verify job log (possible false negative) and manual retry

### InternalError: Out of Memory

- Reason: unknown

- Hypothesis: high db usage demand from concurrent `s3 -> redshift` operations

- Resolution: free db space and/or manual retry

### Host terminated

- Reason: the spot nature of the instances used at aws batch

- Resolution: manual retry

### Stuck queries

- Reason: unknown

- Resolution: [prevent-locks-blocking-queries](https://aws.amazon.com/es/premiumsupport/knowledge-center/prevent-locks-blocking-queries-redshift/#Resolution).

### InternalError stl_load_errors

- Reason: possible ETL bug

- Resolution: unknown (try re-execution)

- Note: this issue should not be raised

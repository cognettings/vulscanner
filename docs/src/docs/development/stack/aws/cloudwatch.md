---
id: cloudwatch
title: CloudWatch
sidebar_label: CloudWatch
slug: /development/stack/aws/cloudwatch
---

## Rationale

We use [CloudWatch][cloudwatch]
for monitoring our entire [AWS][aws] infrastructure.
We can monitor our applications,
react to performance changes within them,
optimize resource utilization,
and get a unified view of operational health.
The main reasons why we chose it
over other alternatives
are the following:

- It is a core AWS service.
  Once we start creating infrastructure,
  CloudWatch begins to monitor it.
- It integrates seamlessly with most AWS services.
  Some examples are [EC2][ec2],
  [S3](/development/stack/aws/s3/),
  and
  [DynamoDB](/development/stack/aws/dynamodb/introduction/).
- It complies with [several](https://aws.amazon.com/compliance/iso-certified/)
  certifications from [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)
  and [CSA](https://en.wikipedia.org/wiki/Cloud_Security_Alliance).
  Many of these certifications are focused
  on granting that the entity follows best practices
  regarding secure [cloud-based](https://en.wikipedia.org/wiki/Cloud_computing)
  environments
  and information security.
- It supports [custom dashboards](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create_dashboard.html)
  for visualizing metrics
  using diagrams like
  bars, pies, numbers, among others.
  Other customizations such as timespans
  and [resource metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/viewing_metrics_with_cloudwatch.html)
  as axes
  are also available.
- It supports [alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
  using [AWS SNS](https://aws.amazon.com/sns/),
  allowing email notifications to be triggered
  when [resource metric conditions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ConsoleAlarms.html)
  are not met or
  [anomalies are detected](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Create_Anomaly_Detection_Alarm.html).
- Resources can be [written as code](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
  using [Terraform](/development/stack/terraform/).

## Alternatives

> **Note:** > [GCP Cloud Monitoring](https://cloud.google.com/monitoring)
> and [Azure Monitor](https://docs.microsoft.com/en-us/azure/azure-monitor/overview)
> are alternatives
> that did not exist at the time we migrated to the cloud.
> A review of each of them is pending.

## Usage

We use [CloudWatch][cloudwatch] for monitoring

- [EC2][ec2]
  instance performance;
- [EBS](/development/stack/aws/ebs/)
  disk usage and performance;
- [S3](/development/stack/aws/s3/)
  bucket size and object number;
- [ELB](/development/stack/aws/elb/)
  load balancer performance;
- [Redshift](/development/stack/aws/redshift/)
  database usage and performance;
- [DynamoDB](/development/stack/aws/dynamodb/introduction/)
  tables usage and performance;
- [SQS](https://aws.amazon.com/sqs/)
  sent, delayed, received and deleted messages;
- [ECS](https://aws.amazon.com/ecs/)
  cluster resource reservation and utilization,
  and
- [Lambda][lambda]
  invocations, errors, duration, among others.

We do not use CloudWatch for

- [synthetic monitoring](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html)
  (we use [Checkly](https://www.checklyhq.com/) instead);
- [ServiceLens](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ServiceLens.html)
  (it only supports [Lambda][lambda] functions,
  [API Gateway](https://aws.amazon.com/api-gateway/),
  and [Java-based](<https://en.wikipedia.org/wiki/Java_(programming_language)>)
  applications);
- [Contributor Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights.html)
  (we use [Cloudflare](/development/stack/cloudflare/) instead);
- [Container Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContainerInsights.html)
  (we use [New Relic](https://newrelic.com/);
  pending review);
- [Lambda Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights.html)
  (we currently use [Lambda][lambda]
  for a few non-critical tasks);
- [CloudWatch agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html)
  (it could increase visibility
  for [EC2][ec2] machines;
  pending review);
- [CloudWatch Application Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-application-insights.html)
  (it only supports [Java-based](<https://en.wikipedia.org/wiki/Java_(programming_language)>)
  applications),
  or
- writing our [alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
  as code
  using [Terraform](/development/stack/terraform/)
  (pending to be done).

## Guidelines

- You can access the [CloudWatch][cloudwatch] console
  after [authenticating to AWS](/development/stack/aws#guidelines).
- You can watch CloudWatch metrics
  from the monitoring section
  of each [AWS][aws] service.

[aws]: /development/stack/aws/
[cloudwatch]: https://aws.amazon.com/cloudwatch/
[lambda]: /development/stack/aws/lambda/
[ec2]: /development/stack/aws/ec2/

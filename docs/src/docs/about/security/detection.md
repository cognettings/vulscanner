---
id: detection
title: Threat Detection
sidebar_label: Threat Detection
slug: /about/security/detection
---

## Description

For threat detection purposes
we adopted [Amazon GuardDuty](https://aws.amazon.com/guardduty/).
It continuously monitors for
malicious activity and
unauthorized behavior
to protect AWS accounts,
Amazon Elastic Compute Cloud (EC2) workloads,
container applications,
and data stored in
Amazon Simple Storage Service (S3).

GuarDuty uses machine learning,
anomaly detection,
network monitoring,
and malicious file discovery for
threat and intrusion detection tasks.

It is capable of
analyzing tens of billions of events
across multiple AWS data sources,
such as AWS CloudTrail event logs,
Amazon Virtual Private Cloud (VPC) Flow Logs,
Amazon Elastic Kubernetes Service (EKS) audit
and system-level logs, and DNS query logs.

## S3 Protection

S3 protection is a feature offered by Amazon GuardDuty that
enhances the monitoring capabilities for data stored in Amazon
S3 buckets. By default, GuardDuty monitors bucket-level API
operations related to S3 resources. However, with S3 protection
enabled, GuardDuty expands its monitoring to include object-level
API operations within S3 buckets. This means it can detect
suspicious or potentially malicious activities at a more granular level.

![S3 Protection Configuration](https://res.cloudinary.com/fluid-attacks/image/upload/v1689107662/docs/about/security/S3Protection.png)

## EKS Protection

EKS Protection in Amazon GuardDuty offers threat detection coverage for Amazon
Elastic Kubernetes Service (Amazon EKS) clusters in your AWS environment. It
includes two key components: EKS Audit Log Monitoring and EKS Runtime Monitoring.

EKS Audit Log Monitoring focuses on detecting suspicious activities within EKS
clusters by analyzing Kubernetes audit logs. These logs capture a sequential
record of actions performed by users, applications using the Kubernetes API,
and the control plane.

On the other hand, EKS Runtime Monitoring provides real-time threat detection
for Amazon EKS nodes and containers in your AWS environment. By leveraging the
Amazon EKS add-on GuardDuty security agent, it monitors and analyzes runtime
events within your EKS clusters, helping to identify potential security
threats.

By configuring your accounts with both EKS Audit Log Monitoring and EKS
Runtime Monitoring, you can achieve comprehensive EKS Protection. This
setup enables monitoring at the cluster control plane level and extends
down to the individual pod or container operating system level, providing
optimal security coverage for your EKS environment.

![EKS Protection Configuration](https://res.cloudinary.com/fluid-attacks/image/upload/v1689107670/docs/about/security/EKSProtection.png)

## Malware Protection

Malware Protection in Amazon GuardDuty is a feature designed to
identify potential malware presence in Amazon EC2 instances and
container workloads within your AWS account. It performs scans
on the Amazon Elastic Block Store (EBS) volumes attached to these
instances or workloads.

There are two types of scans offered by Malware Protection:

- **GuardDuty-initiated malware scan:** This scan is initiated by
  GuardDuty on a periodic basis. It automatically scans the EBS
  volumes associated with your EC2 instances and container workloads
  to detect any signs of malware.

- **On-demand malware scan:** With this option, you can manually
  trigger a malware scan for specific EBS volumes. It allows
  you to initiate a scan whenever needed, providing flexibility
  in scanning resources on-demand.

By leveraging these scanning capabilities, Malware Protection
helps you proactively detect the potential presence of malware
in your EC2 instances and container workloads. For more detailed
information about the differences between these scan types, you
can refer to the GuardDuty Malware Protection documentation.

![Malware Protection Configuration](https://res.cloudinary.com/fluid-attacks/image/upload/v1689107678/docs/about/security/MalwareProtection.png)

## AWS GuardDuty Summary

While GuardDuty generates detailed findings and insights based on the last
10,000 events, it does not directly generate predefined reports summarizing
these findings. However, by analyzing the generated findings, you can gain
valuable insights into common attack vectors, suspicious user behavior,
unauthorized access attempts, data exfiltration attempts, malicious IP
addresses, vulnerable EC2 instances, anomalous network traffic, cryptocurrency
mining activity, suspicious DNS activity, and policy violations. Regularly
reviewing and addressing these findings enables you to proactively strengthen
your security measures and protect your AWS resources against potential
threats and attacks.

![GuardDuty Summary](https://res.cloudinary.com/fluid-attacks/image/upload/v1689349887/docs/about/security/Summary.png)

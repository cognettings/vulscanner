---
slug: toyota-three-data-leaks/
title: Leaking Data, Not Oil, for 10 Years
date: 2023-06-08
subtitle: Toyota's ancient and recently disclosed data leaks
category: attacks
tags: cybersecurity, credential, code, cloud, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1686264813/blog/toyota-three-data-leaks/cover_toyota.webp
alt: Photo by Snowscat on Unsplash
description: We describe the data leaks recently disclosed by Toyota Motor Corporation lasting five, eight and ten years.
keywords: Toyota, Toyota Connected Corporation, T Connect, Data Leak, Cloud Environments, Source Code, Ten Years, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Content Writer & Editor
source: https://unsplash.com/photos/lypqQBIRXpo
---

Five years is how long a data leak exposed the email addresses
and management numbers
of about 300,000 of Toyota Motor Corporation's customers.
The firm disclosed this on October 7 last year.
What happened was that part of the T-Connect site source code
publicly available on GitHub
had an access key for the T-Connect customer database.

Almost ten years is how long a data leak exposed the car-location information
of more than 2 million of Toyota's customers.
The firm disclosed this only on May 12 this year.
A cloud misconfiguration allowed accessing the contents of a database
without requiring a password.

And eight years is how long yet another data leak exposed vehicle data
and customer information
of over 260,000 of Toyota's customers.
The firm disclosed this on May 31.
It found out about the leak
in the couple of weeks checking its cloud environments for misconfigurations
following the previous discovery.

Let's see the known details of each one of these leaks.

## Oops! That shouldn't have been there

A bit of background:
Toyota Connected Corporation offers a service called T-Connect,
whose application allows customers to know their vehicle's status,
control systems like door locks and air-conditioner,
and access entertainment,
navigation and customer service options.
The leaks described affected users of this product.

Let's first talk about the [earliest announcement](https://global.toyota/jp/newsroom/corporate/38095972.html),
which happens to be about the most recent blunder.
The development of the T-Connect website has been in charge of subcontractors,
who left in the source code an access key to a customer database.
This was available to everyone on GitHub from December 2017,
until September 15, 2022,
when the leak was discovered.
The code was made private on that second date,
and the access keys were changed two days later.

In the leaked database there were 296,019 cases of email addresses
from customers registered to the website between July 2017
and the date of discovery.
There were also the corresponding numbers
that are assigned to customers for management purposes.
Toyota reported that it could neither confirm nor deny
whether the data was accessed and stolen by malicious hackers.
It warned its customers
that they could be the target of [spoofing](../spoofing/)
and [phishing](../blog/phishing/) attacks,
though.
Also,
it created a form in its website
where users could see if their email was compromised,
and opened a dedicated call center.

So let's see the security issue here.
Unfortunately,
it's really not something uncommon,
as we've noted [elsewhere](../secure-infra-code/),
to find credentials stored in source code during security testing.
There may be reasons why this practice is being kept up
(e.g., making it easier and quicker for devs to access assets and services
and update configurations in early development stages).
But,
in any case,
it should be noticed during development and eliminated before deployment.
What's more,
developers should be aware of how risky this practice is.
Now,
the responsibility of those devs aside,
why did it take Toyota so long to find out about this leak?
This is one of the pieces missing from what has been reported.
It seems, though,
like no automated nor [penetration testing](../../product/mpt/) were done
in all those years.
For five years their customers may have been receiving scams.
But five years is only the shortest-lived leak discussed in this blog post.

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/penetration-testing/"
title="Get started with Fluid Attacks' Penetration Testing solution
right now"
/>
</div>

## A check ten years overdue

As though the above and following unfortunate leaks were drawn out
of a cautionary tale to warn companies about two very common security issues,
our next two leaks are due to misconfiguration of the cloud environments.
[The lengthiest leak](https://global.toyota/jp/newsroom/corporate/39174380.html)
had been exposing part of the data
that Toyota Motor Corporation entrusted to Toyota Connected Corporation
due to the corresponding database not requiring a password.
Upon discovery,
the former went on to block access and continue investigation
of all the cloud environments managed by the latter.
This specific database was publicly available between November 6, 2013,
and April 17, 2023.

The database exposed information of approximately 2.15 million customers
in Japan
using the following services between January 2, 2012, and April 17, 2023:
T-Connect,
G-Link (like T-Connect but for Lexus, Toyota's luxury brand),
G-Link Lite (for U-Cars other than Lexus certified pre-owned vehicles)
or G-BOOK (former name of T-Connect).
Specifically,
the contents of the database were the vehicles' chassis number,
location information with time data
and integrated GPS navigation terminal ID number.
Moreover,
anyone could have accessed video taken by the vehicles' driving recorder
between November 14, 2016, and April 4, 2023.
No personally identifiable information was exposed.
And,
from what Toyota said in its press release,
it seems that the leak had yet to be leveraged by malicious hackers.
But this is hardly an ideal situation.

This time,
Toyota reported that the roots of the problem were
that data handling rules were not sufficiently explained
and lacked thoroughness.
The fact that these are identified
as the main causes of a ten-year-old blunder,
undetected through a big chunk of cloud computing evolution,
speaks of a cybersecurity culture
that has been begging to take itself seriously.
(If this comment seems harsh,
let's remember
that this firm led the [global automotive market share in 2022](https://www.statista.com/statistics/316786/global-market-share-of-the-leading-automakers/).)
Toyota promised in its press release that it will educate employees,
audit cloud settings
and continuously monitor the status of these settings.

Looking further for misconfigurations in its cloud environments,
Toyota found out about [the leak it disclosed most recently](https://global.toyota/en/newsroom/corporate/39241625.html).
From what it says in their press release,
it can only be guessed
that this leak arose under the same circumstances as the previous one.
This time,
the affected database could be accessed publicly from February 9, 2015,
until May 12, 2023.

The data included navigation terminal ID numbers,
some map data update files and updated data creation dates
of approximately 260,000 customers in Japan.
But the situation is riskier
for customers in "some countries in Asia and Oceania."
Toyota does not disclose the approximate number of the impacted,
but does say that their following data was leaked
from October 2016 until May 2023:
name, phone number, address, email address, customer ID,
vehicle registration number
and Vehicle Identification Number (i.e., chassis number).
This case is the worst so far!
As a response,
Toyota promises to "deal with the case in each country
in accordance with the personal information protection laws
and related regulations of each country."

Hopefully these leaks motivate every organization
to check their [secure coding practices](../secure-coding-practices/)
and the configuration of their cloud environments.
And hopefully they are starting
to have their cybersecurity continuously evaluated
with [vulnerability scanning](../vulnerability-scan/)
and [penetration testing](../../solutions/penetration-testing/).
The latter specially evolves alongside the threat landscape
so that companies having it performed in their system
can find out their resistance to attacks
simulating those launched by malicious hackers.

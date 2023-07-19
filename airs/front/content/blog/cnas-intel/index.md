---
slug: cnas-intel/
title: CNAs Intelligence
date: 2023-05-12
subtitle: A hacker's view of the performance of Researcher CNAs
category: opinions
tags: cybersecurity, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1683904807/blog/cnas-intel/sven-mieke-fteR0e2BzKo-unsplash.webp
alt: Photo by Sven Mieke on Unsplash
description: We've been a CNA for a while, and this is an analysis of our performance.
keywords: Cybersecurity Success, Security Status, Ethical Hacking, Pentesting, Vulnerability
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: VP of Hacking and Research
source: https://unsplash.com/photos/fteR0e2BzKo
---

On June 2, 2021, Fluid Attacks was admitted as a CNA by MITRE.
A CVE Numbering Authority, or CNA, is responsible for
assigning CVE IDs to vulnerabilities found in software.
MITRE grants the CNA the right to determine whether
certain issue can be considered a vulnerability. That means
that as a CNA it's at our discretion whether to flag an issue as
a vulnerability based on whether there's a violation of the
security policy of the application, whether there's any negative
impact on the product, and the analysis of the
product owner regarding the issue.

The other variable in the responsibility of CNAs
is the chosen *software*. MITRE limits
the scope of CVE ID assignment to software that is
licensable and publicly available, either paid or
free. Also, each CNA has a scope. Some CNAs assign CVE
IDs only to their own products (Microsoft, Apple, Adobe,
for example).
Our scope is any software that is not within the scope
of other CNAs, which means that we can't assign CVE IDs
to products from Microsoft, for example, but still, the
universe of software is huge.

Having the ability to assign CVE IDs, our research team
has created a [Disclosure Policy](../../advisories/policy/),
which we follow to talk to a vendor privately once we have
identified a possible vulnerability in their software.
In an ideal world, the vendor would acknowledge the
vulnerabilities, create fixes and inform us of this within a
defined period of time, after which we make the
vulnerability public in our [Advisories](../../advisories/)
page. More information on our disclosure process
is detailed [here](../security-advisories/).

To this date, we have assigned 76 CVE IDs and want
to check our performance with similar CNAs. Let's
first see the process of gathering the information.

## Gathering the data

As mentioned before, every CNA has a defined scope,
but there is additional metadata associated to the CNAs.

MITRE provides certain ways to interact with their
information. Red Hat created a
[tool](https://github.com/RedHatProductSecurity/cvelib)
which can be used to check basic information of the CNA,
reserve CVE IDs and list the IDs published and reserved,
among other tasks.

``` console
aroldan ~  $ cve org
Fluid Attacks — Fluid Attacks
├─ Roles: CNA
├─ Created: Wed Jun  2 19:49:20 2021
└─ Modified:    Fri May  5 03:13:21 2023
aroldan ~  $ cve list | grep PUBLISHED | wc -l
      76
aroldan ~  $ cve list | head -2
CVE ID           STATE       OWNING CNA      RESERVED BY                                RESERVED ON
CVE-2022-0698    PUBLISHED   Fluid Attacks   aroldan@fluidattacks.com (Fluid Attacks)   Mon Feb 21 02:32:28 2022
aroldan ~  $ cve show CVE-2022-0698
CVE-2022-0698
├─ State:   PUBLISHED
├─ Owning CNA:  Fluid Attacks
├─ Reserved by: aroldan@fluidattacks.com (Fluid Attacks)
└─ Reserved on: Mon Feb 21 02:32:28 2022
```

But it is limited only to the current CNA, which is
identified using certain secret parameters.

Other information can be seen on the CVE Program's
[List of Partners](https://www.cve.org/PartnerInformation/ListofPartners).

![List of Partners](https://res.cloudinary.com/fluid-attacks/image/upload/v1683904865/blog/cnas-intel/Screenshot_2023-05-11_at_4.24.22_PM.webp)

As can be seen, Fluid Attacks' organization type is
*Researcher*.
To check our performance with other *Researcher* CNAs, we
must first filter what other CNAs have the same type.
A CNA can have multiple types:

![Airbus](https://res.cloudinary.com/fluid-attacks/image/upload/v1683904916/blog/cnas-intel/Screenshot_2023-05-11_at_4.33.23_PM.webp)

Airbus, for example, is both a Vendor and a Researcher,
and its scope includes Airbus products as well as
third-party software.

However, we just want to check CNAs that have *only* the
type *Researcher*, just like us.

That List of Partners has a filter field but it's not
very advanced. But if we use simple tools, we see that
the List of Partners page is actually a client-side
application bundled into a JS file:

![GetJS](https://res.cloudinary.com/fluid-attacks/image/upload/v1683904942/blog/cnas-intel/getjs1.webp)

That JS script has actually little code, but has embedded a
JSON with all the CNAs information:

![ParseJS1](https://res.cloudinary.com/fluid-attacks/image/upload/v1683905414/blog/cnas-intel/parsejs1.webp)

With some simple filters, the JSON can be extracted
from the JS:

```JSON
aroldan ~  $ curl -s https://www.cve.org/js/app.3611fa3b.js  | grep -Eo 'g=JSON.parse\(.*\);r.Z.use' | sed -e "s/g=JSON\.parse('//g; s/');r.Z.use//g; s/<a href=\\\'//g; s/\\\' target=\\\'_blank\\\'>//g; s/\\\'//g" | json_pp
[
   {
      "CNA" : {
         "TLR" : {
            "organizationName" : "MITRE Corporation",
            "shortName" : "mitre"
         },
         "isRoot" : false,
         "roles" : [
            {
               "helpText" : "",
               "role" : "CNA"
            }
         ],
         "root" : {
            "organizationName" : "n/a",
            "shortName" : "n/a"
         },
         "type" : [
            "Vendor"
         ]
      },
      "cnaID" : "CNA-2009-0001",
      "contact" : [
         {
            "contact" : [
               {
                  "label" : "Adobe security contact page",
                  "url" : "https://helpx.adobe.com/security/alertus.html"
               }
            ],
...
```

And with the extracted JSON, queries can be made directly.
First, let's list the number of CNAs:

```bash
aroldan ~  $ curl -s https://www.cve.org/js/app.3611fa3b.js  | grep -Eo 'g=JSON.parse\(.*\);r.Z.use' | sed -e "s/g=JSON\.parse('//g; s/');r.Z.use//g; s/<a href=\\\'//g; s/\\\' target=\\\'_blank\\\'>//g; s/\\\'//g" | json_pp | jq -c '.[]' | wc -l
     288
aroldan ~  $
```

Nice. To the date of this writing, there are 288 CNAs active.

As we can search now with any filter, let's check
Fluid Attacks' CNA metadata:

```bash
aroldan ~  $ curl -s https://www.cve.org/js/app.3611fa3b.js  | grep -Eo 'g=JSON.parse\(.*\);r.Z.use' | sed -e "s/g=JSON\.parse('//g; s/');r.Z.use//g; s/<a href=\\\'//g; s/\\\' target=\\\'_blank\\\'>//g; s/\\\'//g" | json_pp | jq '.[] | select (.organizationName == "Fluid Attacks")'
{
  "CNA": {
    "TLR": {
      "organizationName": "MITRE Corporation",
      "shortName": "mitre"
    },
    "isRoot": false,
    "roles": [
      {
        "helpText": "",
        "role": "CNA"
      }
    ],
    "root": {
      "organizationName": "n/a",
      "shortName": "n/a"
    },
    "type": [
      "Researcher"
    ]
  },
  "cnaID": "CNA-2021-0020",
  "contact": [
    {
      "contact": [],
      "email": [
        {
          "emailAddr": "help@fluidattacks.com",
          "label": "Email"
        }
      ],
      "form": []
    }
  ],
  "country": "Colombia",
  "disclosurePolicy": [
    {
      "label": "Policy",
      "language": "",
      "url": "https://fluidattacks.com/advisories/policy/"
    }
  ],
  "organizationName": "Fluid Attacks",
  "resources": [],
  "scope": "Vulnerabilities in third-party software discovered by Fluid Attacks that are not in another CNAâs scope",
  "securityAdvisories": {
    "advisories": [
      {
        "label": "Advisories",
        "url": "https://fluidattacks.com/advisories/"
      }
    ],
    "alerts": []
  },
  "shortName": "Fluid Attacks"
}
```

Cool. Now we can find all the CNAs that are *only* the
*Researcher* type:

```bash
aroldan ~  $ curl -s https://www.cve.org/js/app.3611fa3b.js  | grep -Eo 'g=JSON.parse\(.*\);r.Z.use' | sed -e "s/g=JSON\.parse('//g; s/');r.Z.use//g; s/<a href=\\\'//g; s/\\\' target=\\\'_blank\\\'>//g; s/\\\'//g" | json_pp | jq -c '.[] | select ( .CNA.type == ["Researcher"])' | wc -l
      16
aroldan ~  $
```

Surprisingly, out of the 288 current CNAs, there are
just 16 *Researcher*-only CNAs in the world.

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/red-teaming/"
title="Get started with Fluid Attacks' Red Teaming solution right now"
/>
</div>

## Performance of Researcher CNAs

We have now the CNAs that share the same type as us.
At Fluid Attacks, we have a dedicated team performing
research, with a clear prioritization model and a well-oiled
methodology for finding vulnerabilities in software that
fits our scope.

Measuring the performance of a Researcher CNA is hard
because it all depends on the internal process taken
to emit CVE IDs.

The only publicly available parameter to compare these
CNAs is basically the number of CVE IDs assigned in total
and CVE IDs assigned per year.

One of the metadata which is only visible on the JSON
is the CNA ID.

```bash
aroldan ~  $ curl -s https://www.cve.org/js/app.3611fa3b.js  | grep -Eo 'g=JSON.parse\(.*\);r.Z.use' | sed -e "s/g=JSON\.parse('//g; s/');r.Z.use//g; s/<a href=\\\'//g; s/\\\' target=\\\'_blank\\\'>//g; s/\\\'//g" | json_pp | jq '.[] | select ( .CNA.type == ["Researcher"] and .organizationName == "Fluid Attacks") | .cnaID'
"CNA-2021-0020"
```

According to the value, it is safe to assume that the
CNA ID contains the year in which the organization
was accepted by MITRE as CNA.

Together with that, this is the data gathered from the *Researcher*
class CNAs:

| CNA                                                                          | Country     | \# CVEs | CNA ID Year | CVEs/Year | Ranking (Total) | Ranking (CVEs/Year) |
| ---------------------------------------------------------------------------- | ----------- | ------- | ----------- | --------- | --------------- | ------------------- |
| Cyber Security Works Pvt. Ltd                                                | India       | 55      | 2020        | 13.75     | 5               | 7                   |
| Fluid Attacks                                                                | Colombia    | 76      | 2021        | 25.33     | 3               | 4                   |
| Larry Cashdollar                                                             | USA         | 9       | 2016        | 1.13      | 10              | 11                  |
| Talos                                                                        | USA         | 55      | 2016        | 6.88      | 5               | 8                   |
| Government Technology Agency of Singapore Cyber Security Group (GovTech CSG) | Singapore   | 18      | 2021        | 6.00      | 9               | 9                   |
| AppCheck Ltd                                                                 | UK          | 6       | 2021        | 2.00      | 11              | 10                  |
| VulDB                                                                        | Switzerland | 480     | 2001        | 20.87     | 1               | 5                   |
| Dutch Institute for Vulnerability Disclosure (DIVD)                          | Netherlands |         | 2022        | 0.00      |                 | 13                  |
| Automotive Security Research Group (ASRG)                                    | USA         | 1       | 2022        | 0.50      | 12              | 12                  |
| ZUSO Advanced Research Team (ZUSO ART)                                       | Taiwan      | 36      | 2022        | 18.00     | 8               | 6                   |
| The Missing Link Australia (TML)                                             | Australia   | 51      | 2022        | 25.50     | 7               | 3                   |
| NetRise                                                                      | USA         | 0       | 2022        | 0.00      | 13              | 13                  |
| Austin Hackers Anonymous                                                     | USA         | 0       | 2023        | 0.00      |                 | 13                  |
| STAR Labs SG Pte. Ltd                                                        | Singapore   | 100     | 2023        | 100.00    | 2               | 1                   |
| Securifera, Inc                                                              | USA         | 61      | 2023        | 61.00     | 4               | 2                   |
| Halborn                                                                      | USA         | 0       | 2023        | 0.00      | 13              | 13                  |

## CNA performance analysis

- VulDB is the CNA with the most CVEs assigned. However, its performance
  per year is ranked as fifth.
- STAR Labs SG has the best CNA performance per year.
- Fluid Attacks has the third-best performance in the total of
  CVE IDs assigned and the fourth-best in assignments per year. Not bad!
- Fluid Attacks has the best performance in America!

## Conclusions

This was a hacker's view of the performance of
*Researcher* CNAs.
The data shows Fluid Attacks has had an outstanding performance.
Please note that there are other research teams in the world
that look for vulnerabilities and report them directly
via the MITRE Root CNA, but those were not included in this
analysis.

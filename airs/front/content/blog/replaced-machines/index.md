---
slug: replaced-machines/
title: Will Machines Replace Us?
date: 2018-02-13
category: philosophy
subtitle: Automatic detection vs. manual detection
tags: security-testing, software, vulnerability
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331053/blog/replaced-machines/cover_yfml2t.webp
alt: Data has a better idea sign
description: Vulnerability detection by an automated tool is not enough to conclude that an app is secure. The knowledge and experience of a person are still necessary.
keywords: Vulnerability Detection, Manual Detection, Automatic Detection, Security, Web Application, Automated Tools, Ethical Hacking, Pentesting
author: Andres Cuberos
writer: cuberos
name: Andrés Cuberos Lopera
about1: Electronic Engineer
about2: Enjoy the small things in life like a good beer, music and sleep
source: https://unsplash.com/photos/1K6IQsQbizI
---

More than 20 years have passed since Garry Kasparov, the chess world
champion, was defeated by Deep Blue, the supercomputer designed by IBM.
For many people, that event was proof that machines had managed to
[exceed human
intelligence](https://theconversation.com/twenty-years-on-from-deep-blue-vs-kasparov-how-a-chess-match-started-the-big-data-revolution-76882).
This belief raised many doubts and concerns regarding technological
advances, which went from workers worried about their jobs to people
imagining that the apocalypse was coming (an idea encouraged by
Hollywood).

All fiction aside, that first concern was well-founded and made some
sense. Every year we witness new machines on the market with the ability
to complete tasks with precision and speed and outperform dozens of
experienced workers. By machine, I don’t mean a robot looking like
Arnold Schwarzenegger in *The Terminator*. It could be any device
programmed to complete a specific task, for example, self-driving cars,
robotic arms and tools to detect vulnerabilities in web apps. As
cybersecurity specialists, what can we expect from all this? Are we
becoming increasingly expendable?

<div class="imgblock">

![Robot holding a firearm with an explosion in the background](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331052/blog/replaced-machines/terminator_w63xoh.webp)

<div class="title">

Figure 1. The inevitable outcome that Hollywood shows us.

</div>

</div>

Fortunately, our future does not look so bleak. Even though there are
many powerful automated tools for vulnerability detection, the human
role is still vital if a detailed and effective security analysis is
desired. There are still situations in which we have the upper hand:

- Tools may have large vulnerability databases. They can know how to
  find security flaws and what risk levels they represent. However,
  they do not have that human factor that comes with experience and
  allows a security analyst to identify which vulnerabilities can be
  combined to create a more critical attack vector. Expertise can
  enable a person to find vulnerabilities that a machine may overlook

- Analyzers generate reports with all their findings and criticality,
  but how complete are they? They tell you how many input fields are
  affected by a vulnerability, but do they tell you which inputs allow
  sensitive data extraction? Do they tell you how to exploit a form to
  modify a database? Unfortunately, the answer is no. Automated tools
  only determine the existence of flaws. How those flaws can be
  exploited and leveraged to an attacker’s advantage is strictly a
  human skill.

- A false positive is the report of the discovery of a vulnerability
  that [does not actually
  exist](http://resources.infosecinstitute.com/automated-tools-vs-a-manual-approach/#gref).
  It’s a common problem among these tools, resulting from the
  inability to exploit a given flaw. A tool that does not adequately
  filter out false positives can do more harm than good. If you use it
  to avoid the cost of hiring a security professional, you may have no
  idea which of the vulnerabilities it reports are false positives.
  The task of filtering them may then fall to the developer, who may
  not necessarily be security savvy.

  False positives are also one of the reasons why these tools are not
  commonly used in Continuous Integration environments. If we program
  an integrator to check every change made to a source code and stop
  the application deployment if an error is found, false positives
  could make those deployments a headache.

- Netsparker (developer of one of these tools) [agrees with this
  position](https://www.netsparker.com/blog/web-security/owasp-top-10-web-security-scanner/):
  no analyzer can detect all vulnerabilities classified as the
  [Top 10](https://www.owasp.org/index.php/Top_10-2017_Top_10) most
  critical. They conclude that an analyzer cannot determine whether an
  application is functioning as intended and aligned with business
  objectives, or whether sensitive information (which varies by
  business type) is properly protected, or whether user privileges are
  correctly assigned. In these and many other cases, human reasoning
  must make the final decision.

Our goal is not to take merit away from these tools. We use many of them
in our professional life, and they are powerful allies. What we want is
to revise the mistaken belief that they are sufficient to decide whether
a web app is secure or not.

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/ethical-hacking/"
title="Get started with Fluid Attacks' Ethical Hacking solution right now"
/>
</div>

To do this, we developed an experiment. We used the insecure web
application bWAPP and the automated analyzers W3af, Wapiti and OWASP
ZAP. All of them share the features of being open source and able to be
executed from the command line. Thanks to this, it is possible to use
them in a Continuous Integration environment. For bWAPP, we assumed a
total of 170 vulnerabilities, based on the company [that developed the
app](http://www.mmebvba.com/sites/default/files/downloads/bWAPP_sample_report.pdf).
Let’s see how our contestants performed:

<div class="tc">

**Table 1. bWAPP Vulnerability Analysis**

</div>

| Tool      | Detected | % Not Detected | Time     |
| --------- | -------- | -------------- | -------- |
| W3af      | 28       | 83.5%          | 00:02:30 |
| Wapiti    | 26       | 84.7%          | 00:02:00 |
| ZAP-Short | 42       | 75.3%          | 00:19:00 |
| ZAP-Full  | 59       | 65.3%          | 01:30:00 |

ZAP-Short refers to the ZAP tool with only the XSS and SQLi plugins
enabled. ZAP-Full refers to the same tool with all of its plugins
enabled. It’s important to note that the application authentication had
to be disabled. We did this to allow the tools to work properly from the
command line. This fact took the experiment further away from reality
and left a layer of the web app unanalyzed.

Another important detail is that the analyzers were not targeted at the
main site, as a real test would do. The target of the attack was a
specific bWAPP page where links to all other pages are listed —this way,
the tool achieves complete identification. bWAPP uses forms to reach all
other pages, so targeting the attack at the main page would result in 0
sites of interest being found. Tools such as Burp solve this problem [by
evaluating the
forms](https://support.portswigger.net/customer/portal/questions/12285606-spidering-form-submission),
but others fail in the same situation due to their inability to navigate
the main site.

To facilitate the analysis of the results, let’s take the best (by
ZAP-Full) and the worst (by Wapiti) and compare them against the whole
surface of the application. Let’s see what coverage was achieved.

<div class="imgblock">

![Coverage comparison between two analyzers with the scope of an application](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331050/blog/replaced-machines/yield_p99vw1.webp)

<div class="title">

Figure 2. Visual representation of the best and worst results.

</div>

</div>

We can see that even the best of the tools we used left out more than
half of the vulnerabilities, and false positives may exist among those
it found. In addition, it took an hour and a half to finish the
analysis, a time that is not appropriate for a Continuous Integration
environment.

Companies wishing to reduce costs by avoiding hiring security analysts,
relying solely on automated tools, would remediate vulnerabilities and
gain a false sense of security. They would ignore the fact that more
than half of the flaws could still be present to be exploited by
malicious users. In this way, the resources saved during development
would be spent, with interest, at the production stage.

## Conclusions

Yes, the rivalry between humans and machines has been present for a long
time now, and it will remain that way for a lot more. However, it is not
necessary to see this as a rivalry in all aspects. For example, in the
field of cybersecurity, it can be a complementary relationship, where
the tools help the analysts perform repetitive tasks faster, and the
analysts add their instinct and experience to detect the maximum amount
of vulnerabilities efficiently.

Paraphrasing Kasparov in [his TED
talk](https://www.ted.com/talks/garry_kasparov_don_t_fear_intelligent_machines_work_with_them),
the relationship between humans and machines, through an effective
process, is the perfect recipe to achieve our grandest dreams.

<div class="imgblock">

![Handshake between a human and a robot](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331052/blog/replaced-machines/coexistence_xfdu7g.webp)

<div class="title">

Figure 3. An alternative outcome to the human-machine relationship.

</div>

</div>

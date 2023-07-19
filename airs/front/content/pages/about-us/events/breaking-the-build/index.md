---
slug: about-us/events/breaking-the-build/
title: Breaking the Build
subtitle: Our DevSecOps Habits
category: events
description: The conference Breaking the Build presents Fluid Attacks' SecDevOps habits that allow us to keep improving every day, and how to implement them in your company.
keywords: Fluid Attacks, SecDevOps, Habits, Breaking The Build, CI-CD, Conference, Pentesting, Ethical Hacking
eventspage: yes
banner: events-bg
---

## 1\. Objective

The term **DevSecOps** has grown in popularity
in recent years.
However,
webinars addressing this topic
tend to only focus on its benefits,
or possible use cases,
ignoring people's main motivation
to attend this kind of event.

It is fairly safe to assume that
people want to also find out **how this works**
and **where to start**.
Many speakers demonstrate how to perform tests
over an extremely simple environment,
completely unrelatable to our everyday tasks,
and, in this case,
new questions emerge,
such as:
**Does this work?**
Or,
**how can I apply this to my company?**

Based on the above,
in this talk,
we seek to answer the posed questions
by sharing the methodologies and work practices,
or **habits**,
that allow us to implement a DevSecOps culture
in the execution of our projects;
from the infrastructure management
to the development of our orchestration platform
for vulnerability remediation.

These habits allow us
not only to increase our productivity,
and generate value for our customers
on a daily basis,
but also to increase the security of our production deployments.
Thereby,
we have been able to reach the following average rates:

<div class="avarage-rates-section">
<a href="https://gitlab.com/fluidattacks/universe/-/merge_requests?scope=all&state=merged"
target="_blank">
<div class="fl w-100 w-50-l pa2">
<div class="outline-transparent bg-button-red hv-bg-fluid-rd pointer white pv3
fw7 f3 t-all-3-eio br2 bc-fluid-red ba poppins tc">
<div>Production deployment frequency</div>
<div>70/day</div>
</div>
</div>
</a>
<a href="https://gitlab.com/fluidattacks/universe/-/merge_requests?scope=all&state=merged&search=%22rever%22"
target="_blank">
<div class="fl w-100 w-50-l pa2">
<div class="outline-transparent bg-button-red hv-bg-fluid-rd pointer white pv3
fw7 f3 t-all-3-eio br2 bc-fluid-red ba poppins tc">
<div>Deployment success</div>
<div>99.99%</div>
</div>
</div>
</a>
</div>

## 2\. Content

This **seminar/workshop** aims to implement the concepts and techniques
covered in [Burn the Datacenter](../burn-the-datacenter/).
Everything is performed **live**
over real infrastructure and applications,
giving the audience a look
into the backstage of the process:
The tools used,
the logs that allow us to identify issues,
and even the source code that defines each step
for the correct deployment of our applications,
always focusing on how our infrastructure and products are updated
in **real time**.

To help understand how everything happens
and demonstrate how to take the first step
to reach this configuration,
we also explain all the work habits
that have allowed us to reach this point
and keep improving daily.
These include topics such as:

- Continuous hacking the systems to guarantee
  the integration of the security part in the SDLC.

- Source code management inside repositories,
  following a **monorepo** structure
  (say goodbye to multirepo).

- Keep a clean and small environment for the developers,
  including the changes to the master branch,
  avoiding code accumulation
  and reaching **zero inventory**
  (leaving gitflow behind).

- Generate daily value to the customers
  through a **micro changes** methodology
  (instead of big changes
  every 3 weeks or more).

- Migrate and manage all the infrastructure
  as versioned source code,
  turning it into **immutable infrastructure**
  (avoiding management consoles
  and unauthorized changes).

- Define Continuous Integration environments as source code,
  pipeline as code,
  in a way that can easily be configured and modified
  for all kinds of tests
  (avoiding graphical interface limitations
  for pipeline configurations).

- Avoid servers at any cost,
  migrating to cloud services
  and reaching a **serverless** infrastructure.

- Safe password management when deploying an application,
  avoiding sensitive information disclosure in source code
  and **keeping the secrets protected**.

- Deploy **ephemeral environments**
  that allow testing all the developed features
  before passing to production
  (reducing project complexity
  by avoiding development environments,
  testing, QA and others).

- **Breaking the build**
  even before making a commit to the repository
  using local reproducible integration tests
  to check the source code.

- Perform tests over the source code
  and over the deployment
  that **break the build** as a result of the smallest error
  (instead of only notifying and allowing the error
  to keep evolving/growing):

    - Unit testing

    - Functional testing

    - Coverage

    - Strict Linters

    - Security gates (SAST y DAST)

    - E2E

- Extreme reduction of build times
  by using the **cache** correctly.

- Take advantage of the features
  presented in the version control client Git:

    - Peer review

    - Squashing

    - Rebasing

    - Rollback

    - Trigger builds

- **Telemetry** accessible to developers
  (not logs,
  only available for infrastructure area).

Each above-mentioned point is explained
while accessing Fluid Attacks' systems
to look at its implementation and operation.
According to the needs or interest of the participants,
it is possible to focus on the topics
they deem most important.

## 3\. Experience

This **workshop** has been presented to professionals in technology
and auditing areas for companies such as:
[Accenture](https://www.accenture.com/co-es/new-applied-now),
[Arus](https://www.arus.com.co/),
[ATH](https://www.ath.com.co/wps/themes/html/ath/index.html),
[Avianca](https://www.avianca.com/co/es/),
[B89](https://www.b89.io/),
[Bancolombia](https://www.grupobancolombia.com/wps/portal/personas),
[Banitsmo](https://www.banistmo.com/),
[BIVA](https://www.biva.mx/en/web/portal-biva/home),
[Cadena](https://www.cadena.com.co/),
[Cidenet](http://cidenet.com.co/),
[Colpatria](https://www.colpatria.com/),
[Cognox](http://www.cognox.co),
[Coordiutil](https://www.vendesfacil.com/),
[Corona](https://www.corona.co/),
[EAFIT](http://www.eafit.edu.co/),
[Evendi Digital](https://evendidigital.com/),
[F2X](https://www.f2x.com.co/),
[GCO](http://www.gco.com.co/),
[Grupo AVAL](https://www.grupoaval.com/wps/portal/grupo-aval/aval/),
[Grupo Éxito](https://www.grupoexito.com.co/es/),
[Interbank](https://interbank.pe/),
[Komet Sales](https://www.kometsales.com/),
[Nutresa](https://gruponutresa.com/),
[Payválida](https://www.payvalida.com/),
[Protección](https://www.proteccion.com/wps/portal/proteccion/),
[RUNT](https://www.runt.com.co/),
[Seti](https://seti.com.co/),
[Banco Pichincha](https://www.bancopichincha.com.co/web/personas),
[Soy Yo](https://www.soyyo.co/),
[BTG Pactual](https://www.btgpactual.com.co/),
[Caja Cusco](http://www.cmac-cusco.com.pe/),
[Banco Azul](https://www.bancoazul.com/),
[Sistecrédito](https://www.sistecredito.com/),
[Banco Agromercantil](https://www.bam.com.gt/),
[Bantrab](https://www.bantrab.com.gt/),
[Telered](https://www.telered.com.pa/),
[Virtualsoft](https://virtualsoftlatam.com/),
[Linea Directa](https://www.lineadirecta.com.co/),
[OxxO](https://www.oxxo.com/),
[Chubb](https://www.chubb.com/co-es/),
[Banco Bolivariano](https://www.bolivariano.com/),
[ACH](https://www.achcolombia.com.co/home),
[Sodexo](https://www.sodexo.co/),
[Mutualser](https://www.mutualser.com/),
[Niubiz](https://www.niubiz.com.pe/),
[Nequi](https://www.nequi.com.co/),
[La Haus](https://www.lahaus.com/),
[Banco General Panamá](https://www.bgeneral.com/),
[Yappy](https://www.bgeneral.com/yappy/),
[MFTech](https://www.mftech.io/),
[Banco Industrial](https://www.corporacionbi.com/gt/bancoindustrial/)
and [Tech and Solve](http://www.techandsolve.com/).

## 4\. Where?

The presentation is  hosted in  an external venue.

## 5\. Duration

The **workshop** has a duration of **6 hours**
(it is not possible to reduce its duration).
It comprises a live demonstration of our practices,
a morning break,
and a lunch break.

## 6\. When?

The **workshop** is designed to be performed
from **9 a.m.** to **3 p.m.**,
with a **30-minute** break at **12 m.**
The event date must be scheduled in agreement
between the participants and Fluid Attacks.

## 7\. Details

1. **Investment**:
    The space and food
    for this workshop
    are completely covered by Fluid Attacks.
    The attendees must commit their time and
    cover their transportation expenses,
    including vehicles parking costs,
    in case the facility exceeds its capacity.

2. **Material**:
    As with all events offered by Fluid Attacks,
    the event material is sent to the attendees
    once they complete the [online satisfaction survey](https://fluidattacks.formstack.com/forms/talk?Content=Breaking%20the%20build&Speaker=Juan%20Restrepo&Virtual=No).

## 8\. Audience

The **workshop** is suitable
for both technical and managerial personnel,
and the satisfaction rate for both profiles is equally high.
However,
if you wish to promote new changes and experimentation
within your company,
it is important to include people with decision-making power.

The **workshop** is designed
for an audience of between **14 and 16** people
on the customer side,
plus 4 additional participants
on Fluid Attacks' side.

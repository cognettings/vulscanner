---
id: main
title: Main
sidebar_label: Main
slug: /development/writing/documentation/main
---

## General

* **DG01:** We *must* create **one-word titles** for the sections
  (those that appear in the top menu).

* **DG02:** We *must* create short titles for the subsections
  (those that appear in the left side menu),
  not exceeding **32 characters**.
  (This does not apply to the Requirements and Vulnerabilities subsections).

* **DG03:** We *must not* be repetitive
  in the handling of titles and subtitles.
  Example (the subtitle *Criteria* is unnecessary
  in the introduction of the section with the same name):

  ![DG03](https://res.cloudinary.com/fluid-attacks/image/upload/v1624900945/docs/development/writing/dgb_qdmbql.webp)

* **DG04:** We *must* express the names of the sections and subsections
  in the same way whenever we refer to them.

* **DG05:** We *must not* use the same section or subsection names
  in other subsections or elements within them.
  For instance, we do not want URLs ending like this:
  /security/**transparency**/open-source/**transparency**/.

* **DG06:** For each section (e.g., Machine, Development, Criteria),
  we *must* write an introduction that makes it clear to readers
  what they will find there in general and in the subsections.

* **DG07:** We *should* be consistent
  in the presentation of the introductions to all sections.
  Based on recommendations by the American Lecturer,
  [Robert Pozen](https://www.amazon.com/Extreme-Productivity-Boost-Results-Reduce-ebook/dp/B007HBLNSS),
  we *can* follow three steps:
  (a) Contextualize the reader with facts or background data and issues
  that may be driving them to spend their time there.
  (b) Mention, as a summary, the main topic of the section,
  i.e., what we are going to discuss next.
  (c) Explain the organization, the text structure,
  and be coherent with the titles and subtitles within the section.
  We can follow a sequence, saying something like:
  "In the first part, we will expose [...].
  In the second part, we will describe [...]."

* **DG08:** Suppose a subsection contains subtitles in its text block
  on at least two levels
  (i.e., a group of subtitles is part of a larger subtitle).
  In this case, we *should* provide at least one introductory sentence
  for this subsection
  unless a separate introduction already corresponds to it.

* **DG09:** We *should* keep the presentation structure
  of the subsections that are part of the same level
  homogeneous (e.g., all of them with an introductory paragraph).

* **DG10:** We *should* exhibit all segments
  of the same group of information in a subsection
  following the same style
  (e.g., saying what the user will find in each case).

* **DG11:** We *must* include all first,
  second and third level subtitles of a subsection
  in the menu on the right side.

* **DG12:** For all subsections,
  we *must* present the subtitles of the right-hand menu
  in a homogeneous way
  (e.g., all without bold).

* **DG13:** When we speak in the first person,
  we *must* do so as a group (i.e., using the pronoun *we*),
  not as an individual.

* **DG14:** We *must* use illustrative images
  every time we explain the elements of an application or software.

* **DG15:** We *must* upload all the images we need to [Cloudinary](https://cloudinary.com/)
  and then use their corresponding links
  (which *must* have the filename extension .webp
  inside the .md files).

* **DG16:** In cases where we include warnings for the reader,
  pointing out something that *is not* part of the content,
  we *must* use the following command in Markdown
  (the word *Note* is just an option): `> **NOTE:** > [Text]`.
  Example:

  ![DG16](https://res.cloudinary.com/fluid-attacks/image/upload/v1624050029/docs/development/writing/dga_kqtp4r.webp)
  > **NOTE:**
  > This section of our documentation is under construction.

## FAQ

* **DF01:** We *must* answer the questions without circumlocutions.

* **DF02:** We *must* use the same names of the concepts
  (especially the keywords)
  in the questions and the answers.

## [Glossary](https://docs.fluidattacks.com/about/glossary)

* **DS01:** We *must* generate customized definitions,
  which may be paraphrases of other people's texts.

* **DS02:** We *must* display the words in alphabetical order (A-Z).

* **DS03:** We *must* state the definitions in a generalized way
  and without directing them to the reader.
  Thus, we *must* mention the work of `Fluid Attacks`
  only if necessary.

## [Requirements](https://docs.fluidattacks.com/criteria/requirements/)

* **DR01:** We *should* create short titles for the requirements,
  preferably no longer than **32 characters**.

* **DR02:** We *must* make a complete exposition of each requirement,
  including the following segments of information
  with the corresponding subtitles:
  requirement (i.e., main sentence), description,
  associated vulnerabilities, and references.

* **DR03:** We *should* ideally write the main sentence of each requirement
  in **150 characters** or less.

* **DR04:** We *should* write the main sentence of each requirement
  starting with the subject in charge of fulfilling a specific task,
  accompanied by the modal verb *must*
  (e.g., The system must provide a secure mechanism
  to regenerate a user's password.).

* **DR05:** In the description of the requirements,
  we *should* complement the information of the main sentence
  with the explanation of the processes involved,
  short definitions of elements
  and justifications of the requirements.

* **DR06:** We *must* put in quotation marks
  all external information (copied from the source)
  that is part of the references
  (e.g., [CWE](https://cwe.mitre.org/), [OWASP](https://owasp.org/)).

## [Vulnerabilities](https://docs.fluidattacks.com/criteria/vulnerabilities/)

* **DV01:** We *must* make a complete exposition of each vulnerability
  (i.e., including description and associated requirements).

> **NOTE:**
> This subsection of our documentation is under construction.

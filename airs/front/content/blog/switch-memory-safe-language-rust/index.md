---
slug: switch-memory-safe-language-rust/
title: Care For Memory Safety Yet?
date: 2023-05-08
subtitle: Why so many are switching to Rust
category: opinions
tags: cybersecurity, code, trend
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1683551984/blog/switch-memory-safe-language-rust/cover_rust.webp
alt: Photo by Phil Hearing on Unsplash
description: Memory-related security issues are common and often critical. To reduce their presence, ongoing projects are writing in memory-safe languages like Rust.
keywords: Rust, Memory Safety, Memory Unsafe, Memory Safe Languages, Secure By Design, Android, Google, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/AHGPhgPFYp0
---

Quite recently,
[Prossimo](https://www.memorysafety.org/about/),
a project by the Internet Security Research Group (ISRG),
informed the public
that [it is rewriting](https://www.memorysafety.org/blog/sudo-and-su/)
two core Unix-like command line tools,
sudo and su,
in the memory-safe programming language [Rust](https://www.rust-lang.org/).
The short description for this initiative reads:
"Let's make the utilities that mediate privileges safer."
And that is but one of its initiatives.
Some of the others are writing an [alternative to OpenSSL](https://www.memorysafety.org/initiative/rustls/)
and [Linux kernel drivers](https://www.memorysafety.org/initiative/linux-kernel/)
in Rust.
Also recently,
[Microsoft has been rewriting](https://www.theregister.com/2023/04/27/microsoft_windows_rust/)
Windows libraries in that language.
Why, essentially?
Basically,
the people behind these projects understand the critical severity
and exploitability of memory-related security issues detected in software
and are therefore pushing for a switch
to writing new source code in memory-safe languages.

The change is also supported by one of the best practices
mentioned in a recent publication
authored by the Cybersecurity and Infrastructure Security Agency (CISA),
the National Security Agency (NSA),
the Federal Bureau of Investigation (FBI)
and the cybersecurity authorities of Australia,
the United Kingdom,
Canada,
Germany,
the Netherlands
and New Zealand.
We're talking about their guide
to develop Secure-by-Design and -Default products,
which we summarized in a [previous post](../secure-by-design-and-default/).

Let's see what memory-related issues are,
how memory-safe languages like Rust are helping to address them,
and what are a couple of challenges related to the switch to Rust.

## Memory-related vulnerabilities

Software memory-related vulnerabilities include the following:

- The software writes data outside the bounds of the intended buffer,
  i.e., before the beginning or past the end of that buffer's allocated memory.
  This is known as an out-of-bounds write.

- The software reads data outside the bounds of the intended buffer.
  This is known as an out-of-bounds read.

- The software does not always free memory when it is no longer needed.

- The software attempts to fetch memory that has already been freed.

- The software attempts to use a variable that has not been initialized.

Exploiting these issues may lead to several different consequences.
For example,
while the out-of-bounds read weakness can compromise confidentiality,
allowing an attacker to get secret information,
the out-of-bounds write weakness can compromise integrity and availability,
allowing an attacker to modify memory,
execute unauthorized code or commands
or crash the software.

Memory-safety weaknesses are very common.
In a 2019 study,
the Microsoft Security Response Center (MSRC) informed
that around [70% of the CVEs Microsoft](https://github.com/Microsoft/MSRC-Security-Research/blob/master/presentations/2019_02_BlueHatIL/2019_01%20-%20BlueHatIL%20-%20Trends%2C%20challenge%2C%20and%20shifts%20in%20software%20vulnerability%20mitigation.pdf)
has addressed in over a decade
have been of this kind.
Similarly,
in 2019, [76% of Android 10 vulnerabilities](https://security.googleblog.com/2022/12/memory-safe-languages-in-android-13.html)
were of this kind.
And that same year [it was reported](https://langui.sh/2019/07/23/apple-memory-safety/)
that 71.5% of MacOS 10.14 vulnerabilities
and 66.3% of iOS 12 vulnerabilities were of this kind.

These vulnerabilities can be detected through security testing,
ideally before they reach the notice of malicious threat actors.
In order to detect improperly implemented or configured
memory protection mechanisms,
it might be necessary to perform [manual penetration testing](../../product/mpt/).
Ethical hackers can simulate "real-world" cyberattacks,
proceeding like malicious hackers would
to try and make the target software behave in unexpected ways,
but doing so with the permission of the organizations that own the products.
Moreover,
a measure to reduce the chances of having these weaknesses is
considering the programming language in use.

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/penetration-testing/"
title="Get started with Fluid Attacks' Penetration Testing solution right now"
/>
</div>

## Memory-safe languages to the rescue

The issues mentioned above can be prevented to a significant extent
by using memory safe programming languages.
They manage memory automatically
(i.e., do not rely on the developers adding memory protections).
Some memory-safe languages are Go, Java, JavaScript, Kotlin, Python and Rust.
Whereas C, C++ and assembly are among the languages that lack memory safety.
When using the latter languages,
the security measures that need to be taken increase code size
and negatively affect memory and performance.
These measures [include](https://security.googleblog.com/2022/12/memory-safe-languages-in-android-13.html)
"additional sandboxing, sanitizers, runtime mitigations and hardware protections."

The relationship between programming language and memory-safety issues is
what is motivating many to make the shift.
For its part, [Google has been](https://security.googleblog.com/2022/12/memory-safe-languages-in-android-13.html)
progressively integrating new code written in memory-safe languages
into the Android operating system.
In fact,
Android 13, released in 2022, is the first one
where the majority of new code is in those languages.
Remarkably,
their switch from C and C++ has coincided
with a reduction of memory-safety vulnerabilities.
Specifically,
from 2019 to 2022,
memory-safety issues went from 76% to 35% of the total detected issues.
Moreover,
this reduction has meant fewer critical severity vulnerabilities,
remotely exploitable vulnerabilities
and vulnerabilities exploited in the wild,
as most security issues with these traits are related to memory management.
Currently,
Google is one of the funders of Prossimo's initiatives
and is scaling up its own use of Rust.

The development of Rust began in 2010,
and its 1.0 version was released in 2015.
Its adoption is growing and,
as it's now plain to see,
[the language is used](https://blog.rust-lang.org/inside-rust/2022/04/04/lang-roadmap-2024.html)
in major tech companies.
Why is it so popular?
At least for Google,
apart from what we mentioned above,
it satisfies the need to have memory safety in the lower layers of the OS,
since neither Java nor Kotlin are eligible for this.
And,
for the community in general,
it has been pointed out that Rust can reduce memory usage dramatically
(an analytics startup [reported a 92% decrease](https://www.rust-lang.org/static/pdfs/Rust-Tilde-Whitepaper.pdf)
in their product's).

## A couple of challenges

To conclude,
let's mention a couple of challenges related to the switch to Rust.
The first one is that [the learning curve](https://blog.rust-lang.org/inside-rust/2022/04/04/lang-roadmap-2024.html#Theme-Flatten-the-learning-curve)
has been a discouraging factor to begin using the language.
And indeed the Rust Lang Team shares
that onboarding time is around three to six months.
They say, however,
that they "will identify and eliminate many of those patterns
and idiosyncracies [sic] that one must learn to use Rust."

The second challenge we wanted to mention is
that ransomware-as-a-service gangs (e.g., Agenda, BlackCat, Hive)
are [now writing in Rust](https://www.itpro.com/security/ransomware/368476/why-are-ransomware-gangs-pivoting-to-rust).
Since this programming language handles memory quite efficiently,
it helps ransomware remain functional.
Also,
ransomware may evade static analysis due to how new the language is.
And as it is quite complex,
it is harder to reverse engineer,
which in turn makes generating decryptors more difficult.

Malicious attackers are exploiting weaknesses constantly,
and that is why having a preventive and proactive security stance is key.
Want us to check your software for vulnerabilities while you develop?
Implement [Continuous Hacking](../../services/continuous-hacking/) today.
You can also start your [free trial](https://app.fluidattacks.com/SignUp),
which covers automated security testing.

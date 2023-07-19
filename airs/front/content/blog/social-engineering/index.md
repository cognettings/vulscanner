---
slug: social-engineering/
title: Beware of Being Played With
date: 2021-09-20
subtitle: Discover social engineers' weapons of influence
category: attacks
tags: social-engineering, cybersecurity, training, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1632164071/blog/social-engineering/cover_social-engineering.webp
alt: Photo by Marco Bianchetti on Unsplash
description: Read this post to learn the psychological tactics used in cyberattacks and what personality traits make targets more (or less) susceptible to fall for them.
keywords: Social Engineering, Weapons, Influence, Personality, Osint, Information, Cyberattack, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/BtU2LKWjAsA
---

Are you comfortable posting pictures of the town where you were born?
How about sharing a story about your first pet? Yeah? You have no
problem having the name of your elementary school on your profile or
talking in your blog about your most favorite food? No? By the way, can
you please tell us, what was your mom’s name before she was married?

The previous topics are related to some of the most common password
reset questions. When the particular answers to these questions are
readily available on the Internet, they can be easily found by a social
engineer targeting you. What happens next is that they will try to use
[phishing](../phishing/) against you to deploy
[ransomware](../ransomware/) on your computer, among other
possibilities. But you wouldn’t notice until it’s too late.

In this post, we will expand on [a previous
entry](../attacking-weakest-link/) about how social engineering works.
We’ll see why it is effective and how to prevent being scammed.

## What is social engineering?

Social engineering can be
[defined](https://www.dictionary.com/browse/social-engineering) as "a
technique that uses psychological manipulation \[…​\] to force people to
disclose private personal or corporate information, or take a particular
action." As explained in [our latest post](../thinking-like-hacker/), an
attack, ethical or not, has to be planned first with an exploration
mindset. As investigator and author [Joe Gray
says](https://nostarch.com/download/samples/PractiSocialEngine_samplechapter.pdf),
"Rarely will an effective social engineering attack happen without an
informed understanding of the target." Gray is an expert in gathering
Open Source Intelligence (OSINT), which is information taken from
publicly available sources and used in the intelligence context. Gray
[explains](https://www.youtube.com/watch?v=qIiLPLI6tNI) that
intelligence means that each piece of information is gathered on the
basis of how it furthers the investigation.

In one [talk](https://www.youtube.com/watch?v=fpIbitxescs), Gray said
that most OSINT operations start with a single piece of information: "A
business, a name, an email address, physical address, phone number, meta
data." This is further matched with social media accounts, blogs,
websites, even leaked information in password dumps. (Talking about
dumps: They may even search your garbage\! That is a thing called
[Dumpster
Diving](https://searchsecurity.techtarget.com/definition/dumpster-diving).)
While gathering OSINT of a company, Gray likes to check the Securities
and Exchange Commission (SEC) files. These files allow him to "find out
how the business is doing, find out some of the things the business has
been struggling with, or what the business is looking out for in the
future."

After extensive research, social engineers get a good idea of an
employee’s likes and dislikes and the organization’s operating
environment, organizational structure and lingo. Eventually, they come
up with a reason to talk to their target. For example, Gray tells an
anecdote about how he learned that the CEO of the company for which he
was doing ethical social engineering was retiring and that the Chief
Operating Officer (COO) would be taking over. So he set off to buy a web
domain and design a legit-looking survey website. Then, he impersonated
the COO in an email, using direct quotes from him, which he found in
sources like press releases. In this email, he asked employees to fill
in the survey, which prompted them to share sensitive information. Out
of 150 targets, he got 17 usernames, 18 passwords and 17 sets of
password-reset questions.

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/ethical-hacking/"
title="Get started with Fluid Attacks' Ethical Hacking solution right now"
/>
</div>

## Weapons of influence

Social engineers' techniques are often analyzed using the principles of
influence proposed by psychologist Robert Cialdini in his book
[*Influence: The Psychology of
Persuasion*](https://www.harpercollins.com/products/influence-new-and-expanded-robert-b-cialdini?variant=32903969996834).
Here are some brief descriptions of social engineers' actions appealing
to Cialdini’s principles and the reasons why they make people talk:

- Claiming to have the same interests as the target in order to
  increase their **likability**, for we tend to cooperate more with
  persons who share our affinities.

- Claiming that they are acting under the **authority** of the CEO, an
  expert or a specific law, which works because we tend to obey these
  people or rules.

- Asking for sensitive information after having granted the target a
  great offer in a (bogus) product, appealing to our tendency for
  **reciprocity**.

- Claiming that a target’s peer has already shared some information,
  so the target should cooperate too, because having **social proof**
  that something our peer did is appropriate, we tend to follow their
  lead.

- Claiming that there is limited time to take action, like paying a
  ransom before impending doom, forcing the target to act fast, which
  works because the **scarcity** of time makes us act more recklessly.

- Convincing the target that doing what they’re told is consistent
  with their values, which works because we are pressured daily to
  maintain **consistency** in our acts.

After earning the confidence of their target, social engineers commonly
get the info they want and may even ask victims to click on dangerous
links. Shortly after, they leave abruptly on some made-up excuse.

## Some phishes are easier to catch

You may think: "Certainly some people are more sensible than others? Not
everyone is as easily influenced?" Well, there may be some people who
are more vulnerable to some of the weapons mentioned above. A [recent
review](https://cybersecurity.springeropen.com/articles/10.1186/s42400-020-00050-w)
article, published in the journal Cybersecurity, lists some traits that
make some people easier to manipulate.

According to the review, people who are more
[agreeable](https://dictionary.apa.org/agreeableness), meaning they tend
to cooperate more, are more vulnerable to the scammer’s likability, use
of authority and social proof, and demand for reciprocity. The authors
argue that these people would be more susceptible to fall for phishing
and to share passwords. Those who are more
[conscientious](https://dictionary.apa.org/conscientiousness), meaning
they are organized and hardworking, may also fall for the use of
authority and reciprocity, and yield to the pressure to maintain
consistency. Finally, those who are more
[extraverted](https://dictionary.apa.org/extraversion) would react more
promptly to the scarcity of time.

But it is argued that some traits may protect against the influence of
social engineers. The authors suggest that
[neuroticism](https://dictionary.apa.org/neuroticism), that is, higher
proneness to experience situations as distressing, indicates lesser
vulnerability to the weapons of influence. Furthermore, they suggest
that people who are more [open to new
experiences](https://dictionary.apa.org/openness-to-experience), being
also probably more tech-savvy, are not open to being manipulated by
social engineers.

## That sounds phishy!

We already listed some tips on how to prevent social engineers' most
favorite scams [here](../attacking-weakest-link/) and
[here](../phishing/). In short, look out for generic email subjects,
awful spelling and grammar, and emails or calls prompting life or death
decisions. They are all fishy.

Let’s add to the list some of the
[tips](https://us-cert.cisa.gov/ncas/tips/ST04-014) provided by the
United States Computer Emergency Readiness Team (US-CERT):

- Check the sender’s email address. Are there misspelled words trying
  to pass for a legit company’s address?

- Do not open a link before inspecting it. Has the URL been shortened?
  Also, hover your cursor over the link. Is it awfully long? Is it a
  hot mess?

- If you are being asked to download an attachment, ask yourself if
  the request makes total sense. Remember that attackers use time
  scarcity to manipulate you.

Finally, have in mind that conducting ethical OSINT and social
engineering can help you identify what sensitive corporate data is
being, or could be, shared publicly. Then, data removal and educating
employees on how to detect scams and limit the sensitive information
they share may be the best options.

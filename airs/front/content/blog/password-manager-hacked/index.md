---
slug: password-manager-hacked/
title: Your Password Manager Was Hacked!
date: 2023-05-18
subtitle: Benefits and risks of these increasingly used programs
category: attacks
tags: credential, cybersecurity, vulnerability, hacking, cryptography
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1684451818/blog/password-manager-hacked/cover_password_manager_hacked.webp
alt: Photo by Jelleke Vanooteghem on Unsplash
description: We describe the password managers, their advantages and disadvantages, some recent security incidents, and give you some recommendations on their use.
keywords: Password Manager, Master Password, Password Vault, Multifactor Authentication, Social Engineering, Credential Stuffing, Password Cracking, Pentesting, Ethical Hacking
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/2OCh8tuNsBo
---

If someone asked you
to list from memory all the passwords or credentials
you must type in for all the applications or services you use,
do you think you could do it?
You would probably be among most people
who would say "no."
The fact is,
[some say](https://www.darkreading.com/vulnerabilities-threats/how-password-managers-can-get-hacked),
"Today,
the average person needs to remember upward of 100 passwords."
However,
it is also possible that
you are an individual with an extraordinary memory,
or that, like me,
you are pretty far from that average
because you draw on so few services,
or that, like many,
you use a small number of passwords repeatedly almost everywhere,
so your answer would be "yes."
Also,
you could give an emphatic "yes"
just because you usually have to remember only *one* password
since you use a password manager.

Having to remember only one password
for all the services you access
is undoubtedly enormously useful.
This is something that password managers have made possible.
But,
both among those who do not yet resort to them
and among those who do,
sometimes prompted by startling news on the web,
these questions often arise:
Are these services secure enough?
Are they worth using,
or are there more risks than benefits?
Before addressing these questions,
let us introduce the term "password manager"
for those unfamiliar with it.

## What is a password manager?

Password managers are applications
that allow you to create,
store and use all your passwords in an organized way
from a single place.
These programs vary in their features,
depending on the provider,
but commonly offer the following **benefits**:

- You manage a unique password,
  the master password,
  the only one you have to remember,
  being the one with which you access your "password vault,"
  where you store all your other credentials
  (e.g., passwords for websites and credit card numbers).
  This credential must generally meet minimum complexity requirements.

- They can create complicated passwords,
  i.e., long and random (completely unrelated),
  for the different online services you access.
  Therefore,
  you avoid the typical hassle of creating them on your own
  and the high risk of them repeating or following similar patterns.

- You can even stop worrying about knowing
  what each of your passwords is
  and save time
  because these programs can automatically fill in your username and password
  on the sites you need to get access.

- They use industry-standard encryption protocols
  such as AES 256-bit and XChaCha20
  to protect your data,
  making it almost impossible to decrypt.
  Decrypting this information will depend on the master password.

- They work under the zero-knowledge security principle.
  That is,
  only you,
  as the customer,
  can know the information that the password manager stores in encrypted form,
  only you,
  not even the provider,
  have the master password to unlock your password vault.
  [The information is encrypted](https://cybernews.com/best-password-managers/are-password-managers-safe/)
  before it leaves your device.

- As an additional level of security,
  they can give you the option of two-factor or multi-factor authentication
  so that when you request access,
  they send verification codes to other devices.
  They can even use biometric authentication,
  where your fingerprint or facial recognition is required
  as an addition or replacement to your master password
  to enter your password vault.

- They can remind you to change credentials regularly
  and reassess their strength or complexity.
  Some of them can even scan the dark web
  to verify if any of your passwords appear online.

Regarding the **disadvantages** of password managers,
aspects such as installation,
storage capacity, compatibility with multiple devices,
price and learning how to use them
are typically mentioned.
Nevertheless,
what interests us most here is the disadvantage in terms of security:
The risks of cybercriminals getting into the password manager you use
and losing the information stored in it.
Password managers are often attractive to criminals
because they reflect that
there is only one step to take,
a single point of failure to break,
to get into a user's password vault.

## Risks of password managers

One of the main risks lies not in the password manager itself
but in the user and their devices.
Through [social engineering techniques](../social-engineering/),
such as [phishing](../phishing/),
malicious hackers can send you to fake sites.
For example,
[it has been reported](https://www.darkreading.com/vulnerabilities-threats/how-password-managers-can-get-hacked)
that earlier this year,
some Google Ads were discovered
that redirected users to false sites of well-known password managers
such as 1Password and Bitwarden to steal their master passwords.
It has also been said that
Google found this year that Bitwarden,
Dashlane and Apple's Safari browser password manager
could "be manipulated into auto-filling passwords on untrusted pages."

Through social engineering techniques,
attackers can also manage
to infect your devices with malware.
Being the infected device where you run the password manager,
the attacker can use,
for instance,
the so-called keyloggers
—tools that record what you type in your system—
to steal your master password.
Another substantial risk is being logged into the password manager
on multiple devices,
even when it is not necessary,
and having one of them stolen.
Finally,
there is the risk of losing or forgetting your master password.
The solution here will depend on each provider.
Still,
they can give you preventive recommendations from the start,
such as keeping a printed copy of your master password in a secure place,
like a safe deposit box,
or having a family member or trusted person as a backup.
Although they may be minor,
these latter measures would also entail risks.

A problem within the password managers themselves,
for example,
is that not all of them require the user
to utilize two-factor or multi-factor authentication.
This feature,
which can save your data
if somehow an attacker has taken possession of your master password,
should not be optional.
On the other hand,
there is the risk
that the provider may not make a backup copy of your password vault
in case the server breaks down,
but it would be rare indeed.

No service on the Internet is root-and-branch secure.
Security vulnerabilities are also present and overlooked
in even the most renowned password managers.
[Recently](https://www.darkreading.com/vulnerabilities-threats/how-password-managers-can-get-hacked),
for instance,
a vulnerability identified in KeePass
allowed exporting usernames and passwords in clear text.
Therefore,
these companies must be in continuous security testing
and vulnerability remediation.
(At this point,
it should be noted that not all password managers strive for security
in the same way and with the same resources).
And,
although it is not always something that requires their intervention,
users (you) should be on the lookout for patching updates.

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/security-testing/"
title="Get started with Fluid Attacks' Security Testing solution right now"
/>
</div>

Malicious hackers are on the prowl day and night,
looking for weaknesses in systems and humans.
As is evident,
several password managers have already been hacked.
And,
though it is not something that happens very often,
here we mention some recent outstanding security incidents.

## Three recent notable incidents

**April 2021**.
For about two days,
the password manager **Passwordstate** was invaded by hackers.
Similar to the [SolarWinds case](../solarwinds-attack/),
[this was](https://techcrunch.com/2021/08/04/passwordstate-supply-chain-attack/)
a supply chain attack.
[The criminals took advantage](https://password-managers.bestreviews.net/faq/which-password-managers-have-been-hacked/)
of the software's update functionality
to deliver a DLL file to users
while upgrading to the latest version.
This file succeeded in stealing sensitive information such as usernames,
passwords and domain names
and sending it to the attackers' server.
Making matters worse,
these individuals undertook phishing attacks,
sending emails to users posing as Passwordstate,
asking them to download a remediation file for the hack.
Some customers luckily remained unaffected
because the update had to be installed manually.
Only in August of the same year,
the company released an update
to remove the troublesome software update feature.

**August 2022**.
The password manager **LastPass** [informed its customers](https://password-managers.bestreviews.net/faq/which-password-managers-have-been-hacked/)
about an incident in its development environment
that lasted about four days
and in which
part of its source code and technical information was compromised.
There was no evidence at the time
that customer data had been exposed.
It was not until November
that the company discovered that
attackers had access to sensitive information
such as usernames, email addresses, phone numbers,
billing addresses and more
(information that can be used for social engineering attacks).
In addition,
the attackers accessed AES 256-bit encrypted data
within LastPass customers' vaults.
The company confirmed that such information was safe
because of its zero-knowledge architecture.
However,
[it warned that](https://techcrunch.com/2022/12/22/lastpass-customer-password-vaults-stolen/)
hackers could resort to [brute force](../pass-cracking/)
to crack master passwords
and decrypt stolen copies of password vaults.

[It was later revealed that](https://techcrunch.com/2022/12/14/parsing-lastpass-august-data-breach-notice/)
it all started with the compromise of the account
of one of [LastPass DevOps engineers](https://www.darkreading.com/attacks-breaches/lastpass-breach-reveals-important-lessons)
on [his personal computer](https://therecord.media/lastpass-attacker-hacked-engineers-home-computer-keylogger),
which,
when it should not be so,
he was using for his work.
In detail,
the criminals exploited a vulnerability in a third-party software package
called Plex
that allowed them to perform remote code execution
and implanted a keylogger on the victim's device
to capture his credentials.
It is worth noting that
Plex was apparently only used for the employee's personal purposes
and had a patch available for the exploited vulnerability
75 versions ago!

**December 2022**.
[More than six thousand](https://techcrunch.com/2023/01/15/norton-lifelock-password-manager-data/)
**Norton LifeLock** customers
had their accounts compromised,
some of whom were using the password manager feature.
[The targets were attacked](https://password-managers.bestreviews.net/faq/which-password-managers-have-been-hacked/)
individually
as part of a "[credential stuffing](../credential-stuffing/)"
strategy
(i.e., previously exposed credentials are manipulated
to hack into accounts in other apps or services
that may use the same),
and the threat actors did not compromise Norton's systems themselves.
For two weeks or so,
the hackers undertook attacks
until the company detected the large volumes of failed logins.
From there,
it proposed resetting passwords on the affected accounts
and suggested to its users the use of two-factor authentication.
[Some customers' password vaults](https://www.darkreading.com/remote-workforce/norton-lifelock-warns-on-password-manager-account-compromises)
could have been compromised
if their master passwords were identical or similar
to their Norton account credentials.

## Conclusions and recommendations

Without a doubt,
the more password managers are used,
the more cybercriminals will try to attack and impact them.
Although we know that
every online product or service brings cybersecurity risks,
it seems that using password managers has more advantages than disadvantages.
You and your company,
for example,
with a good password manager,
can mitigate [two significant risks](https://www.darkreading.com/vulnerabilities-threats/how-password-managers-can-get-hacked):
the use of weak credentials and password reuse.

Here are some recommendations you can take into account
when using password managers:

- As you must create a unique master password,
  your responsibility
  (hopefully suggested by the provider)
  is to make it as complex as possible.
  Of course,
  do not use this or a similar password elsewhere.

- Only enter your password manager when necessary.
  Do not leave it running on one or more devices.

- Even if the password manager does not require it,
  enable multi-factor authentication.
  This security option will only take a few seconds of your time
  whenever you log into your vault
  and will make it much more complicated for cyberattacks to succeed.

- A good provider,
  in its continuous monitoring,
  will notify you if your sensitive information may be compromised
  at any time.
  In such cases,
  as a preventive measure,
  change your master password
  and then those inside your vault.

- It is wise to keep your devices protected
  with reliable antivirus software
  and avoid following links or downloading suspicious files.

Nowadays,
some of the most recommended password managers are
[1Password](https://1password.com/),
[Keeper](https://www.keepersecurity.com/),
[NordPass](https://nordpass.com/),
[Dashlane](https://www.dashlane.com/),
and [Bitwarden](https://bitwarden.com/).
However,
if, as in my case
(obviously, for my non-work accounts),
it is not yet in your plans to use a password manager,
make sure you have your credentials written down
or printed on a piece of paper
and stored in a safe place.

P.S.
No, Mr. Goodman,
I don't keep that piece of paper under my desk lamp.

<div class="imgblock">

![Saul Goodman](https://res.cloudinary.com/fluid-attacks/image/upload/v1684451817/blog/password-manager-hacked/goodman_password_manager_hacked.webp)

<div class="title">

(Source: [NYT](https://static01.nyt.com/images/2022/08/01/arts/01saul-recap/01saul-recap-videoSixteenByNine3000.jpg).)

</div>

</div>

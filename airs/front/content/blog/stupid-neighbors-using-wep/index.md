---
slug: stupid-neighbors-using-wep/
title: Stupid Neighbors Using WEP
date: 2017-04-24
category: attacks
subtitle: Solving Yashira WEP Security challenge
tags: hacking, training, cryptography
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331104/blog/stupid-neighbors-using-wep/cover_zfucpe.webp
alt: Photo by Bernard Hermant on Unsplash
description: In this article, we explain how to crack a Wired Equivalent Privacy (WEP) algorithm by analyzing its traffic.
keywords: Security, WEP, Wifi, Password, Encryption, Network, Ethical Hacking, Pentesting
author: Juan Aguirre
writer: juanes
name: Juan Esteban Aguirre González
about1: Computer Engineer
about2: Netflix and hack.
source: https://unsplash.com/photos/X0EtNWqMnq8
---

Wi-Fi security has not always been the best. The first attempt at
securing Wi-Fi access points was termed Wired Equivalent Privacy (WEP).
WEP is a security algorithm that was implemented on IEEE 802.11 wireless
networks. The original 802.11 wireless standard was ratified in 1997 to
include this enhancement. Due to it’s many known vulnerabilities, this
encryption method has mostly been replaced by WPA (Wi-Fi Protected
Access) and WPA2 (Wi-Fi Protected Access II).

"A WEP key is a kind of security passcode for Wi-Fi devices. WEP keys
enable a group of devices on a local network to exchange encrypted
messages with each other while hiding the contents of the messages from
easy viewing by outsiders" (Mitchell, 2017). The WEP key is the
combination of a shared secret and the IV (Initialization Vector). The
IV is a short 24-bit value and it is sent in the clear text portion of
the message. The short length of the IV forces it to repeat itself.
There exist a 50% possibility that the IV will repeat itself after only
5000 packets. This is dangerous because the reuse of the same IV
produces identical key streams. This would allow an attacker to perform
a successful analytic attack. Despite the many discovered and exploited
vulnerabilities, we still see a number of access points using WEP
encryption.

I heard about some folks at yashira.org who went out on a drive on a
Wi-Fi hunt and found an access point using WEP. They quickly sniffed all
the traffic they could and have now come to us with a challenge.

## Yashira Challenge: WEP Security

In this challenge, the folks at yashira.org have come to us with the
capture file of all the traffic from the access point using WEP
encryption. Our task is to find out the WEP key.

<div class="imgblock">

![reto](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331102/blog/stupid-neighbors-using-wep/image1_rgy41c.webp)

<div class="title">

Figure 1. Challenge 182 on yashira.org

</div>

</div>

To solve this challenge we are going to be using aircrack. Aircrack is a
complete suite of tools that are used to assess Wi-Fi network security.
Aircrack is a very complete tool that has many usage options, all the
options are important, they are there for a reason. With the correct
options and data, aircrack can be used to crack any WEP key within
minutes. A complete manual on how to install and use this tool can be
found at: [Aircrack
Guide](https://www.aircrack-ng.org/doku.php?id=install_aircrack)

WEP has many vulnerabilities and before we can exploit them we should
understand how the basic authentication works. WEP’s authentication
consist of a four-step handshake. 1. The client sends an authentication
request to the access point 2. The access point responds with a clear
text challenge 3. The client encrypts the challenge text using the
configured WEP key and sends it back in another authentication request. 4.
The access point decrypts the response. If it matches the challenge
text, it sends back a positive response.

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/ethical-hacking/"
title="Get started with Fluid Attacks' Ethical Hacking solution right now"
/>
</div>

With some basic understanding of how WEP works we can start trying to
crack the key. The first thing we need to do is look at the capture file
and understand it. So let’s open a terminal on kali and run the basic
aircrack command on it $aircrack-ng redwifi.cap. This command will
attempt to decrypt the WEP key with the PTW method by default unless
specified otherwise.

<div class="imgblock">

![aircrack](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331103/blog/stupid-neighbors-using-wep/image2_kdn3u3.webp)

<div class="title">

Figure 2. aircrack-ng redwifi.cap command output

</div>

</div>

From this we see that we do not have enough IV packets to easily crack
the key, we need an other way to do this. A dictionary attack is good
but in order for it to work, we need more information.

If we had access to the network all we would need to do is listen for a
long enough period of time and then we would have enough IVs and we
would not need to perform a dictionary attack. If you are as impatient
as I am and you do not want to sit around for hours waiting to get
enough IVs, you can inject the traffic yourself. Wireless device packet
injection allows you inject ARP traffic to the access point and then,
with a sniffing tool, gather enough IV to crack the key. Since we no
longer have access to the network and we count only with the capture
file, we must try something else.

Although the previous command did not work it revealed some important
information. We now have both the ESSID and the BSSID. The ESSID
"WLAN\_1F" tells us a lot. After a couple of questions to Mr.Google we
can find that all the ESSID of type "WLAN\_XX" are automatically
generated and belong to a series of routers from Telefonica, a service
provider. Further readings on the topic and on how the ESSID is
generated reveal that the creation of the ID is based on the BSSID.
There exist a number of tools that generate WEP dictionaries for
Telefonica routers based on the BSSID and the ESSID. Wlandecrypter is
one of them. We can generate a dictionary with the following command:
$wlandecrypter \[BSSID\] \[ESSID\] wordlistdoc.lst

<div class="imgblock">

![dictionary](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331102/blog/stupid-neighbors-using-wep/image3_ifwlhe.webp)

<div class="title">

Figure 3. Generating a dictionary with wlandecrypter

</div>

</div>

Now that we have the capture file and the dictionary file we can move on
to the actual attack. We will be performing a brute force attack using a
dictionary to reduce the number of forceful key attempts. To do this we
can use the following command: $aircraack -w wordlistdoc.lst redwifi.cap

<div class="imgblock">

![cracking](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331102/blog/stupid-neighbors-using-wep/image4_anrc8t.webp)

<div class="title">

Figure 4. Cracking a WEP key with aircrack-ng and a dictionary

</div>

</div>

And there it is, we managed to successfully crack and decrypt the WEP
key.

Given some basic knowledge, WEP encryption is relatively easy to decrypt
and if the attacker has enough time to sniff a lot of traffic and obtain
a large amount of IVs then the attacker can always successfully decrypt
the key. If you are still using WEP encryption this should give you a
couple of reasons to upgrade and if for some reason there is a technical
restriction that forces you to use WEP, then here are two pieces of
advice that can help you implemented in a more secure manner. 1. You
must perform a periodic change of your keys. This will make it a lot
more difficult for an attacker to perform a successful brute force
attack on your network. 2. Use encrypted tunneling protocols which can
provide secure data transmission over an insecure network. Such protocol
include but are not limited to: a. IPSec b. Secure Shell

## References

1. [Mitchell, B. What is a WEP Key? Retrieved
    April 24, 2017](https://www.lifewire.com/what-is-a-wep-key-818305)

## Challenge Link

[Yashira WEP
Security](http://www.yashira.org/index.php?mode=Retos&resp=inforeto&level=182)

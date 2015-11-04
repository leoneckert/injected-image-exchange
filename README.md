# injected-image-exchange

Injected Image Exchange is a project that builds upon the amazing mitmproxy (https://github.com/mitmproxy/mitmproxy).

The project came to life as part of Adam Harvey's 'Stratosphere of Surveillance' class at ITP, NYU. 

---
useful tutorial, references and inspirational projects:

most importantly and a thousand thanks to mitmproxy: https://github.com/mitmproxy/mitmproxy

setting up a raspberry pi as a router as seen in this adafruit tutorial: https://learn.adafruit.com/downloads/pdf/setting-up-a-raspberry-pi-as-a-wifi-access-point.pdf

Working with a Raspberry Pi for network attacks by Jesse Lauwers : http://jesselauwers.github.io/Raspberry-Pi-Kali-MITM/

setting up a man in the middle browser by Jeffrey Quesnelle: http://jeffq.com/blog/setting-up-a-man-in-the-middle-device-with-raspberry-pi-part-1/

Men in Grey by the Critical Engineering Working Group: https://criticalengineering.org/projects/men-in-grey/
Newstweek by Julian Oliver and Daniil Vasiliev: http://newstweek.com
Honeypot Router by Peter B Marks : http://blog.marxy.org/2013/08/reverse-engineering-network-traffic.html

---

It consists of a Raspberry Pi turned router, connected to a 'real' network via Ethernet and visible to other devices via a Wifi Dongle. On the Pi/the router the mitmproxey (to be found here: https://github.com/mitmproxy/mitmproxy) is installed and crucial part to the project. Mitmproxy allows to scan all traffic passing through the router, inspect the http requets, manipulate them, retrieving information from the internet, and return a request back to the original client. 

*image exchange (main script)
At 'manipulating them' is where this project intervenes through two python scripts. One script (exchange_imgs.py)is specified to catch requests for images that match a certain resolution criteria and stores them in
a dictionary together with the ip address of the client who sent the request.
In the response, a randomly chosen image, originally requested by another client on the network, is re- turned, and then deleted from the dictionary.
In practice, the images on the site you visit, will be swapped with other images from other clients’ browsing and vice versa. 

*admin monitor
The project includes an “admin” monitor showing all the images that are stored in the dictionary at any given time. The main script constantly updated a csv file with all the image urls that are currently "up for grab"/ have not yet been returned to users. A second script (redirect_admin.py) runs, when a client visits "openwifi.com" (openwifi is the name of the network) on which it hosts the list of url. The admin then opens the html file (admin_page.html) locally which pulls the url from openwifi.com and presents them on a "admin page". This feature is meant for installation purposes, but also has other uses we want to explore in the future. 

The image exchange, as of now, only works for http requests. Here are some sites we tried mostly or were surprised by the fact they are working during sessions:

nytimes.com
economist.com
...most news sites
instagram (in the phone app)
spotify (on the phone, exchanges album covers)
...


----

Injected Image Exchange (IIE) is meant to provoke questions. We envision participants to connect to the router, knowing what it does, but expect them not to keep that in mind at all times while browsing.
Oftentimes, the effects of the image injections are subtle, only shifting the meaning of news headlines and comments ever so slightly. At other times, changes are more obvious and extreme or show private images one is clearly not meant to see - however the realisation lies near that it is a trade-off: if I see other people’s data instead of mine, I am giving my data away at the same time, not knowing to whom.
How does this alter a user’s behaviour? And how quickly do they forget that they are being surveilled? In how far is IIE different from every other router? Which gates does our re- quests and information pass before we get a response?

----

things to explore in the future:

- testing in scnenarios with many users, not knowing each other and browsing on the network for a longer period.
- experimenting with different accesabilty for the admin view (one person can access, everyone can etc.)




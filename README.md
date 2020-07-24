# SteamUI-OldGlory
A set of tweaks to the Steam UI, and also a reference, so you can learn to make your own tweaks. Check `/dev` branch for in-progress tweaks

## Quick Usage
Install SteamFriendsPatcher (https://github.com/PhantomGamers/SteamFriendsPatcher/releases) \
After running it and patching, you should find `libraryroot.custom.css` file in `Steam/steamui`.\
Replace it with the `libraryroot.custom.css` here on this repository.\
To debug the Steam Library yourself, run Steam with the ` -dev` tag.\
Create a shortcut to `Steam` -> `Right Click` -> `Properties`. In `Target`, after `Steam.exe"` add `  -dev`

## Long Story Short

In Oct 2019, Valve pushed out the new Steam UI update. Needless to say, many people hated it. There is so much wasted space and usability issues that I reverted right back to the old UI. This worked for about 7 months, until in June 2020, Valve changed something in how Steam packages are handled that broke the old UI. For me, I could no longer see the client after log in. So since then I've moved to the new UI, but got to work on CSS modifications right away.

This Steam Discussions thread became my main way of communicating my progress on tweaking the new Steam UI to make it less terrible. https://steamcommunity.com/discussions/forum/0/2451595019863406679/
There are a lot of instructions and tips there, such as accessing the Developer Tools (*Ctrl+ Shift+I*) which is important to be able to debug your way around the Steam UI.

## CSS Tweaking Commence

After a week, I would say I had made considerable improvements in a "first phase" of tweaks.
The main differences/upgrades between the vanilla new UI and mine were:

- Made the left sidebar display more games like the old UI did
- Condense Home/Categories/Recent Activity/Ready to Play/Search Bar down to 2 rows
- remove lots of padding everywhere
- on the game page, swapped the columns around so Friends who play/Achievements/Trading Cards/DLC/Screenshots gets more space
- Increased the opacity of the white text for Last Played, Play Time, Achievements...

https://gyazo.com/aa37f6846e6771ecbc51f08808b93864

Two of my biggest gripes: the left sidebar not being compact enough, and the Friends Activity with padding taking up way too much space on the game page, were now tweaked.

My third gripe was many of my games had those portrait game images with the horrid blurry background in them. I searched up this https://github.com/wynick27/steam-missing-covers-downloader, contributed my own fix, as it had been broken due to the same package changes that broke the old UI, and boom! I was able to import 235 images for myself. You can have a look there and also on my fork (as I compiled an .exe if you are unwilling to install Python)

So, the main css file: `libraryroot.custom.css`. It is designed to be used with SteamFriendsPatcher (https://github.com/PhantomGamers/SteamFriendsPatcher). Download and open the program up, after it patches, you should find a `libraryroot.custom.css` file in `Steam/steamui`. Replace the file with the one here on the repository. 

## Can you do JavaScript Tweaks?

So, back to more tweaking. CSS can do a lot of cosmetic tweaks, but it has its limits. I understood CSS enough (some good ol' brute-force Google searching helps), but when it came to JavaScript, the minified JS files were a solid obstacle and I felt I had no idea how to decipher it to make tweaks.

But eventually, I've figured out enough to make JS + CSS tweaks (https://imgur.com/a/mL4QNYB) enabling landscape game images - like in the Grid view the old UI had (https://imgur.com/a/qcIHx0l), and wrote a Python script to automate changing any JS. Now, the script is still not user-consumer-friendly-ready, but a quick glance at the code and you'll see that it finds and replaces certain strings in the JavaScript. If you want to add any tweaks of your own, the variable `fixes_dict` is where to put them. Of course, I could just make it so that it reads your tweaks from an external file, but that's not essential for now. Just run `js_parser.py` to apply the JavaScript tweaks. Additionally, there is a limitation that the script only reads one line at a time, so you cannot use multiple lines as your search criteria to "find and replace", at the moment.

I have been able to increase the number of screenshots it shows on a game's page from 4 to 8. Tried to get it to generate 9, but was unable to find the specific variable (it generates an array of 8 screenshots by default). Also increased the number of DLC visible to 12 - the JS generates an array of 23! They are just not displayed on the page. https://imgur.com/a/3WTdrXP

There are a few niggling minor bugs as a result of all this tweaking. See if you can find them. But for the most part, it's been a much more usable experience for me already.

Here is a proof of concept of recreating the List view: https://imgur.com/a/ZqvqrkR
## Long Story Short

In Oct 2019, Valve pushed out the new Steam UI update. Needless to say, many people hated it. There is so much wasted space and usability issues that I reverted right back to the old UI. This worked for about 7 months, until in June 2020, Valve changed something in how Steam packages are handled that broke the old UI. For me, I could no longer see the client after log in. So since then I've moved to the new UI, but got to work on CSS modifications right away.

This Steam Discussions thread became my main way of communicating my progress on tweaking the new Steam UI to make it less terrible. https://steamcommunity.com/discussions/forum/0/2451595019863406679/
There are a lot of instructions and tips there, such as accessing the Developer Tools (*Ctrl+Shift+I*) which is important to be able to debug your way around the Steam UI.

## CSS Tweaking Commence

After a week, I would say I had made considerable improvements in a "first phase" of tweaks.
The main differences/upgrades between the vanilla new UI and mine were:

- Made the left sidebar display more games like the old UI did
- Condense Home/Categories/Recent Activity/Ready to Play/Search Bar down to 2 rows
- remove lots of padding everywhere
- on the game page, swapped the columns around so Friends who play/Achievements/Trading Cards/DLC/Screenshots gets more space
- Increased the opacity of the white text for Last Played, Play Time, Achievements...

https://gyazo.com/aa37f6846e6771ecbc51f08808b93864

## Missing/Blurred Game Images

Many of my games had those portrait game images with the horrid blurry background in them. I searched up this https://github.com/wynick27/steam-missing-covers-downloader, contributed my own fix, as it had been broken due to the same package changes that broke the old UI, and boom! I was able to import 235 images for myself. For a compiled .exe, look here: https://github.com/Jonius7/steam-missing-covers-downloader/releases/tag/new-format-fix

So, about the main css file: `libraryroot.custom.css`. It is designed to be used with SteamFriendsPatcher (https://github.com/PhantomGamers/SteamFriendsPatcher). Download and open the program up, after it patches, you should find a `libraryroot.custom.css` file in `Steam/steamui`. Replace the file with the one here on the repository. 

## Can you do JavaScript Tweaks?

CSS can do a lot of cosmetic tweaks, but it has its limits. I understood CSS enough (some good ol' brute-force Google searching helps), but when it came to JavaScript, the minified JS files were a solid obstacle and I felt I had no idea how to decipher it to make tweaks.

But eventually, I've figured out enough to enable landscape game images (https://imgur.com/a/mL4QNYB) - like in the Grid view the old UI had (https://imgur.com/a/qcIHx0l), and wrote a Python script to automate changing any JS. A quick glance at the code and you'll see that it finds and replaces certain strings in the JavaScript. If you want to add any tweaks of your own, edit the file `fixes.txt`. Just run `js_tweaker.py` to apply the JavaScript tweaks. 

the JS goes through this process:

- `libraryroot.js` - original file
- `libraryroot.beaut.js` - beautified js using `jsbeautifier`
- `libraryroot.modif.js` - beautified js with modified tweaks from `fixes.txt`
- `libraryreet.js` - minified `libraryroot.modif.js` using `jsmin`

There is a limitation that the script only reads from `libraryroot.beaut.js` one line at a time, so you cannot use multiple lines as your search criteria to "find and replace", at the moment.

`js_tweaker` will use `libraryroot.beaut.js` if it already exists. This means:

- you can experiment in `libraryroot.modif.js` and delete it afterwards if you want to go back to the clean version `libraryroot.beaut.js`

I have been able to increase the number of screenshots it shows on a game's page from 4 to 8. Tried to get it to generate 9, but was unable to find the specific variable (it generates an array of 8 screenshots by default). Also increased the number of DLC visible to 12 - the JS generates an array of 23! They are just not displayed on the page. https://imgur.com/a/3WTdrXP

There are a few niggling minor bugs as a result of all this tweaking. See if you can find them. But for the most part, it's been a much more usable experience for me already.

Additionally, here is a proof of concept of recreating the List view: https://imgur.com/a/ZqvqrkR
# SteamUI-OldGlory

A set of tweaks to the Steam UI, and also a reference, so you can learn to make your own tweaks. Check `/dev` branch for in-progress tweaks \
![Alt Text](https://media.giphy.com/media/ehn6NIV3ZzVWaLyiDv/giphy.gif)

[<img src="https://i.imgur.com/2TZn4ET.png" alt="Video Guide to Tweaking the Steam Library"/>](https://www.youtube.com/watch?v=7_3e9j8FFv8)

<details>
    <summary><h3>Showcase of Tweaks</h3></summary><br>
    Condensed sidebar buttons <br>
    <img src="https://i.imgur.com/YDCDMD1.png" alt="img" style="zoom: 40%;" /> <br><br>
    Show more games <br>
    <img src="https://i.imgur.com/c0AJnsn.png" alt="Show more games" style="zoom: 55%;" /> <br><br>
    Fix blurred images <br>
    <img src="https://media.giphy.com/media/YIKhhaK166Iynrcer8/giphy.gif" alt="Fix blurred images" style="zoom: 100%;" /> <br><br>
    Improved game page layout <br>
    <img src="https://i.imgur.com/7UvT6OX.png" alt="Fix blurred images" style="zoom: 50%;" /> <br><br>
    Show more DLC and screenshots <br>
    <img src="https://media.giphy.com/media/cbPuBtJ1ez2v55SptR/giphy.gif" alt="Show more DLC" style="zoom:80%;" /> <br><br>
    Play bar moved up into box <br>
    <img src="https://i.imgur.com/HrgBUPl.png" alt="Play bar moved up into box" style="zoom:80%;"

​    

 



</details>





## Quick Usage

#### Patching and CSS

- Install **_SteamFriendsPatcher_**: (https://github.com/PhantomGamers/SteamFriendsPatcher/releases)
- After running it and patching, you should find `libraryroot.custom.css` file in `Steam/steamui`.
- Replace it with **_SteamUI-OldGlory's_** `libraryroot.custom.css`.
- Latest Release: (https://github.com/Jonius7/SteamUI-OldGlory/releases/latest)

#### JavaScript Tweaks

The file for modifying JavaScript, `js_tweaker.py` is a [Python](https://www.python.org/downloads/ "Python Downloads Page") script. \
The file that contains the list of JavaScript tweaks is `fixes.txt`.\
Each line contains one tweak with the original JS separated by two spaces from the tweaked JS: 

[original js]&#9608;&#9608;[new js] 

Required libraries: `jsbeautifier`, `jsmin`.

- Run `pip install jsbeautifier` and `pip install jsmin` from the command-line.

- Copy `js_tweaker.py` and `fixes.txt` to `Steam/steamui` and run it.

#### Fix Blurred Game Images

[Steam Missing Covers Downloader](https://github.com/Jonius7/steam-missing-covers-downloader/releases/tag/new-format-fix)



## Quick Links

- [Video Guide](https://www.youtube.com/watch?v=7_3e9j8FFv8)
- [GIF of tweaks](https://gyazo.com/38d0101b493741501697b4a0f5f0818f)
- [More DLC and Screenshots, more info!](https://imgur.com/a/3WTdrXP)
- [JS Tweaks](https://imgur.com/a/mL4QNYB)
- [Is Steam Grid View Back?](https://imgur.com/gallery/qcIHx0l)
- [Steam List View Proof of Concept](https://imgur.com/a/ZqvqrkR)
- [Steam Discussions](https://steamcommunity.com/discussions/forum/0/2451595019863406679/)



## What's New?

#### Release 3

New CSS for:

- Play Button Box
- Vertical Nav Bar (BETA)
- Classic Layout (BETA)

New Configurable variables at top of CSS file

BETA CSS is functionally working, but may require some manual uncommenting in the CSS and JS

- Update compatibility with [steam-library](https://github.com/AikoMidori/steam-library)

rework [`README.md`](README.md)

- moved long exploratory story to [docs/story.md](docs/story.md)
  moved [CSS changelog](docs/CSS%20changelog.md) to its own file

[`js_tweaker`](js_tweaker) now accepts blank lines for [`fixes.txt`](fixes.txt) readability
added explanatory comments for each group of tweaks in [`fixes.txt`](fixes.txt)



## steam-library Support

https://github.com/AikoMidori/steam-library
**SteamUI-OldGlory** mostly works with Shiina's **steam-library** CSS skin by simply copying the code in **steam-library's** `libraryroot.custom.css` and pasting it above **SteamUI-OldGlory's** `libraryroot.custom.css` code. 

However, I have provided a compatibility CSS file and batch file to hopefully streamline the process.

In layman's terms:

- copy and paste into `Steam/steamui` from **SteamUI-OldGlory**: 
  - `libraryroot.custom.css`
  - `steam-library_compat.css` 
  - `steam-library_compat.bat` 
- copy and paste into `Steam/steamui` from **steam-library**:
  - `config.css` 
- run `steam-library_compat.bat`. It will prompt you asking you to confirm. Type Y and press Enter.
- a backup of your `libraryroot.custom.css` will be made at `libraryroot.custom.css.backup`
- Reload the Steam Library (either End Task on Steam Client WebHelper or trigger reload of `Steam/steamui` folder)

You should be set to go!

![preview image](https://i.imgur.com/4gWzhj9.png)

## Dev Notes

#### For more details, go to [Story](docs/story.md).

#### [CSS Changelog](docs/CSS%20Changelog.md)

#### Debugging Steam Library Yourself

To debug the Steam Library yourself, run Steam with the ` -dev` tag.

- Create a shortcut to `Steam` -> `Right Click` -> `Properties`.
- In `Target`, after `Steam.exe"` add `  -dev` so the end of Target looks like this: `Steam.exe" -dev`
- After opening Steam, open up the Dev Tools by clicking in the library window and pressing `Ctrl + Shift + I`

#### Build `js_tweaker.exe`

`pyinstaller --hidden-import six --onefile js_tweaker.py`
The `.spec` file is included for redundancy's sake.

#### What does `js_tweaker` do?

the JS goes through this process:

- `libraryroot.js` - original file
- `libraryroot.beaut.js` - beautified js using `jsbeautifier`
- `libraryroot.modif.js` - beautified js with modified tweaks from `fixes.txt`
- `libraryreet.js` - minified `libraryroot.modif.js` using `jsmin`

Limitation that the script only reads from `libraryroot.beaut.js` one line at a time, so you cannot use multiple lines as your search criteria to "find and replace", at the moment.

`js_tweaker` will use `libraryroot.beaut.js` if it already exists. This means:

- you can experiment in `libraryroot.modif.js` and delete it afterwards if you want to go back to the clean version `libraryroot.beaut.js`

​    https://i.gyazo.com/426eeaa53affa5b6b1521d27c9a7eede.gif
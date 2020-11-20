# SteamUI-OldGlory

A set of tweaks to the Steam UI, and also a reference, so you can learn to make your own tweaks. Check `/dev` branch for in-progress tweaks.

#### [Download Latest Version](https://github.com/Jonius7/SteamUI-OldGlory/releases/latest)

### Video Guide and GIF

<img src="https://media.giphy.com/media/ehn6NIV3ZzVWaLyiDv/giphy.gif" alt="Alt Text" style="zoom:95%;" />

[<img src="https://i.imgur.com/2TZn4ET.png" alt="Video Guide to Tweaking the Steam Library"/>](https://www.youtube.com/watch?v=7_3e9j8FFv8)

### Showcase of Tweaks

<details><summary>(click to expand)</summary><br>
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
    <img src="https://i.imgur.com/HrgBUPl.png" alt="Play bar moved up into box" style="zoom:80%;" />
</details>



## Quick Usage

#### Patching and CSS

- Install [**SteamFriendsPatcher**](https://github.com/PhantomGamers/SteamFriendsPatcher/releases). Run it, it will patch some files.
- Download [**SteamUI-OldGlory**](https://github.com/Jonius7/SteamUI-OldGlory/releases) and copy `libraryroot.custom.css` over to `Steam/steamui`.

#### JavaScript Tweaks

For running `js_tweaker.exe`: 

- Copy `js_tweaker.exe` and `fixes.txt` to `Steam/steamui` and run it. 

For running `js_tweaker.py` (requires [Python](https://www.python.org/downloads/ "Python Downloads Page")): 

- Run `pip install jsbeautifier` and `pip install jsmin` from the command-line.

- Copy `js_tweaker.py` and `fixes.txt` to `Steam/steamui` and run it.

`fixes.txt`  contains the list of JavaScript tweaks.\
Each tweak is under its own *Section Heading* marked with the line starting `###`.\
Tweaked lines are the original JS separated by two spaces from the tweaked JS:\
[original js]&#9608;&#9608;[new js]\
Some tweaks are disabled by default. Remove the `###` for each line under the *Section Heading* to enable.\
Commented lines with `###`, and blank lines are ignored. You can use this to make `fixes.txt` more readable.

#### Fix Blurred Game Images

- Download [Steam Missing Covers Downloader](https://github.com/Jonius7/steam-missing-covers-downloader/releases/tag/new-format-fix) and run `missing_cover_downloader`

## Quick Links

- [Video Guide](https://www.youtube.com/watch?v=7_3e9j8FFv8)
- [SteamUI-OldGlory Wiki](https://github.com/Jonius7/SteamUI-OldGlory/wiki)
- [GIF of tweaks](https://gyazo.com/38d0101b493741501697b4a0f5f0818f)
- [(Images) More DLC and Screenshots, more info!](https://imgur.com/a/3WTdrXP)
- [(Images) JS Tweaks](https://imgur.com/a/mL4QNYB)
- [(Images) Is Steam Grid View Back?](https://imgur.com/gallery/qcIHx0l)
- [(Images) Steam List View Proof of Concept](https://imgur.com/a/ZqvqrkR)
- [Steam Discussions](https://steamcommunity.com/discussions/forum/0/2451595019863406679/)



## What's New?
>
>#### Release 3.2.2
>
>- Fixed `steam-library_compat.bat` sometimes duplicating `libraryroot.custom.css` code
>
>- Extra fixes in `fixes.txt` - disable the What's New shelf from loading in the background
>
>#### Release 3.2
>
>- Fixes to CSS and JS tweaks to work with Steam Client Oct 8 update.
>- Delete `libraryroot.beaut.js` from directory, and run `js_tweaker` to apply JS tweaks to the > new version.
>
>#### Release 3.1
>
>- Quick update to custom CSS, cleaner glass effect
>
>- CSS Hotfixes
>
>#### Release 3
>
>New CSS for:
>
>- Play Button Box (BETA)
>- Vertical Nav Bar (BETA)
>- Classic Layout (BETA)
>
>New *configurable variables* at top of CSS file
>
>BETA CSS is functionally working, but may require some manual uncommenting in the CSS and JS
>
>[`js_tweaker`](https://github.com/Jonius7/SteamUI-OldGlory/blob/Release_3/js_tweaker) and [`fixes.txt`](https://github.com/Jonius7/SteamUI-OldGlory/blob/Release_3/fixes.txt) reworked for readability
>
>
>
>[More details...](https://github.com/Jonius7/SteamUI-OldGlory/releases)


## steam-library Support

https://github.com/AikoMidori/steam-library
To use Shiina's **steam-library** CSS skin with **SteamUI-OldGlory**:

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

If you want to remove **steam-library's** changes, go into `libraryroot.custom.css` and delete the top lines up to and including `/* === END steam-library tweaks for SteamUI-OldGlory === */`

## Dev Notes

#### For more details, go to [Story](docs/story.md).

#### [CSS Changelog](docs/CSS%20Changelog.md)

#### [SteamUI-OldGlory Wiki](https://github.com/Jonius7/SteamUI-OldGlory/wiki)

#### Debugging Steam Library Yourself

To debug the Steam Library yourself, run Steam with the ` -dev` tag.

- Create a shortcut to `Steam` -> `Right Click` -> `Properties`.
- In `Target`, after `Steam.exe"` add `  -dev` so the end of Target looks like this: `Steam.exe" -dev`
- After opening Steam, open up the Dev Tools by clicking in the library window and pressing `Ctrl + Shift + I`

#### Build `js_tweaker.exe`

`pyinstaller --hidden-import six --onefile js_tweaker.py`
The `.spec` file is included for redundancy's sake.

Sometimes you may need to install `pyinstaller` like this: [Windows Compilers](https://wiki.python.org/moin/WindowsCompilers#Which_Microsoft_Visual_C.2B-.2B-_compiler_to_use_with_a_specific_Python_version_.3F)

This is mainly for me to try and get an `.exe` that doesn't trigger false positives on [virustotal.com](virustotal.com)

#### What does `js_tweaker` do?

the JS goes through this process:

- `libraryroot.js` - original file
- `libraryroot.beaut.js` - beautified js using `jsbeautifier`
- `libraryroot.modif.js` - beautified js with modified tweaks from `fixes.txt`
- `libraryreet.js` - minified `libraryroot.modif.js` using `jsmin`

Limitation that the script only reads from `libraryroot.beaut.js` one line at a time, so you cannot use multiple lines as your search criteria to "find and replace", at the moment.

`js_tweaker` will use `libraryroot.beaut.js` if it already exists. This means:

- you can experiment in `libraryroot.modif.js` and delete it afterwards if you want to go back to the clean version `libraryroot.beaut.js

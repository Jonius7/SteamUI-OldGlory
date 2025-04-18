<h1 align="center">SteamUI-OldGlory</h1>

<p align="center">A set of customisable <b>Steam Library tweaks</b>, with an <b>installer</b>.</br>Also <b>a reference</b> that you can use to learn how to make your own tweaks.</p>

<p align="center">
	<a href="https://github.com/Jonius7/SteamUI-OldGlory/releases"><img alt="GitHub all releases downloads" src="https://img.shields.io/github/downloads/Jonius7/SteamUI-OldGlory/total"></a>
	<a href="https://github.com/Jonius7/SteamUI-OldGlory/stargazers"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Jonius7/SteamUI-OldGlory?color=dda113"></a>
    <a href="https://github.com/Jonius7/SteamUI-OldGlory/releases/latest"><img alt="GitHub latest release version" src="https://img.shields.io/github/v/release/Jonius7/SteamUi-OldGlory?display_name=release"></a>
	<a href="https://github.com/Jonius7/SteamUI-OldGlory/issues?q="><img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed-raw/Jonius7/SteamUI-OldGlory?color=c733c3&label=issues%20solved"></a>
    <a href="https://github.com/Jonius7/SteamUI-OldGlory/tree/master"><img alt="Lines of code in project" src="https://img.shields.io/endpoint?url=https://ghloc.vercel.app/api/Jonius7/SteamUI-OldGlory/badge?filter=.py$,.scss$,.rs$,.json$&style=flat&logoColor=white&label=Lines%20of%20Code"></a>
    <a href="https://github.com/Jonius7/SteamUI-OldGlory/commits/dev"><img alt="GitHub commits on /dev since last merge" src="https://img.shields.io/github/commits-since/Jonius7/SteamUI-OldGlory/latest/dev?label=commits%20since"></a>
</p>




<h3 align="center"><a href="https://github.com/Jonius7/SteamUI-OldGlory/releases/latest">Download Latest Version</a> | <a href="https://github.com/Jonius7/SteamUI-OldGlory#quick-guide">Quick Guide</a> | <a href="https://github.com/Jonius7/SteamUI-OldGlory/wiki">Wiki</a> | <a href="https://github.com/Jonius7/SteamUI-OldGlory/issues/56">Known Issues</a> | <a href="https://github.com/Jonius7/SteamUI-OldGlory#troubleshooting">Troubleshooting</a> | <a href="https://discord.gg/hScVrvxJWy">Discord</a></h3>

<p align="center">Check <a href="https://github.com/Jonius7/SteamUI-OldGlory/tree/dev"><code>/dev</code></a> branch for in-progress tweaks.</p>

## Video Guide and GIF

<img src="https://media.giphy.com/media/OjD2H5dci42cYRVvWN/source.gif" alt="Alt Text" style="zoom:95%;" /> 

[<img src="https://i.imgur.com/FYDDWVW.png" alt="Video Guide to Customising The Steam Library"/>](https://youtu.be/foCewvyOszQ)

<p align="left"><a href="https://youtu.be/foCewvyOszQ"><img alt="YouTube Video Views" src="https://img.shields.io/youtube/views/foCewvyOszQ?style=social"></a></p>

## Showcase of Tweaks

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
    <img src="https://i.imgur.com/HrgBUPl.png" alt="Play bar moved up into box" style="zoom:80%;" /> <br><br>
    Classic Layout <br>
    <img src="https://i.imgur.com/7FPUtlP.png" alt="Classic Layout" style="zoom:80%;" />
</details>


## Quick Guide
### Using SFP (SteamFriendsPatcher)
- Install [**SFP (SteamFriendsPatcher)**](https://github.com/PhantomGamers/SFP/releases). Run it, it will patch some files.

- Download [**SteamUI-OldGlory**](https://github.com/Jonius7/SteamUI-OldGlory/releases). Extract the files to a folder, and run `old_glory.exe`

- Select the options you want to use, then click **Install**.

- In **SFP**, click the **Settings** icon in the bottom left, select the **Steam** -> **Steam skin** dropdown and choose **OldGlory**.
  

### Using Millennium Patcher

- Install [**Millennium**](https://github.com/SteamClientHomebrew/Millennium).

- Download [**SteamUI-OldGlory**](https://github.com/Jonius7/SteamUI-OldGlory/releases). Extract the files to a folder, and run `old_glory.exe`

- Select the options you want to use, then click **Install**.

- Open up Steam, go to **Steam** -> **Millennium** -> **Themes** -> **Client Theme**, click on the dropdown and select **OldGlory**.

- You can continue to customise your options in the SteamUI-OldGlory Installer, click **Install** and Steam should update accordingly.


### Using SteamUI-OldGlory standalone (old method)

SteamUI-OldGlory supports patching the CSS directly however it only covers patching the main window (not friends list, store page or Big Picture)

- In the SteamUI-OldGlory Installer under **Advanced Options** -> **Patching** you can use the **Patch CSS** option. Change the **Install Location** from **SFP/Millennium** to **steamui**
- If you decide to use SFP/Millennium in the future you can use the **Unpatch CSS** option and Change the **Install Location** back to **SFP/Millennium**

### Fix Blurry Portrait Game Images

- To fix all your blurry portrait game images, use this build of [**Steam Missing Covers Downloader**](https://github.com/Jonius7/steam-missing-covers-downloader/releases/latest).



## More Info

### Other Config

- [If using Shiina's steam-library theme](https://i.imgur.com/1cSW7iI.png), click **Apply config.css** under **Advanced Options**

### SteamUI-OldGlory Updates

- SteamUI-OldGlory will do an update check upon startup and link you to the Github page to download a new release if available.
- For smaller updates SteamUI-OldGlory should prompt you to download new files when they are released.

## Customising CSS

##### Enable/Disable CSS modules and features

Since version 5.11, OldGlory can enable/disable individual CSS modules and features via **CSS Options -> CSS Sections**. 

##### [version < 5.11] **Manual Editing** (CSS/SCSS)

- **[OLD HOW TO: Enable/Disable CSS modules and features manually](https://imgur.com/a/PocNfPE)**

<details><summary>More details</summary>
<ul>   
<li><tt>variables.css</tt>  contains a list of CSS variables that tweak certain parts of the Library.</li>
  <li>Most of these can be configured using the GUI, but there are additional options here you can set manually.</li>
  <li>If you manually edit the file, use the <b>Reload Config</b> button to load them into the Installer. </li><br>
<li><tt>scss/libraryroot.custom.scss</tt> contains the <tt>@imports</tt> for each of the CSS "modules", that each cover a different part of the Steam library.</li>
    <li>You can enable and disable certain modules by adding <tt>// </tt> to the beginning of the line</li>
    <li>Click <b>Install</b> in the Configurer to apply your changes.</li>
</ul>
</details>

<img src="https://media.giphy.com/media/5ZiZcGpMvRyEdOliSk/giphy.gif" alt="GUI Images" style="zoom:95%;" />

## OldGlory Installer (GUI)

#### [Installer GUI Details](docs/Installer%20GUI%20Details.md)

## Included files:

- `old_glory.exe` - App to apply **SteamUI-OldGlory's** tweaks
- `variables.css` - CSS variables to customise
- `fixes.txt` - JS tweaks
- `libraryroot.custom.css` - output CSS file. Do not edit this directly, use the `\scss` folder files and **Compile CSS** button
- `skin.json` - JSON file for compatibility with Millennium
- `README.md` - this file
- `\scss` - (New in Release 5.0)
  - `libraryroot.custom.scss` - contains all the `@imports` for smaller `.scss` files. The GUI handles enabling/disabling `_module_playbarbox`, `_module_verticalnavbar`, `_module_landscapegameimages`, `_module_classiclayout`, `_classic`, `_module_homeicon`. 
  - `_custom_module1.scss`- put your custom CSS code here
  - `_custom_module2.scss` - put your custom CSS code here

- `\themes` - Folder containing theme files
  - Each theme gets its own folder containing:
  - `libraryroot.custom.css` - the CSS file for the theme
  - `preview.png` - the preview image for the theme

- Themes include:
  -  **Shiina's** [steam-library](https://github.com/AikoMidori/steam-library) dark theme
  - **Thespikedballofdoom's** [Dark Library](https://gamebanana.com/guis/35092) theme
  - **FatheredPuma81's** Full Dark Mode theme
  -  Theme based on **EliteSkylu's** [Acrylic Steam](https://www.reddit.com/r/Steam/comments/jot6vi/let_me_introduce_you_a_project_of_my_steam_ui/) concept
  -  Crisp Cut by **Jonius7**, emphasising white app section boxes
  -  Pure [Light] theme by **Snudgee**
  -  [OG-Steam-Library](https://github.com/ungstein/OG-Steam-Library) Theme, by **ungstein**
  
- `old_glory_data.json` data for `old_glory.exe`. Editing it is not required but it allows some data to be updated/hotfixed outside of having to rebuild the `.exe`

Other files are copied from the`Steam\steamui` directory as required.

`config.css` for Shiina's steam-library theme will be created from `config.css.original` the first time you enable the theme. Alternatively, you can put your existing `config.css` file here and the app will use it.

#### JavaScript Tweaks

Some tweaks are disabled by default. Under **JS Options**, you can select which options to enable/disable.

##### **Manual Editing** (JS - fixes.txt)

<details><summary>More details</summary>
<ul>   
<li><tt>fixes.txt</tt>  contains the list of JavaScript tweaks.</li>
<li>Each tweak is under its own <b>Section Heading</b> marked with the line starting <tt>###</tt>.</li>
    <li>Tweaked lines are the original JS separated by <b>two spaces</b> from the tweaked JS:</li>
<li><tt>[original js]&#9608;&#9608;[tweaked js]</tt></li>
<li>Remove the <tt>###</tt> for each line under the Section Heading to enable.</li>
<li>When <tt>old_glory</tt> applies the JS tweaks, commented lines with <tt>###</tt>, and blank lines are ignored. You can use this to make <tt>fixes.txt</tt> more readable.</li>
    <li>NEW (Release 5.5): You can now use the previous line of JS to search for the line you want. Just separate the two lines with <tt>~~</tt></li>
    <ul><li>Format: <tt>[previous line JS]~~[original JS]&#9608;&#9608;[tweaked JS]</tt></li></ul>
    <li>(Planned): Using any single variable letter with <tt>$^</tt></li>
    <ul><li>Eg: <tt>Lo.searchSuggestions</tt> becomes <tt>$^$^.searchSuggestions</tt></li></ul>
    </ul>
    </details>


## Quick Links

- [Video Guide 2](https://youtu.be/foCewvyOszQ)
- [Video Guide 1](https://youtu.be/7_3e9j8FFv8)
- [SteamUI-OldGlory Wiki](https://github.com/Jonius7/SteamUI-OldGlory/wiki)
- [GIF of tweaks](https://gyazo.com/38d0101b493741501697b4a0f5f0818f)
- [Steam Missing Covers Downloader](https://github.com/Jonius7/steam-missing-covers-downloader/releases)
- [(Images) Collapse Game Page Sections](https://imgur.com/a/2GNoC3u)
- [(Images) More DLC and Screenshots, more info!](https://imgur.com/a/3WTdrXP)
- [(Images) JS Tweaks](https://imgur.com/a/mL4QNYB)
- [(Images) Is Steam Grid View Back?](https://imgur.com/gallery/qcIHx0l)
- [(Images) Steam List View Proof of Concept](https://imgur.com/a/ZqvqrkR)
- [(Images) Sticky Header background and Left Sidebar font](https://imgur.com/a/XzMAlxr)
- [(Images) Game Properties Horizontal Tabs](https://imgur.com/a/mqRCPc8)
- [Steam Discussions [1]](https://steamcommunity.com/groups/for_a_better_steam_client/discussions/0/2970650017896633625/)
- [Steam Discussions [2]](https://steamcommunity.com/discussions/forum/0/2451595019863406679/)



## steam-library Support

Shiina's **steam-library** theme is included as one of the starting themes you can choose from.

https://github.com/AikoMidori/steam-library

![preview image](https://i.imgur.com/4gWzhj9.png)



## Troubleshooting

If Library is not working, try one of these things (and **restart Steam** if necessary). If it still doesn't work, try the next thing in the list.

- Check **SFP (SteamFriendsPatcher)** or **Millennium** is running.
- Go to Task Manager and End Task on **Steam Client WebHelper** (let it restart)
- Use **Remake JS** button under **Settings and About** (this should also be done when Steam Client updates and the JS has changed)
- Use **Reset** button under **Settings and About**
- Delete `steamui` folder and restart Steam
  - Optional: Try these **Steam Settings** (and restart Steam)
    - **Downloads** -> **Clear Download Cache**
    - **Web Browser** -> **Delete Web Browser Cache**

If none of these steps work, please open an [Issue](https://github.com/Jonius7/SteamUI-OldGlory/issues/new/choose)

- State whether you are on Steam Beta Update or not.
- Which CSS Options/JS Options you have enabled/disabled.



The program can't start because `api-ms-win-crt-math-l1-1-0.dll` is missing from your computer.

- Install [Microsoft Visual C++ Redistributable 2015-2019](https://support.microsoft.com/en-au/help/2977003/the-latest-supported-visual-c-downloads)

## Dev Notes

#### For more details, go to [Story](docs/story.md)

#### [CSS Changelog](docs/Changelog%20-%20CSS.md) | [GUI Changelog](docs/Changelog%20-%20old_glory%20GUI.md)

#### [SteamUI-OldGlory Wiki](https://github.com/Jonius7/SteamUI-OldGlory/wiki)

#### Debugging Steam Library Yourself

To debug the Steam Library yourself, run Steam with the ` -dev` tag.

- Create a shortcut to `Steam` -> `Right Click` -> `Properties`.
- In `Target`, after `Steam.exe"` add `  -dev` so the end of Target looks like this: `Steam.exe" -dev`
- After opening Steam, open up the Dev Tools by clicking in the library window and pressing `F12`.

#### Build `old_glory`

Requires Python `3.8+`, Rust (tested with `1.75.0`)

Create a [Python Virtual Environment](https://docs.python.org/3/library/venv.html)

​	Linux: `sudo apt install python3-venv` , then: [link](https://docs.python.org/3/library/venv.html)

Activate it:

​	Windows: "*<venv>*\Scripts\Activate"

​	Linux: source *<venv>*/bin/activate

Install pyinstaller:
	`pip install pyinstaller`

Install libraries using `pip`: 
	`pip install jsbeautifier rjsmin libsass Pillow requests requests_oauthlib maturin pyppeteer pyyaml rich schema gitpython`

Run:

​	`maturin develop`:		

Build `old_glory.exe`:
	`pyinstaller --clean old_glory.spec`

The `.spec` file is included in the repository.

##### Advanced

Sometimes you may need to install `pyinstaller` like this:
[Building PyInstaller Bootloader](https://pyinstaller.readthedocs.io/en/stable/bootloader-building.html)	 [Windows Compilers](https://wiki.python.org/moin/WindowsCompilers#Which_Microsoft_Visual_C.2B-.2B-_compiler_to_use_with_a_specific_Python_version_.3F)

This is mainly for me to try and get an `.exe` that doesn't trigger false positives on [virustotal.com](virustotal.com)

In the future, I may try to build using `cx_freeze` instead.

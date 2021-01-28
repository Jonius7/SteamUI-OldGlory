# SteamUI-OldGlory

A set of tweaks to the Steam UI, and also a reference, so you can learn to make your own tweaks.

Check [`/dev`](https://github.com/Jonius7/SteamUI-OldGlory/tree/dev) branch for in-progress tweaks.

On Steam Beta? Check [`/beta`](https://github.com/Jonius7/SteamUI-OldGlory/tree/beta) branch for some files you may need.

#### [Download Latest Version](https://github.com/Jonius7/SteamUI-OldGlory/releases/latest) | [Wiki](https://github.com/Jonius7/SteamUI-OldGlory/wiki) 

### Video Guide and GIF

<img src="https://media.giphy.com/media/OjD2H5dci42cYRVvWN/source.gif" alt="Alt Text" style="zoom:95%;" /> 

[<img src="https://i.imgur.com/FYDDWVW.png" alt="Video Guide to Customising The Steam Library"/>](https://youtu.be/foCewvyOszQ)

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
    <img src="https://i.imgur.com/HrgBUPl.png" alt="Play bar moved up into box" style="zoom:80%;" /> <br><br>
    Classic Layout <br>
    <img src="https://i.imgur.com/7FPUtlP.png" alt="Classic Layout" style="zoom:80%;" />
</details>




## Quick Usage

#### Patching and CSS

- Install [**SteamFriendsPatcher**](https://github.com/PhantomGamers/SteamFriendsPatcher/releases). NOTE (if running v0.1.36-beta, [**"Steam Beta"** in Settings, needs to be ticked.](https://i.imgur.com/jmSaoEE.png)) Run it, it will patch some files.
- Download [**SteamUI-OldGlory**](https://github.com/Jonius7/SteamUI-OldGlory/releases). Extract the files to a folder, and run `old_glory.exe`
- Select the options you want to use, then click **Install**.
- To fix all your blurry game portrait images, use this build of [**Steam Missing Covers Downloader**](https://github.com/Jonius7/steam-missing-covers-downloader/releases/tag/new-format-fix).

##### **Manual Editing** (CSS/SCSS)

<details><summary>More details</summary>
<ul>   
<li><tt>variables.css</tt>  contains a list of CSS variables that tweak certain parts of the Library.</li>
  <li>A few of these can be configured using the GUI, but there are additional options here you can set manually.</li>
  <li>If you manually edit the file, use the <b>Reload Config</b> button to load them into the Configurer. </li><br>
<li><tt>scss/libraryroot.custom.scss</tt> contains the @imports for each of the CSS "modules", that each cover a different part of the Steam library.</li>
    <li>You can enable and disable certain modules by adding <tt>// </tt> to the beginning of the line</li>
    <li>Click <b>Install</b> in the Configurer to apply your changes.</li>
</ul>
</details>
<img src="https://media.giphy.com/media/5ZiZcGpMvRyEdOliSk/giphy.gif" alt="GUI Images" style="zoom:95%;" />

#### OldGlory Configurer (GUI)

##### Main Options

- **Install CSS Tweaks** - main layout tweaks will be applied to Steam Library
- **Box Play Button** - turns the Play Bar into a floating box in the header
- **Vertical Nav Bar** - turns the Navigation/Links bar into a floating vertical menu in the header, on the right side
- **Classic Layout** - Vertical Nav Bar is now aligned with the game page content, with the Friends Activity/News column pushed to the bottom of the page.
- **Landscape Game Images** - changes Portrait Game Images in the HOME page to Landscape ones.
- **Library Theme**

**Actions**

- **Install** - Will install selected CSS and JS tweaks. If no JS options have changed, will just install the CSS tweaks (which is somewhat faster than installing both CSS and JS)
  - The app will copy the needed files to and from `steamui` folder as need.
- **Reload Config** - If you have modified `fixes.txt` `variables.css` or `old_glory.json` manually, then Reload Config will grab these new values and update the checkboxes and values in the GUI (CSS Options + JS Options), without having to restart the GUI app. Changing files in `/scss` or `/themes` doesn't require Reload Config. 

In **Advanced -> Quick Links**:

- **Open OldGlory folder**: open the OS file explorer to the main folder where OldGlory and files are located . 
- **Open steamui folder**: open the `steamui` folder within ` Program Files/Steam` where the library files are located.

In **Settings and About**:

- **Remake JS** - Deletes local JS files and re-applies JS tweaks. 
  Use this when some JS tweaks may not apply due to new JavaScript. Usually:
  - after a Steam Client update, or 
  - switching between Steam Stable and Steam Beta
  - Technical details: 
    `clear_js_working_files` - deletes local `library.js`, `libraryroot.js`, `libraryroot.beaut.js`
    `run_js_tweaker` - recreates `libraryroot.beaut.js` and applies JS tweaks

- **Reset** - triple click to reset the `steamui` directory back to using default library theme. Useful if something screws up or you want to test a clean slate.

##### CSS Options

- **What's New** - Changes position and display of What's New
- **Game List Zoom** - Compact rows for Left Sidebar (Games List)
- **Show Left Sidebar** - Show/Hide Left Sidebar (Games List)
- **Glare/Shine** - Removes glare/reflection on HOME page images
- **Game Image Transition** - Fade in time for HOME page images
- **Home Page Grid Spacing**
- **Game Page Layout** - Swap Game page columns or default
- **Game Image Opacity** - HOME page: Dim Game Images, or Uninstalled Game Images
- **[Open variables file]** - opens `variables.css` using OS default text editor
- **[Open scss file]** - opens `scss/libraryroot.custom.scss` using OS default text editor

**JS Options**

- **Home Page Grid Spacing** - sets grid spacing to 8px 5px (default 24px 16px)
- **Increase Number of Screenshots and DLC displayed** - On game page: Screenshots: 4 -> 8, DLC 6 -> 12
- **HoverPostion Fix for GameListEntry** - Hover position fix if using 75% **Game List Zoom** in CSS Options
- **Scrolling Tweak** - Scroll past ADD SHELF Button on load
- **Change Game Image Grid Sizes** - Change the size of Game Images on the HOME page, based on <u>width in pixels</u>. There are 3 values here to change, corresponding to Small, Medium, Large sizes in settings. Defaults are:
  - <u>Small</u>		  `111`
  - <u>Medium</u>	 `148`
  - <u>Large</u>		  `222`
- ***Vertical Nav Bar*** - corresponds to Main Option **Vertical Nav Bar**. No need to configure manually.
- ***Landscape Images JS Tweaks***  - corresponds to Main Option **Landscape Game Images**. No need to configure manually.
- **Stop What's New Events from Loading** - removes loading of What's New Events
- **HOME page Scrolling, reduce number of ComputeLayout calls** - Improve smoothness of HOME page Scrolling
- **Game Properties Window Size** - Reduce width of Game Properties window to closely match old one
- **CLASSIC Sticky image background and spillover into sidebar** - Game Header image will stay in background as you scroll, and is visible through the Left Sidebar (Games List)
- **\*\*Experimental\*\* Don't load HOME game images, only alt text** - Can improve performance by not loading images and only the alt text
- **\*\*Experimental\*\* Remove Game Page Bloat** - Game pages will only load the Play and Navigation bars. May improve performance.



#### Included files:

- `old_glory.exe` - App to apply **SteamUI-OldGlory's** tweaks
- `variables.css` - CSS variables to customise
- `fixes.txt` - JS tweaks
- `libraryroot.custom.css` - output CSS file. Do not edit this directly, use the `\scss` folder files
- `\scss` - (New in Release 5.0)
  - `libraryroot.custom.scss` - contains all the `@imports` for smaller `.scss` files. The GUI handles enabling/disabling `_module_playbarbox`, `_module_verticalnavbar`, `_module_landscapegameimages`, `_module_classiclayout`. Manually comment out the other modules (for now)
  - `_user_module1.scss`- put your custom CSS code here
  - `_user_module2.scss` - put your custom CSS code here

- `\themes` - Folder containing theme files
  - `_shiina.scss` and `config.css.original` - **Shiina's** [steam-library](https://github.com/AikoMidori/steam-library) dark theme
  - `_spiked.scss` - **Thespikedballofdoom's** [Dark Library](https://gamebanana.com/guis/35092) theme
  - `_acrylic.scss` - Theme based on **EliteSkylu's** [Acrylic Steam](https://www.reddit.com/r/Steam/comments/jot6vi/let_me_introduce_you_a_project_of_my_steam_ui/) concept
  - `_crispcut.scss` - (WIP) Theme by **Jonius7**, emphasising white app section boxes
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
    <li>(Planned, coming soon): Using any single variable letter with <tt>$^</tt></li>
    <ul><li>Eg: <tt>Lo.searchSuggestions</tt> becomes <tt>$^$^.searchSuggestions</tt></li></ul>
    </ul>
    </details>



#### Fix Blurred Game Images

- Download [Steam Missing Covers Downloader](https://github.com/Jonius7/steam-missing-covers-downloader/releases/tag/new-format-fix) and run `missing_cover_downloader`

## Quick Links

- [Video Guide](https://youtu.be/foCewvyOszQ)
- [SteamUI-OldGlory Wiki](https://github.com/Jonius7/SteamUI-OldGlory/wiki)
- [GIF of tweaks](https://gyazo.com/38d0101b493741501697b4a0f5f0818f)
- [Steam Missing Covers Downloader](https://github.com/Jonius7/steam-missing-covers-downloader/releases/tag/new-format-fix)
- [(Images) More DLC and Screenshots, more info!](https://imgur.com/a/3WTdrXP)
- [(Images) JS Tweaks](https://imgur.com/a/mL4QNYB)
- [(Images) Is Steam Grid View Back?](https://imgur.com/gallery/qcIHx0l)
- [(Images) Steam List View Proof of Concept](https://imgur.com/a/ZqvqrkR)
- [(Images) Sticky Header background and Left Sidebar font](https://imgur.com/a/XzMAlxr)
- [(Images) Game Properties Horizontal Tabs](https://imgur.com/a/mqRCPc8)
- [Steam Discussions [1]](https://steamcommunity.com/groups/for_a_better_steam_client/discussions/0/2970650017896633625/)
- [Steam Discussions [2]](https://steamcommunity.com/discussions/forum/0/2451595019863406679/)



## What's New?
>
>#### Release 5.5
>
>- (GUI) NEW Expanded CSS Options page:
>   - **What's New** 	**Game List Zoom** 	**Show Left Sidebar** 	**Glare/Shine** 
>   - **Game Image Transition** 	**Home Page Grid Spacing**
>   - **Game Page Layout** 	**Game Image Opacity** 
>- CSS enhancements
>  - NEW Classic Steam appearance CSS (WIP)
>  - NEW Game Properties - horizontal tab bar
>  
>- NEW JS tweaks:
>  - Smoother HOME page Scrolling
>  - Game Header: sticky background position and spillover into sidebar
>  - (*Experimental*) Don't load HOME game images, only alt text
>  - (*Experimental*) Load only essential parts of Game Page (Play Bar and Navigation Bar)
>  
>- JS tweaks `fixes.txt` can now use previous line of JS to search for the line you want. Just separate the two lines with `~~`
>
>- NEW Auto-update feature for small file updates 
>  - CSS: `scss/` folder, `variables.css`, `themes/` folder	
>  - JS: `fixes.txt`		JSON: `old_glory_data.json`
>
>[More details...](https://github.com/Jonius7/SteamUI-OldGlory/releases)
>
>---
>
>[Compare with Release 5.0.1](https://github.com/Jonius7/SteamUI-OldGlory/compare/Release_5.0.1...Release_5.5) | [Changelog](https://github.com/Jonius7/SteamUI-OldGlory/releases/tag/Release_5.5)
>
>


## steam-library Support

Shiina's **steam-library** theme is included as one of the starting themes you can choose from.

https://github.com/AikoMidori/steam-library

![preview image](https://i.imgur.com/4gWzhj9.png)



## Troubleshooting

The program can't start because `api-ms-win-crt-math-l1-1-0.dll` is missing from your computer.

- Install [Microsoft Visual C++ Redistributable 2015-2019](https://support.microsoft.com/en-au/help/2977003/the-latest-supported-visual-c-downloads)

## Dev Notes

#### For more details, go to [Story](docs/story.md).

#### [CSS Changelog](docs/CSS%20Changelog.md)

#### [SteamUI-OldGlory Wiki](https://github.com/Jonius7/SteamUI-OldGlory/wiki)

#### Debugging Steam Library Yourself

To debug the Steam Library yourself, run Steam with the ` -dev` tag.

- Create a shortcut to `Steam` -> `Right Click` -> `Properties`.
- In `Target`, after `Steam.exe"` add `  -dev` so the end of Target looks like this: `Steam.exe" -dev`
- After opening Steam, open up the Dev Tools by clicking in the library window and pressing `F12`.

#### Build `old_glory`

Requires Python 3.8+

Install pyinstaller:
	`pip install pyinstaller`

Install libraries using `pip`: 
	`pip install jsbeautifier jsmin pillow requests requests_oauthlib libsass`

Build `old_glory.exe`:
	`pyinstaller -w --hidden-import six --icon=steam_oldglory.ico --clean --onefile old_glory.spec`

The `.spec` file is included in the repository.

##### Advanced

Sometimes you may need to install `pyinstaller` like this:
[Building PyInstaller Bootloader](https://pyinstaller.readthedocs.io/en/stable/bootloader-building.html)	 [Windows Compilers](https://wiki.python.org/moin/WindowsCompilers#Which_Microsoft_Visual_C.2B-.2B-_compiler_to_use_with_a_specific_Python_version_.3F)

This is mainly for me to try and get an `.exe` that doesn't trigger false positives on [virustotal.com](virustotal.com)

In the future, I may try to build using `cx_freeze` instead.

#### What does `js_tweaker` do?

the JS goes through this process:

- `libraryroot.js` - original file
- `libraryroot.beaut.js` - beautified js using `jsbeautifier`
- `libraryroot.modif.js` - beautified js with modified tweaks from `fixes.txt`
- `libraryreet.js` - minified `libraryroot.modif.js` using `jsmin`

Limitation that the script only reads from `libraryroot.beaut.js` one line at a time, so you cannot use multiple lines as your search criteria to "find and replace", at the moment.

`js_tweaker` will use `libraryroot.beaut.js` if it already exists. This means:

- you can experiment in `libraryroot.modif.js` and delete it afterwards if you want to go back to the clean version `libraryroot.beaut.js

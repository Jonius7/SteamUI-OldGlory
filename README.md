# SteamUI-OldGlory

A set of tweaks to the Steam UI, and also a reference, so you can learn to make your own tweaks. \
Check `/dev` branch for in-progress tweaks.

#### [Download Latest Version](https://github.com/Jonius7/SteamUI-OldGlory/releases/latest)

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

- To fix all your blurry game portrait images, use this build of [**Steam Missing Covers Downloader**](https://github.com/Jonius7/steam-missing-covers-downloader/releases/tag/new-format-fix).

  ![https://i.imgur.com/A85LCCn.png](https://i.imgur.com/A85LCCn.png)

#### Included files:

- `old_glory.exe` - App to apply **SteamUI-OldGlory's** tweaks
- `variables.css` - CSS variables to customise
- `fixes.txt` - JS tweaks
- `libraryroot.custom.css` - output CSS file. Do not edit this directly, use the `/scss` folder files
- `\scss` - (New in Release 5.0)
  - `libraryroot.custom.scss` - contains all the `@imports` for smaller `.scss` files. The GUI handles enabling/disabling `_module_playbarbox`, `_module_verticalnavbar`, `_module_landscapegameimages`, `_module_classiclayou`t. Manually comment out the other modules (for now)
  - `_user_module1.scss`- put your custom CSS code here
  - `_user_module2.scss` - put your custom CSS code here

- `\themes` - Folder containing theme files
  - `_shiina.scss` and `config.css.original` - **Shiina's** [steam-library](https://github.com/AikoMidori/steam-library) dark theme
  - `_spiked.scss` - **Thespikedballofdoom's** [Dark Library](https://gamebanana.com/guis/35092) theme
  - `_acrylic.scss` - Theme based on **EliteSkylu's** [Acrylic Steam](https://www.reddit.com/r/Steam/comments/jot6vi/let_me_introduce_you_a_project_of_my_steam_ui/) concept
  - `_crispcut.scss` - (WIP) Theme by **Jonius7**, emphasising white app section boxes

Other files are copied from the`Steam\steamui` directory as required.

`config.css` for Shiina's steam-library theme will be created from `config.css.original` the first time you enable the theme. Alternatively, you can put your existing `config.css` file here and the app will use it.



#### JavaScript Tweaks

Some tweaks are disabled by default. Under JS Options, you can select which options to enable/disable.\

**Manual Editing**

<details><summary>More details</summary>`fixes.txt`  contains the list of JavaScript tweaks.<br>Each tweak is under its own *Section Heading* marked with the line starting `###`.<br>
Tweaked lines are the original JS separated by two spaces from the tweaked JS:<br>
[original js]&#9608;&#9608;[new js]<br>
Remove the `###` for each line under the *Section Heading* to enable.<br>
Commented lines with `###`, and blank lines are ignored. You can use this to make `fixes.txt` more readable.</details>


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
- [Steam Discussions [1]](https://steamcommunity.com/groups/for_a_better_steam_client/discussions/0/2970650017896633625/)
- [Steam Discussions [2]](https://steamcommunity.com/discussions/forum/0/2451595019863406679/)



## What's New?
>
>#### 5.0
>
>- Themes working again with 22 Dec Steam Client Update.
>
>- SteamUI-OldGlory now uses [Sassy CSS (Sass)](https://github.com/Jonius7/SteamUI-OldGlory/wiki/Chrome-DevTools).
>  Particular components such as scrollbar, a HOME icon, sidebar, play bar, navbar are now in their own `.scss` files.
>
>- ---
>
>    **Use `variables.css` instead of `libraryroot.custom.css` to manually edit CSS variables**
>    `libraryroot.custom.css` is completely generated now. Editing it manually and trying to **Install** will likely not apply your changes. Instead look for stuff to change in `variables.css`, and the `scss` folder.  
>    If things are still too confusing, I may look at simplifying the folder structure next release.
>
>    ---
>
>- GUI `v0.9.5.5` -> `v0.9.6.9`
>  The GUI is now using JSON to store some of the data. This has the benefit of being editable outside of having to rebuild the .exe
>
>- Issues fixed from #5
>
> - Themes working again
>    - Auto-select current theme on startup
>    - New DLC Manager scss - no longer requires JavaScript for row height
>
>###Future Releases
>Now that Sass is implemented, time to add more toggleable features.
>Continue building the auto-updating system. The ideal state is to be able to push out .scss, fixes.txt, or old_glory_data.json hotfixes smoothly, and leave the GUI changes as the major updates.
>
>[Compare with Release 4.1.1](https://github.com/Jonius7/SteamUI-OldGlory/compare/Release_4.1.1...Release_5.0) | [Changelog](https://github.com/Jonius7/SteamUI-OldGlory/releases/tag/Release_4.1.1)
>
>
>[More details...](https://github.com/Jonius7/SteamUI-OldGlory/releases)


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
	`pip install jsbeautifier jsmin pillow requests libsass`

Build `old_glory.exe`:
	`pyinstaller -w --hidden-import six --icon=steam_oldglory.ico --clean --onefile old_glory.spec`

The `.spec` file is included in the repository.

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

## SteamUI-OldGlory GUI Changelog

1.1.7.3	     **(Release 5.16.2)** Fix Updater token

*1.1.7.2*	     **(Release 5.16.1)** Remove git dependency "bad git executable"

**1.1.7.1**	     **(Release 5.16)** Disable Remake JS button

1.1.7		Disable JS Tweaks options, unfinished Download Themes tab

1.1.6.1		*(5.16-pre1)* New ThemeUpdater class

1.1.6		Add new functions to download Github theme repo, extract zip

**1.1.5.4**	     **(Release 5.15)** Small fixes (alternate registry path for Steam InstallPath)

1.1.5.3	    *(5.15-pre3)* Hide console window when checking for Steam on Windows, add check on Linux

1.1.5.2	     	*(5.15-pre2)* Move `refresh_steam` threading into 2 functions

1.1.5.1	     Precise 2 layers of threading on `refresh_steam` for maximum responsiveness

1.1.5			*(5.15-pre1)* Working implementation of refreshing Steam window upon installing (caveat of freezing)

1.1.4.2	     	*(5.14.2-pre1)* Add Millennium URL Link to Settings and About

1.1.4.1	     Make `fixes.txt` Linux compatible, fix inconsistencies with line endings

1.1.4		Quick CSS Frame now scrollable

1.1.3.3	    Add Unpatch CSS function, no longer creates empty `libraryroot.custom.css`

**1.1.3.2**	     **(Release 5.14.1)** Fix error if steamui\skins\OldGlory folder isn't created

1.1.3.1	    Fix not accepting default package location

**1.1.3**		**(Release 5.14)** Now auto-checks if there is a new Steam Update and notifies accordingly

1.1.2			*(5.14-pre1)* New Install Location dropdown (now compatible with Millennium)

**1.1.1.1**	    **(Release 5.13)**  New class mapping, remove defunct JS tweaks

**1.1.1**	       **(Release 5.12.1)** Full Dark Mode Theme (FatheredPuma81), Metro Top Bar CSS

**1.1.0.1**	    **(Release 5.12)** *No changes*

1.1.0.0 		*(5.12-pre1)* Now uses Rust for JS beautification

1.0.1.2		 *(5.11.2-pre1)* Fix JS tweaks for Steam Beta 28 March (incl Landscape Game Images)

**1.0.1.1**           **(Release 5.11.1)** Fix frame scrolling error (`_tkinter.TclError: invalid command name`)

1.0.1		     (*5.11.1-pre1*) Fix expired login token (for checking updates)

**1.0**		  **(Release 5.11)** New CSS Sections functionality

0.9.30.3		(*5.11-pre4*)	More CSS/JS Mode Menu Functionality

0.9.30.2		(*5.11-pre3*)	Add Hovertooltips and proper name Labels

0.9.30.1		(*5.11-pre2*)	Working checkboxes and modifying libraryroot.custom.scss

0.9.29.2		(*5.11-pre1*)	Add Checkboxes for CSS Sections feature

**0.9.27.12**	**(Release 5.10.7)** Fix not downloading themes files

**0.9.27.10**	**(Release 5.10.6)** Fix `no module named 'six'` error

**0.9.27.8**	  **(Release 5.10.5)** Remove hardcoded filenames

**0.9.27.7**	  **(Release 5.10.4)** Fix JS tweaks for steam Update 17 Nov 2022

**0.9.27.5**	  **(Release 5.10.3)** Update to patch `2783.js`

**0.9.27.4**	  **(Release 5.10.2)** Update to patch `3991.js`

**0.9.27.1**	  **(Release 5.10)** No longer needs SFP to patch CSS

**0.9.25.6** 	 **(Release 5.9)** New themes directory format, fix JS tweaks for 18 Aug update

0.9.25.1		(*5.9-pre1*) New themes directory format (folder for each theme)	

**0.9.11.31**	**(Release 5.8.6)** New Versions of JS Tweaks for Steam Update 28 July

**0.9.11.29**	**(Release 5.8.5)** New versions of JS tweaks for Steam update 13 May 

0.9.11.25 	*(Release 5.8.4-pre1)* New version JS tweaks working up to Change Game Image Sizes

**0.9.11.23** 	**(Release 5.8.3)** Fix extra newlines being added when updating files

**0.9.11.21** 	**(Release 5.8.2.1)** Fix critical bug where themes and CSS tweaks were not applying

**0.9.11.11**	**(Release 5.8.1)** Fix JS tweaks not applying since 5 Mar Steam Update

**0.9.11.10**	**(5.8)** Backported run_js_tweaker, working JS with `library.js`

​	0.9.24.4	Piecemeal changes

​	0.9.24		*(5.8-pre8)*	33% faster performance - pre-compiling Regex strings

​	0.9.23	   `Install` button now disables while installing

​	0.9.22.4	*(5.8-pre7)* 	`refs` functionality completed, fixed `write_modif_file` 

​	0.9.20.5	Generating `refs` list, filter out tweaks that don't have `refs`

**0.9.11.5**	**(Release 5.7.4.2)** Hotfix patching JS, change to use `rjsmin`

0.9.11.4 	*(5.7.4.1)* Remove number-specific JS reference

​	0.9.20.2	Search for `refs` (WIP), update JS Beautify Messages

​	0.9.19		*(5.8-pre6)* 	JS Tweaks Schema Validation and populating `@Values@`

​	0.9.17		*(5.8-pre5)*	Can now set libraryroot CSS filename, launch SteamFriendsPatcher button 

**0.9.11.2	(Release 5.7.4)** Fixed bug with error: `No such file or directory: 'librery.js'`

​	0.9.16		*(5.8-pre4)*	Fixed longstanding GUI slow responsiveness switching Frames while tweaks are Installing

​	0.9.15.1	*(5.8-pre3)*	Change Install buttons layout

​	0.9.14.1	*(5.8-pre2)*	Working Regex find and replacements

​	0.9.12.1	Reading `.yml`

**0.9.11.0**	**(Release 5.7.3)** Now using tweaked JS in `librery.js` (original file `library.js`)

**0.9.10.7**	**(Release 5.7.2)** Changed order of js tweaking (also fixes nasty bug "invariant failed...")

**0.9.10.4**	**(Release 5.7.1.1)**

0.9.10.1	*(5.7-pre1)* Split code into `manager.py`, simpler config/parsing writing code (Part 1)

0.9.9.10	*(5.6.5-pre3)*

0.9.9.01	<u>(5.6.5-beta1)</u>  Split code into `custom_tk.py`, added "CSS + JS" selector

0.9.8.20	(*5.6-pre1*)	Updated to use new config version

0.9.8.14	(*5.5.5-pre2*)

0.9.8.13	(*5.5.5-pre1*)

0.9.8.11    (*R5.5.4*) More print output messages, fix `copy_files_from_steam` Reset bug

**0.9.8.10**   **(Release 5.5.3)** Fix `os_makedirs` download file

**0.9.8.8**	 **(Release 5.5.2)** Downloads new files from remote

**0.9.8.7**	 **(Release 5.5.1)** Fix UnicodeEncodeError: 'charmap' codec can't encode character `'\u266a'`

**0.9.8.6** 	**(Release 5.5)** Added `Apply config.css` button for shiina's `steam-library`

0.9.8.5 	Linux - Fix icon not loading, and `xdg-open` not opening path

0.9.8.3	 Add Check for Updates button

0.9.8.1     Small File Update Check and Download working

0.9.7.22   Added "Small Update" GUI window

0.9.7.16   Log box now expands with window resize.

0.9.7.12   Added working Expanded CSS Options

0.9.7.4	 Added `ScrollFrame` to JS Options

0.9.7		Now reads from variables.css ("What's New") 

**0.9.6.11**   **(Release 5.0.1)** Fixed issue with libraryroot.custom.css not apply on clean install

**0.9.6.9** 	**(Release 5.0)** Theme and module selection functionality working

0.9.6.6     Redid Theme selection

0.9.6.3	 Add JSON parsing

0.9.6.0	 Add tabs to main page

**0.9.5.5**    **(Release 4.1.1)** Remove `HyperlinkText` class flawed implementation and used `tkHyperlinkManager`

0.9.5.4	Add DPI scaling to be fixed to fit on Windows 8 125%

**0.9.5.2**    **(Release 4.1)**

0.9.5.1	Add some CSS changing depending on whether JS is being applied
				Move images into subfolder

0.9.5	   Add clickable Hyperlinks in `Settings/About`
				Add update check and clickable hyperlink.
				Fix `Failed to execute script old_glory` when `libraryroot.custom.css` is missing.

0.9.4.8	Increase Window size + resizable

**0.9.4.7**    **(Release 4.0.2)** Steam Client Update 8 Dec

0.9.4.5	Fix backslashes (Linux/Mac) + print traceback

**0.9.4.3**	**(Release 4.0.1)** Fix `library.js` not found bug on initial setup/Reset

**0.9.4** 	  **(Release 4)** First public version

*0.9.3.1*	Added About links

<u>*0.9.3*</u>	   Merge submodule into main repository

*0.9.2*	   `config.css` configuration for shiina's `steam-library`

*0.9.1*	   Added Settings window, `Remake JS` and `Reset` buttons functionality

*0.8.98*	 Library theme selection

*0.8.95*	 CSS variables reading and writing

*0.8.90*	 `Change Grid Image Sizes` selection

*0.8*		  Update `js_tweaker` to copy original files from Steam directory

*0.7.1*	   Reloading JS fixes using `Reload Config`

*0.5.5*	   Added `Landscape Game Images` option

*0.5*          Last version before putting Detailed Line by Line CSS Dropdowns on the backburner

*0.4*          Shrink images, populating and configuring CSS Options page (many changes)

*0.3.5*	  `js_tweaker` integration






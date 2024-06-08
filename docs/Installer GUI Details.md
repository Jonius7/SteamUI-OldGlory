##### Main Options

*   **Install CSS Tweaks** - main layout tweaks will be applied to Steam Library
*   **Box Play Button** - turns the Play Bar into a floating box in the header
*   **Vertical Nav Bar** - turns the Navigation/Links bar into a floating vertical menu in the header, on the right side
*   **Classic Layout** - Vertical Nav Bar is now aligned with the game page content, with the Friends Activity/News column pushed to the bottom of the page.
*   **Landscape Game Images** - changes Portrait Game Images in the HOME page to Landscape ones.
*   **Library Theme** - applies the library theme shown in the dropdown

**Actions**

*   **Install** - Will install selected CSS and JS tweaks. If no JS options have changed, will just install the CSS tweaks (which is faster than installing both CSS and JS)
    *   The app will copy the needed files to and from the `steamui\skins\OldGlory` folder as need.
*   **Reload Config** - If you have modified `fixes.txt` `variables.css` or `old_glory.json` manually, then Reload Config will grab these new values and update the checkboxes and values in the GUI (**CSS Options** + **JS Options**), without having to restart the GUI app. Changing files in `/scss` or `/themes` doesn't require Reload Config.

**Advanced Settings**:

*   **Open OldGlory folder** - open the OS file explorer to the main folder where OldGlory and files are located .
*   **Open steamui folder** - open the `steamui` folder within `Program Files/Steam` where the library files are located.
*   **Apply config.css**: (For Shiina's steam-library theme) This option has been added to accommodate those who might have their own `config.css` in `[steamdir]/steamui` already. If you are instead editing the `config.css` in `themes/`, clicking this button will copy `config.css` over to `[steamdir]/steamui`.
    *   This may change in the future
*   **Patch CSS** - Patches CSS files located in `steamui\css` to allow a `libraryroot.custom.css` in `steamui` folder to be applied.
*   **Unpatch CSS** - Undos what Patch CSS does (useful when switching to using SFP/Millennium)
*   **Install Location** - defaults to **SFP/Millennium** which is the `steamui\skins\OldGlory` folder. steamui is `steamui` folder, **Local** just adds files to the SteamUI-OldGlory folder (good for developers)
*   **Compile CSS** - Just compiles the `.scss` files + `variables.css` into a `libraryroot.custom.css` file (good for developers)

In **Settings and About**:

*   **Remake JS** - Deletes local JS files and re-applies JS tweaks. Use this when some JS tweaks may not apply due to new JavaScript. Usually:
    *   after a Steam Client update, or
    *   switching between Steam Stable and Steam Beta
    *   Technical details: 
        *   `clear_js_working_files` - deletes local JS files including`library.js`, `library.beaut.js` `chunk~2dcc5aaf7.js` `chunk~2dcc5aaf7.beaut.js`
        *   `run_js_tweaker` - recreates JS files and applies JS tweaks
*   **Reset** - triple click to reset the `steamui` directory back to using default library theme. Useful if something screws up or you want to test a clean slate.

##### CSS Options

*   **What's New** - Changes position and display of What's New
*   **Game List Zoom** - Compact rows for Left Sidebar (Games List)
*   **Show Left Sidebar** - Show/Hide Left Sidebar (Games List)
*   **Game Image Glare/Shine** - Removes glare/reflection on HOME page images
*   **Game Image Transition** - Fade in time for HOME page images
*   **Home Page Grid Spacing** - Choose between compact or default
*   **Game Page Layout** - Swap Game page columns or default
*   **Game List Zoom Size** - Changes the sidebar/game list zoom size (show more or less games in list)
*   **DLC Available Content** - Show/Hide DLC Available Content box
*   **Recommend This Game** - Show/Hide Recommend This Game box
*   **\[Open variables file\]** - opens `variables.css` using OS default text editor
*   **\[Open scss file\]** - opens `scss/libraryroot.custom.scss` using OS default text editor

**JS Options**

*   **Enable Patching JS**
*   **Increase Number of Screenshots and DLC displayed** - On game page: Screenshots: 4 -> 8, DLC 6 -> 12
*   **Disable screenshot slideshow on hover** - Hovering over games on HOME page will only show the Game Box art, not the screenshot slideshow
*   **Change Game Image Grid Sizes** - Change the size of Game Images on the HOME page, based on width in pixels. There are 3 values here to change, corresponding to Small, Medium, Large sizes in settings. Defaults are:
    *   Small `111`
    *   Medium `148`
    *   Large `222`
*   **_Landscape Images JS Tweaks_** - corresponds to Main Option **Landscape Game Images**. No need to configure manually.
*   **Stop What's New Events from Loading** - removes loading of What's New Events
*   **Expand Show more Details Panel by default** - The Show More Details Panel (i) will expand by default on game page load
*   **Don't load HOME game images, only alt text** - Can improve performance by not loading images and only the alt text
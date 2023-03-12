@echo off

pyinstaller -w --hidden-import six --icon=steam_oldglory.ico --log-level=DEBUG --clean --onedir old_glory.spec


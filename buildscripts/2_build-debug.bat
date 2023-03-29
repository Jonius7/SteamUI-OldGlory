@echo off

pyinstaller -w --hidden-import six --icon=steam_oldglory.ico --log-level=DEBUG --clean --onefile old_glory.spec


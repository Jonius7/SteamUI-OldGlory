@echo off
python -m pstats js_tweaker.prof
sort time
stats 30

pause
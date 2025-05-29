@echo off
REM add all changes
git add .

REM set commit message
set commit_message=%1
if "%commit_message%"=="" set commit_message=auto commit

REM commit
git commit -m "%commit_message%"

REM push
git push
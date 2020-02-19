#!/bin/bash

OPTIONS="-hvurt --exclude-from /home/deg/bin/cpCentralPark-excludeList.txt --progress --delete"

FROM=/home/CentralPark
TO=/centralPark

#   set flags=-n
#   if "%1"=="move"  set flags=
#   if "%1"=="delete" set flags=--delete
#   if "%1"=="deletecheck" set flags=-n --delete

rsync $OPTIONS $FROM/users/     $TO/users/
rsync $OPTIONS $FROM/media/     $TO/media/
rsync $OPTIONS $FROM/kids/      $TO/kids/
rsync $OPTIONS $FROM/static/    $TO/static/
rsync $OPTIONS $FROM/staticOld/ $TO/staticOld/
rsync $OPTIONS $FROM/newStuff/  $TO/newStuff/


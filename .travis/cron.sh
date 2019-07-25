#!/bin/bash

set -x

if nox -s build; then
  set -e
  datetime=`date "+%Y-%-m-%-d"`
  git add hstspreload/
  git commit -m "Automated updates to the HSTS preload list on $datetime"

  git remote rm origin
  git remote add origin https://sethmlarson:${GITHUB_TOKEN}@github.com/sethmlarson/hstspreload > /dev/null 2>&1
  git push origin master --quiet
fi

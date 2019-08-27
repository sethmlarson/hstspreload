#!/bin/bash

set -x

if nox -s build; then
  set -e
  # Deal with detached head state that Travis puts us in
  git checkout master

  # Change our Git username and email to not be Travis user
  git config --global user.name "Seth Michael Larson"
  git config --global user.email "sethmichaellarson@gmail.com"

  # Create a commit with the date attached
  datetime=`date "+%Y-%-m-%-d"`
  git add hstspreload/
  git commit -m "Automated updates to the HSTS preload list on $datetime"

  # Use our GitHub token to make the commit
  git remote rm origin
  git remote add origin https://sethmlarson:${GITHUB_TOKEN}@github.com/python-http/hstspreload > /dev/null 2>&1
  git push origin master --quiet
fi

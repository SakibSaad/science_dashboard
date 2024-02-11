#!/bin/bash

# go to previous folder
cd ..

# make zip
zip -r Map.zip Map

# remove folder
rm -r Map

# push to github
git add .
git commit -m "some fix"
git push

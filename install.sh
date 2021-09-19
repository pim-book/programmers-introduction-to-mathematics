#!/bin/sh
while read module; do
  pip install $module
done < requirements.txt

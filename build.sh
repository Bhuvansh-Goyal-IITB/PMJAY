#!/usr/bin/env bash

./clean.sh

pyinstaller --noconsole --clean -n PMJAY --onefile --icon assets/app_icon.ico --hidden-import=babel.numbers main.py
cp -r assets/ dist/
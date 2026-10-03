# list available recipes
default:
    @just --list

# show the current version
version:
    @sed -n 's/^VERSION = "\(.*\)"$/\1/p' src/version.py

# release, commit and tag a new version (YEAR.MONTH.RELEASE); without argument the next one is computed
release version="":
    @python3 tools/release.py {{ version }}

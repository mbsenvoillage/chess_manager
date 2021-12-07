# chess_manager

## Purpose

Chess manager is your favorite companion to managing chess tournaments following the Swiss Matching System.
Select players, number of rounds, time control and you're ready to start your tournament.
You then only need to enter results for a round for the next round matches to be automatically generated.
Thanks to its database you can pick up were you left off.

## Requirements

This program will work for versions of Python from 3.8 and above. You will need the package installer [pip](https://pypi.org/project/pip/) to install dependencies and [virtualenv](https://pypi.org/project/virtualenv/#description) if you want to create an isolated environment for this project.

## Installation

You will first need to clone this repo. Then just run from inside the downloaded directory `pip install -r requirements.txt`

## Code Style Enforcement

Flake8 can be used to make sure files comply to PEP8 style recommendations. In order to check
if a file complies with PEP8, just run `flake8 <name_of_file>`.
If you wish to generate an html report, you can run the following command `flake8 --format=html --htmldir=flake-report <name_of_file>`

## Usage

To start the program just run `python3 main.py`

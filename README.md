# hello_swanson: a fullstack application that displays Ron Swanson quotes.

### Credit
Quotes were originally taken from and the project was inspired by
the “Ron Swanson Quotes API” - https://github.com/jamesseanwright/ron-swanson-quotes#ron-swanson-quotes-api


## Build & Project Background
The goal of this project was 3-fold:
* Gain further experience constructing APIs and build on previous projects.
* Practice building APIs in multiple back-end langauges.
* Gain exposure to React basics.

Build is as follows:
* Back-end written in Python, utilizing Flask as a microframework.
* Front-end written mostly with React.
* Project is hosted on Heroku.
* All data is stored and retrieved on a PSQL database.


## Front End Stories

### Get a random Ron Swanson quote
A user can get Ron Swanson quotes at the click of a button
* It should allow me to click a button/image to get a Swanson word of wisdom

### Get a random Ron Sqanson quote with varying word length
A user I can get quotes that are a requested size.
* User can select a small, medium or large quote.
* Small - get a quote with 4 or fewer words.
* Medium - get a quote between 5-12 words.
* Large - get a quote with 13 or more words.

## Back End Stories

### Vote for Quotes
When a user sees a quote:
* The user can rate each quote from 1-5.
* The user (or given ip address) cannot vote more than 1 time for each quote.

### Average Quote Rating
A user can see the average rating of a quote
* When displaying a quote, the average rating is displayed


## Other Information - Loading the DB
quotes.txt
* All quotes are contained in this file.

quoteDB.txt
* txt used to create database.

import.py
* Load all quotes from quotes.txt into quotes table.

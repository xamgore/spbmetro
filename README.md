### Goal

I want to parse the [@spbmetro](https://t.me/spbmetro) channel and make a text classifier to get information:

* which subway station was opened / closed
* when did it happen
* what was the reason

Then it will be possible to notify citizens more efficiently: make predictions in 2GIS / Yandex.Maps while building A-B routes; or just for a nice infographics.

### About

* `metro.json` — names of subway stations, lines, colors, transfers
* `export.py` — script to export [channel](https://t.me/spbmetro) messages from telegram
* `history.json` — dumped messages, refined by myself
* `validate_time.py` — used for validation of my refinements 
* `structure.py` — data objects with typings, describing subway and history

Run this project via PyCharm, cause I don't really get, how to run it from CLI.

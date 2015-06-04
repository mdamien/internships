How to extract the data from scratch
========================================

- Make the basic list of all internships: `data/basics.json`
    - Go to the "Historique des stages" page, do the most extensive search possible
    - Save the page as `data/all.html`
    - execute `python3 basics.py && python3 basics2.py`
- Download every internship under `STAGES/`
    - With the network panel console of your browser, copy the CURL request when displaying an internship
    - Paste it in `download.py`
    - Execute `download.py` (you can execute 10 in parrallel for example)
- Execute `parse_stages.py` to get the parsed internships as `data/details.json`
- Execute `enrich.py` to merge `data/basics.json` and `data/details.json`
- Execute `make_csv.py` to have a nice csv

Another thing, the addresses are geolocated in `data/geolocated.json`, if you add new adresses, you need to geolocate them:
- Just execute `geolat.py`
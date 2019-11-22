import logging
import os

import requests

from flask import Flask, redirect, request

app = Flask(__name__)
app.config['TIMDEX_URL'] = os.getenv('TIMDEX_URL',
                                     default='https://timdex.mit.edu/graphql')


logging.basicConfig(level=logging.INFO)


@app.route('/')
def redirector():

    bibid = request.args.get('bibid')
    if not bibid:
        logging.info(f"No bib id supplied")
        return redirect("https://mit.worldcat.org/", code=302)

    url = app.config['TIMDEX_URL']

    query = f'''{{ recordId(id: "{bibid}" ){{ oclcs }} }}'''

    retrieve = requests.post(url, data={'query': query})

    if retrieve.status_code != 200:
        logging.info(f"TIMDEX response code: {retrieve.status_code}")
        return redirect("https://mit.worldcat.org/", code=302)

    data = retrieve.json()
    if 'errors' in data:
        logging.info('Errors in data returned from TIMDEX')
        return redirect("https://mit.worldcat.org/", code=302)

    if not data['data']['recordId']['oclcs']:
        logging.info('No oclcs found in data returned from TIMDEX')
        return redirect("https://mit.worldcat.org/", code=302)

    oclc = data['data']['recordId']['oclcs'][0]
    return redirect(f"https://mit.worldcat.org/oclc/{oclc}", code=302)


@app.route('/ping')
def ping():
    return "pong"

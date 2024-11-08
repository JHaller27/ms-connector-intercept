# Built-in imports
from pathlib import Path
import json

# Local imports
from mods.buybox_connector import mods as buybox_mods
from mods.overview_connector import mods as overview_mods

# Third-party imports
from fastapi import FastAPI
import requests


app = FastAPI()


@app.get('/')
def ping():
	return {'message': 'pong'}


MMTV_PRODUCT_FAMILIES = {'Movies', 'TV'}

@app.get('/api/buybox')
@app.get('/api/buyBox')
async def buybox(locale: str, bigId: str):
	productId_parts = bigId.split('/')

	p = Path() / 'buybox' / f"{productId_parts[0].upper()}.json"
	if p.is_file():
		with p.open() as fp:
			print(f'Using file {p}')
			obj = json.load(fp)

	else:
		url = f'https://msstoreapippe.microsoft.com/api/buybox?locale={locale}&bigId={bigId}'
		print(f'Calling live API {url}')
		resp = requests.get(url)
		if not resp.ok:
			return resp

		obj = resp.json()

	if obj['pageData']['productFamily'] in MMTV_PRODUCT_FAMILIES:
		try:
			obj = buybox_mods.run(obj)
		except Exception as e:
			print(e)

	return obj


@app.get('/api/entertainment/overview')
def mmtv_overview(locale: str, productId: str):
	productId_parts = productId.split('/')

	p = Path() / 'mmtv_overview' / f"{productId_parts[0].upper()}.json"

	if p.is_file():
		with p.open() as fp:
			obj = json.load(fp)

	else:
		url = f'https://msstoreapippe.microsoft.com/api/entertainment/overview?isMoviesAndTv=true&locale={locale}&productId={productId}'
		resp = requests.get(url)
		if not resp.ok:
			return resp

		obj = resp.json()
		obj = overview_mods.run(obj)

	return obj


@app.get('/api/seo')
def seo(bigId: str, locale: str):
	productId_parts = bigId.split('/')

	p = Path() / 'seo' / f"{productId_parts[0].upper()}.json"

	if p.is_file() and False:
		with p.open() as fp:
			obj = json.load(fp)

	else:
		url = f'https://msstoreapippe.microsoft.com/api/seo?locale={locale}&environment=ppe&bigId={bigId}'
		resp = requests.get(url)
		if not resp.ok:
			return resp

		obj = resp.json()

	return obj

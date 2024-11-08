from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from pathlib import Path
import json
import html
from rich import print

from compapi import mods as comp_api_mods
from buybox_connector import mods as buybox_mods
from overview_connector import mods as overview_mods


app = FastAPI()
app.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*'],
)


@app.get('/')
def ping():
	return {'message': 'pong'}


@app.get('/compositeapi')
async def compapi(req: Request):
	url = str(req.url).replace('8000', '4000')
	resp = requests.get(url)
	if resp.ok:
		return resp.json()
	return resp


@app.post('/compositeapi')
async def compapi(req: Request):
	url = str(req.url).replace('8000', '4000')
	print(url)

	if req.query_params.get('component') == 'BuyBox':
		bb_path = Path('buybox') / req.query_params.get('locale') / ('%s.json' % req.query_params.get('productId'))
		print(bb_path)
		if bb_path.is_file():
			with bb_path.open() as fp:
				data = json.load(fp)
			return comp_api_mods.run(data)

	data = await req.body()
	# print(data)
	resp = requests.post(url, data=data)
	if not resp.ok:
		print(resp.reason)
		raise HTTPException(resp.status_code, detail=resp.reason)

	data = resp.json()

	return comp_api_mods.run(data)


@app.get('/cascadesharedapidev/api/uhf', response_class=HTMLResponse)
async def uhf(req: Request):
	# https://www.microsoft.com/cascadesharedapiprod/api/uhf?privacyNotice=true&locale=en-us&msaem=prod&responseElement=css_header&partner=MSConsumer&headerId=MSConsumerSkipToMainHeader&footerId=MSConsumerFooter
	url = f'https://www.microsoft.com/cascadesharedapiprod/api/uhf?{req.query_params}'
	resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'})

	# tbl = Table('status', 'partner', 'headerId', 'footerId')
	# with Live(tbl):
	# 	if not resp.ok:
	# 		tbl.add_row(f'[red]{resp.status_code}[/red]', '-', '-', '-')
	# 		return resp

	# 	data = html.unescape(resp.content.decode('utf-8'))
	# 	tbl.add_row(f'[green]{resp.status_code}[/green]', req.query_params.get('partner'), req.query_params.get('headerId'), req.query_params.get('footerId'))

	# 	return data

	if not resp.ok:
		return resp

	return html.unescape(resp.content.decode('utf-8'))


MMTV_PRODUCT_FAMILIES = {'Movies', 'TV'}

@app.get('/api/buybox')
@app.get('/api/buyBox')
async def buybox(locale: str, bigId: str):
	productId_parts = bigId.split('/')

	p = Path() / 'buybox' / f"{productId_parts[0].upper()}.json"
	if p.is_file():
		with p.open() as fp:
			obj = json.load(fp)

	else:
		url = f'https://msstoreapippe.microsoft.com/api/buybox?locale={locale}&bigId={bigId}'
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

	if p.is_file() and False:
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

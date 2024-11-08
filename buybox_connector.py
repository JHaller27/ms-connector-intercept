from func_mods import FuncMods
from copy import deepcopy


mods = FuncMods()


# @mods.add
def selectors(obj):
	print('bb_mod: Selectors')

	additional_sku_ids = {
		'0001': ['0005'],
		'0002': ['0004'],
		'0003': ['0009'],
	}

	# Add CTAs
	new_cta = {
		'hasInterstitial': False,
		'actionType': 'AddToCart',
		'enabledConditions': [
			{
				'value': True,
			}
		],
		'visibilityConditions': [
			{
				'value': True,
			}
		],
		'availabilityId': '8D6KGWXXGKW4',
		'focusRank': 620
	}
	for sku_id, addl_sku_ids in additional_sku_ids.items():
		obj['skuInfo'].setdefault(sku_id, {})['CallToAction'] = deepcopy(new_cta) | {'label': f'Rent $123 - {sku_id}', 'disclaimer': f"Once you select Rent you'll have 14 days to start watching the movie and 48 hours to finish it. ({sku_id})"}
		for asku_id in addl_sku_ids:
			obj['skuInfo'][asku_id]['CallToAction'] = deepcopy(new_cta) | {'label': f'Buy $45 - {asku_id}'}

		obj['skuInfo'][sku_id]['XboxCTA'] = deepcopy(new_cta) | {'label': '$24.99 with Xbox Game Pass Ultimate', 'secondaryLabel': 'Join Now', 'uri': '/en-us/p/xbox-game-pass-ultimate/cfq7ttc0khs0'}

	# Trim skuMap & selectors
	obj['skuMap'] = {
		'0': ['0002', '0005',],
		'1': ['0001', '0004',],
		'2': ['0003', '0009',],
	}

	obj['selectors'] = [
		{
			'selectionItems': [
				{'label': 'SD'},
				{'label': 'HD'},
				{'label': 'UHD'},
			],
		},
	]

	return obj


# @mods.add
def ownership(obj):
	print('bb_mod: Ownership')

	for skuId, skuObj in obj['skuInfo'].items():
		skuObj["AppIdentityOpenButton"] = {
			"uri": "mswindowsvideo://play/?bigCatId=8D6KGWXX6ZFP&zestId=b9925d0b-0100-11db-89ca-0019b92a3933&itemType=movie&UserId=ecbd592966af1b804710b1ee265e8ce0b36ff26113187f1f969a3422f0a91928",
			"hasInterstitial": False,
			"actionType": "Open",
			"enabledConditions": [
				{
					"value": False
				}
			],
			"visibilityConditions": [
				{
					"value": True
				}
			],
			"focusRank": 100,
			"label": "Watch"
		}
		skuObj["AppIdentityopenMoviesAndTvAppButton"] = {
			"uri": "mswindowsvideo://details/?bigCatId=8D6KGWXX6ZFP&zestId=b9925d0b-0100-11db-89ca-0019b92a3933&itemType=movie&UserId=ecbd592966af1b804710b1ee265e8ce0b36ff26113187f1f969a3422f0a91928",
			"hasInterstitial": False,
			"actionType": "openMoviesAndTvApp",
			"enabledConditions": [
				{
					"value": True
				}
			],
			"visibilityConditions": [
				{
					"value": True
				}
			],
			"focusRank": 5000,
			"label": "Open Movies & TV"
		}

		skuObj['AppIdentityInstallButton'] = {
			'actionType': 'Watch',
			'label': 'Watch',
			'uri': 'https://www.xkcd.com/',
		}
		skuObj['AppIdentityInstallOnDevicesButton'] = {
			'actionType': 'OpenApp',
			'label': 'Open Movies & TV',
			'uri': 'https://www.xkcd.com/',
		}
		skuObj['SubscriptionMessage'] = {
			'value': f'subscriptionMessage-{skuId}',
		}
		skuObj["OwnershipMessage"] = {
			"value": "You own this product",
		}
		skuObj['PreorderAvailabilityMessage'] = {
			'value': 'Coming soon'
		}
	return obj


# @mods.add
def duplicate_images(obj):
	imgs = obj['productInfo']['images']
	for skuObj in obj['skuInfo'].values():
		skuObj['images'] = deepcopy(imgs)
	return obj


# @mods.add
def clarify_price(obj):
	for skuId, skuObj in obj['skuInfo'].items():
		if skuObj['price'] is None:
			continue
		skuObj['price']['currentPrice'] += f' - {skuId}'

	return obj


# @mods.add
def product_metadata(obj):
	obj['metadata'] = [
		{
			'text': '2023',
		},
		{
			'text': 'Action/Adventure',
			'type': 'genre'
		},
		{
			'text': 'Sci-Fi/Fantasy',
			'type': 'genre'
		},
		{
			'text': '1 h 55 min',
			'type': 'text'
		},
		{
			'text': 'English audio',
			'type': 'text'
		},
		{
			'text': 'CC',
			'alt': 'Closed Captions',
			'type': 'badge'
		},
		{
			'text': 'HDR',
			'alt': 'High Dynamic Range',
			'type': 'badge'
		},
		{
			'text': 'PG-13',
			'alt': 'For ages 13 and up',
			'type': 'badge'
		},
	]

	for metaIdx, metaObj in enumerate(obj['metadata']):
		metaObj['id'] = metaIdx

	return obj


# @mods.add
def description(obj):
	# obj['productInfo']['description'] = 'A research team on an exploratory dive into the depths of the ocean are pitted against colossal, prehistoric sharks. To survive, they must outrun, outsmart and outswim these predators.'
	obj['productInfo']['description'] = '''Lorem ipsum odor amet, consectetuer adipiscing elit. Amet metus curabitur consequat enim lacus iaculis. Pellentesque curae ipsum elementum senectus egestas feugiat.'''
	for skuInfo in obj['skuInfo'].values():
		skuInfo['description'] = 'Sku ' + obj['productInfo']['description']
	return obj


# @mods.add
def fix_casing(obj):
	dict_to_camel(obj['pageData'])

	for skuObj in obj['skuInfo'].values():
		if 'CallToAction' not in skuObj:
			continue

		dict_to_camel(skuObj['CallToAction'])
		if 'enabledConditions' in skuObj['CallToAction']:
			list_to_camel(skuObj['CallToAction']['enabledConditions'])

	list_to_camel(obj['productInfo']['images'])

	list_to_camel(obj['selectors'])
	for selector in obj['selectors']:
		list_to_camel(selector['selectionItems'])

	return obj


# @mods.add
def remove_nulls(obj):
	for m in obj['metadata']:
		if m['alt'] is None:
			del m['alt']
	return obj


# @mods.add
def mock_image(obj):
	imgs: list = obj['productInfo']['images']
	bg_imgs = list(filter(lambda i: i['purpose'].lower() == 'background', imgs))
	if len(bg_imgs) != 0:
		# width = bg_imgs[0]['width']
		# height = bg_imgs[0]['height']
		width = 2160
		height = 3840

		width = 600
		height = 800

		bg_imgs[0]['baseUri'] = f'https://picsum.photos/{width}/{height}'

	return obj


@mods.add
def fake_price(obj):
	print('bb_mod: Fake price')
	for skuId, skuObj in obj['skuInfo'].items():
		skuObj['price'] = {
			'currentPrice': f'$1.99',
			'originalPrice': f'$19.99',
			'currencyCode': 'USD',
			'priceType': 'Purchase',
		}
	return obj


# @mods.add
def pricing_message(obj):
	print('bb_mod: Pricing message')
	for skuId, skuObj in obj['skuInfo'].items():
		print(skuObj)
		skuObj['PricingMessage'] = {
			# 'value': skuObj.get('buyOrRentInAnyFormatMessage', {}).get('value')
			'value': f'PricingMessage-{skuId}'
		}
		skuObj['DiscountMessage'] = {
			'value': f'DiscountMessage-{skuId}'
		}
	return obj


def list_to_camel(l: list[dict]) -> None:
	for x in l:
		dict_to_camel(x)


def dict_to_camel(d: dict) -> None:
	k_map = {k: to_camel(k) for k in d}
	for k_old, k_new in k_map.items():
		d[k_new] = d[k_old]
		if k_new != k_old:
			del d[k_old]


def to_camel(s: str) -> str:
	return s[0].lower() + s[1:]
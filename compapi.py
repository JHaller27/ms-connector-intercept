from func_mods import FuncMods
from enum import StrEnum
from copy import deepcopy


class ProductActionType(StrEnum):
    PushToInstall = 'InstallOnDevices'
    BuildABundle = 'BuildABundle'
    AddToCart = 'AddToCart'
    ConfigureDevice = 'ConfigureDevice'
    Manage = 'Manage'
    OutOfStock = 'OUTOFSTOCK'
    NotAvailable = 'NOTAVAILABLE'
    AddToWishlist = 'AddToWishlist'
    Buy = 'Buy'


mods = FuncMods()


@mods.add
def title_image(obj):
	print('Mod: title_image')

	for sku in obj['product']['skuInfo'].values():
		sku: dict
		sku['displayImage'] = {
			"uri": "https://placehold.co/400x600.png",
			"purpose": "tile",
			"alt": "The Meg 2: The Trench",
			"height": 600,
			"width": 400,
			"imagePosition": "",
			"system": "rtdam",
		}
	return obj


@mods.add
def ownership(obj):
	print('Mod: ownership')

	for skuId, sku in obj['product']['skuInfo'].items():
		sku: dict
		sku['ownershipStatus'] = f'ownershipStatus-{skuId}'
		sku['subscriptionMessage'] = f'subscriptionMessage-{skuId}'
		sku['ownershipGlyph'] = f'my-movies-tv'
		sku['ownershipActions'] = _getOwnershipActions()
	return obj


@mods.add
def selectors(obj):
    if obj['product']['productId'].upper() != '8D6KGWXXGKW4':
        return obj

    print('bb_mod: Selectors')

    additional_sku_ids = {
        '0005': ['0001'],
        '0004': ['0002'],
        '0009': ['0003'],
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
        'focusRank': 620,
    }
    for sku_id, addl_sku_ids in additional_sku_ids.items():
        obj['product']['skuInfo'][sku_id]['CallToAction'] = deepcopy(new_cta) | {'label': 'Buy $123'}
        for asku_id in addl_sku_ids:
            obj['product']['skuInfo'][asku_id]['CallToAction'] = deepcopy(new_cta) | {'label': 'Rent $45'}
            obj['product']['skuInfo'][sku_id]['CallToAction'].setdefault('moreCtaSkus', []).append(asku_id)

    # Trim skuMap & selectors
    obj['product']['skuOrder'] = {
        '0': ['0005'],
        '1': ['0004'],
        '2': ['0009'],
    }
    obj['selectorInfo'][0]['selectionItems'] = [
        {'label': 'SD', 'skuId': '0005'},
        {'label': 'HD', 'skuId': '0004'},
        {'label': 'UHD', 'skuId': '0009'},
    ]

    return obj



def _getAction(text = 'foobar-actTxt', uri = 'https://www.xkcd.com/'):
	obj = {
		'action': ProductActionType.Buy,
		'actionText': text,
		'actionTextSecondary': 'foobar-actTxt2',
		'behaviorTag': 0,
		'disabled': False,
		# 'renderFormat'?: string,
		'uri': uri,
		# 'availabilityId'?: string,
		# 'skuId'?: string,
	}
	return obj


def _getOwnershipActions():
	obj = {
		'primary': _getAction('Watch', 'https://xkcd.com/1'),
		'secondary': [_getAction('Open Movies & TV', 'https://xkcd.com/2')],
		'expand': True,
	}
	return obj

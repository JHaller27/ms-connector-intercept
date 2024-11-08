from mods.func_mods import FuncMods


mods = FuncMods()


# @mods.add
def fix_prices(obj: dict):
    for x in obj['otherSeasons']:
        x['price'] = x['price']['listPriceString']

    for x in obj['episodes']:
        x['price'] = '$%s' % x['price']['currentValue']

    return obj

def updateBuyPaylod(paylod, request, value_to_set):
    for item in value_to_set.items():
        paylod[item[0]] = item[1]
    return paylod    
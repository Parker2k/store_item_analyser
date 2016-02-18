import json
import csv


if __name__ == "__main__":
    with open('data/tesco_and_asda_upcs.txt') as upcs:
        upc_set = frozenset(line.rstrip() for line in upcs)

    with open('data/JSON_RAW/tesco_name_upc.json', encoding='utf-8') as tesco:
        data = json.load(tesco)
        tescoProductsWithMatchedUpcs = [datum for datum in data if datum['upc'] in upc_set]

    with open('data/JSON_RAW/asda_name_upc.json', encoding='utf-8') as asda:
        data = json.load(asda)
        asdaProductsWithMatchedUpcs = [datum for datum in data if datum['upc'] in upc_set]

    with open('tesco_asda_upc_name.csv', 'w', encoding='utf-8') as dataFile:
        data = []
        new_list = []
        writer = csv.writer(dataFile, lineterminator='\n')
        for i, datum in enumerate(tescoProductsWithMatchedUpcs):
            for k, datum1 in enumerate(asdaProductsWithMatchedUpcs):
                if datum['upc'] == datum1['upc']:
                    # new_product = datum['name'].lower() + ' ' + datum1['name'].lower()
                    # new_list.append([' '.join(set(new_product.split()))])

                    data = [datum['upc'], tescoProductsWithMatchedUpcs[i]['name'],
                            asdaProductsWithMatchedUpcs[k]['name']]
                    writer.writerow(data)

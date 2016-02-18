from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from operator import itemgetter
import gc
import csv


# initialises list to memory by loading each file and making it a list
def initialise_list():
    data = []
    with open('data/tesco_asda_upc_name.csv', encoding='utf-8') as mainFile:
        reader = csv.reader(mainFile)

        for csvRow in reader:
            data.extend([csvRow])
        # structure of CSV without headers - UPC, Tesco, Asda
        upcnum = []
        tesco_item = []
        asda_item = []

        for row in data:
            upcnum.append(row[0].lower())
            tesco_item.append(row[1].lower())
            asda_item.append(row[2].lower())

        data = [upcnum, tesco_item, asda_item]
        return data

if __name__ == "__main__":
    tfidf_vectorizer = TfidfVectorizer()
    newList = []
    dataSet = initialise_list()
    upc = dataSet[0]
    cached_list = dataSet[1]
    search_terms = dataSet[2]
    csv_result = []
    # fit_transform the learning set
    cached_list_matrix = tfidf_vectorizer.fit_transform(cached_list)
    # transform the set you want to match
    search_term_matrix = tfidf_vectorizer.transform(search_terms)
    gc.collect()
    cosine_similarities = cosine_similarity(search_term_matrix, cached_list_matrix)

    for i, row in enumerate(cosine_similarities):
        search_vector = cosine_similarities[i]
        search_term = search_terms[i]
        expected_term = cached_list[i]
        upc_num = upc[i]
        search_vector_with_upc = zip(upc, cached_list, search_vector)
        results = sorted(search_vector_with_upc, key=lambda quality: -quality[2])

        for result in results[:1]:
            if result[0] == upc_num:
                match = True
            else:
                match = False
            # CSV structure
            # UPC NUMBER|SEARCH TERM(Tesco)|MATCHED TERM(asda)|
            #                                   |MATCHED UPC|TDIDF SCORE|EXPECTED TERM(Tesco)| MATCH?
            csv_result.append([upc_num, search_term, result[1],
                               result[0], result[2], expected_term, int(match)])

    sorted_by_name = sorted(csv_result, key=itemgetter(1))
    sorted_by_quality = sorted(sorted_by_name, key=itemgetter(4), reverse=True)

    with open('csvdump1.csv', 'w', encoding='utf-8') as data_file:
        writer = csv.writer(data_file,  lineterminator='\n')
        writer.writerow(['UPC NUMBER', 'SEARCH TERM(Tesco)', 'MATCHED TERM(asda)',
                         'MATCHED UPC', 'TDIDF SCORE', 'EXPECTED TERM(Tesco)', 'MATCHED?'])
        writer.writerows(sorted_by_quality)

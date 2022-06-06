import pathlib
import progressbar
import sys
import wget
import json
import gzip
import csv

# review types to get
types = ['reviews_Books_5', 'reviews_Electronics_5', 'reviews_Sports_and_Outdoors_5', 'reviews_Video_Games_5', 'reviews_Baby_5']
#types = ['reviews_Baby_5']

# paths
url_format = 'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/{type}.json.gz'
file_in_format = './{type}.json.gz'
file_out_format = './{type}.csv'
# the data folder should be a sylbing to the folder this file is in
data_folder = pathlib.Path(__file__).parent.joinpath('../data').resolve()

# download all the data
for type in types:
    print('downloading {type}'.format(type = type))
    curr_url = url_format.format(type = type)
    curr_file = str(data_folder.joinpath(file_in_format.format(type = type)))
    wget.download(curr_url, curr_file)

# convert the files to a format useable by LIWC
for type in types:
    print('processing {type} into form compatable with LIWC'.format(type = type))
    
    file_in = data_folder.joinpath(file_in_format.format(type = type))
    file_out = data_folder.joinpath(file_out_format.format(type = type))

    # add in a progress bar because this is a _long_ process and we may want to take a nap
    line_number = 0
    with progressbar.ProgressBar(max_value = progressbar.UnknownLength) as bar:
        with gzip.open(file_in, 'r') as file_in:
            with open(file_out, 'w', encoding = 'utf-8', newline = '') as file_out:
                writer = csv.writer(file_out, delimiter = ',', quoting = csv.QUOTE_NONE)
                writer.writerow(['asin', 'reviewerID', 'reviewText'])
                for line in file_in:
                    bar.update(line_number)
                    review = eval(line)
                    asin = review['asin']
                    reviewerID = review['reviewerID']
                    # it can work over a CSV, but does not respect escaped commas which produces a bad result
                    reviewText = review['reviewText'].replace(',', '').replace('"', '').strip()
                    try:
                        writer.writerow([asin, reviewerID, reviewText])
                    except:
                        print('issue found')
                        print('asin: ' + asin)
                        print('reviewerID: ' + reviewerID)
                        print('reviewText: ' + reviewText)
                line_number = line_number + 1
            pass
        pass
    pass
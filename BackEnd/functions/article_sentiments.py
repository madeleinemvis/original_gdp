from csv import DictReader
import sys
import csv
from csv import DictWriter
from afinn import Afinn



class PredictSentiment:

    # making sure really long csv fields could be read and processed
    maxInt = sys.maxsize

    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

    # reads in a csv file
    def read(self, filename):
        rows = []
        with open(filename, "r", encoding='utf-8-sig',errors='ignore') as table:
            r = DictReader(table)
            for line in r:
                rows.append(line)
        return rows

    # extracts the text bodies from a csv file and puts them in a dictionary
    def readBodies(self,file_bodies):
        bodies_read = {}
        bodies = self.read(file_bodies)
        for body in bodies:
            bodies_read[int(float(body['Body ID']))] = body['articleBody']
        return bodies_read

    # returns a predicted sentiment for an input text 
    def get_article_sentiment_Afinn(self, article: str) -> str:
        af = Afinn()
        analysisPol = af.score(article)
        if analysisPol > 0:
            return 'positive'
        elif analysisPol == 0:
            return 'neutral'
        else:
            return 'negative'

    # loops throuh a dictionary of text bodies, gets each text body's sentiment and writes it to a csv file (not currently used)
    def getPredictions(self, file):
        bodies_read=self.readBodies(file)
        with open('./sentiment_predictions.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Body ID', 'Sentiment']
            writer = DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
            writer.writeheader()
            for index in range(len(bodies_read)):
                writer.writerow({'Body ID': index, 'Sentiment': self.get_article_sentiment_Afinn(bodies_read[index])})


if __name__ == "__main__":
    p = PredictSentiment()


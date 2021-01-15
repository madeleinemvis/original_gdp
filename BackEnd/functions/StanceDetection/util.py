# Adapted from @amazingclaude/Fake_News_Stance_Detection

from csv import DictReader
from csv import DictWriter
import numpy as np
from io import StringIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .refuting import refuting_features_title, refuting_features_body, mutual_information_title, mutual_information_body

label_ref = {'agree': 0, 'disagree': 1, 'discuss': 2, 'unrelated': 3}
label_ref_rev = {0: 'agree', 1: 'disagree', 2: 'discuss', 3: 'unrelated', 4: 'agree', 5: 'disagree', 6: 'discuss',
                 7: 'unrelated', 8: 'agree', 9: 'disagree', 10: 'discuss', 11: 'unrelated'}
stop_words = [
    "a", "about", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along",
    "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as", "at", "back", "be",
    "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "co",
    "con", "could", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight",
    "either", "eleven", "else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill", "find", "fire", "first", "five", "for",
    "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had",
    "has", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself",
    "him", "himself", "his", "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed", "interest",
    "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made",
    "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much",
    "must", "my", "myself", "name", "namely", "neither", "nevertheless", "next", "nine", "nobody", "now", "nowhere",
    "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours",
    "ourselves", "out", "over", "own", "part", "per", "perhaps", "please", "put", "rather", "re", "same", "see",
    "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some",
    "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take",
    "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though",
    "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve",
    "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what",
    "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon",
    "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will",
    "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves"
]


# Define data class
class FNCData:


    def __init__(self, file_instances, file_bodies):
        self.instances = self.read(file_instances)
        bodies = self.read(file_bodies)
        self.heads = {}
        self.bodies = {}

        # Process instances
        for instance in self.instances:
            if instance['Headline'] not in self.heads:
                head_id = len(self.heads)
                self.heads[instance['Headline']] = head_id
            instance['Body ID'] = int(instance['Body ID'])

        # Process bodies
        for body in bodies:
            self.bodies[int(float(body['Body ID']))] = body['articleBody']

    def read(self, filename):

        rows = []

        # reads in from a file, if the file contains text from pdf, all the null bytes are removed 
        with open(filename, "r", encoding='utf-8-sig', errors='ignore') as table:
            data = table.read()
            data = data.replace('\x00', '?')
            r = DictReader(StringIO(data))
            for line in r:
                rows.append(line)

        return rows


# Define tf, tf-idf functions
# taken from  @amazingclaude/Fake_News_Stance_Detection
def bow_train(train, test, lim_unigram):
    """

    Process train set, create relevant vectorizers

    Args:
        train: FNCData object, train set
        test: FNCData object, test set
        lim_unigram: int, number of most frequent words to consider

    Returns:

        bow_vectorizer: sklearn CountVectorizer
        tfreq_vectorizer: sklearn TfidfTransformer(use_idf=False)
        tfidf_vectorizer: sklearn TfidfVectorizer()

    """
    heads = []
    heads_track = {}
    bodies = []
    bodies_track = {}
    body_ids = []

    test_heads = []
    test_heads_track = {}
    test_bodies = []
    test_bodies_track = {}
    test_body_ids = []

    id_ref = {}
    # Identify unique heads and bodies
    for instance in train.instances:
        head = instance['Headline']
        body_id = instance['Body ID']
        if head not in heads_track:
            heads.append(head)
            heads_track[head] = 1
        if body_id not in bodies_track:
            bodies.append(train.bodies[body_id])
            bodies_track[body_id] = 1
            body_ids.append(body_id)

    for instance in test.instances:
        head = instance['Headline']
        body_id = instance['Body ID']
        if head not in test_heads_track:
            test_heads.append(head)
            test_heads_track[head] = 1
        if body_id not in test_bodies_track:
            test_bodies.append(test.bodies[body_id])
            test_bodies_track[body_id] = 1
            test_body_ids.append(body_id)


    # Create vectorizers and BOW and TF arrays for train set
    bow_vectorizer = CountVectorizer(max_features=lim_unigram, stop_words=stop_words)
    bow = bow_vectorizer.fit_transform(heads + bodies)  # Train set only
    # bow_train_only=bow_vectorizer.fit_transform(heads + bodies)

    tfreq_vectorizer = TfidfTransformer(use_idf=False).fit(bow)
    # tfreq = tfreq_vectorizer.transform(bow_train_only).toarray()  # Train set only

    tfidf_vectorizer = TfidfVectorizer(max_features=lim_unigram, stop_words=stop_words).fit(
        heads + bodies + test_heads + test_bodies)  # Train and test sets

    return bow_vectorizer, tfreq_vectorizer, tfidf_vectorizer

# taken from  @amazingclaude/Fake_News_Stance_Detection
def pipeline_test(dataset_number, test, bow_vectorizer, tfreq_vectorizer, tfidf_vectorizer):
    """

    Process test set

    Args:
        dataset_number:Choose which feature as the input
        test: FNCData object, test set
        bow_vectorizer: sklearn CountVectorizer
        tfreq_vectorizer: sklearn TfidfTransformer(use_idf=False)
        tfidf_vectorizer: sklearn TfidfVectorizer()

    Returns:
        test_set: list, of numpy arrays

    """

    
    feat_vec = []
    test_set = []

    heads_track = {}
    bodies_track = {}
    head_refuting_track = {}
    body_refuting_track = {}
    head_mutual_track = {}
    body_mutual_track = {}
    word2vec_track = {}
    wmd_track = {}
    cos_track = {}

    # Process test set
    for instance in test.instances:
        head = instance['Headline']
        body_id = instance['Body ID']
        if head not in heads_track:
            head_bow = bow_vectorizer.transform([head]).toarray()
            head_tf = tfreq_vectorizer.transform(head_bow).toarray()[0].reshape(1, -1)
            head_tfidf = tfidf_vectorizer.transform([head]).toarray().reshape(1, -1)
            heads_track[head] = (head_tf, head_tfidf)
        else:
            head_tf = heads_track[head][0]
            head_tfidf = heads_track[head][1]
        if body_id not in bodies_track:
            body_bow = bow_vectorizer.transform([test.bodies[body_id]]).toarray()
            body_tf = tfreq_vectorizer.transform(body_bow).toarray()[0].reshape(1, -1)
            body_tfidf = tfidf_vectorizer.transform([test.bodies[body_id]]).toarray().reshape(1, -1)
            bodies_track[body_id] = (body_tf, body_tfidf)
        else:
            body_tf = bodies_track[body_id][0]
            body_tfidf = bodies_track[body_id][1]
        if (head, body_id) not in cos_track:
            tfidf_cos = cosine_similarity(head_tfidf, body_tfidf)[0].reshape(1, 1)
            cos_track[(head, body_id)] = tfidf_cos
        else:
            tfidf_cos = cos_track[(head, body_id)]

        # =====Creating refuting/MI words vector=====================
        if dataset_number == 2:
            if head not in head_refuting_track:
                head_refuting_vector = refuting_features_title(head)
                head_refuting_track[head] = head_refuting_vector
            else:
                head_refuting_vector = head_refuting_track[head]

            if body_id not in body_refuting_track:
                body_refuting_vector = refuting_features_body(test.bodies[body_id])
                body_refuting_track[body_id] = body_refuting_vector
            else:
                body_refuting_vector = body_refuting_track[body_id]

        if dataset_number == 3:
            if head not in head_mutual_track:
                head_mutual_information = mutual_information_title(head)
                head_mutual_track[head] = head_mutual_information
            else:
                head_mutual_information = head_mutual_track[head]

            if body_id not in body_mutual_track:
                body_mutual_information = mutual_information_body(test.bodies[body_id])
                body_mutual_track[body_id] = body_mutual_information
            else:
                body_mutual_information = body_mutual_track[body_id]

        # =================concatenating feature vectors==============.
        if dataset_number == 1:
            feat_vec = np.squeeze(np.c_[head_tf, body_tf, tfidf_cos])
            test_set.append(feat_vec)
        if dataset_number == 2:
            feat_vec = np.squeeze(np.c_[head_tf, body_tf, tfidf_cos, head_refuting_vector, body_refuting_vector])
            test_set.append(feat_vec)
        if dataset_number == 3:
            feat_vec = np.squeeze(np.c_[head_tf, body_tf, tfidf_cos, head_mutual_information, body_mutual_information])
            test_set.append(feat_vec)
    return test_set

# writes the stance predictions next to ech text body ID into a csv file (not currently used)
def save_predictions(pred):
    with open('./stance_predictions.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Body ID', 'Stance']
        writer = DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        for index, instance in enumerate(pred):
            writer.writerow({'Body ID': index, 'Stance': label_ref_rev[instance]})

# returns a dictionary in the form {url1: stance1, url2: stance2...}
def get_predictions(pred, urls):
    predictions = {}
    for index, instance in enumerate(pred):
        predictions[urls[index].url] = label_ref_rev[instance]

    return predictions


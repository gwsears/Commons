import os
import re
import nltk
import pandas as pd
import gensim
import string
from nltk.tokenize.moses import MosesTokenizer

stopw = gensim.parsing.preprocessing.STOPWORDS
punc = string.punctuation
punc = punc + "●" + "•" + "-" + "ø"
tokenizer = nltk.tokenize.moses.MosesTokenizer()
stemmer = nltk.stem.snowball.SnowballStemmer("english")
stoplist = nltk.corpus.stopwords.words('english')
wht_space = set('\t\r\x0b\x0c')
name_file_path = os.path.join("C:\\Users", os.getlogin(), r"\IPython Books\Perseus Notebooks\Data\name_list.csv")
name_list = pd.read_csv(name_file_path)
name_list = name_list['names'].tolist()
name_list = set(name_list)
month_list = ["jan", "january" "feb", "february", "mar", "march", "apr", "april", "may", "jun", "june", "jul", "july",
              "aug", "august", "sep", "sept", "september", "oct", "october", "nov", "november", "dec", "december"]
number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

bigram = gensim.models.Phrases.load(os.path.join("C:\\Users", os.getlogin(), r"C:\Users\erics_qp7a9\Google Drive\IPython Books\trigram_model.p"))
bigrammer = gensim.models.phrases.Phraser(bigram)


def remove_noise(text, sent=False):
    # CV/Resume Specific Cleaning
    regex_email = re.compile(r"((\w|\d|\.)+)(@)(\w+)(\.)(\w{3})")
    regex_dates = re.compile(r"([A-z]+\.? ?\d{2,4}| +- (P|p)resent)|(\d{2}\/\d{2}\/\d{2,4})")
    regex_phone_numbers = re.compile(r"(\d{3}(-|.)){2}(\d{4})")
    regex_three_or_more = re.compile(r"\w*(.)(\1){2,}\w*")  # If a word contains a series of 3 or more identical letters
    regex_bullets = re.compile(r"(•|✓|#|\*|●  *)|(\d[.|:])|( ?- )")
    regex_hyperlinks = re.compile(r"(http)([a-z]|[A-Z]|[\d]|\.|\/|\?|\=|&|:|-)+")
    regex_numbers_only = re.compile(r"\d+[^A-z]")
    regex_punctuation = re.compile(
        r"(!|\"|#|\$|%|&|\||\)|\(|\*|\+|,|-|\.|\/|:|;|<|=|>|\?|@|\[|\\|\]|\^|_|`|\{|\||\}|~|')")
    if sent:
        for space in wht_space:
            text.replace(space, "\n")
        sent_holder = nltk.tokenize.sent_tokenize(text)
        quiet_sents_clean = []
        for sent in sent_holder:
            sent = regex_phone_numbers.sub(" ", sent)
            sent = regex_email.sub(" ", sent)
            sent = regex_hyperlinks.sub(" ", sent)
            sent = regex_three_or_more.sub(" ", sent)
            sent = regex_numbers_only.sub(" ", sent)
            sent = regex_punctuation.sub(" ", sent)
            sent = sent.lower()
            for space in set(string.whitespace):
                sent.replace(space, " ")
            sent = tokenizer.tokenize(sent)
            sent = ' '.join([word for word in sent if word not in stopw and word not in stoplist
                             and word not in name_list and word not in punc and word not in month_list and word_number_test(
                word) is True])
            quiet_sents_clean.append(sent)
        return quiet_sents_clean

    else:
        quiet_text = text
        quiet_text = regex_phone_numbers.sub(" ", quiet_text)
        quiet_text = regex_email.sub(" ", quiet_text)
        quiet_text = regex_hyperlinks.sub(" ", quiet_text)
        quiet_text = regex_dates.sub(" ", quiet_text)
        quiet_text = regex_three_or_more.sub(" ", quiet_text)
        quiet_text = regex_bullets.sub(" ", quiet_text)
        quiet_text = regex_numbers_only.sub(" ", quiet_text)
        quiet_text = regex_punctuation.sub(" ", quiet_text)
        clean_text = quiet_text.lower()
        for space in set(string.whitespace):
            clean_text.replace(space, " ")
            clean_text = tokenizer.tokenize(clean_text)
            clean_text = ' '.join([word for word in clean_text if word not in stopw and word not in stoplist
                                   and word not in name_list and word not in punc and word not in month_list and word_number_test(
                word) is True])
    return clean_text


def word_number_test(word):
    if any(num in word for num in number_list):
        word_length = len(word)
        number_count = 0
        for letter in word:
            if letter in number_list:
                number_count += 1
        ratio = number_count / word_length
        if ratio >= 0.1:
            return False
        else:
            return True
    else:
        return True


def document_to_tokens(clean_text, lem_tokens):
    tokens = tokenizer.tokenize(clean_text)
    if lem_tokens:
        pos_tokens = nltk.pos_tag(tokens)
        stemmed_tokens = token_stemmer(pos_tokens)
        return stemmed_tokens
    else:
        tokens = ' '.join(tokens)
        return tokens


def token_stemmer(pos_tagged_tokens):
    lemmatizer = nltk.WordNetLemmatizer()
    stemmed_tokens = []
    for tagged_tuple in pos_tagged_tokens:
        token = tagged_tuple[0]
        pos_tag = get_wordnet_pos(tagged_tuple[1])
        if pos_tag is False:
            lemmed_token = lemmatizer.lemmatize(token)
        else:
            lemmed_token = lemmatizer.lemmatize(token, pos_tag)
        stemmed_tokens.append(lemmed_token)
    stem_join_tokens = ' '.join(token for token in stemmed_tokens)
    return stem_join_tokens


# https://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
def get_wordnet_pos(treebank_tag):
    wordnet = nltk.corpus.wordnet
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return False


def clean_it(text, lem_tokens=True, gram_tokens=True, sent_mode=False):
    quiet_text = remove_noise(text, sent=sent_mode)  # sent_mode will return a list of sentences
    if sent_mode:
        sent_holder = []
        for sent in quiet_text:  # String form
            if lem_tokens:
                sent = document_to_tokens(sent, lem_tokens=True)  # returns String form
            if gram_tokens:  # Must be list form
                sent = sent.split()  # List form
                clean_tokens = bigrammer[sent]
                continue_gram = True
                while continue_gram is True:
                    new_tokens = bigrammer[clean_tokens]  # Detect new phrases, must be tokens
                    if clean_tokens != new_tokens:
                        clean_tokens = new_tokens
                    else:
                        sent = new_tokens  # List form
                        sent = ' '.join(new_tokens)  # String rom
                        continue_gram = False
            sent_holder.append(sent)  # sent clean complete, append
            # Sent Holder Ready
        return sent_holder
    elif sent_mode is False:
        if lem_tokens:
            text_tokens = document_to_tokens(quiet_text, lem_tokens=True)
        else:
            text_tokens = document_to_tokens(quiet_text, lem_tokens=False)
        text_tokens = text_tokens.split()
        clean_tokens = ' '.join(
            [token for token in text_tokens if len(token) > 2 and token not in stopw and token not in punc])
        clean_tokens = clean_tokens.split()
        if gram_tokens:
            clean_tokens = bigrammer[clean_tokens]
            continue_gram = True
            while continue_gram is True:
                new_tokens = bigrammer[clean_tokens]  # Detect new phrases, must be tokens
                if clean_tokens != new_tokens:
                    clean_tokens = new_tokens
                else:
                    continue_gram = False
        clean_tokens = ' '.join(clean_tokens)
        return clean_tokens

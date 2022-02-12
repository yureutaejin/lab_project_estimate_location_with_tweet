#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Library
from rake_nltk import Rake
import pandas as pd
import json
import sys

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scipy import sparse
from gensim.models import word2vec

import re
import string


# In[2]:


# words for preprocessing
# %%
stop_words = list([
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves", "A", "About", "Above", "Across", "After", "Afterwards", "Again", "Against",
    "All", "Almost", "Alone", "Along", "Already", "Also", "Although", "Always",
    "Am", "Among", "Amongst", "Amoungst", "Amount", "An", "And", "Another",
    "Any", "Anyhow", "Anyone", "Anything", "Anyway", "Anywhere", "Are",
    "Around", "As", "At", "Back", "Be", "Became", "Because", "Become",
    "Becomes", "Becoming", "Been", "Before", "Beforehand", "Behind", "Being",
    "Below", "Beside", "Besides", "Between", "Beyond", "Bill", "Both",
    "Bottom", "But", "By", "Call", "Can", "Cannot", "Cant", "Co", "Con",
    "Could", "Couldnt", "Cry", "De", "Describe", "Detail", "Do", "Done",
    "Down", "Due", "During", "Each", "Eg", "Eight", "Either", "Eleven", "Else",
    "Elsewhere", "Empty", "Enough", "Etc", "Even", "Ever", "Every", "Everyone",
    "Everything", "Everywhere", "Except", "Few", "Fifteen", "Fifty", "Fill",
    "Find", "Fire", "First", "Five", "For", "Former", "Formerly", "Forty",
    "Found", "Four", "From", "Front", "Full", "Further", "get", "give", "go",
    "Had", "Has", "Hasnt", "Have", "He", "Hence", "Her", "Here", "Hereafter",
    "Hereby", "Herein", "Hereupon", "Hers", "Herself", "Him", "Himself", "His",
    "How", "However", "Hundred", "I", "Ie", "If", "In", "Inc", "Indeed",
    "Interest", "Into", "Is", "It", "Its", "Itself", "Keep", "Last", "Latter",
    "Latterly", "Least", "Less", "Ltd", "Made", "Many", "May", "Me",
    "Meanwhile", "Might", "Mill", "Mine", "More", "Moreover", "Most", "Mostly",
    "Move", "Much", "Must", "My", "Myself", "Name", "Namely", "Neither",
    "Never", "Nevertheless", "Next", "Nine", "No", "Nobody", "None", "Noone",
    "Nor", "Not", "Nothing", "Now", "Nowhere", "Of", "Off", "Often", "On",
    "Once", "One", "Only", "Onto", "Or", "Other", "Others", "Otherwise", "Our",
    "Ours", "Ourselves", "Out", "Over", "Own", "Part", "Per", "Perhaps",
    "Please", "Put", "Rather", "Re", "Same", "See", "Seem", "Seemed",
    "Seeming", "Seems", "Serious", "Several", "She", "Should", "Show", "Side",
    "Since", "Sincere", "Six", "Sixty", "So", "Some", "Somehow", "Someone",
    "Something", "Sometime", "SometimeS", "Somewhere", "Still", "Such",
    "System", "Take", "Ten", "Than", "That", "The", "Their", "Them",
    "Themselves", "Then", "Thence", "There", "Thereafter", "Thereby",
    "Therefore", "Therein", "Thereupon", "These", "They", "Thick", "Thin",
    "Third", "This", "Those", "Though", "Three", "Through", "Throughout",
    "Thru", "Thus", "To", "Together", "Too", "Top", "Toward", "Towards",
    "Twelve", "Twenty", "Two", "Un", "Under", "Until", "Up", "Upon", "Us",
    "Very", "Via", "Was", "We", "Well", "Were", "What", "Whatever", "When",
    "Whence", "Whenever", "Where", "Whereafter", "Whereas", "Whereby",
    "Wherein", "Whereupon", "Wherever", "Whether", "Which", "While", "Whither",
    "Who", "Whoever", "Whole", "Whom", "Whose", "Why", "Will", "With",
    "Within", "Without", "Would", "Yet", "You", "Your", "Yours", "Yourself",
    "Yourselves"])


# In[3]:


# function

# %% keywords split해서 하나로 합쳐주기

def listsum(inputlist):
    results = []
    listlen = len(inputlist)
    for i in range(listlen):
        temp = inputlist[i].split(" ")
        for j in range(len(temp)):
            if (len(temp[j]) > 2):
                results.append(temp[j])

    results = list(dict.fromkeys(results))
    return results

# %% 수정본 , rank 값이 1보다 큰 애들 적용

def extractor(newsset, stop_words):
    # stop_words = stopwords.words('english')
    r1 = Rake(stopwords=stop_words)
    # r2 = Rake()
    title = newsset['Title']
    title = preprocess_news(title)
    news = newsset['text']
    news = preprocess_news(news)
    # date = newsset['Date']
    # keyword = []
    r1.extract_keywords_from_text(title)
    r1.get_ranked_phrases()
    title_scores = r1.get_ranked_phrases_with_scores()

    r1.extract_keywords_from_text(news)
    r1.get_ranked_phrases()
    text_scores = r1.get_ranked_phrases_with_scores()

    # keyword.append(news_scores[i][1])
    # keyword.append(title_scores[i][1])
    title_tp = []
    text_tp = []
    new_text_scores = text_scores[:10]  # int(len(text_scores)/10)]
    for data in new_text_scores:
        text_tp.append(data[1])

    for i in range(len(title_scores)):
        if ((title_scores[i][0]) > 1):
            title_tp.append(title_scores[i][1])

    # return title_tp,text_tp
    return listsum(title_tp), listsum(text_tp)

# %% keyword extract from title, text no rank

def extractor_norank(newsset, stop_words):
    # stop_words = stopwords.words('english')
    r1 = Rake(stopwords=stop_words)
    # r2 = Rake()
    title = newsset['Title']
    # title = preprocess_news(title)
    news = newsset['text']
    # news = preprocess_news(news)

    # date = newsset['Date']
    # keyword = []
    r1.extract_keywords_from_text(title)
    r1.get_ranked_phrases()
    title_scores = r1.get_ranked_phrases_with_scores()

    r1.extract_keywords_from_text(news)
    r1.get_ranked_phrases()
    text_scores = r1.get_ranked_phrases_with_scores()

    # keyword.append(news_scores[i][1])
    # keyword.append(title_scores[i][1])
    title_tp = []
    text_tp = []
    for i in range(len(title_scores)):
        # 랭킹 메기는 것 없앰
        title_tp.append(title_scores[i][1])
        text_tp.append(text_scores[i][1])

    # return title_tp,text_tp
    return listsum(title_tp), listsum(text_tp)

# %%
def remove_emojis(data):
    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
                      u"\U00002702-\U000027B0"
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)


# %%
def preprocess_tweet(text):
    # convert text to lower-case
    nopunc = text.lower()
    nopunc = re.sub("\\’", "'", nopunc)
    nopunc = re.sub("\\'s", "", nopunc)
    nopunc = re.sub("\\'d", "", nopunc)
    nopunc = re.sub("\\'m", "", nopunc)
    nopunc = re.sub("\\'ve", "", nopunc)
    nopunc = re.sub("\\'re", "", nopunc)

    # remove URLs
    nopunc = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '', nopunc)
    nopunc = re.sub(r'http\S+', '', nopunc)
    # remove usernames
    nopunc = re.sub('@[^\s]+', '', nopunc)
    # remove the # in #hashtag
    nopunc = re.sub(r'#([^\s]+)', r'\1', nopunc)
    # remove rt
    nopunc = re.sub('^(rt )', '', nopunc)
    # Check characters to see if they are in punctuation
    nopunc = re.sub("  ", " ", nopunc)

    # \'를 제외했음, it's 같은 '도 생략되어버림.
    punctuations = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'
    result = [char for char in nopunc if char not in punctuations]
    # Join the characters again to form the string.
    result = ''.join(result)

    result = remove_emojis(result)
    return result


# %%
def preprocess_news(inputnews):
    inputnews = inputnews.lower()
    inputnews = re.sub("\\'s", "", inputnews)
    inputnews = re.sub("\\'d", "", inputnews)
    inputnews = re.sub("\\'m", "", inputnews)
    inputnews = re.sub("\\'ve", "", inputnews)
    inputnews = re.sub("\\'re", "", inputnews)

    inputnews = [char for char in inputnews if char not in string.punctuation]
    # Join the characters again to form the string.
    inputnews = ''.join(inputnews)

    return inputnews


# %%


def is_word_in_text(word, text):
    """
    Check if a word is in a text.

    Parameters
    ----------
    word : str
    text : str

    Returns
    -------
    bool : True if word is in text, otherwise False.

    Examples
    --------
    >>> is_word_in_text("Python", "python is awesome.")
    True

    >>> is_word_in_text("Python", "camelCase is pythonic.")
    False

    >>> is_word_in_text("Python", "At the end is Python")
    True
    """
    pattern = r'(^|[^\w]){}([^\w]|$)'.format(word)
    pattern = re.compile(pattern, re.IGNORECASE)
    matches = re.search(pattern, text)
    return bool(matches)

#%%
def tf_vectorizer(filtered_news, filtered_tw, my_stop_words):
    
    tfidf_vectorizer = TfidfVectorizer(stop_words = set(my_stop_words))
    
   
    tfidf_matrix = tfidf_vectorizer.fit_transform([filtered_news,filtered_tw])
    return cosine_similarity(tfidf_matrix[0],tfidf_matrix[1])[0][0]


# In[4]:


# load news json file

# %%
# with open('데이터수집.전처리코드/Data/CNNtest_9_Boston2018.json', encoding="UTF-8") as newsfile:
with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/news_data/2_result_data/2_2018_CNNtest_9_122011.json', encoding="UTF-8") as newsfile:
    newsfile = newsfile.read()
    news_data = json.loads(newsfile)
    newslen = len(news_data['news'])


# In[5]:


# %% without split
resultpd = pd.DataFrame(columns=["Text", "Date"])

for i in range(newslen):
    title_norank, text_norank = (extractor_norank(news_data["news"][i], stop_words))
    title_result, text_result = (extractor(news_data["news"][i], stop_words))
    date = news_data["news"][i]['Date']
    tempdf = pd.DataFrame(
        {"ExtTitle_no": [title_norank], 'ExtText_no': [text_norank], "ExtTitle": [title_result], "Date": date,
         'ExtText': [text_result], "Title": news_data["news"][i]["Title"], "Text": news_data['news'][i]['text']})

    resultpd = resultpd.append(tempdf, ignore_index=True)

# newsmerge = resultpd.groupby(["Date"]).agg({"Title":'sum'}).reset_index()

# %% 상위 10개, 전처리 후
resultpd1 = pd.DataFrame(columns=["Text", "Date"])

for i in range(newslen):
    title_norank, text_norank = (extractor_norank(news_data["news"][i], stop_words))
    title_result, text_result = (extractor(news_data["news"][i], stop_words))
    date = news_data["news"][i]['Date']
    tempdf = pd.DataFrame(
        {"ExtTitle_no": [title_norank], 'ExtText_no': [text_norank], "ExtTitle": [title_result], "Date": date,
         'ExtText': [text_result], "Title": news_data["news"][i]["Title"], "Text": news_data['news'][i]['text']})

    resultpd1 = resultpd1.append(tempdf, ignore_index=True)

# newsmerge = resultpd.groupby(["Date"]).agg({"Title":'sum'}).reset_index()
# %% 상위 10개, 전처리 전
resultpd2 = pd.DataFrame(columns=["Text", "Date"])

for i in range(newslen):
    title_norank, text_norank = (extractor_norank(news_data["news"][i], stop_words))
    title_result, text_result = (extractor(news_data["news"][i], stop_words))
    date = news_data["news"][i]['Date']
    tempdf = pd.DataFrame(
        {"ExtTitle_no": [title_norank], 'ExtText_no': [text_norank], "ExtTitle": [title_result], "Date": date,
         'ExtText': [text_result], "Title": news_data["news"][i]["Title"], "Text": news_data['news'][i]['text']})

    resultpd2 = resultpd2.append(tempdf, ignore_index=True)

# %% 상위 10개, 전처리 후, 샌프란
resultpd3 = pd.DataFrame(columns=["Text", "Date"])

for i in range(newslen):
    title_norank, text_norank = (extractor_norank(news_data["news"][i], stop_words))
    title_result, text_result = (extractor(news_data["news"][i], stop_words))
    date = news_data["news"][i]['Date']
    tempdf = pd.DataFrame(
        {"ExtTitle_no": [title_norank], 'ExtText_no': [text_norank], "ExtTitle": [title_result], "Date": date,
         'ExtText': [text_result], "Title": news_data["news"][i]["Title"], "Text": news_data['news'][i]['text']})

    resultpd3 = resultpd3.append(tempdf, ignore_index=True)


# In[6]:


# newsmerge = resultpd.groupby(["Date"]).agg({"Title":'sum'}).reset_index()
# %%
# with open('C:/Users/cowgi/Desktop/University/bigbaselab/PredictLocation_TweetAndNews/boston_tweet_more_150_everymonth_golbang.json', encoding="UTF-8") as twfile:
with open('/estimate_location_with_tweet/data/tweet_data/4_result_data/boston2_user_filtered_count0.json', encoding="UTF-8") as twfile:
    twfile = twfile.read()
    tw_data = json.loads(twfile)
    usernum = len(tw_data['users'])
    


# In[7]:


# %%
wnews = []
wtweets = []
countlist = []
countlist_no = []
keywordlist = []
keywordlist_no = []
wkeys = []
wkeys_no = []
unions = []

# with open('C:/Users/cowgi/Desktop/University/bigbaselab/PredictLocation_TweetAndNews/CNN_result/join_tweet/200708_1.json', 'a' ,encoding='UTF-8') as tf:
#    sys.stdout = tf
for t in range(usernum):
    try:
        eachuser = tw_data['users'][t]
        username = eachuser['id']
        usertimeline = eachuser['timeline']
        # count = 0

        # datecount = 0
        # print("{\"id : \"%s\":["%(username))
        for i in range(len(usertimeline)):
            date = usertimeline[i]["date"]
            text = preprocess_tweet(usertimeline[i]["text"])
            # text = usertimeline[i]["text"]

            for j in range(len(resultpd3)):
                if (date == resultpd3._get_value(j, "Date")):
                    count = 0
                    count_no = 0
                    keywords = []
                    keywords_no = []
                    for word in resultpd3._get_value(j, "ExtText"):
                        if is_word_in_text(word, text):
                            count += 1
                            keywords.append(word)
                    for word in resultpd3._get_value(j, "ExtText_no"):
                        if is_word_in_text(word, text):
                            count_no += 1
                            keywords_no.append(word)

                    #  n(A)+n(B)
                    unions.append(len(text.split()) + len(resultpd3._get_value(j, "ExtText")))
                    wnews.append(resultpd3._get_value(j, "Title"))
                    wtweets.append(text)
                    countlist.append(count)
                    countlist_no.append(count_no)
                    keywordlist.append(keywords)
                    keywordlist_no.append(keywords_no)
                    wkeys.append(resultpd3._get_value(j, "ExtText"))
                    wkeys_no.append(resultpd3._get_value(j, "ExtText_no"))
    except:
        continue


# In[8]:


#%%
 
Toppd = pd.DataFrame()
 
Toppd["NewsTitle"] = wnews
Toppd["Tweet"] = wtweets
Toppd["howmany"] = countlist
Toppd["matched_kewords"] = keywordlist
Toppd["Extkey"] = wkeys
Toppd["howmany_norank"] = countlist_no
Toppd["matched_kewords_norank"] = keywordlist_no
Toppd["Extkey_norank"] = wkeys_no
Toppd["Union"] = unions
tmp = []
tmp_no = []
for i in range(len(Toppd["Extkey"])):
    tmp.append(len(Toppd["Extkey"][i]))
    tmp_no.append(len(Toppd["Extkey_norank"][i]))
Toppd["numKeys"] = tmp
Toppd["numKeys_norank"] = tmp_no
Toppd["ratio"] = Toppd["howmany"]/Toppd["numKeys"]
Toppd["ratio_norank"] = Toppd["howmany_norank"]/Toppd["numKeys_norank"]
Toppdresult = Toppd
#finalresult = Toppdresult.sort_values(by=["howmany_norank","numKeys_norank"],ascending=[False,True])
finalresult = Toppdresult.sort_values(by=["howmany","Union"],ascending=[False,True])
#finalresult = finalresult.sort_values(by=["numKeys_norank"],ascending=True)
finalresult = finalresult.reset_index(drop=True)
finalresult = finalresult[:200]
 
#finalresult.to_excel("C:/Users/cowgi/Desktop/University/bigbaselab/PredictLocation_TweetAndNews/CNN_result/join_tweet/keywordTop200_sanfransisco.xlsx")
#finalresult.to_excel("C:/Users/cowgi/Desktop/University/bigbaselab/keywordTop200_sort_top10rank_nopre.xlsx")
#finalresult.to_excel("C:/Users/cowgi/Desktop/University/bigbaselab/keywordTop200_sort_top10rank_befpre.xlsx")
finalresult.to_excel("/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/analysis_data/keywordTop200_sort_top10rank_aftpre_sanfran2.xlsx")


# In[9]:


#%%
tf_wnews = []
tf_wtweets = []
tf_similarity = []
tf_date = []
for t in range(usernum):
    try:
        eachuser = tw_data['users'][t]
        username = eachuser['id']
        usertimeline = eachuser['timeline']
        #count = 0
        datecount = 0
        
        for i in range(len(usertimeline)):
            date = usertimeline[i]["date"]
            text = preprocess_tweet(usertimeline[i]["text"])
            
            for j in range(len(resultpd)):
        
                if(date == resultpd._get_value(j,"Date")):
                    newstext = resultpd._get_value(j,"Text")
                    newstext = preprocess_news(newstext)
                    
                    tf_wnews.append(resultpd._get_value(j,"Title"))
                    tf_wtweets.append(text)
                    tf_date.append(date)
                    tf_similarity.append(tf_vectorizer(text, newstext, stop_words))
    except:
        continue


# In[10]:


#%%
 
tf_Toppd = pd.DataFrame()
 
tf_Toppd["NewsTitle"] = tf_wnews
tf_Toppd["Tweet"] = tf_wtweets
tf_Toppd["Date"] = tf_date
tf_Toppd["similarity"] = tf_similarity
 
tf_result = tf_Toppd
tf_result = tf_result.sort_values(by=["similarity"],ascending=False)
tf_result = tf_result.reset_index(drop=True)
tf_result = tf_result[:200]
 
tf_result.to_excel("/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/analysis_data/TF_IDF_Top200_sanfransisco.xlsx")


# In[11]:


#%% DocSim 활용하여 word2vec 모델 사용
import gensim
 
pre_model = gensim.models.KeyedVectors.load_word2vec_format('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/model/GoogleNews-vectors-negative300.bin', binary = True) 
 
sys.path.append("/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/model")


# In[12]:


from DocSim import DocSim
ds = DocSim(pre_model,stopwords = stop_words)
 
#%%
w2v_wnews = []
w2v_wtweets = []
w2v_similarity = []
w2v_date = []

for t in range(usernum):
    eachuser = tw_data['users'][t]
    username = eachuser['id']
    usertimeline = eachuser['timeline']
    
    datecount = 0
    
    for i in range(len(usertimeline)):
        date = usertimeline[i]["date"]
        text = preprocess_tweet(usertimeline[i]["text"])
        
        for j in range(len(resultpd)):
            if (date == resultpd._get_value(j, "Date")):
                try:
                    newstext = resultpd._get_value(j, "Text")
                    newstext = preprocess_news(newstext)
                    text_scores = ds.calculate_similarity(text, [newstext])
                    w2v_similarity.append(text_scores[0]["score"])
                    w2v_wnews.append(resultpd._get_value(j, "Title"))
                    w2v_wtweets.append(text)
                    w2v_date.append(date)
                    
                    
                except:
                    continue


# In[13]:


#%%           
w2v_Toppd = pd.DataFrame()
 
w2v_Toppd["NewsTitle"] = w2v_wnews
w2v_Toppd["Tweet"] = w2v_wtweets
w2v_Toppd["Date"] = w2v_date
w2v_Toppd["similarity"] = w2v_similarity
 
w2v_result = w2v_Toppd
w2v_result = w2v_result.sort_values(by=["similarity"],ascending=False)
w2v_result = w2v_result.reset_index(drop=True)
w2v_result = w2v_result[:200]
 
w2v_result.to_excel("/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/analysis_data/Word2Vec_Top200_sanfransisco.xlsx")
 


# In[14]:


#%%  Doc2Vec pre모델 사용
from gensim.models import Doc2Vec
from scipy import spatial
from gensim.models import doc2vec

d2v_apnews_model = Doc2Vec.load("/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/model/doc2vec_model/doc2vec.bin")
d2v_enwiki_model = Doc2Vec.load("/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/model/doc2vec_model/doc2vec.bin")


# In[15]:


# %%
d2v_wnews = []
d2v_wtweets = []
d2v_ap_similarity = []
d2v_wiki_similarity = []
d2v_date = []
for t in range(usernum):

    eachuser = tw_data['users'][t]
    username = eachuser['id']
    usertimeline = eachuser['timeline']
    # count = 0
    datecount = 0

    for i in range(len(usertimeline)):
        date = usertimeline[i]["date"]
        text = preprocess_tweet(usertimeline[i]["text"])
        for j in range(len(resultpd)):
            if (date == resultpd._get_value(j, "Date")):
                try:
                    first_text = resultpd._get_value(j, "Text")
                    first_text = preprocess_news(first_text)
                    Title = resultpd._get_value(j, "Title")
                    second_text = text

                    vec1 = d2v_apnews_model.infer_vector(first_text.split())
                    vec2 = d2v_apnews_model.infer_vector(second_text.split())

                    vec3 = d2v_enwiki_model.infer_vector(first_text.split())
                    vec4 = d2v_enwiki_model.infer_vector(second_text.split())

                    # 이거 distnace로 안하고 그냥 tf-idf에서 사용헌 cosinesimilarity 써도 될듯.
                    text_scores_ap = spatial.distance.cosine(vec1, vec2)
                    text_scores_wiki = spatial.distance.cosine(vec3, vec4)

                    d2v_ap_similarity.append(1 - text_scores_ap)
                    d2v_wiki_similarity.append(1 - text_scores_wiki)
                    d2v_wnews.append(Title)
                    d2v_wtweets.append(second_text)
                    d2v_date.append(date)

                except:
                    print("empty")
                    continue


# In[16]:


d2v_Toppd = pd.DataFrame()

d2v_Toppd["NewsTitle"] = d2v_wnews
d2v_Toppd["Tweet"] = d2v_wtweets
d2v_Toppd["Date"] = d2v_date
d2v_Toppd["ap_similarity"] = d2v_ap_similarity
d2v_Toppd["wiki_similarity"] = d2v_wiki_similarity

d2v_ap_result = d2v_Toppd
d2v_wiki_result = d2v_Toppd
d2v_ap_result = d2v_ap_result.sort_values(by=["ap_similarity"], ascending=False)
d2v_wiki_result = d2v_wiki_result.sort_values(by=["wiki_similarity"], ascending=False)

d2v_ap_result = d2v_ap_result.reset_index(drop=True)
d2v_wiki_result = d2v_wiki_result.reset_index(drop=True)

d2v_ap_result = d2v_ap_result[:200]
d2v_wiki_result = d2v_wiki_result[:200]

d2v_ap_result.to_excel("/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/analysis_data/Doc2Vec_ap_Top200_sanfransisco.xlsx")
d2v_wiki_result.to_excel("/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/analysis_data/Doc2Vec_wiki_Top200_sanfransisco.xlsx")


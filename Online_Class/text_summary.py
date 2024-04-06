import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


nlp = spacy.load("en_core_web_sm")

# Process whole documents
text = "Virat Kohli (Hindi pronunciation:  is an Indian int, and stands as the fourth-highest in international cricket.[4] He also holds the record for scoring the most centuries in ODI cricket and stands second in the list of most international centuries scored. Kohli was a member of the Indian team that won the 2011 Cricket World Cup, 2013 ICC Champions Trophy, and captained India to win the ICC Test mace three consecutive times in 2017, 2018, and 2019.[5]In 2013, Kohli was ranked number one in the ICC rankings for ODI batsmen. In 2015, he achieved the summit of T20I rankings.[6] In 2018, he was ranked top Test batsman, making him the only Indian cricketer to hold the number one spot in all three formats of the game. He is the first player to score 20,000 runs in a decade. In 2020, the International Cricket Council named him the male cricketer of the decade.[7]He has received many accolades for his performances in cricket. He won the ICC ODI Player of the Year award four times in 2012, 2017, 2018, and 2023. He also won the Sir Garfield Sobers Trophy, given to the ICC Cricketer of the Year, on two occasions, in 2017 and 2018 respectively. In 2018, he became the first player to win both ICC ODI and Test Player of the Year awards in the same year. Also, he was named the Wisden Leading Cricketer in the World for three consecutive years, from 2016 to 2018. At the national level, Kohli was honoured with the Arjuna Award in 2013, the Padma Shri in 2017, and India's highest sporting honour, the Khel Ratna award, in 2018.In 2018, Time magazine included him on its list of the 100 most influential people in the world. Kohli has been deemed one of the most commercially viable athletes, with estimated earnings of in the year 2022."
# print(len(text))
# for i in range(len(text)):
#         if i > 3489:
                #   debug = True
#                 print(text[i], " ")
#         if i > 3500:
#                 break


def summarizer(text):

        stopwords = list(STOP_WORDS)
        print((stopwords))
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)


        tokens = [elem.text for elem in doc]
        # print(tokens)

        word_freq = {}

        for word in doc:
                if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
                        if word.text not in word_freq.keys():
                                word_freq[word.text] = 1
                        else:
                                word_freq[word.text] += 1

        # print(word_freq)

        max_freq = max(word_freq.values())

        for word in word_freq.keys():
                word_freq[word] = word_freq[word]/max_freq
        # print(word_freq)
        sent_tokens = [sent for sent in doc.sents]

        sent_scores = {}
        for sent in sent_tokens:
                for word in sent:
                        if word.text in word_freq.keys():
                                if sent not in sent_scores.keys():
                                        sent_scores[sent] = word_freq[word.text]
                                else:
                                        sent_scores[sent] += word_freq[word.text]


        optimised_len = int(len(sent_tokens)*.4)
        # print(optimised_len)

        summary = nlargest(optimised_len, sent_scores, key = sent_scores.get)

        word_sz_of_summ = 0
        line_of_summary = len(summary)
        # print(line_of_summary)

        for i in range(len(summary)):
                word_sz_of_summ+=(len(summary[i]))
                
        # print(word_sz_of_summ, "count")

        # print(n)
        # print(summary)
        if line_of_summary == 0:
                summary_text = "Please Enter the sufficient Length Of sentences To get the summarised result"
                return (summary_text, text, line_of_summary)
        else:
                summary_text = ' '.join([str(sentence) for sentence in summary])
                return summary_text, text, line_of_summary

                # return summary,text,  line_of_summary
# summarizer(text)

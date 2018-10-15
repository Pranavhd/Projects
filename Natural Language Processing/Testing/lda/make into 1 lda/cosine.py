import re, math
from collections import Counter

WORD = re.compile(r'[a-zA-Z]+')
digits = re.compile(r'[0-9]+[.]?[0-9]*')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     all_digits = digits.findall(text)
     for i in range(len(all_digits)):
         all_digits[i] = float(all_digits[i])
         
     my_dict = {}
     result = zip(words,all_digits)
     my_dict.update(result)
     #print(my_dict)
     return my_dict

##text1 = '0.031*"flight" + 0.025*"americanair" + 0.018*"seat" + 0.014*"virginamerica" + 0.009*"next"'
##text2 = '0.025*"flight" + 0.024*"united" + 0.013*"plane" + 0.013*"seat" + 0.012*"usairways"'
##
##vector1 = text_to_vector(text1)
##vector2 = text_to_vector(text2)
##
##cosine = get_cosine(vector1, vector2)
##print('Cosine:', cosine)

list_10_topics = [(0, '0.031*"flight" + 0.025*"americanair" + 0.018*"seat" + 0.014*"virginamerica" + 0.009*"next"'), 
(1, '0.030*"flight" + 0.028*"problem" + 0.015*"booking" + 0.015*"ticket" + 0.014*"online"'), 
(2, '0.009*"pick" + 0.008*"new" + 0.007*"volume" + 0.007*"sorry" + 0.006*"extremely"'), 
(3, '0.123*"jetblue" + 0.044*"southwestair" + 0.010*"thanks" + 0.009*"fleek" + 0.009*"would"'), 
(4, '0.052*"americanair" + 0.032*"thank" + 0.030*"thanks" + 0.027*"you" + 0.026*"united"'), 
(5, '0.044*"americanair" + 0.034*"flight" + 0.032*"hour" + 0.018*"2" + 0.016*"hold"'), 
(6, '0.079*"flight" + 0.069*"americanair" + 0.055*"cancelled" + 0.027*"get" + 0.027*"flightled"'), 
(7, '0.048*"americanair" + 0.020*"united" + 0.020*"aa" + 0.016*"jetblue" + 0.014*"southwestair"'), 
(8, '0.043*"usairways" + 0.040*"flight" + 0.032*"united" + 0.016*"time" + 0.014*"never"'), 
(9, '0.126*"usairways" + 0.058*"service" + 0.055*"customer" + 0.026*"americanair" + 0.009*"thanks"')]

list_each_lda = [('0.025*"flight" + 0.024*"united" + 0.013*"plane" + 0.013*"seat" + 0.012*"usairways"'),
                 ('0.063*"flight" + 0.051*"cancelled" + 0.027*"flightled" + 0.019*"americanair" + 0.015*"usairways"'),
('0.029*"united" + 0.018*"usairways" + 0.015*"americanair" + 0.013*"jetblue" + 0.011*"southwestair"'),
('0.035*"americanair" + 0.019*"usairways" + 0.015*"flight" + 0.014*"customer" + 0.014*"service"'),
('0.020*"bag" + 0.017*"united" + 0.015*"luggage" + 0.011*"jetblue" + 0.011*"baggage"'),
('0.023*"flight" + 0.022*"united" + 0.017*"usairways" + 0.013*"americanair" + 0.010*"gate"'),
('0.028*"flight" + 0.020*"united" + 0.017*"americanair" + 0.015*"usairways" + 0.009*"get"'),
('0.038*"flight" + 0.023*"united" + 0.019*"usairways" + 0.017*"hour" + 0.017*"delayed"'),
('0.017*"usairways" + 0.017*"united" + 0.016*"line" + 0.013*"gate" + 0.012*"americanair"'),
('0.038*"bag" + 0.028*"united" + 0.016*"usairways" + 0.015*"luggage" + 0.015*"americanair"')]

answer_list = []
for each_lda in list_each_lda:
    max_so_far = -1
    index = -1
    for each_10_topics in list_10_topics:
        text1 = each_lda
        text2 = each_10_topics[1]

        vector1 = text_to_vector(text1)
        vector2 = text_to_vector(text2)

        cosine = get_cosine(vector1, vector2)
        if cosine>max_so_far:
            max_so_far = cosine
            index = each_10_topics[0]
    answer_list.append(index)

print(answer_list)

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from functools import reduce
 
ps = PorterStemmer()


from flask import Flask, render_template, request

app = Flask(__name__)



import emoji
def emoji_stems():
    stems = {}
    for emote in emoji.EMOJI_DATA.keys():
        s=[]
        for w in emoji.EMOJI_DATA[emote]['en'].replace(':', '').split('_'):
            s.append(ps.stem(w))
        stems[emote]=s
    return stems

def sentence_to_emote(sentence,limit=5):
    result = ''
    stems = emoji_stems()
    sentence=sentence.split()
    for word in sentence:
        if word=='love' or word=='Love:
            result+=emoji.emojize(':blue_heart:')+' '
            continue
        temp=ps.stem(word)
        i=0
        while i<limit:
            for emote in stems.keys():
                    if i<len(stems[emote]) and temp==stems[emote][i]:
                        result+=(emoji.emojize(emoji.EMOJI_DATA[emote]['en'])) + ' '
                        i=limit
            i+=1
        if i==limit:
            result+=word + ' '
    return result


@app.route('/')
def index():
    return render_template('goojle.html')

@app.route('/', methods=["GET", "POST"])
def result():
    result = ''
    if request.method == "POST":
        input_text = ''.join(request.form['input-text'])
        result = sentence_to_emote(input_text)
    return render_template('goojle.html', input=input_text, result=result) 

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000, debug=True)


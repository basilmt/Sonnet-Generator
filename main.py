from flask import Flask, jsonify
from joblib import load
from nltk.corpus import wordnet, cmudict
from markdown import markdown
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

STATUS_COMPLETE = "complete"
STATUS_INCOMPLETE = "incomplete"
STATUS_FAILED = "failed"

@app.route('/')
def hello():
    return jsonify({ 
        "data" : "Hello Intruder",
        "message" : "to get to documentation - /docs",
        "stats" : STATUS_COMPLETE 
        })

@app.route('/greet')
def greet():
    return jsonify({ 
        "data" : "Hello Random Person",
        "message" : "to get to documentation - /docs",
        "stats" : STATUS_COMPLETE 
        })

@app.route('/greet/<name>')
def greetPerson(name):
    return jsonify({
        "data" : f"Hello {name}",
        "message" : "to get to documentation - /docs",
        "stats" : STATUS_COMPLETE 
        })

@app.route('/docs')
def docs():
    with open('README.md','r') as markdown_file:
        content = markdown_file.read()
        return markdown(content)

@app.route('/line')
def line():
    text_model = model()
    ans = generateLine(text_model,None)[0]
    return jsonify({
        "data" : ans,
        "message" : "One line completed",
        "stats" : STATUS_COMPLETE
        }), 200


@app.route('/line/<start>')
def lineWithStart(start):
    text_model = model()
    try:
        test = text_model.make_sentence_with_start(start, strict=False, min_words = 8, max_words = 12)
        if test is not None:
            paincases = [",", ":", ".", ";", "!"]
            if test[0] in paincases :
                test = test[2:]
            if test[0] == " ":
                test = test[1:]
            test = replaceWords(test)
        message = f"One line with starting {start}"
        stats = STATUS_COMPLETE
        code = 200
    except:
        test = None
        message = "Sorry, No content"
        stats = STATUS_FAILED
        code = 204

    return jsonify({
        "data" : test,
        "message" : message,
        "stats" : stats
    }) ,code


@app.route('/lines')
def lines():
    text_model = model()
    ans = generate(text_model=text_model, number_of_lines=10)
    return jsonify({
        "data" : ans,
        "message" : "10 lines completed",
        "stats" : STATUS_COMPLETE
    })


@app.route('/lines/<number_of_lines>')
def linesNum(number_of_lines):
    try:
        number_of_lines = int(number_of_lines)
    except ValueError:
        return jsonify({
            "data" : "parameter should be a number",
            "message" : "Bad Request",
            "stats" : STATUS_FAILED
        }), 400
    except:
        return jsonify({
            "data" : "something went wrong",
            "message" : "Bad Request, maybe",
            "stats" : STATUS_FAILED
        }), 400 

    if number_of_lines <=4 :
        text_model = model()
        ans = generate(text_model = text_model, number_of_lines = number_of_lines)
        return jsonify({
            "data" : ans,
            "message" : f"{number_of_lines} lines completed",
            "stats" : STATUS_COMPLETE
            })
    else:
        text_model = model()
        ans = generate(text_model = text_model, number_of_lines = 4)
        mem = ans[-1].split(' ')[-1]
        return jsonify({
            "data" : ans,
            "message" : f"{len(ans)} lines made, {number_of_lines - len(ans)} to go",
            "url-endpoint" : f"/lines/{number_of_lines}/{len(ans)}/{mem}",
            "stats" : STATUS_INCOMPLETE
            })


@app.route('/lines/<number_of_lines>/<number_of_lines_rendered>/<memory>')
def linesNumCont(number_of_lines, number_of_lines_rendered, memory):
    try:
        number_of_lines = int(number_of_lines)
        number_of_lines_rendered = int(number_of_lines_rendered)
    except ValueError:
        return jsonify({
            "data" : "parameter should be a number",
            "message" : "Bad Request",
            "stats" : STATUS_FAILED
        }), 400
    except:
        return jsonify({
            "data" : "something went wrong",
            "message" : "Bad Request",
            "stats" : STATUS_FAILED
        }), 400 

    if number_of_lines - number_of_lines_rendered <= 0:
        return jsonify({
            "data" : "you've had enough",
            "message" : "Bad Request",
            "stats" : STATUS_FAILED
        }), 400 

    text_model = model()
    if number_of_lines - number_of_lines_rendered >= 4:
        ans = generate(text_model = text_model, number_of_lines = 4, memory=memory)
    else:
        ans = generate(text_model = text_model, 
                        number_of_lines = number_of_lines, 
                        memory=memory, i=number_of_lines_rendered)

    if number_of_lines_rendered + len(ans) >= number_of_lines :
        return jsonify({
            "data" : ans,
            "message" : f"all {number_of_lines} are rendered",
            "stats" : STATUS_COMPLETE
            })
    else:
        mem = ans[-1].split(' ')[-1]
        return jsonify({
            "data" : ans,
            "message" : f"{number_of_lines_rendered + len(ans)} lines made, {number_of_lines - (number_of_lines_rendered + len(ans))} to go",
            "url-endpoint" : f"/lines/{number_of_lines}/{number_of_lines_rendered + len(ans)}/{mem}",
            "stats" : STATUS_INCOMPLETE
            })

def model():
    return load('model.joblib')

def generate(text_model, number_of_lines = 14, memory = None, i=0):
    '''
    Generate a 14 line sonnet
    return a list of 14 lines
    print_to_terminal parameter for printing lines to terminal
    '''
    lines = []
    rhyme = [None,None]
    checkNum = number_of_lines + 1 - number_of_lines % 4 
    while i < number_of_lines :
        test, memory = generateLine(text_model,memory)
        if test is not None:
            inx = i % 2
            if rhyme[inx] is None:
                rhyme[inx] = memory
                if i == checkNum:
                    syns = getSynonyms(memory)
                    if syns:
                        r = rhym(rhyme[0],syns)
                        if r is not None:
                            test = test.split(" ")
                            test[-1] = r
                            test = " ".join(test)
                    
            else:
                syns = getSynonyms(memory)
                if syns:
                    r = rhym(rhyme[inx],syns)
                    if r is not None:
                        test = test.split(" ")
                        test[-1] = r
                        test = " ".join(test)

                rhyme[inx] = None
            
            lines.append(test)
            i += 1

    return lines


def getSynonyms(word):
    '''
    Fetch all the available synonyms of a particular word
    returns a list of synonyms
    '''
    syn = []
    paincases = ["d", "me"]
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            nameTemp = lemma.name().lower()
            if ( nameTemp.find('_') == -1 and
            nameTemp.find('-') == -1 and word not in paincases):
                syn.append(nameTemp)

    return list(set(syn))



def rhym(prevWord,potWords):
    '''
    Check for rhyming  a word with potWords
    potWords is a list of potential words to check from
    returns a word with maximun match by checking syllables
    if no words are available return None
    '''

    entries = cmudict.entries()
    syllablesPrev = [(word, syl) for word, syl in entries if word == prevWord]
    syllablesPot = [(word, syl) for word, syl in entries if word in potWords]
    nlevel = 0
    nword = None
    for (word, syllable) in syllablesPrev:
        for (wordp, syllablep) in syllablesPot:
            level = compareSylls(syllable, syllablep)
            if level != 0:
                if level == 3:
                    return wordp
                elif level > nlevel :
                    nlevel = level
                    nword = wordp
    return nword


def compareSylls(syllable, syllablep):
    '''
    compare two given syllables
    return number of common syllables at the end
    '''

    level = len(syllablep) if len(syllablep) < len(syllable) else len(syllable)
    if level > 3 :
        level = 3
    while level > 0:
        if syllable[-level:] == syllablep[-level:] :
            return level
        else:
            level -= 1
    return 0


def generateLine(text_model,memory):
    '''
    generate a single line from text_model and 
    memory from last word of previous line
    '''

    if memory == None:
        test = text_model.make_short_sentence(80, tries=100, min_words = 8, max_words = 11)


    else:

        try:
            test = text_model.make_sentence_with_start(memory, strict=False, min_words = 9, max_words = 12)
            test = test[len(memory)+1:]

        except:
            test = text_model.make_short_sentence(80, tries=100, min_words = 8, max_words = 11)

    if test is not None:
        paincases = [",", ":", ".", ";", "!"]
        if test[0] in paincases :
            test = test[2:]
        if test[0] == " ":
            test = test[1:]
        test = replaceWords(test)
        memory = (test.split(" ")[-1])

    return test, memory


def replaceWords(text):
    '''
    check for new english word from text
    Replacing them with old english word set
    reurn thenew text with replaced words
    '''
    
    checkWord = ["are","do","does","before","have","were","why","often","yes","anything","no","hurry",
    'peevish', 'thunderbolt', 'lightning',
     'ferry', 'sorrowful', 'believe', 'relax', 'uncontrolled', 'free',
      'open', 'unrestrained',
       'futile', 'unsettle', 'untamed', 'weak', 'ignorant', 'lowering', 'health', 'masks', 'wave',
         'sky', 'whether', 'worthless', 'bastard', 'must', 'know',
          'quickly', 'stabbed']

    replaceWord = ["art","dost","doth","'ere","hast","wast","wherefore","oft","ay","aught","nay","hie", 
    'tetchy', 'thunder-stone', 'thunder-stone',
     'traject', 'tristful', 'trowest', 'unbend', 'unbitted', 'unbound',
      'unbraced', 'unhoused',
       'unprevailing', 'unprovide', 'unreclaimed', "unsinew'd",
        'untaught', 'vailing', 'verdure', 'vizards',
         'wafter', 'welkin', "whe'r", 'whoreson', 'whoreson', 'wilt', 'wot',
          'yarely', 'yerked' ]

    
    textar = text.split(" ")
    for i, word in enumerate(textar):
        if word in checkWord:
            textar[i] = replaceWord[i]
    return " ".join(textar)

if __name__ == '__main__':
    app.run(debug=True)
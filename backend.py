import markovify
import sys
import nltk
from nltk.corpus import wordnet
from nltk.corpus import cmudict


def main():
    '''
    Import necessary packages
    return the trained model
    '''
    

    # Read text from file
    print("Loading data...")
    text = loadData()

    

    # convering to one sentence per line
    text = text.replace(" <eos> ","\n")
    text = text.replace(" <eos>","")

    # Train model
    # Using markovify
    # NewlineText for better accuracy
    # state size = 3 for better accuracy
    text_model = markovify.NewlineText(text, state_size=3)

    return text_model



def generate(text_model,print_to_terminal = False):
    '''
    Generate a 14 line sonnet
    return a list of 14 lines
    print_to_terminal parameter for printing lines to terminal
    '''
    i = 0
    memory = None
    lines = []
    rhyme = [None,None]
    while i < 14 :
        test, memory = generateLine(text_model,memory)
        if test is not None:
            inx = i % 2
            if rhyme[inx] is None:
                rhyme[inx] = memory
                if i == 13:
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
            if print_to_terminal:
                print(test)

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
    memory from last word of previous word
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





def loadData():
    '''
    Load data from /datasets
    multiple datasets can be read at once
    return a text containing all the dataset for training
    '''
    import os
    text = ""
    directory = "datasets"
    # Read all files in directory
    # and extract words

    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), encoding='utf8') as f:
            text += f.read()

    return text



if __name__ == "__main__":
    print("\nTo open with UI run\npython uiscroll.py\n")
    mod = main()
    generate(mod,True)
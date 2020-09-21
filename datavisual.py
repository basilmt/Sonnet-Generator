from backend import loadData
import markovify
import termcolor


def lexical_diversity(text):
    '''
    for calculating lexial diversity
    source : nltk
    '''
    return len(set(text)) / len(text)

def percentage(count, total):
    '''
    for calculating precentage
    source : nltk
    '''
    return round(100 * count / total , 5)


text = loadData()
t = text.split(" ")


# visualisation of dataset
termcolor.cprint("\nAnalysis of Dataset", "green")
print(f"\nTotal word count : {len(t)}")
print(f"Unique word count : {len(set(t))}")
print(f"Lexical Diversity : {lexical_diversity(t)}")
# to check average words per line
print(f'\nAverage no. of words per line in dataset: {len(text.split(" "))/text.count("<eos>")}')

neweng = ["are","do","does","before","have","were","why","often","yes","anything","no","hurry",
    'peevish', 'thunderbolt', 'lightning',
     'ferry', 'sorrowful', 'believe', 'relax', 'uncontrolled', 'free',
      'open', 'unrestrained',
       'futile', 'unsettle', 'untamed', 'weak', 'ignorant', 'lowering', 'health', 'masks', 'wave',
         'sky', 'whether', 'worthless', 'bastard', 'must', 'know',
          'quickly', 'stabbed']

oldeng = ["art","dost","doth","'ere","hast","wast","wherefore","oft","ay","aught","nay","hie", 
    'tetchy', 'thunder-stone', 'thunder-stone',
     'traject', 'tristful', 'trowest', 'unbend', 'unbitted', 'unbound',
      'unbraced', 'unhoused',
       'unprevailing', 'unprovide', 'unreclaimed', "unsinew'd",
        'untaught', 'vailing', 'verdure', 'vizards',
         'wafter', 'welkin', "whe'r", 'whoreson', 'whoreson', 'wilt', 'wot',
          'yarely', 'yerked' ]

          



termcolor.cprint("\nSearching for old english words", "green")
termcolor.cprint("\nOld english words\n", "green")


for word in oldeng:
    print(f"    {word} : {text.count(word)}")

termcolor.cprint("\nLexical diversity\n","green")
for word in oldeng:
    print(f"    {word} : {percentage(text.count(word),len(t))} %")

print()

termcolor.cprint("New english words\n","green")
for word in neweng:
    print(f"    {word} : {text.count(word)}")

termcolor.cprint("\nLexical diversity\n","green")

for word in neweng:
    print(f"    {word} : {percentage(text.count(word),len(t))} %")

print()






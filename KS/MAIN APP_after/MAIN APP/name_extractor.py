import nltk
from nameparser.parser import HumanName

# TEST CASE 
text = ['in the car version 2 and Abhinav Anand.',
         'hi there John Vogue.','Regards,', 'Gaurav Sharma']

def get_human_names(text):
    '''
    takes a string and
    returns a list of names present in it.
    '''
    tokens = nltk.tokenize.word_tokenize(text)  # tokenize
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)  # chunking
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: #avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []

    return (person_list)


def crawl_names(lines):
    '''
    takes a list of lines 
    join the lines to form 
    a string and extract the names
    using the get_human_names function
    above
    '''
    text = '\n'.join(lines)
    names = get_human_names(text)
    return names


print(crawl_names(text))


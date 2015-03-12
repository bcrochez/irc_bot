# -*-coding:UTF-8 -*

import random
random.seed()

print("---- start loading citations ----")

names = ['cinema', 'informatique', 'litt_fr', 'sciences', 'transfo', 'philo', 'proverbes']


def load_citations():
    global citations
    global names
    citations = {}
    for name in names:
        try:
            f = open('module/citations/'+name+'.txt', encoding='utf-8')
        except:
            names.remove(name)
            print("*** impossible d'ouvrir: "+name+" ***")
            continue
        citations_tmp = []
        for citation in f.read().split('%'):
            citations_tmp.append(citation.strip())
        citations[name] = citations_tmp
        print("  -- "+name+" file load --")
        f.close()
    
citations = {}
load_citations()
    
print("---- citations module loaded ----")

def load_cita_theme(theme):
    global citations
    global names
    if theme not in names:
        names.append(theme)
    try:
        f = open('citations/'+theme+'.txt', encoding='utf-8')
    except:
        names.remove(theme)
        print("*** impossible d'ouvrir: "+theme+" ***")
        return 0
    citations_tmp = []
    for citation in f.read().split('%'):
        citations_tmp.append(citation.strip())
    citations[theme] = citations_tmp
    print("  --  "+theme+" file load  --")
    f.close()
    return 1

def get_random_citation():
    total = 0
    for name in names:
        total += len(citations[name])
    i = random.randint(0, total-1)
    for name in names:
        if i < len(citations[name]):
            return citations[name][i]
        i -= len(citations[name])

def get_citation_by_theme(theme):
    i = random.randint(0, len(citations[theme])-1)
    return citations[theme][i]

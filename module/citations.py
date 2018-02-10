# -*-coding:UTF-8 -*

import random, os, sys
random.seed()

print("---- start loading citations ----")

names = ['cinema', 'informatique', 'litt_fr', 'sciences', 'transfo', 'philo', 'proverbes']
path = os.path.dirname(sys.argv[0])

def load_citations():
    global citations
    global names
    citations = {}
    error_names = []
    for name in names:
        try:
            f = open(path+'/module/citations/'+name+'.txt', encoding='utf-8')
        except:
            error_names.append(name)
            print("*** impossible d'ouvrir: "+name+" ***")
            continue
        citations_tmp = []
        for citation in f.read().split('%'):
            citations_tmp.append(citation.strip())
        citations[name] = citations_tmp
        print("  -- "+name+" file load --")
        f.close()
    for name in error_names:
        names.remove(name)
        
citations = {}
load_citations()
    
print("---- citations module loaded ----")

def load_cita_theme(theme):
    global citations
    global names
    if theme not in names:
        names.append(theme)
    try:
        f = open(path+'/module/citations/'+theme+'.txt', encoding='utf-8')
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

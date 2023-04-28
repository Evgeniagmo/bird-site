from proj_maths.models import Russianbirds

def db_get_birds_for_table():
    birds = []
    for i, item in enumerate(Russianbirds.objects.all()):
        birds.append([i+1, item.species_name, item.latin, item.observation_number])
    return birds

def db_add_observation(new_bird, new_location):
    for item in Russianbirds.objects.filter(species_name__exact=new_bird):
        if item.observation_number is None:
            item.observation_number = 1
        else:
            item.observation_number += 1
        item.save()


"""
def db_write_term(new_term, new_definition):
    term = Terms(term=new_term, definition=new_definition)
    term_addition = TermAuthors(termid=term.termid, termsource="user")
    term.save()
    term_addition.save()

def db_get_terms_stats():
    db_terms = len(TermAuthors.objects.filter(termsource="db"))
    user_terms = len(TermAuthors.objects.filter(termsource="user"))
    terms = Terms.objects.all()
    defin_len = [len(term.definition) for term in terms]
    stats = {
        "terms_all": db_terms + user_terms,
        "terms_own": db_terms,
        "terms_added": user_terms,
        "words_avg": sum(defin_len)/len(defin_len),
        "words_max": max(defin_len),
        "words_min": min(defin_len)
    }
    return stats
"""
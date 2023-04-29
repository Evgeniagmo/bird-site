from datetime import datetime
from proj_maths.models import Russianbirds, Observations, Observers


def db_get_birds_for_table():
    birds = []
    for i, item in enumerate(Russianbirds.objects.all()):
        birds.append([i + 1, item.species_name, item.latin, item.observation_number])
    return birds


def db_add_observation(new_bird, new_location, user_name, user_email):
    curr_species_id = 0
    for item in Russianbirds.objects.filter(species_name__exact=new_bird):
        curr_species_id = item.species_id
        if item.observation_number is None:
            item.observation_number = 1
        else:
            item.observation_number += 1
        item.save()

    curr_observer_id = 0
    if Observers.objects.filter(observer_email__exact=user_email).count() == 0:
        Observers.objects.create(observer_name=user_name,
                                 observer_email=user_email)
    for item in Observers.objects.filter(observer_email__exact=user_email):
        curr_observer_id = item.observer_id
        if item.observation_count is None:
            item.observation_count = 1
        else:
            item.observation_count += 1
        item.save()

    Observations.objects.create(observer_id=curr_observer_id,
                                species_id=curr_species_id,
                                location=new_location,
                                date=datetime.now().date())


def db_get_birds_stats():
    db_birds = Russianbirds.objects.count() - Russianbirds.objects.filter(observation_number=None).count()
    db_observers = Observers.objects.count()
    db_observations = Observations.objects.count()
    db_observations_today = Observations.objects.filter(date=datetime.now().date()).count()
    birds_all = Russianbirds.objects.all()
    birds_all_count = [bird.observation_number for bird in birds_all if bird.observation_number is not None]
    stats = {
        "birds_all": db_birds,
        "observers_all": db_observers,
        "observations_all": db_observations,
        "observations_today": db_observations_today,
        "birds_max": max(birds_all_count),
        "birds_min": min(birds_all_count),
    }
    return stats


def db_get_description(bird_name):
    bird_info = {"bird_species": bird_name}
    for item in Russianbirds.objects.filter(species_name__exact=bird_name):
        bird_info["bird_genus"] = item.genus_name
        bird_info["bird_latin"] = item.latin
        bird_info["bird_habitat"] = item.habitat
        if item.aka is None:
            bird_info["bird_aka"] = "-"
        else:
            bird_info["bird_aka"] = item.aka
        if item.observation_number is None:
            bird_info["bird_is_seen"] = False
        else:
            bird_info["bird_is_seen"] = True

    return bird_info

from typing import Dict, List

def get_moods(file) -> List[Dict]:
    with open(file, "r", encoding="utf-8") as moods:
        mood_list = list()
        for mood in moods:
            mood_str = mood.split(',')
            mood_list.append({"name": mood_str[0], "description": mood_str[1]})
    return mood_list

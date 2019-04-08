import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions


natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey='34qzJpNfbmmav0ZFkGM9vM_enLCTAOuQsd5s4odeF19l',
    url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api'
)

response = natural_language_understanding.analyze(
    html="<html><head><title>Fruits</title></head><body><h1>Apples and Oranges</h1><p>I love apples! I don't like oranges.</p></body></html>",
    features=Features(emotion=EmotionOptions(targets=['apples','oranges']))).get_result()

print(json.dumps(response, indent=2))


def getEmotions(text):
    response = natural_language_understanding.analyze(
    html="<html><head><title>Fruits</title></head><body><h1>Apples and Oranges</h1><p>I love apples! I don't like oranges.</p></body></html>",
    features=Features(emotion=EmotionOptions())).get_result()
    print(response)
    return

    
    
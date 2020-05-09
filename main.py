import requests
import json
import pandas
import tweepy
from creds import access_token, access_token_secret, consumer_key, consumer_secret

query = """query {
        country(name: "India") {
        cases
        recovered
        deaths
    }
    state(countryName: "India", stateName: "Gujarat") {
        state
        cases
        deaths
        recovered
        districts {
        district
        cases
        recovered
        deaths
        }
    }
    }"""


def tweet():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    tweet1, tweet2, tweet3 = parseData()
    api.update_status(tweet1)
    api.update_status(tweet2)
    api.update_status(tweet3)


def fetchData(query):
    url = 'https://covidstat.info/graphql/'
    r = requests.post(url, json={'query': query})
    json_data = json.loads(r.text)
    return json_data


def parseData():
    data = fetchData(query)
    countryCase = data['data']['country']
    print(countryCase)
    caseInfo = data['data']['state']
    distCase = data['data']['state']['districts']
    refinedDistCases = refine_dist(distCase).to_dict()
    li = [1, 28, 31]
    tweet1 = f"Daily #COVID19 India UPDATE -- There are {countryCase['cases']} confirmed cases, {countryCase['recovered']} people have recovered, and {countryCase['deaths']} deaths. "
    tweet2 = f"Daily #COVID19 UPDATE -- In {caseInfo['state']}, There are {caseInfo['cases']} confirmed cases, {caseInfo['recovered']} people have recovered, and {caseInfo['deaths']} deaths."
    tweet3 = f"Top {caseInfo['state']} District #COVID19 CASES UPDATE -- "
    for i in li:
        tweet3 += f"{refinedDistCases['district'][i]}  Cases: {refinedDistCases['cases'][i]}, Recovered: {refinedDistCases['recovered'][i]}, Deaths: {refinedDistCases['deaths'][i]}.  "
    # print(tweet1, tweet2, tweet3)
    return tweet1, tweet2, tweet3


def refine_dist(distCase):
    df = pandas.DataFrame(distCase)
    df.sort_values(by=['deaths'], inplace=True, ascending=False)
    return df[0:5]


if __name__ == "__main__":
    parseData()
    tweet()

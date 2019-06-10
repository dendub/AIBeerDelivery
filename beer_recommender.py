import argparse
import json
import numpy as np

# Compute the Pearson correlation score between user1 and user2
def pearson_score(dataset, user1, user2):
    if user1 not in dataset:
        raise TypeError("Cannot find " + user1 + " in the dataset")

    if user2 not in dataset:
        raise TypeError("Cannot find " + user2 + " in the dataset")

    # Beers rated by both user1 and user2
    common_beers = {}

    #get beers rated by both users
    for item in dataset[user1]:
        if item in dataset[user2]:
            common_beers[item] = 1

    num_ratings = len(common_beers)

    # If there are no common beers between user1 and user2, then the score is 0
    if num_ratings == 0:
        return 0

    # Calculate the sum of ratings of all the common beers
    user1_sum = np.sum([dataset[user1][item] for item in common_beers])
    user2_sum = np.sum([dataset[user2][item] for item in common_beers])

    # Calculate the sum of squares of ratings of all the common beers
    user1_squared_sum = np.sum([np.square(dataset[user1][item]) for item in common_beers])
    user2_squared_sum = np.sum([np.square(dataset[user2][item]) for item in common_beers])

    # Calculate the sum of products of the ratings of the common beers
    sum_of_products = np.sum([dataset[user1][item] * dataset[user2][item] for item in common_beers])

    # Calculate the Pearson correlation score
    Sxy = sum_of_products - (user1_sum * user2_sum / num_ratings)
    Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
    Syy = user2_squared_sum - np.square(user2_sum) / num_ratings

    if Sxx * Syy == 0:
        return 0

    return Sxy / np.sqrt(Sxx * Syy)

#Find users similar to chosen user from a dataset
def find_similar_users(dataset, user, num_users):
    if user not in dataset:
        raise TypeError("Cannot find" + user, " in the dataset")
    #Computing Pearson score between chosen user and the rest users in the dataset
    scores = np.array([[x, pearson_score(dataset, user, x)] for x in dataset if x != user])
    #Sort in descendig order
    scores_sorted = np.argsort(scores[:, 1])[::-1]
    #Get the scores of first 'num_users' users
    top_users=scores_sorted[:num_users]
    return scores[top_users]

#Get movie recommendations for a specified user
def get_recommendations(dataset, input_user):
    if input_user not in dataset:
        raise TypeError("Cannot find " + input_user + " in the dataset")

    #To track scores
    overall_scores = {}
    similarity_scores = {}

    #Finding the similarity score between chosen user and the rest users from a dataset
    for user in [x for x in dataset if x != input_user]:
        similarity_score = pearson_score(dataset, input_user, user)

        if similarity_score <= 0:
            continue

        #The list of beers that have already received a rating from the current user, but not yet rated by the chosen user
        filtered_list = [x for x in dataset[user] if x not in dataset[input_user] or dataset[input_user][x] == 0]

        for item in filtered_list:
            overall_scores.update({item: dataset[user][item] * similarity_score})
            similarity_scores.update({item: similarity_score})

    if len(overall_scores) == 0:
        return ["No recommendations possible"]

    # Generate beer ranks by normalization based on overall_scores
    beer_scores = np.array([[score/similarity_scores[item], item]
            for item, score in overall_scores.items()])

    # Sort in decreasing order
    beer_scores = beer_scores[np.argsort(beer_scores[:, 0])[::-1]]

    # Extract the beer recommendations
    beer_recommendations = [beer for rating, beer in beer_scores]

    return beer_recommendations

def main(name):
    user = name

    ratings_file = "ratings.json"

    with open(ratings_file, "r") as f:
        data = json.loads(f.read())

    print("Users similar to " + user + ":")
    similar_users = find_similar_users(data, user, 5)
    print("User\t\tSimilarity Score")
    for item in similar_users:
        print(item[0], round(float(item[1]), 4))

    movies = get_recommendations(data, user)
    result="Beer recommendations for " + user + ":"
    for i, movie in enumerate(movies):
        result += "\n" + (str(i+1) + '. ' + movie)
    print(result)
    return result

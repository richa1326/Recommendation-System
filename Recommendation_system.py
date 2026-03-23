'''Users rate items (movies/products)
We find similar users
Recommend items liked by similar users'''

import csv
import math

#Load Dataset from csv
def load_data(filename):
    data={}

    with open(filename , 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            user = row['user']
            item = row['item']
            rating = float(row['rating'])

            if user not in data:
                data[user] = {}

            data[user][item] = rating

        return data





#Find Similarity Between two users
def cosine_similarity(user1 , user2):
    common_items = set((user1.keys()) & user2.keys())

    if not common_items:
        return 0
    
    numerator = sum(user1[item] * user2[item] for item in common_items)
    sum1= sum(user1[item]**2 for item in common_items)
    sum2= sum(user2[item]**2 for item in common_items)

    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if denominator == 0:
        return 0
    
    return numerator/denominator

#Find most similar users

def get_similar_users(target_users , data):
    similarities = {}

    for user in data:
        if user!=target_users:
            sim=cosine_similarity(data[target_users] , data[user])
            similarities[user] = sim

    return sorted(similarities.items() , key=lambda x:x[1] , reverse=True)

# Recommend items

def recommend(target_users , data):
    similar_users = get_similar_users(target_users , data)

    scores={}
    sim_sums={}

    for user , similarity in similar_users:
        for item in data[user]:
            if item not in data[target_users]:
                scores[item] = scores.get(item, 0) + similarity * data[user][item]
                sim_sums[item] = sim_sums.get(item, 0) + similarity

    rankings = []
    for item in scores:
        rankings.append((scores[item]/ sim_sums[item] , item))

    return sorted(rankings , reverse=True)


# MAIN
if __name__ == "__main__":
    data = load_data("data.csv")

    user = "David"
    recs = recommend(user, data)

    print(f"Recommendations for {user}:\n")

    for score, item in recs:
        print(f"{item} → {round(score,2)}")






# -*- coding: utf-8 -*-
"""
    RecommendationSystem.py
    @description:
    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
from collections import OrderedDict
from typing import Iterable

# Third-party app imports
import pandas as pd
import numpy as np
from numpy.random import normal as GaussianDistribution
from pymongo import MongoClient

# Imports from your apps
from src.config import settings


class MyObj:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.private_name)
        # print('Accessing {} giving {}'.format(self.public_name, value))
        return value

    def __set__(self, obj, value):
        # print('Updating %r to %r', self.public_name, value)
        setattr(obj, self.private_name, value)


class RecommendationSystem:
    pol_dic = MyObj()
    rew_dic = MyObj()
    count_dic = MyObj()
    reco_count_dic = MyObj()

    def __init__(self, states: list, username: str | None = None):
        self.df = None
        self.states = states
        self.state_id = None
        self.username = username or "random"

        # Check if the collections exist in Mongo DB
        client = MongoClient(settings.db_uri)
        db = client[settings.DB_NAME]

        # Get all the collections from MongoDB
        self.count_col = db["rl_count"]
        self.pol_col = db["rl_value"]
        self.rew_col = db["rl_reward"]
        self.reco_count_col = db['rl_reco_track']
        self.collections_ = {
            "count_dic": self.count_col,
            "pol_dic": self.pol_col,
            "rew_dic": self.rew_col,
            "reco_count_dic": self.reco_count_col
        }

    def load_data(self, username: str | None = None, state_id: str | None = None):
        def docs_to_dict(lst: Iterable):
            return {f"{x.get('user')}_{x.get('state')}": x.get("data") for x in lst}

        username = username or self.username
        query = {"user": {"$in": list({username, "random"})}}
        self.df = pd.read_csv(f"{settings.PATH_DATA}/videos/preprocessed/cancer_mama_filtered_ordered.csv", index_col=0)
        self.count_dic = docs_to_dict(self.count_col.find(query))  # Dictionary to store the count of products
        self.pol_dic = docs_to_dict(self.pol_col.find(query))  # Dictionary to store the value distribution
        self.rew_dic = docs_to_dict(self.rew_col.find(query))  # Dictionary to store the reward distribution
        self.reco_count_dic = docs_to_dict(self.reco_count_col.find(query))  # Dictionary to store the recommendation

        # Initialize dicts if it is a new user
        if username is not None:
            dicts = [self.count_dic, self.pol_dic, self.rew_dic, self.reco_count_dic]
            for dic in dicts:
                if f"{username}_{self.states[0]}" not in dic.keys():
                    for state in self.states:
                        dic[f"{username}_{state}"] = {}

    def sample_state(self, username: str | None = None) -> str:
        username = username or "random"
        state = np.random.choice(self.states, 1)[0]
        return f"{username}_{state}"

    def update_reward(self, username: str, state_id: str, item: str):
        self._update_reward_and_policy(state_id, item, 5)
        self._update_collections(username, state_id)

    # Method to sample a stateID and then initialize the dictionaries
    def recommendation(self, *, username: str | None = None, state_id: str, n_products: int, epsilon: float) -> list:
        # Initialize variables
        self.state_id = state_id
        username = username or self.username
        segment = state_id.split("_")[-1]
        print(f"[INFO] Recommendation state {state_id}")
        # Start the recommendation process
        if len(self.pol_dic[state_id]):
            print("The context exists")
            # Implement the sampling of products based on exploration and exploitation
            seg_products = self._sample_products(segment, n_products, epsilon)
            # Check if the recommendation count collection exist
            self._reco_coll_checker(username)
            # Update the dictionaries of values and rewards
            self._dic_updater(seg_products, username, state_id)
        else:
            print("The context doesnt exist")
            # Get the list of relevant products
            seg_products = self._get_products(segment, n_products)
            # Add products to the value dictionary and rewards dictionary
            self._dic_adder(seg_products, username, state_id)
        print("[INFO] Completed the recommendation process")
        return seg_products

    # Method to update the recommendation dictionary
    def _reco_coll_checker(self, username: str | None = None):
        username = username or self.username
        state_id = self.state_id.replace("random_", "")
        print("[INFO] Inside the recommendation collection")
        query = {"user": username, "state": {'$exists': True, '$in': [state_id]}}
        if (doc := self.reco_count_col.find_one(query)) is None:
            print("[INFO] Inserting the record in the recommendation collection")
            doc = {"user": username, "state": state_id, "data": {}}
            self.reco_count_col.insert_one(doc)
        return doc

    # Create a function to get a list of products for a certain segment
    def _get_products(self, segment: str, n_products: int) -> list:
        # Get the list of unique products for each segment
        seg_products = list(self.df[self.df['segment'] == segment]['id'].unique())
        seg_products = np.random.choice(seg_products, n_products)
        return seg_products

    # This is the function to get the top n products based on value
    def _top_products(self, segment: str, n_products: int) -> list:
        # Get the top products based on the values and sort them from product with the largest value to least
        state_pol_dic = self.pol_dic[self.state_id]
        top_products = sorted(state_pol_dic.keys(), key=lambda kv: state_pol_dic[kv])[-n_products:][::-1]
        # If the topProducts is less than the required number of products n_products, sample the delta
        while len(top_products) < n_products:
            print("[INFO] top products less than required number of products")
            seg_products = self._get_products(segment, (n_products - len(top_products)))
            new_list = top_products + seg_products
            # Finding unique products
            top_products = list(OrderedDict.fromkeys(new_list))
        return top_products

    # This is the function to create the number of products based on exploration and exploitation
    def _sample_products(self, segment: str, n_products: int, epsilon: float) -> list:
        # Initialise an empty list for storing the recommended products
        seg_products = []
        # Get the list of unique products for each segment
        segment_products = list(map(str, self.df[self.df['segment'] == segment]['id'].unique()))
        # Get the list of top n products based on value
        top_products = self._top_products(segment, n_products)
        # Start a loop to get the required number of products
        while len(seg_products) < n_products:
            # First find a probability
            probability = np.random.rand()
            # Sample a product
            prod = top_products.pop(0) if probability >= epsilon else np.random.choice(segment_products, 1)[0]
            # Add product
            seg_products.append(prod)
            # Ensure that seg_products is unique
            seg_products = list(OrderedDict.fromkeys(seg_products))
        return seg_products

    def _dic_updater(self, products: list, username: str, state_id: str):
        query = {"username": username, "state": self.state_id.replace("random_", "")}
        # Loop through each of the products
        for prod in products:
            # Check if the product is in the dictionary
            if prod in list(self.count_dic.get(state_id, {}).keys()):
                # Update the count by 1
                self.count_dic[state_id][prod] += 1
            else:
                if state_id not in self.count_dic.keys():
                    self.count_dic[state_id] = {}
                self.count_dic[state_id][prod] = 1
            # Update db
            update = {"$set": {f"data.{prod}": self.count_dic[state_id][prod]}}
            self.count_col.update_one(query, update)
            # Check
            if prod in list(self.reco_count_dic.get(state_id, {}).keys()):
                # Update the recommended products with 1
                self.reco_count_dic[state_id][prod] += 1
            else:
                # Initialise the recommended products as 1
                if state_id not in self.reco_count_dic.keys():
                    self.reco_count_dic[state_id] = {}
                self.reco_count_dic[state_id][prod] = 1
            # Update db
            update = {"$set": {f"data.{prod}": self.reco_count_dic[state_id][prod]}}
            self.reco_count_col.update_one(query, update)
            # Check
            if prod not in list(self.pol_dic.get(state_id, {}).keys()):
                # Initialise the value as 0
                self.pol_dic[state_id][prod] = 0
                # Update db
                update = {"$set": {f"data.{prod}": self.pol_dic[state_id][prod]}}
                self.pol_col.update_one(query, update)
            if prod not in list(self.rew_dic.get(state_id, {}).keys()):
                # Initialise the reward dictionary as 0
                self.rew_dic[state_id][prod] = GaussianDistribution(loc=0, scale=1, size=1)[0].round(2)
                # Update db
                update = {"$set": {f"data.{prod}": self.rew_dic[state_id][prod]}}
                self.rew_col.update_one(query, update)
        print("[INFO] Completed the initial dictionary updates")

    def _dic_adder(self, products: list, username: str, state_id: str):
        # Loop through the product list
        for prod in products:
            # Initialise the count as 1
            self.count_dic[state_id][prod] = 1
            # Initialise the value as 0
            self.pol_dic[state_id][prod] = 0
            # Initialise the recommended products as 1
            self.reco_count_dic[state_id][prod] = 1
            # Initialise the reward dictionary as 0
            self.rew_dic[state_id][prod] = GaussianDistribution(loc=0, scale=1, size=1)[0].round(2)
        print("[INFO] Completed the dictionary initialization")
        # Next update the collections with the respective updates
        self._update_collections(username, state_id)
        print('[INFO] Completed updating all the collections')

    @staticmethod
    def _get_reward(value: float | int):
        rew = GaussianDistribution(loc=value, scale=1, size=1)[0].round(2)
        return rew

    def _sa_policy(self, state_id: str, reward: float, prod: str):
        # This function gets the relevant algorithm for the policy update
        # Get the current value of the state
        v = self.pol_dic[state_id][prod]
        # Get the counts of the current product
        n = self.reco_count_dic[state_id][prod]
        # Calculate the new value
        new_v = (1 / n) * (reward - v)
        return new_v

    def _update_reward_and_policy(self, state_id: str, key: str, value: float | int):
        # Get the reward for the product. The reward will be centered around the defined reward for each action
        rew = self._get_reward(value)
        # Update the reward in the reward dictionary
        self.rew_dic[state_id][key] += rew
        # Update the policy based on the reward
        self.pol_dic[state_id][key] += self._sa_policy(state_id, rew, key)

    def _update_collections(self, username: str, state_id: str):
        # Next update the collections with the respective updates
        print('[INFO] Updating all the collections')
        query = {"username": username, "state": state_id.replace("random_", "")}
        for key, coll in self.collections_.items():
            data = {"data": {str(k): v for k, v in getattr(self, key).items() if v}}
            if coll.find_one_and_update(query, {"$set": data}) is None:
                coll.insert_one(query | data)
        print('[INFO] Completed updating all the collections')


class CustomerActions:

    @staticmethod
    def random_action(products: list[str]) -> str:
        print('[INFO] getting the customer action')
        # Sample a value to get how many products will be clicked
        p = [0.50, 0.35, 0.10, 0.025, 0.015, 0.0055, 0.002, 0.00125, 0.00124, 0.00001]
        idx = np.random.choice(np.arange(0, len(p)), p=p)
        return products[idx]

import pandas as pd
import numpy as np
import networkx as nx

def get_data(college):
    offers = pd.read_csv(f"data/offers/{college}_offers.csv")
    commits = pd.read_csv(f"data/commits/{college}_commits.csv")

    offers = offers.loc[offers['ranking'] != 0]
    commits = commits.loc[commits['ranking'] != 0]

    offers['col'] = college
    commits['col'] = college

    return offers, commits

def get_graph(college, edge='ranking'):
    offers, commits = get_data(college)
    
    G_offer = nx.from_pandas_edgelist(offers, source = 'col', target = 'name', edge_attr=edge, create_using = nx.DiGraph())
    G_commit = nx.from_pandas_edgelist(commits, source = 'name', target = 'col', edge_attr=edge, create_using = nx.DiGraph())

    G = nx.compose(G_offer, G_commit)

    return G

def get_weighted_reciprocity(college):
    offers, commits = get_data(college)

    return 2 * np.sum(commits['ranking']) / (np.sum(commits['ranking']) + np.sum(offers['ranking'])) 

def get_reciprocity(college):
    offers, commits = get_data(college)

    return 2 * len(commits['ranking']) / (len(commits['ranking']) + len(offers['ranking']))

def get_avg_rank(college):
    offers, commits = get_data(college)

    return np.mean(offers['ranking']), np.mean(commits['ranking'])

def get_reciprocity_df(colleges):
    rec = pd.DataFrame(colleges, columns=['colleges'])

    rec['rec'] = rec.apply(lambda row : get_reciprocity(row['colleges']), axis = 1)
    rec['w_rec'] = rec.apply(lambda row : get_weighted_reciprocity(row['colleges']), axis = 1)
    rec['offer_rank'], rec['commit_rank']= zip(*rec.apply(lambda row : get_avg_rank(row['colleges']), axis = 1))
    
    return rec
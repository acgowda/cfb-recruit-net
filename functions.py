import pandas as pd
import numpy as np
import networkx as nx

def get_data(college, year):
    """Returns offer and commit data for a college."""

    offers = pd.read_csv(f"data/{year}/{college}_offers.csv")
    commits = pd.read_csv(f"data/{year}/{college}_commits.csv")

    offers = offers.loc[offers['ranking'] != 0]
    commits = commits.loc[commits['ranking'] != 0]

    offers['col'] = college
    commits['col'] = college

    return offers, commits

def get_graph(college, year, edge='ranking'):
    """Returns a graph for a college with commits and offers."""

    offers, commits = get_data(college, year)
    
    G_offer = nx.from_pandas_edgelist(offers, source = 'col', target = 'name', edge_attr=edge, create_using = nx.DiGraph())
    G_commit = nx.from_pandas_edgelist(commits, source = 'name', target = 'col', edge_attr=edge, create_using = nx.DiGraph())

    G = nx.compose(G_offer, G_commit)

    return G

def get_weighted_reciprocity(college, year):
    """Returns the weighted reciprocity of a college's network"""

    offers, commits = get_data(college, year)

    return 2 * np.sum(commits['ranking']) / (np.sum(commits['ranking']) + np.sum(offers['ranking'])) 

def get_reciprocity(college, year):
    """Returns the reciprocity of a college's network"""

    offers, commits = get_data(college, year)

    return 2 * len(commits['ranking']) / (len(commits['ranking']) + len(offers['ranking']))

def get_avg_rank(college, year):
    """Returns the average ranking of players recieving offers and players who commit for a college"""

    offers, commits = get_data(college, year)

    return np.mean(offers['ranking']), np.mean(commits['ranking'])

def get_reciprocity_df(colleges, year):
    """Returns a DataFrame containing reciprocity and ranking measures for the given colleges"""

    rec = pd.DataFrame(colleges, columns=['colleges'])

    rec['rec'] = rec.apply(lambda row : get_reciprocity(row['colleges'], year), axis = 1)
    rec['w_rec'] = rec.apply(lambda row : get_weighted_reciprocity(row['colleges'], year), axis = 1)
    rec['offer_rank'], rec['commit_rank']= zip(*rec.apply(lambda row : get_avg_rank(row['colleges'], year), axis = 1))
    
    return rec
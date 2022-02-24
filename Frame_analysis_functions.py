import pandas as pd
import numpy as np
from tqdm import tqdm

from sklearn.feature_extraction.text import CountVectorizer
from scipy.stats import pearsonr

from procedural_stop_words import procedural_stop_words

from scipy.spatial.distance import cosine

def make_DTM(sub,binary=True,remove_speaker=True):
    """
    Make a Document Term Matrix from topic subset speeches
    
    args:
        - sub: pandas dataframe with speeches and metadata
        - binary: 1 or count for term occurence in document
    returns:
        - Document Term Matrix
    
    """
    # speaker and party ID
    features = sub.groupby('speaker',as_index=False).party_y.first()
    
    # document term matrix
    vectorizer = CountVectorizer(min_df=5,binary=binary,stop_words=procedural_stop_words)
    DTM = vectorizer.fit_transform(sub.speech_processed)
    DTM = pd.DataFrame(DTM.toarray())

    # assign terms to DTM
    terms = vectorizer.get_feature_names()
    
    # associate DTM with speaker and get term-speech frequency by speaker
    DTM['speaker'] = list(sub['speaker'])
    DTM = (DTM
           .groupby('speaker',as_index=False)
           .sum()
           .merge(features,on='speaker',how='left')
          )

    if remove_speaker:
        DTM = DTM.drop('speaker',1)
        DTM.columns = terms + ['party_y']
    else:
        DTM.columns = ['speaker'] + terms + ['party_y']
        
    return DTM


def chi_sq(x):
    """
    Run chi-squared test from Gentzkow et al. 2010.
    to be run on each term in frequency frame
    """
    
    numer = ((x['R']*x['Dn']) - (x['D']*x['Rn']))**2
    denom = (x['R'] + x['D']) * (x['R'] + x['Rn']) * (x['D'] + x['Dn']) * (x['Dn'] + x['Rn'])
    return numer/denom


def chiSq_df(dtm,permute=False):
    """
    sets up dataframe containing term frequencies and
    expected frequencies for chi-square test
    
    args:
        - dtm: Document Term Matrix
        - permute: if True shuffle speaker values (default False)
    returns:
        - term_frequencies dataframe with chi-square stats
    """
    
    if permute: # shuffle party labels
        dtm.party_y = np.random.permutation(dtm.party_y.values)
        
    term_frequencies = dtm.groupby('party_y').sum().T  # term frequency by party
    total_frequencies = term_frequencies.sum()  # total frequencies

    # set up for chi-square test
    term_frequencies['Dn'] =  total_frequencies['D'] - term_frequencies['D'] 
    term_frequencies['Rn'] = total_frequencies['R'] - term_frequencies['R']
    term_frequencies['chi2'] = term_frequencies.apply(chi_sq,1)

    term_frequencies['terms'] = dtm.columns[:-1]
    
    return term_frequencies

def perform_correlations(dtm,permute=False):
    """
    runs correlation analysis on every term with party ID
    method from Jensen et al. 2012
    
    args:
        - dtm: Document Term matrix containing speech-term frequencies
        - permute: if True, shuffle party labels (default False)
    returns:
        - dataframe containing Pearson r values for every word
    """
    
    # contrast code for party
    party_ID = [-1 if party == 'D' else 1 for party in dtm.party_y]
    dtm = dtm.drop('party_y',1)
    
    # normalize frequencies
    dtm_normed = np.apply_along_axis(lambda x: (x - np.mean(x))/np.std(x),0,dtm.to_numpy())
    
    # perform correlation analysis
    if permute:
        party_ID = np.random.permutation(party_ID)
        
    # perform correlations
    corrs = np.apply_along_axis(lambda x: pearsonr(x,party_ID)[0],0,dtm_normed)
    
    df = pd.DataFrame({
            "term":dtm.columns,
            "correlation":corrs,
            'freq':dtm.sum(0)
        }).dropna()
    
    return df

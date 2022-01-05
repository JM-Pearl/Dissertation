from sklearn.decomposition import NMF
import numpy as np
import Rankings
import TC_W2V

metric = Rankings.AverageJaccard()
matcher = Rankings.RankingSetAgreement(metric)

def run_nmf(n_topics,X,topn=10):
    nmf = NMF(n_components=n_topics,
              init='nndsvd',
              max_iter=500)
    
    W = nmf.fit_transform(X)
    H = nmf.components_
    
    term_rankings = []
    for topic_index in range(n_topics):
        term_rankings.append(np.argsort(H[topic_index,:])[::-1])
    term_rankings = np.array(term_rankings)[:,:topn]
    
    return term_rankings, H


def nmf_iters(n_topics,X,runs=10,sample_prop=0.8):
    indices = list(range(X.shape[0]))    
    outer_rankings = []
    for r in range(runs):
        np.random.shuffle(indices)
        S = X[indices[:int(np.floor(sample_prop*X.shape[0]))],:]
        
        term_ranks = run_nmf(n_topics,X,topn=10)
        outer_rankings.append(term_ranks)
    return outer_rankings

        
def get_agreement(reference,iterations,w2v,vocab):

    ref = reference[0]
    ref_H = reference[1]
    
    tc_w2v = [TC_W2V.run_coherence(ref_H,vocab,w2v)]
    stability = []
    
    for it,H in iterations:
        stabil = matcher.similarity(ref,it)
        coherence = TC_W2V.run_coherence(H,vocab,w2v)
        
        stability.append(stabil)
        tc_w2v.append(coherence)
    
    return stability, tc_w2v
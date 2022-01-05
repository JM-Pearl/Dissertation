import numpy as np

def term_rankings(H,terms):
    term_rankings = []
    for topic_index in range(H.shape[0]):
        top_indices = np.argsort(H[topic_index,:])[::-1]
        term_ranking = [terms[i] for i in top_indices[:20]]
        term_rankings.append(term_ranking)
    return term_rankings

def similarity( w2v, ranking_i, ranking_j ):
    sim = 0.0
    pairs = 0
    for term_i in ranking_i:
        for term_j in ranking_j:
            try:
                sim += w2v.wv.similarity(term_i, term_j)
                pairs += 1
            except:
                pass
    if pairs == 0:
        return 0.0
    return sim/pairs

def tc_w2v(term_rankings,w2v):
    topic_scores = []
    overall = 0
    for index, topic in enumerate(term_rankings):
        score = similarity(w2v,topic,topic)
        topic_scores.append(score)
        overall += score
    overall /= len(term_rankings)
    return overall

def run_coherence(H,terms,w2v):
    rankings = term_rankings(H,terms)
    coherence = tc_w2v(rankings,w2v)
    return coherence
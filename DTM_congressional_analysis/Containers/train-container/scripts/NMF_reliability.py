import NMF as nmf_utils
from sklearn.feature_extraction.text import TfidfVectorizer

from multiprocessing import Pool
import time

import pandas as pd
import numpy as np
import joblib,os
from gensim.models import Word2Vec
import datetime


Party = 'R'

base_path = '/opt/ml/'
input_path = os.path.join(base_path,'input/data')
output_path = os.path.join(base_path,'output')
model_path = os.path.join(base_path,f'model')

training_path = os.path.join(input_path,'training')

# read in the data, should be a single .csv file
training_file = os.listdir(training_path)[0]
df = pd.read_csv(os.path.join(training_path,training_file))

congress = training_file.split('.')[0]

# filter house speeches
df = df.loc[df.chamber_x == 'H']
df = df.loc[df.party.isin([Party])]


# make gensim dict and corpus, tfidf transform
procedural_stop_words = ['talk','thing','colleague','hear','floor','think','thank','insert','section','act_chair','amendment','clerk','clerk_designate',
                        'pursuant','minute','desk','amendment_text','amendment_desk','rule','debate','process','offer_amendment','majority','order',
                        'pass','extension','urge','urge_colleague','defeat_previous','yield_balance','member','committee','chairman','mr','subcommittee',
                        'rank_member','mr_chairman','oversight','yield_minute','yield_time','gentlewoman','gentleman','gentlelady','h_r','time_consume',
                        'legislation','measure','rollcall','rollcall_vote','vote_aye','vote_nay','nay','debate','point_order','chair','clause',
                        'clause_rule','germane','sustain','remark','conference','pass','oppose','offer','opposition','ask','speaker','bill',
                        'follow_prayer','approve_date','pledge_journal','morning_hour','today_adjourn','proceeding','deem_expire','reserve','complete',
                        'permit_speak','authorize_meet','session_senate','office_building','entitle','conduct_hearing','m_room','consent','ask_unanimous',
                        'dirksen_senate','senate_proceed','intervene_action','consider','notify_senate','senate','legislative_session','legislation',
                        'legislature','further_motion','motion','lay_table','motion_reconsider','reconsider','hearing','leader','p_m','a_m','period_morning',
                        'period_afternoon','executive_session','follow','senate_proceed','morning_business','authorize','motion_concur','concur','session',
                        'hour','control','follow_morning','senate_resume','follow','monday','tuesday','wednesday','thursday','friday','ask_unanimous',
                        'motion_reconsider','amendment','consent','motion_proceed','cloture','proceed','motion_invoke','cloture_motion','leader','invoke',
                        'no_','modify']

# W2V for coherence
speeches = [i.split() for i in df.speech_processed]
w2v_model = Word2Vec(speeches,window=10,sg=1,workers=10)
print(f"\nmodel training time: {str(datetime.timedelta(seconds=w2v_model.total_train_time))}")

# make DTM
vectorizer = TfidfVectorizer(min_df=0.001,max_df=0.35,stop_words=procedural_stop_words)
X = vectorizer.fit_transform(df.speech_processed)
vocab = vectorizer.get_feature_names()

def RUN_NMF(k):
    print(f'started {k}')
    reference = nmf_utils.run_nmf(k,X)
    iters = nmf_utils.nmf_iters(k,X)
    vals = nmf_utils.get_agreement(reference,iters,w2v_model,vocab)
    print(f'ended {k}')
    return {"k":k,"values":vals}

k_list = [10, 20, 25] + list(range(30,80,2)) + [85,90,95,100,120]
with Pool(35) as p:
    output = p.map(RUN_NMF,k_list)

with open(os.path.join(model_path,f'NMF_{congress}_{Party}_reliabilityEval.pkl'),'wb') as out:
    joblib.dump(output,out)
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
                        'motion_reconsider','amendment','consent','motion_proceed','cloture','proceed','motion_invoke','cloture_motion','invoke',
                        'no_','modify','program','percent','increase','fund','funding','suspension', 'count', 'yesterday', 'tomorrow','act',
                        'previous_question', 'present', 'record','resolution', 'house_concurrent', 'house_joint', 'previous_question', 'yield_such',
                         'introduce', 'call', 're', 'recognize', 'commend', 'cosponsor', 'express', 'print', 'action', 'pursuant_house', 'h_re',
                         'continue', 'sponsor','yield', 'thank_gentleman', 'second', 'friend', 'comment', 'appreciate', 'gentleman_california',
                         'statement', 'distinguished', 'gentleman_texas', 'thank_gentlewoman', 'gentleman_ohio', 'gentleman_illinois', 'gentleman_pennsylvania',
                         'gentleman_florida', 'gentleman_michigan', 'want_commend', 'bring', 'special_order','house_representative', 'leadership', 'bring',
                         'consideration', 'matter', 'other_body', 'adjourn', 'legislative', 'version', 'move', 'meet', 'resolve', 'motion_instruct', 'appropriation_bill',
                        'madam_speaker', 'yield_such', 'reserve_balance', 'bipartisan', 'support_h', 'previous_question', 'introduce', 'important', 'good_friend',
                         'rise_today', 'pleased', 'sponsor', 'rise', 'like_thank', 'representative', 'second', 'want_thank', 'leadership', 'join', 'allow',
                        'consideration', 'discharge_further', 'ask_immediate', 'j_re', 'joint_resolution', 'immediate_consideration', 'week', 'senate_joint',
                         'designate', 'designate_week', 're', 'h_j','america','american','work','law','want','issue','get','try','take','let','question','answer',
                        'report','say','know','come','tell','people','country','language','conference','conference_report','need','see','commission',
                        'let','tell','day','united_state','deal','point','address','look','congress','congressional','go','come','put','agree','yield']

state_names = [i.lower() for i in ["Alaska", "Alabama", "Arkansas", "American_Samoa", "Arizona", "California", "Colorado", "Connecticut", "District_of_Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North_Carolina", "North_Dakota", "Nebraska", "New_Hampshire", "New_Jersey", "New_Mexico", "Nevada", "New_York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto_Rico", "Rhode_Island", "South_Carolina", "South_Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin_Islands", "Vermont", "Washington", "Wisconsin", "West_Virginia", "Wyoming"]]

procedural_stop_words.extend(state_names)
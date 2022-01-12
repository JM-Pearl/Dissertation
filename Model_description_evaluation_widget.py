import ipywidgets as widgets
from IPython.display import display
from ipywidgets import Layout, Box


def get_window_topic_descriptions(topic,mapper):
    topic_id_df = mapper.loc[mapper.dynamic_id == topic]
    descriptions = []
    for ix,row in topic_id_df.iterrows():
        window_id = row['window_id']
        formatted = f"{window_id}: {', '.join(row['window_descriptions'])}"
        descriptions.append(formatted)

    return '\n\n'.join(descriptions)

def run_widget(dynamic_descriptions,mapper):
    dt = widgets.Dropdown(
        options=range(len(dynamic_descriptions)),
        value=0,
        description='Dynamic Topic #:',
        disabled=False,
    )

    terms = widgets.HTML(
        value=',  '.join(dynamic_descriptions[0]),
        placeholder='',
        description='',
    )

    windows = widgets.Textarea(
        value=get_window_topic_descriptions(0,mapper),
        placeholder='Type something',
        description='Window Descriptions',
        disabled=True,
        layout={'width': '100%',"height":'400px'}
    )



    items_layout = Layout( width='auto')     # override the default width of the button to 'auto' to let the button grow

    box_layout = Layout(display='flex',
                        flex_flow='column',
                        align_items='stretch',
                        width='100%')

    items = [dt,terms,windows]

    def on_value_change(change):
        terms.value = ',  '.join(dynamic_descriptions[change['new']])
        windows.value = get_window_topic_descriptions(change['new'],mapper)


    dt.observe(on_value_change, names='value')

    return Box(children=items, layout=box_layout)


def get_speech_info(mapper,DF,year,topic):
    window_sub = mapper.loc[(mapper.year == str(year)) & (mapper.dynamic_label == topic)]
    
    descriptions = []
    for ix,row in window_sub.iterrows():
        window_id = row['topic_id']
        formatted = f"{window_id}: {', '.join(row['window_terms'])}"
        descriptions.append(formatted)
    

    speech_list = DF.loc[(DF.year_x == year) & (DF.topic_id.isin(window_sub.topic_id))]
    if len(speech_list) > 5:
        speech_strings = []
        for ix,row in speech_list.sample(5).iterrows():
            speech_strings.append(f"{row.topic_id}: {row.speech_text}")
    else:
        speech_strings = ['']
        
    return '\n\n'.join(descriptions), '\n\n'.join(speech_strings)
    
def Run_speech_widget(speech_df,mapper):
    
    year = 1983
    topic = 'abortion'
    
    dt = widgets.Dropdown(
        options=speech_df.dynamic_label.unique(),
        value='abortion',
        description='Dynamic Topic #:',
        disabled=False,
    )
    
    year_val = widgets.Dropdown(
        options=speech_df.year_x.unique(),
        value=1983,
        description='Year:',
        disabled=False,
    )
    window_topics, speeches_string = get_speech_info(mapper,speech_df,year,topic)
    
    terms = widgets.Textarea(
        value=window_topics,
        placeholder='',
        description='Window Descriptions',
        disabled=True,
        layout={'width': '100%',"height":'100px'}
    )
    
    speeches = widgets.Textarea(
        value=speeches_string,
        placeholder='',
        description='speeches',
        disabled=True,
        layout={'width': '100%',"height":'400px'}
    )

    items_layout = Layout( width='auto')     # override the default width of the button to 'auto' to let the button grow

    box_layout = Layout(display='flex',
                        flex_flow='column',
                        align_items='stretch',
                        width='100%')

    items = [dt,year_val,terms,speeches]

    def on_value_change(change):
        print(change)
        if change['owner'] == year_val:
            window_topics, speeches_string = get_speech_info(mapper,speech_df,change['new'],dt.value)
        else:
            window_topics, speeches_string = get_speech_info(mapper,speech_df,year_val.value,change['new'])

        
        
        terms.value = window_topics
        speeches.value = speeches_string

    dt.observe(on_value_change, names='value')
    year_val.observe(on_value_change,names='value')
    
    return Box(children=items, layout=box_layout)
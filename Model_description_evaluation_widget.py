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

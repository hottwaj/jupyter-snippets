import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from prettypandas import PrettyPandas
import plotly.plotly_pandas as ply_pd

from functools import reduce
default_td_kwargs = {'style': {'border': 'none'}}
def to_html_table_contents(rows_list, tr_kwargs = {}, td_kwargs = {}):
    td_kwargs = reduce(ply_pd.dict_merge, [{}, default_td_kwargs, td_kwargs])
    return [html.Tr([html.Td([cell], **td_kwargs) for cell in row], **tr_kwargs) 
            for row in rows_list]
            
def dash_assets_folder():
    import os
    fpath, module_file = os.path.split(__file__)
    return fpath + '/dash_assets/'
    
def input_separator():
    return html.Div(style = {'padding': '10px'})

def input_to_int(v):
    try:
        return int(v)
    except (ValueError, TypeError):
        return None
        
        
from io import BytesIO
import base64
def fig_to_uri(in_fig, close_all=True, format='png', figsize=None, **save_args):
    # type: (plt.Figure) -> str
    """
    Save a figure as a URI
    :param in_fig:
    :return:
    """
    if figsize is not None:
        in_fig.set_size_inches(*figsize, forward=True)
        
    in_fig.tight_layout()        
        
    out_img = BytesIO()
    in_fig.savefig(out_img, format=format, **save_args)
    if close_all:
        in_fig.clf()
        #plt.close('all')
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    if format == 'svg':
        return "data:image/svg+xml;base64,{}".format(encoded)
    else:
        return "data:image/png;base64,{}".format(encoded)

def get_input_td_style(**kwargs):
    style = {'vertical-align': 'top', 
             'border-bottom': 'none',
             'padding-bottom': '0px'}
    style.update(kwargs)
    return style
    
def style_table(dtable, font_size = 12, cell_padding = 5):
    dtable.style_cell = {'font-size': font_size, 
                         'font-family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"',
                         'height': '24px'}
    dtable.style_header = {'font-weight': 'bold', 'background': '#eee', 'text-align': 'left'}
    dtable.style_table = {'width': ''}
    has_editable_columns = any([c_info.get('editable', getattr(dtable, 'editable', False)) for c_info in dtable.columns])
    
    if has_editable_columns:
        dtable.style_data_conditional = getattr(dtable, 'style_data_conditional', []) + [
                {
                    'if': {'column_editable': False},
                    'background-color': '#eee',
                }
            ]
    dtable.css = getattr(dtable, 'css', []) + [
        { # override default css for selected/focused table cells
            'selector': 'td.cell--selected',
            'rule': """
                    not-used-outline: 1px solid #3C3C3C;
                    box-shadow: 0 0 5px 1px #3c3c3c;
                    transform: scale(1,1);  /* transform seems to make box-shadow overlay upper and left cells, which otherwise hide the shadow */
                    
                    """
        }, {'selector': 'td.dash-cell',
            'rule': """
                       not-used-background-color: rgb(255,204,153); 
                       not-used--selected-background: rgb(255,204,153) !important;
                       --accent: #3C3C3C !important;
                    """   
        }, {'selector': '.dash-dropdown-cell-value-container',  #dropdown cell values left aligned
            'rule': """
                       text-align: left;
                    """
        }, {'selector': '.dash-spreadsheet-container .dash-spreadsheet-inner table',          #always show dropdown arrow in black
            'rule': """
                        --faded-dropdown: #3C3C3C !important;
                    """
        }, {'selector': '.dash-spreadsheet-inner td, .dash-spreadsheet-inner th',
            'rule': """
                        padding: %dpx !important;
                    """ % cell_padding
        }
        ] + [{ #make not editable cells not look selected
            'selector': 'td.column-%d' % i,
            'rule': """
                       not-used--accent: rgb(211, 211, 211) !important;
                       not-used-border: 1px solid rgb(211, 211, 211) !important;
                       box-shadow: none !important;
                       --selected-background: %s !important;
                    """ % ('#EEE' if has_editable_columns else '#FFF')
        } for i, c_info in enumerate(dtable.columns) 
          if c_info.get('editable', getattr(dtable, 'editable', False)) == False]
    return dtable

def pp_or_df_to_dash_table(pp_or_df_obj, editable = False, styled = True, style_kwargs = {}, caption = None, use_pp_caption = False):
    if isinstance(pp_or_df_obj, PrettyPandas):
        if use_pp_caption:
            caption = pp_or_df_obj.caption
        df = pp_or_df_obj.get_formatted_df(as_html=False).copy()
    else:
        #assume already formatted dataframe
        df = pp_or_df_obj.copy()
        
    if df.index.name is None:
        df.index.name = ''
    index_col = df.index.name
    df = df.reset_index()
    dt = dash_table.DataTable(
        columns=[{"name": i, 
                  "id": i,
                  "editable": editable if i != index_col else False} for i in df.columns],
        data=df.to_dict('records'),
        style_data_conditional=[{
            'if': {'column_id': index_col},
            'backgroundColor': '#eee',
            'font-weight': 'bold',
        }],        
        editable=editable
    )
    
    for k in ['AVERAGE', 'TOTAL']:
        if k in df[index_col].values:
            i = df[df[index_col] == k].index[0]
            dt.style_data_conditional.extend([{
                "if": {"row_index": i},
                "backgroundColor": "#eee",
                'font-weight': 'bold',
            }])

    if styled:
        style_table(dt, **style_kwargs)
    
    if caption is not None:
        return html.Div([html.Label(caption), dt])
    else:
        return dt

def round_dash_table_records(dt_records, precision = 5):
    for rec in dt_records:
        for k in rec:
            if isinstance(rec[k], float):
                rec[k] = round(rec[k], precision)
                
    return dt_records

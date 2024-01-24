import dash
from dash import Dash, html, dash_table, dcc, Input, Output, State 
import pandas as pd

# Sample Data
data = pd.DataFrame({
    'Column1': ['Row 1', 'Row 2', 'Row 3'],
    'Column2': ['Editable', 'Editable', 'Editable']
})

app = Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='table-editing-simple',
        columns=(
            [{'id': 'Column1', 'name': 'Column 1'}] +
            [{'id': 'Column2', 'name': 'Column 2', 'editable': True}]
        ),
        data=data.to_dict('records'),
        editable=True,
        cell_selectable=True # NEU 
    ),
dcc.Input(
    id='editing-columns-input', 
    style={'display': 'none'},
    className='popup'
), # NEU
    html.Button('Update Data', id='editing-columns-button', n_clicks=0),  #NEU
    html.Div(id='editing-columns-output') #NEU
])

@app.callback(
    Output('editing-columns-input', 'style'),
    Input('table-editing-simple', 'active_cell'),
    State('editing-columns-input', 'style')
)


#NEU
def display_input(cell, style):
    if cell and style['display'] == 'none':
        return {'display': 'block'}
    return {'display': 'none'}

@app.callback(
    Output('table-editing-simple', 'data'),
    [Input('editing-columns-button', 'n_clicks'),
     Input('editing-columns-input', 'n_submit')],
    [State('table-editing-simple', 'data'),
     State('table-editing-simple', 'active_cell'),
     State('editing-columns-input', 'value')]
)

#NEU
def update_table(n_clicks, n_submit, rows, cell, value):
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if cell and (trigger == 'editing-columns-button' or trigger == 'editing-columns-input'):
        rows[cell['row']][cell['column_id']] = value
    return rows



if __name__ == '__main__':
    app.run_server(debug=True)

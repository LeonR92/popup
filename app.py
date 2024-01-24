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
        cell_selectable=True
    ),
    dcc.Input(
        id='editing-columns-input', 
        style={'display': 'none'},
        className='popup'
    ),
    html.Button('Update Data', id='editing-columns-button', n_clicks=0),
    html.Div(id='editing-columns-output')
])

@app.callback(
    [Output('table-editing-simple', 'data'),
     Output('editing-columns-input', 'style'),
     Output('editing-columns-input', 'value')],
    [Input('editing-columns-button', 'n_clicks'),
     Input('editing-columns-input', 'n_submit'),
     Input('table-editing-simple', 'active_cell')],
    [State('table-editing-simple', 'data'),
     State('editing-columns-input', 'value')]
)
def update_table_and_input(n_clicks, n_submit, cell, rows, input_value):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'table-editing-simple':
        # Active cell is selected
        if cell:
            row = cell['row']
            col = cell['column_id']
            current_value = rows[row][col]
            return rows, {'display': 'block'}, current_value
        return dash.no_update

    if trigger_id in ['editing-columns-button', 'editing-columns-input']:
        # Update Data button or Enter key in input field is pressed
        if cell:
            rows[cell['row']][cell['column_id']] = input_value
        return rows, {'display': 'none'}, ''

    return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)

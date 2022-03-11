import dash
import dash_bootstrap_components as dbc
import pandas                    as pd
import plotly.express            as px

from dash                        import dash_table, Dash, dcc, html
from dash.dependencies           import Input, Output, State
from dash.exceptions             import PreventUpdate
import dash_vtk

dff = pd.read_csv(r"/home/saim/Desktop/cs-training.csv")
df = dff.iloc[0: 50, :]


#states = df.State.unique() # for bar stuff




def build_view_child(dimensions, spacing, origin, field, enabled, window, level):
    slice_prop = {"colorWindow": window, "colorLevel": level}
    child = [
        dash_vtk.ShareDataSet(
            dash_vtk.ImageData(
                dimensions=dimensions,
                spacing=spacing,
                origin=origin,
                children=dash_vtk.PointData(
                    dash_vtk.DataArray(registration="setScalars", values=field)
                ),
            ),
        ),
    ]

    if "Volume" in enabled:
        child.append(
            dash_vtk.VolumeRepresentation(
                [dash_vtk.VolumeController(), dash_vtk.ShareDataSet()],
            )
        )

    return child



app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


##INIT##
app = dash.Dash(
    __name__,
    suppress_callback_exceptions = True,
    #prevent_initial_callbacks=True,
    title = "My app",
)
server = app.server


# fig = px.bar(df, x = "State", y = "Number of Solar Plants")

# fig.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
# )

app.layout = dbc.Container([

    #dcc.Graph(id = "bar-chart"),

    dash_table.DataTable(
         df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], 
         filter_action = 'native',
         id = 'tbl_out'), 


])

# table callback
# @app.callback(
#     Output('tbl_out', 'children'), 
#      #Output("bar-chart", "figure"), 
#     Input('tbl', 'active_cell')
#     )

# def update_graphs(active_cell):
#     return str(active_cell) if active_cell else "Click the table"







# barchart callback
# @app.callback(
#     Output("bar-chart", "figure"), 
#     [Input("bar-chart", "figure")])

# def update_bar_chart(states):
#     mask = df["State"] == states
#     fig = px.bar(df, x = "State", y = "Number of Solar Plants", barmode = 'group')
#     return fig


##RUN##
if __name__ == '__main__':
    app.run_server(debug = True, 
                   port=8050,
                   host='0.0.0.0'
                   )
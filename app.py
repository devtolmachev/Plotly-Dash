from typing import Any

from dash import Dash, Input, Output, State

from core.web.types.elements import DashElements
from etc.webapp import DF, get_layout

app = Dash(name=__name__)
app.layout = get_layout(DF)


@app.callback(
    Output(component_id='timeline_card', component_property='figure'),
    Input(component_id='states-category', component_property='n_clicks'),
    State(component_id='dropdown-category-states', component_property='value')
)
def update_data(n_clicks: int, category_state: str | list) -> Any:
    elements = DashElements()

    filter_data = DF if isinstance(
        category_state, list) or category_state is None else DF[
        (DF["state"] == category_state)]
    fig = elements.timeline(filter_data, opacity=0.5)

    fig.update_traces(marker=dict(color=filter_data["color"]))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

# Imports
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
from dash import html, dcc
from pandas import DataFrame

from core.database.types import BaseType
from core.web.types.elements import DashElements
from utils.human_readable import HumanReadableTime


def make_df_from_db_data(database: str = 'testDB.db') -> DataFrame:
    """
    Make more humanize dataframe for targets of project
    Parameters
    ----------
    database : Name Database File

    Returns
    -------
    Return Dataframe in which all date-time values brought to
    datetime type

    """
    utils = BaseType(database=database)
    df = pd.read_sql(sql=utils.qm.select('sources', columns='*'),
                     con=utils.database.connection)
    columns: list[str] = [
        "shift_day",
        "operator_auth_end",
        "operator_auth_start",
        "state_end",
        "state_begin",
        "calendar_day"
    ]
    # This list of all name columns which must be a DateTime Object
    for column in columns:
        df[column] = pd.to_datetime(df[column])
    return df


DF = make_df_from_db_data()

# TIMELINE
figure = px.timeline(
    DF,
    x_start='state_begin',
    x_end='state_end',
    y='endpoint_name',
    title='График состояний',
    height=325,
    width=1680,
    hover_data={
        'color': False,
        'state_begin': False,
        'state_end': False,
        'endpoint_name': False,
        'status': False,
        'state': True,
        'reason': True,
        'operator_auth_start': True,
        'duration_min': True,
        "shift_day": True,
        'period_name': True,
        'operator': True
    },
    labels={
        'endpoint_name': '',
        'state': 'Состояние',
        'reason': 'Причина',
        'operator_auth_start': 'Начало',
        'duration_min': 'Длительность',
        "shift_day": "Сменный день",
        'period_name': 'Смена',
        'operator': 'Оператор',
    },
    opacity=.3)


def get_layout(df):
    # Objects of classes
    elements = DashElements()
    hrt = HumanReadableTime()

    # Data
    state_begin = hrt.default(df["state_begin"])
    state_end = hrt.default(df["state_end"])
    items = [x for x in list(set(df["state"]))]
    items.sort()
    # I used list completention to get unique reasons of states.
    # After that I sorted the list alphabetically

    # Elements
    sycle_diogram = elements.get_pie_chart(
        df=df).update_traces(marker=dict(colors=df["color"]))
    dropdown = dcc.Dropdown(items,
                            value=items,
                            id='dropdown-category-states',
                            style={
                                'z-index': '999999'
                            })
    figure.update_traces(
        marker=dict(color=df["color"])).update_layout(bargap=0,
                                                      bargroupgap=0)

    # Make Structure
    cols = [
        dmc.Col([
            elements.build_card(
                html.Div([dropdown], style={
                    "width": '40%',
                    "margin-top": "5px",
                    "margin-left": "500px",
                }),
                html.H1(f'Клиент: {df["client_name"][0]}'),
                html.H3(f'Сменный день: {df["shift_day"][0]}'),
                # I have never made websites at all, and I had little
                # experience with the web. so please do not judge strictly
                # for the web structure.

                # (Я вообще никогда не верстал сайты, и у меня было мало опыта
                # с вебом. Поэтому прошу не судить строго за веб структуру.)
                html.H3(f'Точка учета: {df["endpoint_name"][0]}'),
                html.H3(f'Начало периода: {state_begin}'),
                html.H3(f'Конец периода: {state_end}'),
                dmc.Button('Фильтровать',
                           id='states-category', uppercase=True, size='md',
                           radius='lg',
                           style={
                               "width": '30%',
                               "margin-top": "50px",
                               "margin-left": "32%",
                               'verticalAlign': 'middle',
                           }), **elements.CARD_STYLE
            )], span=6),
        dmc.Col([
            elements.build_card(
                dcc.Graph('sycle diogram',
                          figure=sycle_diogram), **elements.CARD_STYLE
            )], span=6),

        dmc.Col([
            elements.build_card(
                dcc.Graph(figure=elements.timeline(df=df).update_traces(
                    marker=dict(color=df["color"])
                ),
                    id='timeline_card'),
                **elements.CARD_STYLE
            )], span=12)
    ]

    # Build Human Readable Data
    return html.Div(
        dmc.Paper(
            [dmc.Grid(cols)]
        )
    )


# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Привожу значения списков в удобночитаемый формат для отображения
# на веб странице, с помощью списковых включений
DF["duration_min"] = [f'{round(x, 2)} мин.' for x in DF["duration_min"]]
DF["operator_auth_start"] = [
    f"{x.time()} ({x.date().strftime('%d.%m')})"
    if not isinstance(x, pd._libs.NaTType) else 'Работа не шла'
    for x in DF["operator_auth_start"]
]
DF["shift_day"] = [
    x.date().strftime('%d.%m.%y')
    for x in DF["shift_day"]
]

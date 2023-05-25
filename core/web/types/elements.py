import dash_mantine_components as dmc
import plotly.express as px
import plotly.graph_objs as go
from pandas import DataFrame

from utils.exceptions import WrongTypeArgument


class DashElements:
    CARD_STYLE: dict = dict(
        withBorder=True,
        shadow="sh",
        radius="md",
        style={'height': '410px'}
    )

    @staticmethod
    def get_pie_chart(df: DataFrame) -> go.Figure:
        fig = px.pie(df,
                     values="duration_hour",
                     names="reason",
                     color='color',
                     height=390)
        return fig

    @staticmethod
    def build_card(*args, id_element: str = None, **kwargs) -> dmc.Card:
        card = dmc.Card([*args], **kwargs)
        if id_element is not None:
            card = dmc.Card([*args], **kwargs, id=id_element)
        return card

    @staticmethod
    def timeline(df: DataFrame,
                 labels: dict = None,
                 hober_data: dict = None,
                 **kwargs) -> go.Figure:
        if hober_data is None:
            hober_data = {
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
            }

        if labels is None:
            labels = {
                'endpoint_name': '',
                'state': 'Состояние',
                'reason': 'Причина',
                'operator_auth_start': 'Начало',
                'duration_min': 'Длительность',
                "shift_day": "Сменный день",
                'period_name': 'Смена',
                'operator': 'Оператор',
            }

        opacity = kwargs['opacity'] if kwargs.get('opacity') is not None else .3

        timeline = px.timeline(
            df,
            x_start='state_begin',
            x_end='state_end',
            y='endpoint_name',
            title='График состояний',
            height=325,
            width=1680,
            hover_data=hober_data,
            labels=labels,
            opacity=opacity,
            template='plotly_white',
        )

        return timeline

    @property
    def card_style(self) -> dict:
        return self.CARD_STYLE

    @card_style.setter
    def card_style(self, value: dict[str, str | bool]):
        if not isinstance(value, dict):
            raise WrongTypeArgument
        self.CARD_STYLE = value

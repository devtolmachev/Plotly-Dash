class HumanReadableTime:

    def __init__(self, ):
        pass

    @staticmethod
    def default(data: list,
                index: str | int = 0,
                strftime: str = '%d.%m'):
        time = f'{data[index].time()}'
        date = f'({data[index].date().strftime(strftime)})'
        return f"{time} {date}"

import plotly.express as px


def bar_chart():
    wide_df = px.data.medals_wide()
    fig = px.bar(wide_df, x="nation", y=["gold", "silver", "bronze"], title="Wide-Form Input")
    fig.show()


if __name__ == '__main__':
    bar_chart()

import pandas as pd
import plotly.express as px


def main():
    data = pd.read_csv("bleh.csv")
    wide_df = px.data.medals_wide()
    fig = px.bar(data,
                 x="Groep", y=["min 0-6", "min 6-12", "min 12-18"],
                 title="Wide-Form Input")
    fig.show()


if __name__ == '__main__':
    main()

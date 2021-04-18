from datetime import timedelta

from flask import Flask, render_template, request
import pandas as pd


class EventsTableCol:
    str_time = 'str_time'
    value = 'value'
    timestamp = 'timestamp'
    bins = 'bins'


class BinsSelector:
    def __init__(self, initial_timestamp: pd.Timestamp):
        self.start_time = initial_timestamp.replace(minute=0)

    def map_to_bin(self, timestamp: pd.Timestamp):
        delta_from_start = timestamp - self.start_time
        minute = delta_from_start.seconds / 60
        bin_index = int(minute / 5)
        bin_timestamp = self.start_time + timedelta(minutes=bin_index * 5)
        return bin_timestamp


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/load_event_bins")
def load_event_bins():
    csv_path = request.args.get('csv_path')
    list_events = process_event_table(csv_path)
    return render_template('index.html', list_events=list_events)


def process_event_table(csv_path):
    df = pd.read_csv(csv_path, header=None, names=[EventsTableCol.str_time, EventsTableCol.value])
    df[EventsTableCol.timestamp] = pd.to_datetime(df[EventsTableCol.str_time])
    first_event = df[EventsTableCol.timestamp].iloc[0]
    bin_selector = BinsSelector(first_event)
    df[EventsTableCol.bins] = df.apply(lambda row: bin_selector.map_to_bin(row[EventsTableCol.timestamp]), axis=1)
    mean_per_bins = df.groupby(EventsTableCol.bins).mean()
    list_events = mean_per_bins.reset_index().to_dict('records')
    return list_events


if __name__ == '__main__':
    app.run(debug=True)

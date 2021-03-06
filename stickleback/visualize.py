from matplotlib.figure import Figure as matplotlibFigure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs._figure import Figure as plotlyFigure
from plotly.subplots import make_subplots
from typing import Dict, Tuple, Union

def plot_sensors_events(deployid: str, sensors: Dict[str, pd.DataFrame], events: Dict[str, pd.DatetimeIndex], interactive=True) -> Union[plotlyFigure, matplotlibFigure]:
    _sensors = sensors[deployid]
    _events = _sensors.loc[events[deployid]]
    
    if interactive:
        return __plot_sensors_events_interactive(_sensors, _events)
    else:
        return __plot_sensors_events_static(_sensors, _events)

def __plot_sensors_events_interactive(sensors, event_sensors) -> plotlyFigure:
    fig = make_subplots(rows=len(sensors.columns), cols=1,
                        shared_xaxes=True,)
    for i, col in enumerate(sensors.columns):
        fig.append_trace(go.Scatter(
            x=sensors.index,
            y=sensors[col],
            mode="lines"
        ), row=i + 1, col=1)
        fig.append_trace(go.Scatter(
            x=event_sensors.index,
            y=event_sensors[col],
            mode="markers"
        ), row=i + 1, col=1)
        fig.update_yaxes(title_text=col, row=i + 1, col=1)
        
    fig.update_layout(showlegend=False)
    return fig

# FIXME (maybe? might still work)
def __plot_sensors_events_static(sensors, event_sensors) -> matplotlibFigure:
    fig, axs = plt.subplots(len(sensors.columns), 1)
    for i, col in enumerate(sensors.columns):
        # sensor data
        axs[i].plot(sensors.index, sensors[col], "-", zorder=1)
        # events
        axs[i].scatter(event_sensors.index, event_sensors[col], facecolors="none", edgecolors="r", zorder=2)
        axs[i].set_ylabel(col)
        if col == "depth":
            axs[i].invert_yaxis()
        
    return fig

def plot_predictions(deployid: str, sensors: Dict[str, pd.DataFrame], 
                     predictions: Dict[str, Tuple[pd.Series, pd.DataFrame]],
                     outcomes: Dict[str, pd.Series]=None, interactive=True) -> Union[plotlyFigure, matplotlibFigure]:
    lcl, gbl = predictions[deployid]
    data = sensors[deployid].join(lcl)
    predicted_idx = gbl.index[gbl["is_event"] == 1]

    predicted_only = data.loc[predicted_idx]
    actual_only = None
    if outcomes is not None:
        predicted_only = predicted_only.join(outcomes[deployid])
        actual_idx = outcomes[deployid].index[outcomes[deployid].isin(["TP", "FN"])]
        actual_only = data.loc[actual_idx].join(outcomes[deployid])

    if interactive:
        return __plot_predictions_interactive(data, predicted_only, actual_only)
    else:
        return __plot_predictions_static(data, predicted_only, actual_only)

def __plot_predictions_interactive(data: pd.DataFrame, predicted: pd.DataFrame, actual: pd.DataFrame) -> plotlyFigure:
    fig = make_subplots(rows=len(data.columns), cols=1,
                        shared_xaxes=True,)

    pred_color = "purple"
    if "outcome" in predicted.columns:
        pred_color = ["blue" if o == "TP" else "red" for o in predicted["outcome"]]
    if actual is not None:
        actual_color = ["blue" if o == "TP" else "red" for o in actual["outcome"]]

    for i, col in enumerate(data):
        # Line plot
        fig.append_trace(go.Scatter(
            x=data.index,
            y=data[col],
            mode="lines"
        ), row=i + 1, col=1)
        # Predicted events
        fig.append_trace(go.Scatter(
            x=predicted.index,
            y=predicted[col],
            marker_color=pred_color,
            mode="markers"
        ), row=i + 1, col=1)
        # Actual events
        if actual is not None:
            fig.append_trace(go.Scatter(
                x=actual.index,
                y=actual[col],
                mode="markers",
                marker_symbol="circle-open",
                marker_size=10,
                marker_color=actual_color,
            ), row=i + 1, col=1)
        if col == "depth":
            fig.update_yaxes(autorange="reversed", row=i + 1, col=1)
        fig.update_yaxes(title_text=col, row=i + 1, col=1)
        
    fig.update_layout(showlegend=False)
    return fig

# FIXME
def __plot_predictions_static(data, predicted, actual) -> matplotlibFigure:
    fig, axs = plt.subplots(len(data.columns), 1)
    for i, col in enumerate(data):
        # sensor data
        axs[i].plot(data.index, data[col], "-", zorder=1)
        axs[i].set_ylabel(col)
        # predicted events
        axs[i].scatter(predicted.index, 
                        predicted[col], 
                        c=["blue" if o == "TP" else "red" for o in predicted["outcome"]], zorder=2)
        # actual events
        axs[i].scatter(actual.index, 
                        actual[col], 
                        edgecolors=["blue" if o == "TP" else "red" for o in actual["outcome"]],
                        facecolors="none",
                        zorder=3)
        if col == "depth":
            axs[i].invert_yaxis()
        
    return fig

def outcome_table(outcomes: Dict[str, pd.Series]) -> pd.DataFrame:
    def add_deployid(d, o):
        result = pd.DataFrame(o)
        result.insert(0, "deployid", np.full(len(o), [d]))
        return result
    counts = pd.concat([add_deployid(d, o) for d, o in outcomes.items()])
    return counts.groupby(["deployid", "outcome"]).size().unstack(fill_value=0)

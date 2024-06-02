import sys
import os
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dateutil import parser

# Determine if the script is running in a frozen state (compiled by PyInstaller)
if getattr(sys, 'frozen', False):
    # If the script is running as a bundle, adjust the path to the CSV file
    bundle_dir = sys._MEIPASS
    file_path = os.path.join(bundle_dir, 'selected_rows.csv')
else:
    # If the script is not running as a bundle, use the original path
    file_path = 'selected_rows.csv'

# Load the CSV file
df = pd.read_csv(file_path)

# Inspect the 'Time' column to check for potential issues
print("First few rows of the 'Time' column:")
print(df['Time'].head())

# Define a function to parse the time column using dateutil.parser
def parse_time(time_str):
    try:
        return parser.parse(time_str).time()
    except Exception as e:
        print(f"Error parsing time: {time_str} - {e}")
        return None

# Apply the parsing function to the 'Time' column
df['Time'] = df['Time'].apply(parse_time)

# Drop rows where 'Time' conversion failed
df = df.dropna(subset=['Time'])

# Sort the DataFrame by 'Time'
df = df.sort_values(by='Time')

# Specify the relevant columns
relevant_columns = [
    'Time', ' Flow Rate (g/s)', ' CHSS Temperature (C)', ' CHSS Pressure (PSI)', 
    ' Discharge Temperature (C)', ' Ambient Temperature (C)'
]

# Filter the dataframe to include only the relevant columns
df = df[relevant_columns]

# Create a Dash application
app = dash.Dash(__name__)

# Layout of the application
app.layout = html.Div([
    html.H1("OneH2 Data Visualization"),
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col, 'value': col} for col in relevant_columns if col != 'Time'],
        value=[' Flow Rate (g/s)'],
        multi=True
    ),
    dcc.Graph(id='line-graph')
])

# Callback to update the graph based on the selected columns
@app.callback(
    Output('line-graph', 'figure'),
    [Input('column-dropdown', 'value')]
)
def update_graph(selected_columns):
    fig = go.Figure()
    for col in selected_columns:
        fig.add_trace(go.Scatter(x=df['Time'], y=df[col], mode='lines', name=col))
    
    fig.update_layout(title='Line Graph of Selected Columns', xaxis_title='Time', yaxis_title='Value')
    return fig

# Run the application
if __name__ == '__main__':
    # Check if the script is running in a frozen state and disable dev_tools if so
    if getattr(sys, 'frozen', False):
        app.run_server(debug=False, host='0.0.0.0')
    else:
        app.run_server(debug=True, host='0.0.0.0')


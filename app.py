# %% [markdown]
# # Sprint 4
# ### Caroline Lowenstein DS4003

# %%
# import dependencies
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
from jupyter_dash import JupyterDash
import plotly.graph_objs as go

# %%
#import data
data= pd.read_csv('/Users/carolinelowenstein/Desktop/everything/DS/sprint 2/NEW DATA MARCH 27/UPDATED_data.csv')

# %%
# build a bar chart
fig_new = px.bar(data, 
        x = 'Beverage', 
        y = 'Calories',
        color = 'Beverage')
fig_new.update_layout(
    title_text='Starbucks Drinks',
    xaxis_title="Beverages",
    yaxis_title='Calories',
)

# display the chart
fig_new.show()

# %%
#My app

#Dictionary for sizes
all_size_options = {
    'Select a Beverage Type': ['Short', 'Tall', 'Grande', 'Venti'],
    'Brewed Coffee': ['Short- with no milk option', 'Tall- with no milk option', 'Grande- with no milk option', 'Venti- with no milk option'],
    'Caffè Latte': ['Short', 'Tall', 'Grande', 'Venti'],
    'Caffè Mocha': ['Short', 'Tall', 'Grande', 'Venti'],
    'Flavored Latte': ['Short', 'Tall', 'Grande', 'Venti'],
    'Caffè Americano': ['Short', 'Tall', 'Grande', 'Venti'],
    'Cappuccino': ['Short', 'Tall', 'Grande', 'Venti'],
    'Espresso': ['Solo', 'Doppio'],
    'Skinny Latte (Any Flavour)': ['Short', 'Tall', 'Grande', 'Venti'],
    'Caramel Macchiato': ['Short', 'Tall', 'Grande', 'Venti'],
    'White Chocolate Mocha': ['Short', 'Tall', 'Grande', 'Venti'],
    'Hot Chocolate': ['Short', 'Tall', 'Grande', 'Venti'],
    'Caramel Apple Spice': ['Short', 'Tall', 'Grande', 'Venti'],
    'Tazo® Chai Tea Latte': ['Short', 'Tall', 'Grande', 'Venti'],
    'Tazo® Green Tea Latte': ['Short', 'Tall', 'Grande', 'Venti'],
    'Tazo® Full-Leaf Red Tea Latte (Vanilla Rooibos)': ['Short', 'Tall', 'Grande', 'Venti'],
    'Iced Brewed Coffee (With Classic Syrup)': ['Tall', 'Grande', 'Venti'],
    'Shaken Iced Tazo® Tea (With Classic Syrup)': ['Tall'],
    'Banana Chocolate Smoothie': ['Grande'],
    'Orange Mango Banana Smoothie': ['Grande'],
    'Strawberry Banana Smoothie': ['Grande'],
    'Coffee': ['Tall', 'Grande', 'Venti'],
    'Mocha': ['Tall', 'Grande', 'Venti'],
    'Caramel': ['Tall', 'Grande', 'Venti'],
    'Java Chip': ['Tall', 'Grande', 'Venti'],
    'Strawberries & Crème': ['Tall', 'Grande', 'Venti'],
    'Vanilla Bean': ['Tall', 'Grande']
}
#Dictionary for milk types
all_milk_options = {
    'Short': ['Nonfat', '2%', 'Soymilk'],
    'Tall': ['Nonfat', '2%', 'Soymilk'],
    'Grande': ['Nonfat', '2%', 'Soymilk'],
    'Venti': ['Nonfat', '2%', 'Soymilk'],
    'Solo': ['N/A'],
    'Doppio': ['N/A'],
    'Short- with no milk option': ['N/A'],
    'Tall- with no milk option': ['N/A'],
    'Grande- with no milk option': ['N/A'],
    'Venti- with no milk option': ['N/A'],
    'Brewed Coffee': ['N/A'],
    'Espresso':['N/A'],
    'Caramel Apple Spice':['N/A'],
    'Iced Brewed Coffee (With Classic Syrup)': ['N/A'],
    'Shaken Iced Tazo® Tea (With Classic Syrup)': ['N/A']
}

stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=stylesheets)

app.layout = html.Div([

    html.H1('Starbucks Data'),
    html.Div(''' This app displays three interactive activties.  
             1. Choose a beverage 
             2. Choose a size  
             3. Choose a type of milk (if the dring you want requires milk).
             
             Then you will be able to view their nutritional information.
            '''),


    dcc.Dropdown(
        id='drinks-dropdown',
        options=[{'label': option, 'value': option} for option in data['Beverage'].unique()],
        value='Select a Beverage Type',
        placeholder="Select a drink",
        style={'width': '33.3%', 'display': 'inline-block'}
    ),

    dcc.RadioItems(id='size-radio', value=None, style={'width': '33.3%', 'display': 'inline-block'}),

    dcc.RadioItems(id='milk-radio', value=None, style={'width': '33.3%', 'display': 'inline-block'}),

    html.Div(id='display-selected-values'),


    dcc.Graph(id='fig_new')
])

# Callback for setting size options and value
@app.callback(
    Output('size-radio', 'options'),
    Output('size-radio', 'value'),
    Input('drinks-dropdown', 'value')
)
def set_size_options_and_value(selected_drink):
    size_options = [{'label': size, 'value': size} for size in all_size_options[selected_drink]]
    return size_options, size_options[0]['value']

# Callback for setting milk options
@app.callback(
    Output('milk-radio', 'options'),
    Input('size-radio', 'value')
)
def set_milk_options(selected_size):
    milk_options = [{'label': milk, 'value': milk} for milk in all_milk_options[selected_size]]
    return milk_options

# Callback to update the graph
@app.callback(
    Output('fig_new', 'figure'),
    [Input('drinks-dropdown', 'value'),
     Input('size-radio', 'value'),
     Input('milk-radio', 'value')] 
)
def update_graph(selected_drink, selected_size, selected_milk):
    # Filter data based on selected drink, size, and milk
    filtered_data = data[(data['Beverage'] == selected_drink) & 
                         (data['Size'] == selected_size) & 
                         (data['Milk_type'] == selected_milk)]

    if filtered_data.empty:
        return {'data': [], 'layout': {}}

    # Get COLUMNS 3-7 for plotting 
    columns = filtered_data.columns[3:8]

    # Get VALUES for bars
    values = filtered_data.iloc[0, 3:8].tolist()

    #Coffee color theme
    colors = ['#544129', '#7b6853', '#A2907b', '#Bdad9a', '#E8dccd']

    # Create bar traces
    bars = []
    for col, val, color in zip(columns, values, colors):
        bars.append(go.Bar(
            x=[col],
            y=[val],
            name=col,
            marker=dict(color=color)
    ))

    layout = go.Layout(
        title='Starbucks Drink Nutrional Information',
        xaxis=dict(title='Nutrional Information Types'),
        yaxis=dict(title='Numeric Value'),
        barmode='group',
    )

    return {'data': bars, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)



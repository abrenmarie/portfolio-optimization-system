import plotly.express as px
import pandas as pd

def make_pie_chart(results: dict) -> px.pie:
    weights_df = pd.DataFrame(list(results['weights'].items()), columns=['Asset', 'Weight in the portfolio'])
    weights_df = weights_df[weights_df['Weight in the portfolio'] > 0.001]
    
    fig = px.pie(
        weights_df, 
        values='Weight in the portfolio', 
        names='Asset', 
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10))
    return fig

def make_cumulative_returns_chart(returns: pd.DataFrame) -> px.line:
    cumulative_returns = (1 + returns).cumprod() - 1
    
    fig = px.line(
        cumulative_returns,
        labels={'value': 'Cumulative Return', 'begin': 'Date', 'variable': 'Asset'},
        title="Historical Dynamics of Cumulative Returns"
    )
    fig.update_layout(template="plotly_dark", margin=dict(t=40, b=10, l=10, r=10))
    return fig
import streamlit as st
import datetime
import pandas as pd
from src.loader import load_historical_data
from src.optimizer import PortfolioOptimizer

st.set_page_config(page_title="MOEX Portfolio Optimizer", layout="wide")

st.title("Modern Portfolio Theory Optimizer (MOEX Edition)")
st.subheader("Implemented a portfolio optimization model using mean-variance framework")

st.sidebar.header("Settings")
tickers_input = st.sidebar.text_input("MOEX stock tickers", "SBER, GAZP, LKOH, YNDX, NLMK")
tickers = [t.strip().upper() for t in tickers_input.split(",")]

start_date = st.sidebar.date_input("Start date", datetime.date(2023, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date(2026, 1, 1))

risk_aversion = st.sidebar.slider("Risk aversion (λ)", min_value=0.1, max_value=2.0, value=0.5, step=0.1)

if st.sidebar.button("Run optimization"):
    with st.spinner("Loading data from MOEX and calculating..."):
        try:
            start_str = start_date.strftime('%Y-%m-%d')
            end_str = end_date.strftime('%Y-%m-%d')
            
            returns = load_historical_data(tickers, start_date=start_str, end_date=end_str)
            
            if returns.empty:
                st.error("Failed to retrieve data for the specified tickers during this period.")
            else:
                optimizer = PortfolioOptimizer(risk_aversion=risk_aversion)
                results = optimizer.optimize(returns)
                
                from src.visualizer import make_pie_chart, make_cumulative_returns_chart
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(label="Expected Annual Return", value=f"{results['expected_return']:.2%}")
                    st.metric(label="Expected Portfolio Risk (Volatility)", value=f"{results['expected_variance']**0.5:.2%}")
                    
                with col2:
                    st.write("### Optimal Asset Weights")
                    fig_pie = make_pie_chart(results)
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                st.write("---")
                st.write("### Comparative Analysis of Historical Data")
                fig_line = make_cumulative_returns_chart(returns)
                st.plotly_chart(fig_line, use_container_width=True)
                    
        except Exception as e:
            st.error(f"Error in the optimization process: {e}")
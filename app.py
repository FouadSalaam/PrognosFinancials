import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="LeaseIQ Underwriting Cockpit", layout="wide")
st.title("📊 LeaseIQ: Commercial Lease Simulation Engine")
st.caption("Standalone Enterprise Valuation & Underwriting Sandbox")
st.markdown("---")

st.sidebar.header("📥 Interactive Controls")
gla = st.sidebar.slider("Gross Leasable Area (sqm)", min_value=50, max_value=2000, value=250, step=50)
base_rate = st.sidebar.slider("Target Base Rate (QAR/sqm/year)", min_value=1000, max_value=10000, value=4000, step=500)
percentage_rate_input = st.sidebar.slider("Percentage Rent Rate (%)", min_value=1.0, max_value=15.0, value=8.0, step=0.5)
percentage_rate = percentage_rate_input / 100.0

annual_base_rent = gla * base_rate
natural_breakpoint = annual_base_rent / percentage_rate

st.sidebar.markdown("---")
breakpoint_type = st.sidebar.radio("Breakpoint Rule:", ["Natural Breakpoint", "Artificial Breakpoint"])

if breakpoint_type == "Natural Breakpoint":
    breakpoint_value = natural_breakpoint
else:
    breakpoint_value = st.sidebar.slider("Custom Artificial Breakpoint (QAR)", min_value=1000000, max_value=20000000, value=10000000, step=500000)

sales_range = np.linspace(0, 20000000, 500)
natural_rent = [annual_base_rent + max(0, (s - natural_breakpoint) * percentage_rate) for s in sales_range]
artificial_rent = [annual_base_rent + max(0, (s - breakpoint_value) * percentage_rate) for s in sales_range]

fig = go.Figure()
fig.add_trace(go.Scatter(x=sales_range, y=natural_rent, mode='lines', name='Standard ERP Baseline', line=dict(color='#ef4444', width=3, dash='dash')))
fig.add_trace(go.Scatter(x=sales_range, y=artificial_rent, mode='lines', name='LeaseIQ Optimized Output', line=dict(color='#10b981', width=4)))
fig.update_layout(title="<b>Dynamic Annual Rent Yield Curve</b>", xaxis=dict(title="Tenant Gross Annual Sales Volume (QAR)", tickformat=",.0f"), yaxis=dict(title="Estimated Total Annual Rent (QAR)", tickformat=",.0f"), plot_bgcolor="white", hovermode="x unified", legend=dict(orientation="h", y=1.1))

col1, col2 = st.columns([1, 2])
with col1:
    st.metric(label="🔒 Base Guaranteed Rent", value=f"QAR {annual_base_rent:,.0f}")
    st.metric(label="🎯 Active Breakpoint Target", value=f"QAR {breakpoint_value:,.0f}")
    st.info("💡 Adjust the sliders on the left sidebar to watch the green line bend and change instantly!")
with col2:
    st.plotly_chart(fig, use_container_width=True)


import streamlit as st
from datetime import date
from dataclasses import dataclass

st.set_page_config(
    page_title="SynqBot",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

FUTURISTIC_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #0F172A;
    --accent: #3B82F6;
    --secondary: #14B8A6;
    --background: #F8FAFC;
    --card: #FFFFFF;
    --text-main: #111827;
    --text-muted: #6B7280;
    --border: #E5E7EB;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: var(--background);
    color: var(--text-main);
}

[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid var(--border);
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

.hero-card {
    padding: 34px;
    border-radius: 24px;
    background: linear-gradient(135deg, #FFFFFF 0%, #EEF6FF 100%);
    border: 1px solid var(--border);
    box-shadow: 0 8px 28px rgba(15, 23, 42, 0.08);
}

.hero-card h1 {
    font-size: 52px;
    font-weight: 800;
    color: var(--primary);
    margin-bottom: 10px;
}

.hero-card p {
    font-size: 18px;
    color: var(--text-muted);
}

.metric-card {
    padding: 24px;
    border-radius: 20px;
    background: var(--card);
    border: 1px solid var(--border);
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
}

.big-number {
    font-size: 38px;
    font-weight: 800;
    color: var(--primary);
    margin: 0;
}

.small-label {
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.result-table {
    width: 100%;
    border-collapse: collapse;
    background: #FFFFFF;
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid var(--border);
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
}

.result-table th, .result-table td {
    padding: 14px 16px;
    border-bottom: 1px solid var(--border);
    color: var(--text-main);
    font-size: 15px;
}

.result-table th {
    text-align: left;
    color: var(--primary);
    background: #F1F5F9;
    font-weight: 700;
}

.glow {
    color: var(--accent);
}

h2, h3 {
    color: var(--primary);
    font-weight: 800;
}

.stButton > button {
    background: var(--accent);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px 20px;
    font-weight: 700;
}

.stTextInput input, .stNumberInput input {
    border-radius: 12px;
}
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 18px 10px 26px 10px;
    margin-bottom: 8px;
    border-bottom: 1px solid #E5E7EB;
}

.logo-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, #0F172A, #3B82F6);
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 800;
}

.logo-title {
    font-size: 22px;
    font-weight: 800;
    color: #0F172A;
}

.logo-subtitle {
    font-size: 12px;
    font-weight: 600;
    color: #6B7280;
}
</style>
"""
st.markdown(FUTURISTIC_CSS, unsafe_allow_html=True)

@dataclass
class PayoutResult:
    tax_amount: float
    final_payout_after_tax: float
    group_30: float
    raza_15: float
    amaz_hammad_15: float
    amaz_cut_usd: float
    hammad_cut_usd: float
    hamza_team_70: float
    amount_to_pakistan_before_tax: float
    pakistan_tax: float
    amount_sent_to_pakistan: float
    calculated_pkr_received: float
    amaz_hammad_total_pkr: float
    amaz_pkr: float
    hammad_pkr: float
    hamza_pkr: float

def money(x, symbol="$"):
    return f"{symbol}{x:,.2f}"

def pkr(x):
    return f"Rs. {x:,.0f}"

def calculate(
    salary: float,
    overall_tax_rate: float,
    pakistan_tax_rate: float,
    exchange_rate: float,
    additional_deduction: float
) -> PayoutResult:

    tax_amount = round(salary * overall_tax_rate, 2)

    final_payout_before_pakistan_tax = round(
        salary - tax_amount - additional_deduction, 2
    )

    raza_share_rate = 0.15
    group_share_rate = 0.30

    final_payout_after_tax = round(
        final_payout_before_pakistan_tax / (1 + pakistan_tax_rate * (1 - raza_share_rate)),
        2
    )

    group_30 = round(final_payout_after_tax * group_share_rate, 2)

    raza_15 = round(group_30 / 2, 2)

    amaz_hammad_15 = round(group_30 / 2, 2)

    amaz_cut_usd = round(amaz_hammad_15 / 2, 2)

    hammad_cut_usd = round(amaz_hammad_15 / 2, 2)

    hamza_team_70 = round(final_payout_after_tax - group_30, 2)

    amount_to_pakistan_before_tax = round(amaz_hammad_15 + hamza_team_70, 2)

    pakistan_tax = round(
        (final_payout_before_pakistan_tax - raza_15) * pakistan_tax_rate, 2
    )

    amount_sent_to_pakistan = amount_to_pakistan_before_tax

    calculated_pkr_received = round(amount_sent_to_pakistan * exchange_rate, 0)

    amaz_hammad_total_pkr = round(amaz_hammad_15 * exchange_rate, 0)

    amaz_pkr = round(amaz_hammad_total_pkr / 2, 0)

    hammad_pkr = round(amaz_hammad_total_pkr / 2, 0)

    hamza_pkr = round(calculated_pkr_received - amaz_hammad_total_pkr, 0)

    return PayoutResult(
        tax_amount,
        final_payout_after_tax,
        group_30,
        raza_15,
        amaz_hammad_15,
        amaz_cut_usd,
        hammad_cut_usd,
        hamza_team_70,
        amount_to_pakistan_before_tax,
        pakistan_tax,
        amount_sent_to_pakistan,
        calculated_pkr_received,
        amaz_hammad_total_pkr,
        amaz_pkr,
        hammad_pkr,
        hamza_pkr
    )


st.sidebar.markdown("""
<div class="sidebar-logo">
    <div class="logo-icon">F</div>
    <div>
        <div class="logo-title">FlowLedger</div>
        <div class="logo-subtitle">Payout Intelligence</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("Input Panel")

client_name = st.sidebar.text_input("Client Name", value="Truist")
date_range = st.sidebar.text_input("Date Range", value="05/18/26 till 05/29/26")
salary = st.sidebar.number_input("Total Salary Before Tax (USD)", min_value=0.0, value=2112.16, step=10.0, format="%.2f")
exchange_rate = st.sidebar.number_input("Bank Exchange Rate (PKR)", min_value=0.0, value=271.50, step=0.50, format="%.2f")

with st.sidebar.expander("Advanced Settings"):
    overall_tax_rate_percent = st.number_input(
        "Overall Tax Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=32.0,
        step=1.0,
        format="%.0f"
    )

    pakistan_tax_rate_percent = st.number_input(
        "Pakistan Business Tax Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.5,
        step=0.1,
        format="%.1f"
    )

    additional_deduction = st.number_input(
        "Additional Deduction Amount",
        min_value=0.0,
        value=382.48,
        step=10.0,
        format="%.2f"
    )

overall_tax_rate = overall_tax_rate_percent / 100
pakistan_tax_rate = pakistan_tax_rate_percent / 100

result = calculate(
    salary,
    overall_tax_rate,
    pakistan_tax_rate,
    exchange_rate,
    additional_deduction
)
st.subheader(f"Client: {client_name}")
st.caption(f"Payout Period: {date_range}")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="small-label">Salary Before Tax</div><p class="big-number">{money(salary)}</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="small-label">Overall Tax</div><p class="big-number">{money(result.tax_amount)}</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="small-label">Final Payout After Tax</div><p class="big-number glow">{money(result.final_payout_after_tax)}</p></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="small-label">PKR Received</div><p class="big-number">{result.calculated_pkr_received}</p></div>', unsafe_allow_html=True)

st.divider()

left, right = st.columns([1.1, 1])

with left:
    st.markdown("### USD Breakdown")
    st.markdown(f"""
    <table class="result-table">
        <tr><th>Item</th><th>Amount</th></tr>
        <tr><td>Total Salary Before Tax</td><td>{money(salary)}</td></tr>
        <tr><td>Overall Tax ({overall_tax_rate*100:.2f}%)</td><td>{money(result.tax_amount)}</td></tr>
        <tr><td>Final Payout After Tax</td><td><b>{money(result.final_payout_after_tax)}</b></td></tr>
        <tr><td>Raza/Amaz/Hammad 30%</td><td>{money(result.group_30)}</td></tr>
        <tr><td>Raza 15% Excluded From Pakistan Payout</td><td>{money(result.raza_15)}</td></tr>
        <tr><td>Amaz/Hammad 15%</td><td>{money(result.amaz_hammad_15)}</td></tr>
        <tr><td>Amaz USD Cut</td><td>{money(result.amaz_cut_usd)}</td></tr>
        <tr><td>Hammad USD Cut</td><td>{money(result.hammad_cut_usd)}</td></tr>
        <tr><td>Hamza Team 70%</td><td>{money(result.hamza_team_70)}</td></tr>
        <tr><td>Pakistan Business Tax ({pakistan_tax_rate*100:.2f}%)</td><td>{money(result.pakistan_tax)}</td></tr>
        <tr><td>Amount Sent to Pakistan After Pakistan Tax</td><td><b>{money(result.amount_sent_to_pakistan)}</b></td></tr>
    </table>
    """, unsafe_allow_html=True)

with right:
    st.markdown("### PKR Distribution")
    st.markdown(f"""
    <table class="result-table">
        <tr><th>Person / Team</th><th>PKR Amount</th></tr>
        <tr><td>Amaz + Hammad Total</td><td>{pkr(result.amaz_hammad_total_pkr)}</td></tr>
        <tr><td>Amaz</td><td><b>{pkr(result.amaz_pkr)}</b></td></tr>
        <tr><td>Hammad</td><td><b>{pkr(result.hammad_pkr)}</b></td></tr>
        <tr><td>Hamza Team</td><td><b>{pkr(result.hamza_pkr)}</b></td></tr>
    </table>
    """, unsafe_allow_html=True)

st.divider()



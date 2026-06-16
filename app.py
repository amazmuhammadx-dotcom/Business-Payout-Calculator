
import streamlit as st
from datetime import date
from dataclasses import dataclass

st.set_page_config(
    page_title="SynqBot",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

FFUTURISTIC_CSS = """
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
    manual_pkr_received: float | None = None
) -> PayoutResult:
    tax_amount = round(salary * overall_tax_rate, 2)
    final_payout_after_tax = round(salary - tax_amount, 2)

    group_30 = round(final_payout_after_tax * 0.30, 2)
    raza_15 = round(final_payout_after_tax * 0.15, 2)
    amaz_hammad_15 = round(final_payout_after_tax * 0.15, 2)
    amaz_cut_usd = round(amaz_hammad_15 / 2, 2)
    hammad_cut_usd = round(amaz_hammad_15 / 2, 2)
    hamza_team_70 = round(final_payout_after_tax * 0.70, 2)

    # Amount sent to Pakistan excludes Raza's 15%.
    amount_to_pakistan_before_tax = round(final_payout_after_tax - raza_15, 2)

    # Pakistan tax is applied on the amount sent to Pakistan.
    pakistan_tax = round(amount_to_pakistan_before_tax * pakistan_tax_rate, 2)
    amount_sent_to_pakistan = round(amount_to_pakistan_before_tax - pakistan_tax, 2)

    calculated_pkr_received = round(amount_sent_to_pakistan * exchange_rate, 0)
    pkr_received = manual_pkr_received if manual_pkr_received and manual_pkr_received > 0 else calculated_pkr_received

    # PKR allocation follows the real received PKR after bank/exchange settlement.
    amaz_hammad_total_pkr = round(pkr_received * (amaz_hammad_15 / amount_to_pakistan_before_tax), 0) if amount_to_pakistan_before_tax else 0
    amaz_pkr = round(amaz_hammad_total_pkr / 2, 0)
    hammad_pkr = round(amaz_hammad_total_pkr / 2, 0)
    hamza_pkr = round(pkr_received - amaz_hammad_total_pkr, 0)

    return PayoutResult(
        tax_amount, final_payout_after_tax, group_30, raza_15, amaz_hammad_15,
        amaz_cut_usd, hammad_cut_usd, hamza_team_70,
        amount_to_pakistan_before_tax, pakistan_tax, amount_sent_to_pakistan,
        calculated_pkr_received, amaz_hammad_total_pkr, amaz_pkr, hammad_pkr, hamza_pkr
    )

st.markdown("""
<div class="hero-card">
    <h1>FlowLedger</h1>
    <p style="font-size:18px;color:#cbd5e1;">
    Automated salary split, tax deduction, Pakistan payout, exchange-rate conversion, and partner/team distribution.
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("Input Panel")

client_name = st.sidebar.text_input("Client Name", value="Truist")
date_range = st.sidebar.text_input("Date Range", value="05/18/26 till 05/29/26")
salary = st.sidebar.number_input("Total Salary Before Tax (USD)", min_value=0.0, value=2112.16, step=10.0, format="%.2f")
exchange_rate = st.sidebar.number_input("Bank Exchange Rate (PKR)", min_value=0.0, value=271.50, step=0.50, format="%.2f")
manual_pkr = st.sidebar.number_input("Actual PKR Received (optional)", min_value=0.0, value=242172.0, step=100.0, format="%.0f")

with st.sidebar.expander("Advanced Settings"):
    overall_tax_rate = st.number_input("Overall Tax Rate", min_value=0.0, max_value=1.0, value=0.32, step=0.01, format="%.4f")
    pakistan_tax_rate = st.number_input("Pakistan Business Tax Rate", min_value=0.0, max_value=1.0, value=0.005, step=0.001, format="%.4f")

result = calculate(salary, overall_tax_rate, pakistan_tax_rate, exchange_rate, manual_pkr)

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
    st.markdown(f'<div class="metric-card"><div class="small-label">PKR Received</div><p class="big-number">{pkr(manual_pkr if manual_pkr else result.calculated_pkr_received)}</p></div>', unsafe_allow_html=True)

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

with st.expander("Add-on Feature Ideas"):
    st.write("""
    - Save payout history
    - Export PDF report
    - Export Excel report
    - Add multiple clients
    - Add custom partner percentages
    - Add business expense deductions
    - Add bank-fee deduction
    - Add audit log for every payout
    - Add AI explanation of payout calculation
    """)

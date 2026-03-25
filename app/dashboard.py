import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# configuração da pagina

st.set_page_config(
    page_title="HR Attrition Dashboard",
    page_icon="👥",
    layout="wide"
)

# paleta de cores

COLORS = {"No": "#4C72B0", "Yes": "#DD8452"}

# dados

@st.cache_data
def load_data():
    df = pd.read_csv("./data/WA_Fn-UseC_-HR-Employee-Attrition.csv")
    df.drop(columns=["EmployeeCount", "Over18", "StandardHours"], inplace=True)
    df["Attrition_bin"] = (df["Attrition"] == "Yes").astype(int)
    df["SalaryBand"] = pd.cut(
        df["MonthlyIncome"],
        bins=[0, 3000, 6000, 10000, 20000],
        labels=["< 3k", "3k-6k", "6k-10k", "> 10k"]
    )
    return df

df = load_data()

# sidebar

with st.sidebar:
    st.title("🔍 Filtros")
    st.markdown("---")

    departamentos = st.multiselect(
        "Departamento",
        options=sorted(df["Department"].unique()),
        default=sorted(df["Department"].unique())
    )

    generos = st.multiselect(
        "Gênero",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )

    faixa_idade = st.slider(
        "Faixa etária",
        min_value=int(df["Age"].min()),
        max_value=int(df["Age"].max()),
        value=(int(df["Age"].min()), int(df["Age"].max()))
    )

    overtime = st.radio(
        "Hora Extra (OverTime)",
        options=["Todos", "Yes", "No"],
        index=0
    )

    st.markdown("---")
    st.caption("IBM HR Analystics · 1.470 funcionários")

# aplicação de filtros

mask = (
    df["Department"].isin(departamentos) &
    df["Gender"].isin(generos) &
    df["Age"].between(*faixa_idade)
)

if overtime != "Todos":
    mask &= df["OverTime"] == overtime

filtered = df[mask]

# header

st.title("👥 HR Attrition Dashboard")
st.caption("Análise exploratória de turnover · IBM HR Analystics Dataset")
st.markdown("---")

# KPI's

k1, k2, k3, k4, k5 = st.columns(5)

total = len(filtered)
total_saiu = filtered["Attrition_bin"].sum()
taxa = filtered["Attrition_bin"].mean()
salario_med = filtered["MonthlyIncome"].mean()
idade_med = filtered["Age"].mean()

k1.metric("👤 Total funcionários", f"{total:,}")
k2.metric("🚪 Saíram", f"{total_saiu:,}")
k3.metric("📊 Taxa de Attrition", f"{taxa:.1%}")
k4.metric("💰 Salário médio", f"$ {salario_med:,.0f}")
k5.metric("🎂 Idade média", f"{idade_med:.1f} anos")

# tabs

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visão Geral",
    "💼 Cargo & Departamento",
    "💰 Salário & Perfil",
    "😊 Satisfação & Engajamento",
])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            filtered,
            names="Attrition",
            color="Attrition",
            color_discrete_map=COLORS,
            title="Distribuição de Attrition",
            hole=0.45
        )
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        ot = (filtered.groupby("OverTime")["Attrition_bin"]
              .mean()
              .reset_index())
        ot.columns = ["OverTime", "Taxa"]
        fig = px.bar(
            ot, x="OverTime", y="Taxa",
            color="OverTime",
            text_auto=".1%",
            title="Attrition por Hora Extra",
            color_discrete_sequence=["#4C72B0", "#DD8452"],
        )
        fig.update_layout(showlegend=False, yaxis_tickformat=".0%")
        st.plotly_chart(fig, width='stretch')

    years = (filtered.groupby("YearsAtCompany")["Attrition_bin"]
             .mean()
             .reset_index())
    years.columns = ["Anos", "Taxa"]
    fig = px.line(
        years, x="Anos", y="Taxa",
        markers=True,
        title="Taxa de Attrition por Anos na Empresa",
        labels={"Taxa": "Taxa de Attrition"},
        color_discrete_sequence=["#DD8452"]
    )
    fig.update_layout(yaxis_tickformat=".0%")
    st.plotly_chart(fig, width='stretch')

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        role_attr = (filtered.groupby("JobRole")["Attrition_bin"]
                     .mean()
                     .sort_values()
                     .reset_index())
        role_attr.columns = ["Cargo", "Taxa"]
        fig = px.bar(
            role_attr, x="Taxa", y="Cargo",
            orientation="h",
            text_auto=".1%",
            color="Taxa",
            color_continuous_scale="Oranges",
            title="Taxa de Attrition por Cargo"
        )
        fig.update_layout(coloraxis_showscale=False, yaxis_title="")
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        fig = px.sunburst(
            filtered,
            path=["Department", "JobRole", "Attrition"],
            color="Attrition",
            color_discrete_map=COLORS,
            title="Hierarquia: Depto → Cargo → Attrition"
        )
        st.plotly_chart(fig, width='stretch')

with tab3:
    col1, col2 = st.columns(2)

    with col1:
        fig = px.box(
            filtered, x="Attrition", y="MonthlyIncome",
            color="Attrition",
            color_discrete_map=COLORS,
            points="outliers",
            title="Salário Mensal por Attrition"
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        band = (filtered.groupby("SalaryBand", observed=True)["Attrition_bin"]
                .mean()
                .reset_index())
        band.columns = ["Faixa", "Taxa"]
        fig = px.bar(
            band, x="Faixa", y="Taxa",
            text_auto=".1%",
            color="Taxa",
            color_continuous_scale="Oranges",
            title="Attrition por Faixa Salarial"
        )
        fig.update_layout(coloraxis_showscale=False, yaxis_tickformat=".0%")
        st.plotly_chart(fig, width='stretch')
    fig = px.scatter(
        filtered,
        x="Age", y="MonthlyIncome",
        color="Attrition",
        symbol="Gender",
        hover_data=["JobRole", "Department", "YearsAtCompany"],
        color_discrete_map=COLORS,
        opacity=0.65,
        title="Salário x Idade x Attrition",
        labels={"MonthlyIncome": "Salário Mensal (USD)", "Age": "Idade"}
    )
    st.plotly_chart(fig, width='stretch')

with tab4:
    col1, col2 = st.columns(2)

    with col1:
        sat = (filtered.groupby("JobSatisfaction")["Attrition_bin"]
               .mean()
               .reset_index())
        sat.columns = ["Satisfação", "Taxa"]
        fig = px.bar(
            sat, x="Satisfação", y="Taxa",
            text_auto=".1%",
            color="Taxa",
            color_continuous_scale="RdYlGn_r",
            title="Attrition por Satisfação no Trabalho"
        )
        fig.update_layout(coloraxis_showscale=False, yaxis_tickformat=".0%")
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        wlb = (filtered.groupby("WorkLifeBalance")["Attrition_bin"]
               .mean()
               .reset_index())
        wlb.columns = ["WLB", "Taxa"]
        fig = px.bar(
            wlb, x="WLB", y="Taxa",
            text_auto=".1%",
            color="Taxa",
            color_continuous_scale="RdYlGn_r",
            title="Attrition por Work-Life Balance"
        )
        fig.update_layout(coloraxis_showscale=False, yaxis_tickformat=".0%")
        st.plotly_chart(fig, width='stretch')

    # heatmap satisfação x WLB    
    pivot = (filtered.groupby(["JobSatisfaction", "WorkLifeBalance"])["Attrition_bin"]
             .mean()
             .reset_index())
    pivot.columns = ["Satisfação", "WLB", "Taxa"]
    fig = px.density_heatmap(
        pivot, x="WLB", y="Satisfação", z="Taxa",
        color_continuous_scale="RdYlGn_r",
        text_auto=".1%",
        title="Heatmap: Satisfação × Work-Life Balance"
    )
    st.plotly_chart(fig, width='stretch')
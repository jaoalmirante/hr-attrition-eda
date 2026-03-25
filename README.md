# 👥 HR Attrition Dashboard

Dashboard interativo de análise exploratória de dados (EDA) sobre turnover 
de funcionários, construído com Python, Plotly e Streamlit.

🔗 **[Acesse o dashboard ao vivo](https://hr-attrition-eda-jaoalmirante.streamlit.app/)**

---

## 📌 Sobre o projeto

Análise completa do dataset IBM HR Analytics (1.470 funcionários, 35 variáveis)
com foco em identificar os principais fatores de attrition (turnover).

Projeto desenvolvido para demonstrar habilidades de análise de dados aplicadas
a casos reais de People Analytics em consultoria.

---

## 🔍 Principais insights

- Funcionários com **hora extra (OverTime)** têm ~3× mais chance de sair
- **Sales Representatives** lideram o attrition com ~40% de taxa
- Faixa salarial abaixo de **USD 3.000/mês** concentra maior risco
- Pico de saída nos **primeiros 3 anos** de empresa
- Combinação de **baixa satisfação + baixo WLB** = maior risco acumulado

---

## 🛠️ Stack

| Ferramenta   | Uso                              |
|--------------|----------------------------------|
| Pandas       | Limpeza e manipulação de dados   |
| Seaborn      | EDA estática e distribuições     |
| Plotly       | Visualizações interativas        |
| Streamlit    | Dashboard e deploy               |

---

## 📁 Estrutura do projeto
```
hr-attrition-eda/
├── data/                         # Dataset IBM HR Analytics
├── notebooks/
│   └── 01_eda.ipynb              # EDA completa (Pandas + Seaborn + Plotly)
├── app/
│   └── dashboard.py              # App Streamlit
├── assets/                       # Gráficos exportados
├── requirements.txt
└── README.md
```

## ⚙️ Como rodar localmente
```bash
# Clone o repositório
git clone https://github.com/jaoalmirante/hr-attrition-eda.git
cd hr-attrition-eda

# Crie e ative o ambiente virtual
python -m venv .venv
Windows: .venv\Scripts\activate # macOS e Linux: source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Rode o dashboard
streamlit run app/dashboard.py
```

---

## 📊 Dataset

[IBM HR Analytics Employee Attrition & Performance](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)
— Kaggle · Licença: Open Database License (ODbL)
import streamlit as st
import sqlite3
import pandas as pd

st.title("💰 Controle de Gastos")
from datetime import date

data_compra = st.date_input(
    "Data da compra",
    value=date.today()
)

local = st.text_input("Local da compra")

categoria = st.selectbox(
    "Categoria",
    [
        "Alimentação",
        "Combustível",
        "Lazer",
        "Saúde",
        "Outros"
    ]
)

valor = st.number_input(
    "Valor da compra",
    min_value=0.0,
    step=0.01
)

if st.button("Salvar"):

    conexao = sqlite3.connect("data/gastos.db")

    cursor = conexao.cursor()

    cursor.execute(
    """
    INSERT INTO gastos
    (data, local, categoria, valor)
    VALUES (?, ?, ?, ?)
    """,
    (
        str(data_compra),
        local,
        categoria,
        valor
    )
)


    conexao.commit()
    conexao.close()

    st.success("Gasto salvo com sucesso!")

st.divider()

st.subheader("Histórico de Gastos")

conexao = sqlite3.connect("data/gastos.db")

df = pd.read_sql(
    "SELECT * FROM gastos",
    conexao
)

conexao.close()

st.dataframe(df)
import plotly.express as px

if not df.empty:

    grafico = px.pie(
        df,
        names="categoria",
        values="valor",
        title="Gastos por Categoria"
    )

    st.plotly_chart(grafico)
    st.subheader("🏪 Gastos por Estabelecimento")

gastos_local = (
    df.groupby("local")["valor"]
    .sum()
    .reset_index()
)

grafico_local = px.bar(
    gastos_local,
    x="local",
    y="valor",
    color="local",
    text_auto=True,
    title="Quanto gasto em cada local"
)

st.plotly_chart(grafico_local)
st.subheader("📊 Resumo")

total = df["valor"].sum()

maior_gasto = (
    df.groupby("categoria")["valor"]
    .sum()
    .idxmax()
)

st.metric(
    "Total Gasto",
    f"R$ {total:.2f}"
)

st.info(
    f"Sua categoria com maior gasto é: {maior_gasto}"
)
nota = st.file_uploader(
    "📸 Envie uma nota fiscal",
    type=["jpg", "jpeg", "png"]
)
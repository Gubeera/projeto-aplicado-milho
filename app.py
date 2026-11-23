"""Painel simples (R7) - Otimização de dashboards dinâmicos. Lê as tabelas Gold em data/."""
import altair as alt
import streamlit as st
from dados import carregar, indicadores, top_produtos, manejo_matriz

st.set_page_config(page_title="Produtividade de milho (PoC)", layout="wide")
st.title("Produtividade de milho: painel da camada Gold")
st.caption("Prova de conceito com dados sintéticos. Fonte: tabelas Gold geradas pelo pipeline (Bronze → Silver → Gold).")

try:
    tab = carregar()
except FileNotFoundError:
    st.error("Arquivos Parquet não encontrados na pasta data/. Baixe as três tabelas da pasta gold/ do S3 e coloque-as em data/.")
    st.stop()

safra = st.sidebar.radio("Safra", sorted(tab["produto"]["safra"].unique()))
n = st.sidebar.slider("Produtos no ranking", 5, 20, 10)

k = indicadores(tab["produto"], safra)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Registros", k["registros"])
c2.metric("Produtos", k["produtos"])
c3.metric("Produtividade média (sc/ha)", f'{k["media"]:.1f}')
c4.metric("Melhor produto (média)", k["melhor"])

st.subheader("1. Produtos com maior produtividade média")
g1 = (alt.Chart(top_produtos(tab["produto"], safra, n))
      .mark_bar(color="#006C69")
      .encode(x=alt.X("produtividade_media:Q", title="Produtividade média (sc/ha)"),
              y=alt.Y("produto:N", sort="-x", title=None),
              tooltip=["produto", "produtividade_media", "produtividade_min", "produtividade_max", "n_com_produtividade"]))
st.altair_chart(g1, use_container_width=True)

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("2. Produtividade média por região")
    g2 = (alt.Chart(tab["regiao"]).mark_bar()
          .encode(x=alt.X("regiao:N", title=None, axis=alt.Axis(labelAngle=0)), y=alt.Y("produtividade_media:Q", title="sc/ha"),
                  color=alt.Color("safra:N", title="Safra"), xOffset="safra:N",
                  tooltip=["safra", "regiao", "produtividade_media", "n_com_produtividade"]))
    st.altair_chart(g2, use_container_width=True)
with col_b:
    st.subheader("3. Manejo: densidade × resistência a doenças")
    m = manejo_matriz(tab["manejo"], safra)
    g3 = (alt.Chart(m).mark_rect()
          .encode(x=alt.X("densidade_sementes:N", title="Densidade de sementes", sort=["Baixa", "Média", "Alta"], axis=alt.Axis(labelAngle=0)),
                  y=alt.Y("resistencia_doencas:N", title="Resistência a doenças", sort=["Baixa", "Média", "Alta"], axis=alt.Axis(labelAngle=0, labelLimit=200)),
                  color=alt.Color("produtividade_media:Q", title="sc/ha", scale=alt.Scale(scheme="teals")),
                  tooltip=["densidade_sementes", "resistencia_doencas", "produtividade_media", "n_com_produtividade"]))
    st.altair_chart(g3, use_container_width=True)

with st.expander("Ver tabela por produto"):
    st.dataframe(tab["produto"][tab["produto"]["safra"] == safra], use_container_width=True, hide_index=True)

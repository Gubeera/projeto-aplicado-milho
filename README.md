# Painel de produtividade de milho (PoC)

Prova de conceito do Projeto Aplicado (Engenharia e Arquitetura de Dados). Lê as tabelas da camada Gold
do pipeline AWS (Bronze, Silver e Gold) e exibe três visuais. Todos os dados são sintéticos.

## Como executar
1. Baixe as três tabelas da pasta `gold/` do S3 e coloque-as em `data/`.
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

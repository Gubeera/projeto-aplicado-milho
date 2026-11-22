"""Leitura e preparo das tabelas Gold (Parquet) para o painel."""
from pathlib import Path
import pandas as pd

PASTA = Path(__file__).parent / "data"
ARQUIVOS = {
    "produto": "gold_produtividade_por_produto.parquet",
    "regiao": "gold_produtividade_por_regiao.parquet",
    "manejo": "gold_produtividade_por_manejo.parquet",
}
ROTULO_SAFRA = {"safra_verao": "Safra de verão", "safrinha_inverno": "Safrinha de inverno"}

def carregar():
    tabelas = {k: pd.read_parquet(PASTA / v) for k, v in ARQUIVOS.items()}
    for t in tabelas.values():
        t["safra"] = t["safra"].map(ROTULO_SAFRA).fillna(t["safra"])
    return tabelas

def indicadores(tab_produto, safra):
    """Indicadores gerais da safra escolhida, a partir da tabela por produto."""
    t = tab_produto[tab_produto["safra"] == safra]
    com_prod = t["n_com_produtividade"].sum()
    media = (t["produtividade_media"] * t["n_com_produtividade"]).sum() / com_prod if com_prod else float("nan")
    return {"registros": int(t["n_registros"].sum()), "produtos": int(t["produto"].nunique()),
            "media": float(media), "melhor": t.sort_values("produtividade_media", ascending=False).iloc[0]["produto"]}

def top_produtos(tab_produto, safra, n=10):
    t = tab_produto[tab_produto["safra"] == safra].dropna(subset=["produtividade_media"])
    return t.sort_values("produtividade_media", ascending=False).head(n)

def manejo_matriz(tab_manejo, safra):
    t = tab_manejo[(tab_manejo["safra"] == safra) &
                   (tab_manejo["densidade_sementes"] != "Não informada") &
                   (tab_manejo["resistencia_doencas"] != "Não informada")]
    return t

import os
import logging
from datetime import datetime
import pandas as pd
import yfinance as yf

# Configuração de Logs estruturados
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

TICKERS = {
    "EWZ": "EWZ",
    "Ibovespa": "^BVSP",
    "Nasdaq": "^IXIC",
    "Russell 2000": "^RUT",
    "S&P 500": "^GSPC",
    "VIX": "^VIX",
}

def fetch_market_data():
    logging.info("Iniciando a busca de dados no yfinance...")
    results = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for name, ticker in TICKERS.items():
        try:
            # Baixa o dado mais recente do ativo
            data = yf.Ticker(ticker)
            todays_data = data.history(period="1d")

            if todays_data.empty:
                logging.warning(f"Nenhum dado retornado para {name} ({ticker}).")
                continue

            close_price = todays_data["Close"].iloc[-1]
            volume = (
                todays_data["Volume"].iloc[-1]
                if "Volume" in todays_data.columns
                else 0
            )

            results.append({
                "Timestamp": now,
                "Ativo": name,
                "Ticker": ticker,
                "Fechamento/Atual": round(float(close_price), 2),
                "Volume": int(volume),
            })
            logging.info(f"Sucesso ao buscar {name}: {close_price}")

        except Exception as e:
            logging.error(f"Erro ao buscar dados para {name} ({ticker}): {e}")

    if results:
        df = pd.DataFrame(results)
        
        # Garante o caminho absoluto na raiz do projeto para o GitHub Actions encontrar
        output_path = os.path.join(os.getcwd(), "market_data_latest.csv")
        
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        logging.info(f"Dados salvos com sucesso em {output_path}")
        print(df)
    else:
        logging.error("Nenhum dado foi coletado nesta execução.")

if __name__ == "__main__":
    fetch_market_data()

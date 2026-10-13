import logging
from datetime import datetime
import pandas as pd
import yfinance as yf

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
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
          "Fechamento/Atual": round(close_price, 2),
          "Volume": volume,
      })
      logging.info(f"Sucesso ao buscar {name}: {close_price}")

    except Exception as e:
      logging.error(f"Erro ao buscar dados para {name} ({ticker}): {e}")

  if results:
    df = pd.DataFrame(results)
    # Aqui você pode salvar em CSV, enviar para um banco de dados, Telegram ou API
    filename = f"market_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    df.to_csv(filename, index=False)
    logging.info(f"Dados salvos com sucesso em {filename}")
    print(df)
  else:
    logging.error("Nenhum dado foi coletado nesta execução.")


if __name__ == "__main__":
  fetch_market_data()
name: Coleta yfinance Automatizada

on:
  schedule:
    - cron: '15 12 * * 1-5' # 09:15 BRT
    - cron: '0 22 * * 1-5'  # 19:00 BRT
  workflow_dispatch: 

jobs:
  run-script:
    runs-on: ubuntu-latest
    
    # Garante permissão de escrita no repositório
    permissions:
      contents: write

    steps:
      - name: Checkout do código
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          cache: 'pip'

      - name: Instalar dependências
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Executar script de coleta
        run: python main.py

      - name: Commit e Push automático do CSV
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: atualiza dados de mercado automatico [skip ci]"
          file_pattern: market_data_latest.csv
          branch: ${{ github.ref_name }}

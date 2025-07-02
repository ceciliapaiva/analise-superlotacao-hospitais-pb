# Análise de Superlotação em Hospitais da Paraíba – (Jan–Nov 2024)

Este projeto tem como objetivo analisar a superlotação em hospitais do Estado da Paraíba no período de janeiro a novembro de 2024, utilizando dados públicos e ferramentas de análise de dados. A análise abrange aspectos como a taxa de ocupação de leitos SUS, a taxa de óbitos e a distribuição de hospitais especializados e gerais. O objetivo é gerar insights sobre as características que levam à superlotação em um hospital, bem como identificar regiões que demandam soluções mais eficientes. Desenvolvido para pôr em prática os conhecimentos adquiridos na disciplina de análise de dados.

## Dados Utilizados

Os dados utilizados neste projeto foram obtidos de fontes públicas, como:
- **[OpenDataSUS](https://opendatasus.saude.gov.br/dataset/hospitais-e-leitos)**: Dados sobre hospitais e leitos.
- **[PySUS](https://pysus.readthedocs.io/en/latest/databases/data-sources.html#about-sih)**: Dados do Sistema de Informações Hospitalares do SUS (SIH/SUS).

## Estrutura do Projeto

- **`relatorio.ipynb`**: Notebook principal contendo todo o processo de análise, desde a limpeza dos dados até a visualização e interpretação dos resultados.
- **`extrai-dados-pysus.py`**: Script para extração de dados do PySUS.
- **`arquivo-dados.txt`**: Contém links para os arquivos CSV utilizados no projeto.

## Principais Análises

1. **Taxa de Ocupação de Leitos SUS**:
   - Análise da eficiência hospitalar de janeiro a novembro de 2024.
   - Identificação de hospitais com maior taxa de ocupação.

2. **Distribuição de Leitos SUS**:
   - Comparação entre diferentes tipos de unidades hospitalares.
   - Identificação de regiões com maior déficit de leitos.

3. **Taxa de Óbitos**:
   - Relação entre a taxa de óbitos e a taxa de ocupação dos leitos.

4. **CID Principal nos Hospitais Mais Ocupados**:
   - Identificação das condições mais frequentes nos hospitais com maior ocupação.

5. **Modelos Estatísticos**:
   - Regressão linear para prever a taxa de ocupação com base na média de leitos SUS.
   - Regressão logística para analisar fatores associados à ocorrência de óbitos.

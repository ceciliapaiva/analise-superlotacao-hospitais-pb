#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import gdown

st.set_page_config(page_title='Análise de Superlotação em Hospitais da Paraíba', layout='wide')
st.title('Análise de Superlotação em Hospitais da Paraíba – Hospitais da Paraíba (Jan–Nov 2024)')
st.markdown('''
    Este relatório apresenta uma análise da superlotação em hospitais da Paraíba, com foco na taxa de ocupação dos leitos do SUS, 
    média de permanência dos pacientes e taxa de óbitos. Os dados foram obtidos do OpenDataSUS e PySUS.
''')
st.caption('Por: [Cecília Paiva](https://www.linkedin.com/in/ceciliapaiva/)')
st.divider()

st.subheader("Base de Dados Utilizadas")
st.markdown('''
            Os dados utilizados neste projeto foram obtidos de fontes públicas:
            - Hospitais e Leitos | Fonte:[OpenDataSUS](https://opendatasus.saude.gov.br/dataset/hospitais-e-leitos)
            - Sistema de Informações Hospitalares do SUS (SIH/SUS) | Fonte:[PySUS](https://pysus.readthedocs.io/en/latest/databases/data-sources.html#about-sih)
''')
st.divider()

# In[1]:

# ### Hospital e Leito
# Fonte: OpenDataSUS

url_hospital_e_leitos_br = "https://drive.google.com/uc?id=1LRPmb12Et55FEBwi8eL2NgX0s4JQvJ5d"
hospital_e_leitos_br = pd.read_csv(url_hospital_e_leitos_br, encoding='ISO-8859-1')

# Limpeza de dados
hospital_e_leitos_pb = hospital_e_leitos_br[(hospital_e_leitos_br['UF'] == 'PB')]

hospital_e_leitos_pb = hospital_e_leitos_pb.drop(['REGIAO', 'UF', 'MOTIVO_DESABILITACAO', 'CO_TIPO_UNIDADE', 'NATUREZA_JURIDICA', 'NO_COMPLEMENTO'], axis=1)

hospital_e_leitos_pb[['NU_TELEFONE', 'NO_EMAIL']] = hospital_e_leitos_pb[['NU_TELEFONE', 'NO_EMAIL']].fillna('Não se aplica')

hospital_e_leitos_pb = hospital_e_leitos_pb.rename(columns={
    'COMP':'ANO_MES_COMPETENCIA',
    'CNES':'ID_CNES',
    'TP_GESTAO':'TIPO_GESTAO'
})

hospital_e_leitos_pb['TIPO_GESTAO'] = hospital_e_leitos_pb['TIPO_GESTAO'].replace({
    'M':'Municipal',
    'E':'Estadual',
    'D':'Dupla',
    'S':'Sem Gestão'
})


# ### SIH João Pessoa
# Fonte: PySUS

# In[2]:


# Dicionário de Variáveis (https://pcdas.icict.fiocruz.br/conjunto-de-dados/sistema-de-informacoes-hospitalares-do-sus-sihsus/dicionario-de-variaveis/)
# Utilizando gdown para baixar do Google Drive o arquivo CSV com mais de 100MB 
file_id = "1EhOmaJoCLpzDT9HCEY2XmqVnH3KFckVV"
url_sih_pb_2024 = f"https://drive.google.com/uc?id={file_id}"

# Caminho para salvar localmente no Streamlit Cloud
output = 'sih_pb_2024.csv'

# Baixando o arquivo CSV
with st.spinner("Carregando dados do SIH/SUS..."):
    gdown.download(url_sih_pb_2024, output, quiet=False)
    sih_pb_2024 = pd.read_csv(output)

# Limpeza de dados
sih_pb_2024 = sih_pb_2024.drop(['UF_ZI', 'CGC_HOSP', 'N_AIH', 'IDENT', 'CEP', 'MUNIC_RES', 'NASC', 'SEXO',
                                'UTI_MES_IN', 'UTI_MES_AN', 'UTI_MES_AL', 'UTI_MES_TO','UTI_INT_IN', 
                                'UTI_INT_AN', 'UTI_INT_AL', 'UTI_INT_TO', 'DIAR_ACOM', 'QT_DIARIAS',
                                'PROC_SOLIC', 'VAL_SH', 'VAL_SP', 'VAL_SADT', 'VAL_RN', 'VAL_ACOMP',
                                'VAL_ORTP', 'VAL_SANGUE', 'VAL_SADTSR', 'VAL_TRANSP', 'VAL_OBSANG',
                                'VAL_PED1AC', 'VAL_UTI', 'US_TOT', 'DIAG_SECUN','COBRANCA', 'NATUREZA',
                                'NAT_JUR', 'GESTAO', 'RUBRICA', 'IND_VDRL', 'COD_IDADE', 'NACIONAL', 'NUM_PROC',
                                'CAR_INT', 'TOT_PT_SP', 'INSTRU', 'CID_NOTIF', 'CONTRACEP1', 'CONTRACEP2', 'GESTRISCO',
                                'INSC_PN', 'GESTOR_COD', 'GESTOR_TP', 'GESTOR_CPF', 'GESTOR_DT', 'CNPJ_MANT', 'INFEHOSP', 'CID_ASSO',
                                'CID_MORTE', 'COMPLEX', 'FINANC', 'FAEC_TP', 'REGCT', 'AUD_JUST', 'SIS_JUST', 'VAL_SH_FED', 'DIAGSEC6',
                                'DIAGSEC7', 'DIAGSEC8', 'DIAGSEC9', 'TPDISEC1', 'TPDISEC4', 'TPDISEC5', 'TPDISEC6', 'TPDISEC7', 'TPDISEC8', 'TPDISEC9', 
                                'CBOR', 'CNAER', 'VINCPREV', 'CPF_AUT', 'HOMONIMO', 'NUM_FILHOS', 'SEQ_AIH5', 'RACA_COR', 'ETNIA', 'SEQUENCIA', 'REMESSA',
                                'VAL_SP_FED', 'VAL_SH_GES', 'VAL_SP_GES', 'VAL_UCI', 'MARCA_UCI', 'DIAGSEC1', 'DIAGSEC2', 'DIAGSEC3', 'DIAGSEC4', 'DIAGSEC5',
                                'TPDISEC2', 'TPDISEC3', 'MARCA_UTI'], axis=1)

sih_pb_2024 = sih_pb_2024.rename(columns={
    'ESPEC': 'especialidade_leito',
    'PROC_REA': 'procedimento_realizado',
    'VAL_TOT': 'valor_total_aih',
    'DT_INTER': 'dt_internacao',
    'DT_SAIDA': 'dt_saida',
    'DIAG_PRINC': 'cid_principal',
    'MUNIC_MOV': 'municipio_estabelecimento',
    'DIAS_PERM': 'dias_permanencia',
    'MORTE': 'obito',
    'CNES': 'id_cnes',
})

sih_pb_2024 = sih_pb_2024[sih_pb_2024['MES_CMPT'] <= 11]


st.subheader("Percentual de Ocupacão Diária dos Leitos")
st.markdown('Os dados são de janeiro a novembro de 2024')

# In[3]:

# pegando apenas o ano e mes e inserindo em nova coluna
sih_pb_2024['mes_ano'] = sih_pb_2024['dt_internacao'].astype(str).str[:6]
sih_pb_2024['mes_ano_saida'] = sih_pb_2024['dt_saida'].astype(str).str[:6]
sih_pb_2024 = sih_pb_2024[sih_pb_2024['mes_ano'] >= '202401'] # pega apenas o ano de 2024
hospital_e_leitos_pb['mes_ano_leitos'] = hospital_e_leitos_pb['ANO_MES_COMPETENCIA'].astype(str)

# pegando as quantidade de entrada, saidas e leitos por hospital e mês
qtd_entradas = sih_pb_2024.groupby(['id_cnes', 'mes_ano', 'dt_internacao']).size().reset_index(name='qtd_entradas')
qtd_saidas = sih_pb_2024.groupby(['id_cnes', 'mes_ano_saida', 'dt_saida']).size().reset_index(name='qtd_saidas')
qtd_saidas = qtd_saidas.rename(columns={'mes_ano_saida': 'mes_ano', 'dt_saida': 'data'})
qtd_entradas = qtd_entradas.rename(columns={'dt_internacao': 'data'})
qtd_leitos_sus = hospital_e_leitos_pb[['ID_CNES', 'mes_ano_leitos', 'LEITOS_SUS']]
sih_pb_2024['data'] = sih_pb_2024['dt_internacao']
taxa_obitos_pct = sih_pb_2024.groupby(['id_cnes', 'mes_ano', 'data'])['obito'].mean().mul(100).round(2).reset_index(name='taxa_obito_pct')

# juntando e limpando o novo df
df_ocupacao_diaria = pd.merge(qtd_entradas, qtd_saidas, on=['id_cnes', 'mes_ano', 'data'], how='outer')
df_ocupacao_diaria = pd.merge(df_ocupacao_diaria, hospital_e_leitos_pb[['ID_CNES', 'mes_ano_leitos', 'LEITOS_SUS', 'DS_TIPO_UNIDADE', 'MUNICIPIO']], left_on=['id_cnes', 'mes_ano'], right_on=['ID_CNES', 'mes_ano_leitos'], how='left')
df_ocupacao_diaria = pd.merge(df_ocupacao_diaria, taxa_obitos_pct, on=['id_cnes', 'mes_ano', 'data'], how='left')

df_ocupacao_diaria = df_ocupacao_diaria.drop(['mes_ano_leitos', 'ID_CNES'], axis=1)
df_ocupacao_diaria = df_ocupacao_diaria.rename(columns={'LEITOS_SUS': 'total_leitos_sus'})
df_ocupacao_diaria = df_ocupacao_diaria[df_ocupacao_diaria['total_leitos_sus'].notna()]
df_ocupacao_diaria['qtd_entradas'] = df_ocupacao_diaria['qtd_entradas'].fillna(0).astype(int)
df_ocupacao_diaria['qtd_saidas'] = df_ocupacao_diaria['qtd_saidas'].fillna(0).astype(int)
df_ocupacao_diaria['total_leitos_sus'] = df_ocupacao_diaria['total_leitos_sus'].astype(int)
df_ocupacao_diaria['taxa_obito_pct'] = df_ocupacao_diaria['taxa_obito_pct'].fillna(0)

df_ocupacao_diaria['dif_entrada_saida'] = df_ocupacao_diaria['qtd_entradas'] - df_ocupacao_diaria['qtd_saidas']
df_ocupacao_diaria['leitos_ocupados'] = df_ocupacao_diaria.groupby(['id_cnes'])['dif_entrada_saida'].cumsum() 

# Calculando a taxa de ocupação diária
df_ocupacao_diaria['taxa_ocupacao_diaria_pct'] = (df_ocupacao_diaria['leitos_ocupados'] / df_ocupacao_diaria['total_leitos_sus']) * 100
df_ocupacao_diaria['taxa_ocupacao_diaria_pct'] = df_ocupacao_diaria['taxa_ocupacao_diaria_pct'].round(2)

st.dataframe(df_ocupacao_diaria)

# Exibindo gráficos
# ==================================================================================
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.lineplot(
    data=df_ocupacao_diaria,
    x="mes_ano",
    y="taxa_ocupacao_diaria_pct",
    hue="DS_TIPO_UNIDADE",
    palette="bright",
    marker="o",
    ax=ax1
)
ax1.set_title('Distribuição da Taxa de Ocupação dos Leitos SUS na Paraíba')
ax1.set_ylabel('Taxa de Ocupação (%)')
ax1.grid(True)
ax1.tick_params(axis='x', rotation=45)
ax1.legend(loc='upper left', bbox_to_anchor=(1, 1))

st.subheader("Taxa de Ocupação Diária dos Leitos SUS na Paraíba")
st.pyplot(fig1)

# ==================================================================================
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.lineplot(
    data=df_ocupacao_diaria,
    x="mes_ano",
    y="total_leitos_sus",
    hue="DS_TIPO_UNIDADE",
    palette="bright",
    marker="o",
    ax=ax2 
)
ax2.set_title('Distribuição de Leitos SUS na Paraíba')
ax2.set_ylabel('Média Leitos SUS')
ax2.grid(True)
ax2.tick_params(axis='x', rotation=45)
ax2.legend(loc='upper left', bbox_to_anchor=(1, 1))

st.subheader("Leitos SUS na Paraíba")
st.pyplot(fig2)

# ==================================================================================
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.lineplot(
    data=df_ocupacao_diaria,
    x="mes_ano",
    y="taxa_obito_pct",
    hue="DS_TIPO_UNIDADE",
    palette="bright",
    marker="o",
    ax=ax3
)
ax3.set_title('Distribuição da Taxa de Óbitos na Paraíba')
ax3.set_ylabel('Taxa de Óbitos (%)')
ax3.grid(True)
ax3.tick_params(axis='x', rotation=45)
ax3.legend(loc='upper left', bbox_to_anchor=(1, 1))

st.subheader("Taxa de Óbitos na Paraíba")
st.pyplot(fig3)
st.divider()


# In[4]:

# ### Média de Ocupacão Hospitalar
st.subheader("Média de Ocupacão Hospitalar")
st.markdown('''Vamos entender a demanda dos hospitais localizados no Estado da Paraíba.
            ''')

entrada_stats = df_ocupacao_diaria.groupby(['id_cnes'])['qtd_entradas'].mean(numeric_only=True).round(2)
permanencia_stats = sih_pb_2024.groupby(['id_cnes'])['dias_permanencia'].mean().round(2)
leitos_sus_mean = df_ocupacao_diaria.groupby(['id_cnes'])['total_leitos_sus'].mean().round(2)
obitos_mean = sih_pb_2024.groupby(['id_cnes'])['obito'].mean().mul(100).round(0)
taxa_ocupacao_mean_pct = df_ocupacao_diaria.groupby(['id_cnes'])['taxa_ocupacao_diaria_pct'].mean().round(2)

df_stats = pd.DataFrame({
    'qtd_entradas_mean': entrada_stats,
    'dias_permanencia_mean': permanencia_stats,
    'leitos_sus_mean': leitos_sus_mean,
    'obitos_mean': obitos_mean,
    'taxa_ocupacao_mean_pct': taxa_ocupacao_mean_pct
    })

df_stats = df_stats.dropna(subset=['leitos_sus_mean'])
# Em leitos_sus_mean está faltando 5 hospitais que estão registrados em sih_pb_2024, mas não estão em hospital_e_leitos_pb
# Porém, esses hospitais tiveram a ocupacão média diária igual a 0, devido a baixa quantidade de entradas e nenhum dia de permanêcia

df_stats['qtd_entradas_mean'] = df_stats['qtd_entradas_mean'].fillna(0)
df_stats['dias_permanencia_mean'] = df_stats['dias_permanencia_mean'].fillna(0)

# ocupacao_media_diaria = entrada_media * dias_permanencia_media
df_stats['ocupacao_media_diaria'] = df_stats['qtd_entradas_mean'] * df_stats['dias_permanencia_mean']
df_stats['ocupacao_media_diaria'] = df_stats['ocupacao_media_diaria'].round(2)

hospital_e_leitos_pb['ID_CNES'] = hospital_e_leitos_pb['ID_CNES'].astype(int)
df_stats['tipo_unidade'] = hospital_e_leitos_pb.groupby(['ID_CNES'])['DS_TIPO_UNIDADE'].first()
df_stats['nome_hospital'] = hospital_e_leitos_pb.groupby(['ID_CNES'])['NOME_ESTABELECIMENTO'].first()
df_stats['municipio'] = hospital_e_leitos_pb.groupby(['ID_CNES'])['MUNICIPIO'].first()

# Exibindo as Data Frame df_stats
st.dataframe(df_stats)

# distribuição geral da média de ocupação em 2024
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.histplot(
    data=df_stats,
    x='ocupacao_media_diaria',
    kde=True,
    ax=ax4
)
ax4.set_title('Distribuição da Ocupação Média Diária')
ax4.set_xlabel('Média de Ocupação Diária')
ax4.grid(True)

st.subheader("Distribuição da Ocupação Média Diária na Paraíba")
st.pyplot(fig4)

# ### Média de Ocupação Hospitalar
# Vamos entender a demanda dos hospitais localizados no Estado da Paraíba.

# In[5]:

fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=df_stats,
    y='ocupacao_media_diaria',
    hue='tipo_unidade',
    errorbar=None,
    palette='bright',
    ax=ax5
)
ax5.set_title('Distribuição da Ocupação Diária por Tipo de Unidade')
ax5.set_ylabel('Ocupação Média Diária')
ax5.set_xlabel('Tipo de Unidade')
ax5.grid(True)
ax5.legend(loc='upper left', bbox_to_anchor=(1, 1))

st.subheader("Distribuição da Ocupação Diária por Tipo de Unidade na Paraíba")
st.pyplot(fig5)

# ==================================================================================

# quantificar os tipos de unidades na Paraíba
tipos_unidades_sus = hospital_e_leitos_pb[hospital_e_leitos_pb['LEITOS_SUS'] > 0]
contagem_tipos = tipos_unidades_sus['DS_TIPO_UNIDADE'].value_counts()

fig6, ax6 = plt.subplots(figsize=(10, 6))
contagem_tipos.plot(
    kind='bar',
    grid=True,
    ax=ax6
)
ax6.set_title('Tipos de Unidade com SUS na Paraíba')
ax6.set_ylabel('Quantidade de Unidades')
ax6.set_xlabel('Tipo de Unidade')

st.subheader("Tipos de Unidade com SUS na Paraíba")
st.pyplot(fig6)


# In[6]:

# Relação entre Ocupação Diária e Tipos de Unidade
fig7, ax7 = plt.subplots(figsize=(10, 6))
sns.violinplot(
    data=df_stats,
    hue='tipo_unidade',
    y='ocupacao_media_diaria',
    palette='bright',
    ax=ax7
)
ax7.set_title('Relação entre Ocupação Diária e Tipos de Unidade')
ax7.set_ylabel('Ocupação Média Diária')
ax7.set_xlabel('Tipo de Unidade')
ax7.grid(True)
ax7.legend(loc='upper left', bbox_to_anchor=(1, 1))

st.subheader("Relação entre Ocupação Diária e Tipos de Unidade")
st.pyplot(fig7)

# ==================================================================================

# top 6 hospitais mais ocupados
top_6_hospitais = df_stats.nlargest(6, 'ocupacao_media_diaria')
fig8, ax8 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=top_6_hospitais,
    y='ocupacao_media_diaria',
    hue='municipio',
    errorbar=None,
    palette='bright',
    ax=ax8
)
ax8.set_title('Cidades com os Hospitais Mais Ocupados da Paraíba')
ax8.set_ylabel('Ocupação Média Diária')
ax8.set_xlabel('Município')
ax8.grid(True)
ax8.legend(loc='upper left', bbox_to_anchor=(1, 1))

st.subheader("Cidades com os Hospitais Mais Ocupados da Paraíba")
st.pyplot(fig8)

# ==================================================================================

# medidas de centralidade
def medidas_centralidade(df, coluna):
    media = df[coluna].mean()
    mediana = df[coluna].median()
    moda = df[coluna].mode()[0]

    st.subheader(f"Medidas de Centralidade - Coluna: {coluna}")
    st.markdown(f"**Média:** {media:.2f}  \n**Mediana:** {mediana:.2f}  \n**Moda:** {moda:.2f}")

medidas_centralidade(df_stats, 'ocupacao_media_diaria')

# medidas de variabilidade
def medidas_variabilidade(df, coluna):
    q1 = df[coluna].quantile(0.25)
    q3 = df[coluna].quantile(0.75)
    IQR = q3 - q1
    lim_inferior = q1 - 1.5 * IQR
    lim_superior = q3 + 1.5 * IQR
    print(f"IQR: {IQR:.2f}")
    print(f"Limite Inferior: {lim_inferior:.2f}")
    print(f"Limite Superior: {lim_superior:.2f}")
    outliers = df[(df[coluna] < lim_inferior) | (df[coluna] > lim_superior)]

    st.subheader(f"Medidas de Variabilidade — Coluna: {coluna}")
    st.markdown(f"""
    **IQR:** {IQR:.2f}  
    **Limite Inferior:** {lim_inferior:.2f}  
    **Limite Superior:** {lim_superior:.2f}
    """)

    st.subheader("Outliers:")
    st.table(outliers[['municipio', coluna, 'tipo_unidade']])

    st.markdown("**📋 Resumo Estatístico:**")
    st.table(df[coluna].describe().round(2))

medidas_variabilidade(df_stats, 'ocupacao_media_diaria')
st.subheader("Top 6 Hospitais Mais Ocupados")
st.table(top_6_hospitais[['nome_hospital', 'municipio', 'ocupacao_media_diaria']].sort_values(by='ocupacao_media_diaria', ascending=False))
st.markdown('No contexto do Estado da Paraíba, as maiores médias de ocupação diária se encontra em unidades do tipo: hospital geral e hospital especializado (Hospitais que possuem leitos do SUS). Sendo os hospitais especializados os mais afetados, porém, são os que tem menos distribuição no Estado. Foi encontrado 6 dados extremos, provenientes de hospitais localizados em regiões metropolitanas da Paraíba, e esses outliers são os top 6 hospitais com as maiores médias de ocupação diária em 2024.')

# No contexto do Estado da Paraíba, as maiores médias de ocupação diária se encontra em unidades do tipo: hospital geral e hospital especializado (Hospitais que possuem leitos do SUS). Sendo os hospitais especializados os mais afetados, porém, são os que tem menos distribuição no Estado. Foi encontrado 6 dados extremos, provenientes de hospitais localizados em regiões metropolitanas da Paraíba, e esses outliers são os top 6 hospitais com as maiores médias de ocupação diária em 2024.

# ### Quais as CIDs principais mais frequentes nos 10 hospitais mais ocupados?

# In[7]:

st.divider()
st.subheader("CIDs Principais Mais Frequentes nos 10 Hospitais Mais Ocupados")

top_10_ocupacao = df_stats.nlargest(10, 'ocupacao_media_diaria')
cids_frequentes = sih_pb_2024[sih_pb_2024['id_cnes'].isin(top_10_ocupacao.index)]

cids_frequentes = (cids_frequentes.groupby(['id_cnes', 'cid_principal']).size().reset_index(name='qtd_cids_frequentes')
                   .sort_values(['id_cnes', 'qtd_cids_frequentes'], ascending=[True, False]))

cids_freq_hospitais = cids_frequentes.groupby(['id_cnes']).first().reset_index()
cids_freq_hospitais = cids_freq_hospitais.merge(
    hospital_e_leitos_pb[['ID_CNES', 'NOME_ESTABELECIMENTO', 'MUNICIPIO', 'DS_TIPO_UNIDADE']],
    left_on='id_cnes',
    right_on='ID_CNES',
    how='left'
)
cids_freq_hospitais = cids_freq_hospitais.drop(['ID_CNES'], axis=1)
cids_freq_hospitais = cids_freq_hospitais.rename(columns={'NOME_ESTABELECIMENTO': 'nome_hospital', 'MUNICIPIO': 'municipio'})
cids_freq_hospitais = cids_freq_hospitais.drop_duplicates()
cids_freq_hospitais['cid_principal'] = cids_freq_hospitais['cid_principal'].replace({
    'K359': 'Apendicite aguda',
    'S525': 'Fratura da extremidade distal do rádio',
    'Z302': 'Esterilização',
    'O800': 'Parto espontâneo cefálico',
    'I64 ': 'Acidente vascular cerebral',
    'I219': 'Infarto agudo do miocárdio',
    'O82 ': 'Parto por cesariana',
    'F192': 'Síndrome de dependência'
})

st.table(cids_freq_hospitais)

fig9, ax9 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=cids_freq_hospitais,
    x='nome_hospital',
    y='qtd_cids_frequentes',
    hue='cid_principal',
    dodge=False,
    ax=ax9
)
ax9.set_title('Frequência de CIDs por Hospital')
ax9.set_xlabel('Nome do Hospital')
ax9.set_ylabel('Quantidade de CIDs Frequentes')
ax9.tick_params(axis='x', rotation=90)
ax9.grid(True)
ax9.legend(
    title='CID Principal',
    bbox_to_anchor=(1.05, 1),
    loc='upper left',
    borderaxespad=0.)
st.pyplot(fig9)


# ### Taxa de Ocupacão de Leitos SUS
# Vamos ententer a eficiência hospitalar de janeiro a novembro de 2024.

# In[8]:

st.subheader("Taxa de Ocupação de Leitos SUS")
st.markdown('Vamos ententer a eficiência hospitalar de janeiro a novembro de 2024.')

# leitos_sus_mean
medidas_centralidade(df_stats, 'leitos_sus_mean')
medidas_variabilidade(df_stats, 'leitos_sus_mean')
fig10, ax10 = plt.subplots(figsize=(10, 6))
sns.histplot(data=df_stats, x='leitos_sus_mean', kde=True, ax=ax10)
ax10.set_title('Distribuição da Média de Leitos SUS na Paraíba')
ax10.set_xlabel('Média de Leitos SUS')
st.subheader("Distribuição da Média de Leitos SUS na Paraíba")
st.pyplot(fig10)

st.divider()

# taxa_ocupacao_mean_pct
print("\n")
medidas_centralidade(df_stats, 'taxa_ocupacao_mean_pct')
medidas_variabilidade(df_stats, 'taxa_ocupacao_mean_pct')
fig11, ax11 = plt.subplots(figsize=(10, 6))
sns.histplot(data=df_stats, x='taxa_ocupacao_mean_pct', kde=True, ax=ax11)
ax11.set_title('Distribuição da Taxa de Ocupação Média dos Leitos SUS na Paraíba')
ax11.set_xlabel('Taxa de Ocupação Média (%)')
st.subheader("Distribuição da Taxa de Ocupação Média dos Leitos SUS na Paraíba")
st.pyplot(fig11)

st.subheader('Top 10 Hospitais Mais Lotados')
top_10_lotados = df_stats.nlargest(10, 'taxa_ocupacao_mean_pct').sort_values(by='taxa_ocupacao_mean_pct', ascending=False)
st.table(top_10_lotados)
st.divider()


# ### Qual a relação entre os Leitos do SUS e Taxa de Ocupacão?

# In[9]:

st.subheader("Relação entre os Leitos do SUS e a Taxa de Ocupação")  

fig12, ax12 = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df_stats, x='taxa_ocupacao_mean_pct', y='leitos_sus_mean', hue='tipo_unidade', palette='bright', ax=ax12)
ax12.set_title('Relação entre Taxa de Ocupação e Leitos SUS')
ax12.set_xlabel('Taxa de Ocupação Média (%)')    
ax12.set_ylabel('Média de Leitos SUS')
ax12.legend(loc='upper left', bbox_to_anchor=(1, 1))
st.pyplot(fig12)

corr_pearson = df_stats['leitos_sus_mean'].corr(df_stats['taxa_ocupacao_mean_pct'], method='pearson')
corr_spearman = df_stats['leitos_sus_mean'].corr(df_stats['taxa_ocupacao_mean_pct'], method='spearman')
corr_kendall = df_stats['leitos_sus_mean'].corr(df_stats['taxa_ocupacao_mean_pct'], method='kendall')

st.markdown(f"(Leitos SUS com Taxa de Ocupação)\n**Correlação de Pearson:** {corr_pearson:.2f}\n**Correlação de Spearman:** {corr_spearman:.2f}\n**Correlação de Kendall:** {corr_kendall:.2f}")
st.markdown('''A média de leitos do SUS apresenta uma relação moderada com a taxa de ocupação desses leitos em hospitais da Paraíba, 
            conforme demonstrado pelas correlações de Spearman (0,66) e Kendall (0,45). 
            Isso indica que, em geral, quanto maior for a média de leitos SUS disponibilizados por um hospital, 
            maior tende a ser sua taxa de ocupação.''')

# A média de leitos do SUS apresenta uma relação moderada com a taxa de ocupação desses leitos em hospitais da Paraíba, conforme demonstrado pelas correlações de Spearman (0,66) e Kendall (0,45). Isso indica que, em geral, quanto maior for a média de leitos SUS disponibilizados por um hospital, maior tende a ser sua taxa de ocupação.

# ### Qual a relacão entre a Média de Óbitos e a Taxa de Ocupacao dos Leitos?

# In[10]:

st.subheader("Relação entre Média de Óbitos e Taxa de Ocupação")

fig13, ax13 = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df_stats, x='taxa_ocupacao_mean_pct', y='obitos_mean', hue='tipo_unidade', palette='bright', ax=ax13)
ax13.set_title('Relação entre Óbitos e Taxa de Ocupacão Diária')
ax13.set_ylabel('Média de Óbitos (%)')
ax13.set_xlabel('Taxa de Ocupação (%)')
ax13.legend(loc='upper left', bbox_to_anchor=(1, 1))
st.pyplot(fig13)

# Pode ter uma relacao mais forte com tipos de unidades
corr_pearson = df_stats['obitos_mean'].corr(df_stats['taxa_ocupacao_mean_pct'], method='pearson')
corr_spearman = df_stats['obitos_mean'].corr(df_stats['taxa_ocupacao_mean_pct'], method='spearman')
corr_kendall = df_stats['obitos_mean'].corr(df_stats['taxa_ocupacao_mean_pct'], method='kendall')
st.markdown(f"(Média de Óbitos com Taxa Ocupacão)\n**Correlação de Pearson:** {corr_pearson:.2f}\n**Correlação de Spearman:** {corr_spearman:.2f}\n**Correlação de Kendall:** {corr_kendall:.2f}")

# ### Análise de Regressão Linear
# Leitos SUS e Taxa de Ocupacao dos Leitos

# In[11]:

st.divider()
st.subheader("Análise de Regressão Linear")

st.divider()
st.markdown("Leitos SUS e Taxa de Ocupação dos Leitos")

import sklearn.model_selection as ms
import sklearn.linear_model as lm
from sklearn.metrics import mean_squared_error, r2_score

x = df_stats[['leitos_sus_mean']]
y = df_stats[['taxa_ocupacao_mean_pct']]

# Separar os dados em Treino e Teste
x_train, x_test, y_train, y_test = ms.train_test_split(x, y, test_size=0.2, random_state=0)

# Treinando o modelo
regressor = lm.LinearRegression()
regressor.fit(x_train, y_train)

# Previsão
y_pred = regressor.predict(x_test)

# Vizualizar o treino
fig14, ax14 = plt.subplots(figsize=(10, 6))
ax14.scatter(x_train, y_train, color='red')
ax14.plot(x_train, regressor.predict(x_train), color='blue')
ax14.set_title('Dados de Treinamento')
ax14.set_xlabel('Média de Leitos SUS')
ax14.set_ylabel('Taxa de Ocupação Média (%)')
st.pyplot(fig14)

# Vizualizar o teste
fig15, ax15 = plt.subplots(figsize=(10, 6))
ax15.scatter(x_test, y_test, color='green')
ax15.plot(x_test, y_pred, color='blue')
ax15.set_title('Dados de teste')
ax15.set_xlabel('Média de Leitos SUS')
ax15.set_ylabel('Taxa de Ocupação Média (%)')
st.pyplot(fig15)

# Valor especificado
valor_especificado = 260
st.markdown(f"Prevendo a taxa de ocupação média para uma média de {valor_especificado} leitos SUS: {regressor.predict([[valor_especificado]])[0].round(2)}")
st.markdown(f"b0 (intercept): {regressor.intercept_.round(2)}")
st.markdown(f"b1 (coefficient): {regressor.coef_[0].round(2)}")

# Erro residual
fitted = regressor.predict(df_stats[['leitos_sus_mean']])	
residuals = y - fitted

fig16, ax16 = plt.subplots(figsize=(10, 6))
ax16.scatter(x, residuals, color='orange')
ax16.axhline(y=0, color='black', linestyle='--')
ax16.set_title('Resíduos do Modelo')
ax16.set_xlabel('Média de Leitos SUS')
ax16.set_ylabel('Resíduos')
st.pyplot(fig16)

# Avaliando o modelo
RMSE = np.sqrt(mean_squared_error(y, fitted))
r2 = r2_score(y, fitted)
st.markdown(f'===========Avaliando o Modelo===========\nRoot Mean Square Error (RMSE): {RMSE:.2f}')
st.markdown(f'Coefficiente of determination (r2): {r2:.4f}')

st.subheader("Regressão Linear Múltipla")
st.markdown("Vamos fazer um regressão linear múltipla considerando os tipos de unidades, taxa de óbitos e média de ocupacao diária.")

# In[12]:


x = df_stats[['leitos_sus_mean', 'tipo_unidade', 'obitos_mean', 'ocupacao_media_diaria']]
y = df_stats[['taxa_ocupacao_mean_pct']]

# Transformar a variável categórica 'tipo_unidade' em variáveis dummy
# Hospital especializado é o dummies de referência
x_dummies = pd.get_dummies(x, drop_first=True)

# Separar os dados em Treino e Teste
x_train, x_test, y_train, y_test = ms.train_test_split(x_dummies, y, test_size=0.2, random_state=0)

# Treinando o modelo
regressor_multiple = lm.LinearRegression()
regressor_multiple.fit(x_train, y_train)

# Coeficientes
st.markdown(f'Intercept: {regressor_multiple.intercept_.round(3)}')
st.markdown('Coefficients:')
for name, coef in zip(x_dummies.columns, regressor_multiple.coef_.flatten()):
    st.markdown(f' {name}: {coef:.3f}')

# Previsão
y_pred = regressor_multiple.predict(x_test)

# Avaliando o modelo
fitted = regressor_multiple.predict(x_dummies)
RMSE = np.sqrt(mean_squared_error(y, fitted))
r2 = r2_score(y, fitted)
st.markdown(f'''===========Avaliando o Modelo===========
            Root Mean Square Error (RMSE): {RMSE:.2f}''')
st.markdown(f'Coefficiente of determination (r2): {r2:.4f}')

# Calcular os resíduos
residuals = y - fitted

# Gráfico de Resíduos vs Valores Ajustados
fig17, ax17 = plt.subplots(figsize=(10, 6))
ax17.scatter(fitted, residuals, color='orange')
ax17.axhline(y=0, color='black', linestyle='--')
ax17.set_title('Resíduos vs Valores Ajustados')
ax17.set_xlabel('Valores Ajustados (Fitted)')
ax17.set_ylabel('Resíduos')
st.pyplot(fig17)

# ### Regressão Logística
# Sem 'MUNICIPIO' como variável preditora.
st.subheader("Regressão Logística sem Município")
st.markdown("Vamos fazer uma regressão logística para prever a probabilidade de óbito com base na taxa de ocupação, tipo de unidade e idade do paciente.")



# In[13]:


from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

df_combined = sih_pb_2024.merge(df_ocupacao_diaria, on=['id_cnes', 'mes_ano', 'data'], how='left')
df_combined = df_combined.dropna(subset=['taxa_ocupacao_diaria_pct'])

x_predictors = df_combined[['DS_TIPO_UNIDADE', 'IDADE', 'taxa_ocupacao_diaria_pct']]
y_outcome = df_combined['obito']

# Dummies
x_pred_dummies = pd.get_dummies(x_predictors, columns=['DS_TIPO_UNIDADE'], drop_first=True)

# Escalar os dados
scaler = StandardScaler()
x_pred_scaled = scaler.fit_transform(x_pred_dummies)

# Separar os dados em Treino e Teste
x_train, x_test, y_train, y_test = ms.train_test_split(x_pred_scaled, y_outcome, test_size=0.2, random_state=0)

# SMOTE balanceia as classes, aumentando a quantidade de amostras da classe minoritária
smote = SMOTE(random_state=0)
x_train_balanced, y_train_balanced = smote.fit_resample(x_train, y_train)

# Treinando o modelo
logistic_regressor = LogisticRegression(class_weight='balanced', max_iter=1000)
logistic_regressor.fit(x_train_balanced, y_train_balanced)

# Previsao
y_pred = logistic_regressor.predict(x_test)
y_pred_proba = logistic_regressor.predict_proba(x_test)

# Avaliando o modelo
st.header("Avaliação do Modelo")

st.subheader("Distribuição dos Valores Reais")
st.write(y_outcome.value_counts())

st.subheader("Matriz de Confusão")
st.write(confusion_matrix(y_test, y_pred))

st.subheader("Relatório de Classificação")
report = classification_report(y_test, y_pred, output_dict=True)
st.dataframe(pd.DataFrame(report).transpose())

# Coeficientes
coef_df = pd.DataFrame({
    'Variável': x_pred_dummies.columns,
    'Coeficiente': logistic_regressor.coef_[0].round(3)
}).sort_values(by='Coeficiente', ascending=False)

st.subheader("Coeficientes do Modelo")
st.write(f"Intercept: {logistic_regressor.intercept_[0].round(3)}")
st.dataframe(coef_df)

# Com 'MUNICIPIO' como variável preditora.
st.subheader("Regressão Logística com Município")

# In[14]:


x_predictors = df_combined[['MUNICIPIO', 'DS_TIPO_UNIDADE', 'IDADE', 'taxa_ocupacao_diaria_pct']]
y_outcome = df_combined['obito']

# Dummies
x_pred_dummies = pd.get_dummies(x_predictors, columns=['MUNICIPIO', 'DS_TIPO_UNIDADE'], drop_first=True)

# Separar os dados em Treino e Teste
x_train, x_test, y_train, y_test = ms.train_test_split(x_pred_dummies, y_outcome, test_size=0.2, random_state=0)

# Escalar os dados
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

# SMOTE balanceia as classes, aumentando a quantidade de amostras da classe minoritária
smote = SMOTE(random_state=0)
x_train_balanced, y_train_balanced = smote.fit_resample(x_train, y_train)

# Treinando o modelo
logistic_regressor = LogisticRegression(class_weight='balanced', max_iter=2000)
logistic_regressor.fit(x_train_balanced, y_train_balanced)

# Previsao
y_pred = logistic_regressor.predict(x_test)
y_pred_proba = logistic_regressor.predict_proba(x_test)

# Avaliando o modelo
st.header("Avaliação do Modelo")

st.subheader("Distribuição dos Valores Reais")
st.write(y_outcome.value_counts())

st.subheader("Matriz de Confusão")
cm = confusion_matrix(y_test, y_pred)
st.write(cm)

st.subheader("Relatório de Classificação")
report_dict = classification_report(y_test, y_pred, output_dict=True)
report_df = pd.DataFrame(report_dict).transpose()
st.dataframe(report_df)


# In[15]:

# Coeficientes do modelo
coef_df = pd.DataFrame({
    'Variável': x_pred_dummies.columns,
    'Coeficiente': logistic_regressor.coef_[0].round(3)
}).sort_values(by='Coeficiente', ascending=False)

st.subheader("Coeficientes do Modelo")
st.write(f"Intercept: {logistic_regressor.intercept_[0].round(3)}")
st.dataframe(coef_df)

st.divider()
st.header("Conclusões")
st.markdown("""
- A superlotação de hospitais na Paraíba atinge principalmente as regiões metropolitanas, onde a demanda é maior e a oferta de leitos SUS também é maior.
- Existe um possível déficit na distribuição dos hospitais especializados que têm leitos SUS no Estado, os quais têm uma demanda considerável.
- A taxa de óbito influencia na taxa de ocupação; provavelmente um hospital que lida com casos de alta gravidade obtém uma maior taxa de óbito e também uma alta taxa de ocupação.
- Os municípios que se destacaram nas análises são de regiões metropolitanas ou arredores, dos quais muitas outras cidades dependem de seus serviços.
- No geral, poucos hospitais do Estado enfrentaram uma superlotação, sendo esses da categoria hospital especializado e geral localizados nos grandes centros urbanos.
""")
st.info("""
Obrigado por acompanhar esta análise!  
Este trabalho foi desenvolvido com fins acadêmicos e de estudo, com o objetivo de explorar dados e gerar insights sobre a ocupação hospitalar no estado da Paraíba.  

Entre em contato: [maria.paiva@dcx.ufpb.br](mailto:maria.paiva@dcx.ufpb.br)
""")
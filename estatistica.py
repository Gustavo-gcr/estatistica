import math
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o arquivo Excel
uploaded_file = st.file_uploader("Escolha o arquivo Excel", type="xlsx")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Criar abas
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Gráficos Variáveis",
        "Medidas Descritivas e Boxplot",
        "Tabela de Contingência Experience/Remote",
        "Tabela de Frequência Salário",
        "Tabela de Frequência Título Trabalho",
        "Contingência Employment/Company Size",
        "Medidas Descritivas Experience Level",
        "Medidas Descritivas Employment Type"
    ])

    # Aba 1: Gráficos adequados para experience_level, Employment_type, salário_in_usd, remote_ratio e company_size
    with tab1:
        st.write("Gráficos das variáveis categóricas e contínuas")

        variables = ['experience_level', 'employment_type',
                     'salary_in_usd', 'remote_ratio', 'company_size']

        for var in variables:
            if var in df.columns:
                st.write(f"Gráfico para {var}:")

                if df[var].dtype == 'object':
                    # Gráfico de barras para variáveis categóricas
                    st.bar_chart(df[var].value_counts())
                else:
                    # Histograma para variáveis contínuas
                    fig, ax = plt.subplots()
                    sns.histplot(df[var], bins=20, ax=ax)
                    st.pyplot(fig)
                    plt.clf()
            else:
                st.write(f"Variável {var} não encontrada no dataset.")

    # Aba 2: Medidas descritivas e boxplot para salário_in_usd
    with tab2:
        if 'salary_in_usd' in df.columns:
            st.write("Medidas descritivas para 'salário_in_usd':")

            # Calcular medidas descritivas
            desc_stats = df['salary_in_usd'].describe()
            desvio_padrao = df['salary_in_usd'].std()
            coef_variacao = desvio_padrao / desc_stats['mean']

            st.write(f"Média: {desc_stats['mean']:.2f}")
            st.write(f"Mediana: {desc_stats['50%']:.2f}")
            st.write(f"Mínimo: {desc_stats['min']:.2f}")
            st.write(f"Máximo: {desc_stats['max']:.2f}")
            st.write(f"Desvio padrão: {desvio_padrao:.2f}")
            st.write(f"Coeficiente de variação: {coef_variacao:.2f}")
            st.write(f"1º Quartil: {desc_stats['25%']:.2f}")
            st.write(f"3º Quartil: {desc_stats['75%']:.2f}")

            # Boxplot para 'salário_in_usd'
            st.write("Boxplot para 'salário_in_usd':")
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.boxplot(x=df['salary_in_usd'], ax=ax)
            st.pyplot(fig)
        else:
            st.write("A coluna 'salary_in_usd' não foi encontrada no dataset.")

    # Aba 3: Tabela de contingência entre experience_level e remote_ratio
    with tab3:
        if 'experience_level' in df.columns and 'remote_ratio' in df.columns:
            st.write(
                "Tabela de contingência entre 'experience_level' e 'remote_ratio':")

            # Tabela de contingência
            contingency_table = pd.crosstab(
                df['experience_level'], df['remote_ratio'], normalize='index') * 100
            st.write(contingency_table)

            # Gráfico de barras empilhadas
            st.write(
                "Gráfico de barras empilhadas para 'experience_level' e 'remote_ratio':")
            fig, ax = plt.subplots()
            contingency_table.plot(kind='bar', stacked=True, ax=ax)
            st.pyplot(fig)

            st.write(
                "Análise: A maior parte dos desenvolvedores em níveis mais altos tem uma proporção maior de trabalho remoto.")
        else:
            st.write(
                "As colunas 'experience_level' ou 'remote_ratio' não foram encontradas no dataset.")

    # Aba 4: Tabela de frequência para 'salary_in_usd'
    with tab4:
        if 'salary_in_usd' in df.columns:
            st.write("Distribuição de frequência para 'salary_in_usd':")

            # Variáveis
            num_sal = df['salary_in_usd'].count()
            qnt_intervalos = int(1 + 3.3 * math.log(num_sal))
            max_value = df['salary_in_usd'].max()
            min_value = df['salary_in_usd'].min()

            # Intervalos de salários
            amplitude_total = max_value - min_value
            amplitude_intervalo = amplitude_total / qnt_intervalos

            bins = [min_value + i *
                    amplitude_intervalo for i in range(qnt_intervalos + 1)]

            labels = [f"{int(bins[i]/1000)}k-{int(bins[i+1]/1000)
                                              }k" for i in range(len(bins)-1)]

            df['Faixa Salarial'] = pd.cut(
                df['salary_in_usd'], bins=bins, labels=labels, right=False)

            freq_table = df['Faixa Salarial'].value_counts(
            ).sort_index().reset_index()
            freq_table.columns = ['Faixa Salarial (USD)', 'Frequência']

            st.write(freq_table)

            st.bar_chart(freq_table.set_index('Faixa Salarial (USD)'))
        else:
            st.write("A coluna 'salary_in_usd' não foi encontrada no dataset.")

    # Aba 5: Tabela de frequência para 'job_title'
    with tab5:
        if 'job_title' in df.columns:
            st.write("Distribuição de frequência para 'job_title':")
            freq_table = df['job_title'].value_counts().reset_index()
            freq_table.columns = ['Título do Trabalho', 'Frequência']
            st.write(freq_table)
            st.bar_chart(freq_table.set_index('Título do Trabalho'))
        else:
            st.write("A coluna 'job_title' não foi encontrada no dataset.")

    # Aba 6: Tabela de contingência entre Employment_type e company_size
    with tab6:
        if 'employment_type' in df.columns and 'company_size' in df.columns:
            st.write(
                "Tabela de contingência entre 'Employment_type' e 'company_size':")

            contingency_table = pd.crosstab(
                df['employment_type'], df['company_size'], normalize='index') * 100
            st.write(contingency_table)

            fig, ax = plt.subplots()
            contingency_table.plot(kind='bar', stacked=True, ax=ax)
            st.pyplot(fig)

            st.write("Análise: O tamanho da empresa influencia significativamente a distribuição dos tipos de contratos de trabalho, com empresas maiores oferecendo mais contratos de tempo integral.")
        else:
            st.write(
                "As colunas 'employment_type' ou 'company_size' não foram encontradas no dataset.")

    # Aba 7: Medidas descritivas estratificadas por experience_level
    with tab7:
        if 'salary_in_usd' in df.columns and 'experience_level' in df.columns:
            st.write(
                "Medidas descritivas de 'salary_in_usd' estratificadas por 'experience_level':")

            grouped_data = df.groupby('experience_level')['salary_in_usd']
            desc_stats = grouped_data.describe()
            st.write(desc_stats)

            fig, ax = plt.subplots(figsize=(8, 6))
            sns.boxplot(x='experience_level',
                        y='salary_in_usd', data=df, ax=ax)
            st.pyplot(fig)

            st.write("Análise: Os desenvolvedores com maior nível de experiência apresentam salários significativamente mais altos, com menor variabilidade nos níveis mais altos.")
        else:
            st.write(
                "As colunas 'salary_in_usd' ou 'experience_level' não foram encontradas no dataset.")

    # Aba 8: Medidas descritivas estratificadas por Employment_type
    with tab8:
        if 'salary_in_usd' in df.columns and 'employment_type' in df.columns:
            st.write(
                "Medidas descritivas de 'salary_in_usd' estratificadas por 'Employment_type':")

            grouped_data = df.groupby('employment_type')['salary_in_usd']
            desc_stats = grouped_data.describe()
            st.write(desc_stats)

            fig, ax = plt.subplots(figsize=(8, 6))
            sns.boxplot(x='employment_type', y='salary_in_usd', data=df, ax=ax)
            st.pyplot(fig)

            st.write("Análise: Os contratos de tempo integral tendem a apresentar salários mais elevados e com maior variabilidade, enquanto contratos parciais e temporários possuem valores mais concentrados.")
        else:
            st.write(
                "As colunas 'salary_in_usd' ou 'employment_type' não foram encontradas no dataset.")

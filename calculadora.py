import streamlit as st
import altair as alt
import pandas as pd

# CSS Customizado para estilo do site
st.markdown(
    """
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
    }
    .result {
        font-size: 20px;
        margin: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Funções
def calcular_imc(peso, altura):
    return peso / (altura ** 2)

def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso 🟦", "blue"
    elif 18.5 <= imc < 24.9:
        return "Peso normal 🟩", "green"
    elif 25 <= imc < 29.9:
        return "Sobrepeso 🟧", "orange"
    elif 30 <= imc < 34.9:
        return "Obesidade grau I 🟥", "red"
    elif 35 <= imc < 39.9:
        return "Obesidade grau II 🟥", "darkred"
    else:
        return "Obesidade grau III 🟪", "purple"

def peso_ideal(altura):
    return (18.5 * altura ** 2, 24.9 * altura ** 2)

# Título
st.markdown("<h1 class='title'>Calculadora de IMC Personalizada 🏋️</h1>", unsafe_allow_html=True)
st.write("Insira seus dados, peso e altura para calcular seu IMC e obter recomendações de saúde.")

# Entradas de Dados Pessoais
nome = st.text_input("Nome")
idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
genero = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro"])

# Entradas do Usuário para Peso e Altura
col1, col2 = st.columns(2)
with col1:
    peso = st.number_input("Peso (kg)", min_value=0.0, format="%.2f")
with col2:
    altura = st.number_input("Altura (m)", min_value=0.0, format="%.2f")

# Botão de Cálculo e Resultados
if st.button("Calcular IMC"):
    if altura > 0:
        imc = calcular_imc(peso, altura)
        classificacao, cor = classificar_imc(imc)
        peso_min, peso_max = peso_ideal(altura)

        # Exibe informações pessoais e resultados do IMC
        st.markdown(f"<p class='result'>Nome: {nome}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='result'>Idade: {idade} anos</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='result'>Gênero: {genero}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='result'>Seu IMC é: {imc:.2f}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='result' style='color:{cor}'>Classificação: {classificacao}</p>", unsafe_allow_html=True)
        st.write(f"Faixa de peso ideal para sua altura: **{peso_min:.2f} kg** a **{peso_max:.2f} kg**")

        # Adiciona recomendações
        if classificacao == "Peso normal 🟩":
            st.success("Parabéns! Mantenha seu estilo de vida saudável.")
        else:
            st.warning("Considere fazer ajustes na dieta e exercícios para atingir o peso ideal.")

        # Dados para o gráfico Altair
        categorias = ["Abaixo do Peso", "Peso Normal", "Sobrepeso", "Obesidade I", "Obesidade II", "Obesidade III"]
        limites = [18.5, 24.9, 29.9, 34.9, 39.9, 45]
        cores = ["blue", "green", "orange", "red", "darkred", "purple"]

        # Cria o DataFrame inicial
        data = pd.DataFrame({
            'Categoria': categorias,
            'Limite': limites,
            'Cor': cores
        })

        # Adiciona o valor do IMC do usuário
        nova_linha = pd.DataFrame([{'Categoria': 'Seu IMC', 'Limite': imc, 'Cor': cor}])
        data = pd.concat([data, nova_linha], ignore_index=True)

        # Gráfico com Altair
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X('Limite:Q', title='IMC'),
            y=alt.Y('Categoria:N', sort='-x', title='Categoria'),
            color=alt.Color('Cor:N', scale=None),
            tooltip=['Categoria', 'Limite']
        ).properties(
            title="Distribuição do IMC"
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.write("Por favor, insira uma altura válida.")

# Botão de Reset para reiniciar o formulário
if st.button("Reiniciar"):
    st.session_state['peso'] = 0.0
    st.session_state['altura'] = 0.0
    st.session_state['nome'] = ""
    st.session_state['idade'] = 0
    st.session_state['genero'] = "Masculino"
    st.experimental_rerun()

import streamlit as st
import altair as alt
import pandas as pd

# CSS Customizado
st.markdown(
    """
    <style>
    .title { font-size: 36px; font-weight: bold; color: #4CAF50; text-align: center; }
    .result { font-size: 20px; margin: 10px; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 5px; }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializa session_state para os inputs
for campo in ['nome', 'idade', 'genero', 'peso', 'altura']:
    if campo not in st.session_state:
        st.session_state[campo] = 0.0 if campo in ['peso', 'altura'] else ""

# Funções para cálculos e recomendações
def calcular_imc(peso: float, altura: float) -> float:
    """Calcula o IMC."""
    return peso / (altura ** 2)

def classificar_imc(imc: float) -> tuple:
    """Classifica o IMC em categorias de saúde."""
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

def peso_ideal(altura: float) -> tuple:
    """Calcula o intervalo de peso ideal para a altura fornecida."""
    return 18.5 * altura ** 2, 24.9 * altura ** 2

# Cabeçalho
st.markdown("<h1 class='title'>Calculadora de IMC Personalizada 🏋️</h1>", unsafe_allow_html=True)

# Formulário para entrada de dados pessoais
with st.form("dados_pessoais"):
    st.session_state['nome'] = st.text_input("Nome", value=st.session_state['nome'])
    st.session_state['idade'] = st.number_input("Idade", min_value=0, max_value=120, step=1, value=st.session_state['idade'])
    st.session_state['genero'] = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro"], index=["Masculino", "Feminino", "Outro"].index(st.session_state['genero']))

    col1, col2 = st.columns(2)
    with col1:
        st.session_state['peso'] = st.number_input("Peso (kg)", min_value=0.0, format="%.2f", value=st.session_state['peso'])
    with col2:
        st.session_state['altura'] = st.number_input("Altura (m)", min_value=0.0, format="%.2f", value=st.session_state['altura'])

    # Botões de submissão e reset do formulário
    calcular = st.form_submit_button("Calcular IMC")
    st.form_reset_button("Reiniciar")

# Processamento de dados e exibição de resultados
if calcular:
    altura = st.session_state['altura']
    peso = st.session_state['peso']
    if altura > 0:
        imc = calcular_imc(peso, altura)
        classificacao, cor = classificar_imc(imc)
        peso_min, peso_max = peso_ideal(altura)

        # Exibição dos dados do usuário e resultados
        st.write(f"**Nome:** {st.session_state['nome']}, **Idade:** {st.session_state['idade']} anos, **Gênero:** {st.session_state['genero']}")
        st.markdown(f"<p class='result'>**Seu IMC é:** {imc:.2f}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='result' style='color:{cor}'>Classificação: {classificacao}</p>", unsafe_allow_html=True)
        st.write(f"Faixa de peso ideal para sua altura: **{peso_min:.2f} kg** a **{peso_max:.2f} kg**")

        # Recomendações personalizadas
        if classificacao == "Peso normal 🟩":
            st.success("Parabéns! Mantenha seu estilo de vida saudável.")
        else:
            st.warning("Considere ajustes na dieta e exercício. Consulte um profissional de saúde para uma orientação personalizada.")

        # Gráfico de distribuição do IMC com destaque
        categorias = ["Abaixo do Peso", "Peso Normal", "Sobrepeso", "Obesidade I", "Obesidade II", "Obesidade III"]
        limites = [18.5, 24.9, 29.9, 34.9, 39.9, 45]
        cores = ["blue", "green", "orange", "red", "darkred", "purple"]

        data = pd.DataFrame({
            'Categoria': categorias,
            'Limite': limites,
            'Cor': cores
        })

        # Adiciona o IMC do usuário para destacar no gráfico
        data = pd.concat([data, pd.DataFrame([{'Categoria': 'Seu IMC', 'Limite': imc, 'Cor': cor}])], ignore_index=True)

        # Gráfico com Altair
        chart = alt.Chart(data).mark_bar(size=40).encode(
            x=alt.X('Limite:Q', title='IMC'),
            y=alt.Y('Categoria:N', sort='-x', title='Categoria'),
            color=alt.Color('Cor:N', scale=None),
            tooltip=['Categoria', 'Limite']
        ).properties(
            title="Distribuição do IMC"
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.error("Por favor, insira uma altura válida.")

import streamlit as st
import matplotlib.pyplot as plt

def calcular_imc(peso, altura):
    return peso / (altura ** 2)

def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso", "blue"
    elif 18.5 <= imc < 24.9:
        return "Peso normal", "green"
    elif 25 <= imc < 29.9:
        return "Sobrepeso", "orange"
    elif 30 <= imc < 34.9:
        return "Obesidade grau I", "red"
    elif 35 <= imc < 39.9:
        return "Obesidade grau II", "red"
    else:
        return "Obesidade grau III", "darkred"

def peso_ideal(altura):
    return (18.5 * altura ** 2, 24.9 * altura ** 2)

st.title("Calculadora de IMC Melhorada 🏋️")
st.write("Insira seu peso e altura para calcular seu IMC e obter recomendações de saúde.")

peso = st.number_input("Peso (kg)", min_value=0.0, format="%.2f")
altura = st.number_input("Altura (m)", min_value=0.0, format="%.2f")

if st.button("Calcular IMC"):
    if altura > 0:
        imc = calcular_imc(peso, altura)
        classificacao, cor = classificar_imc(imc)
        peso_min, peso_max = peso_ideal(altura)

        # Resultados
        st.markdown(f"**Seu IMC é:** {imc:.2f}")
        st.markdown(f"<h3 style='color:{cor}'>Classificação: {classificacao}</h3>", unsafe_allow_html=True)
        st.write(f"Faixa de peso ideal para sua altura: **{peso_min:.2f} kg** a **{peso_max:.2f} kg**")
        
        # Indicador visual
        fig, ax = plt.subplots()
        categorias = ["Abaixo do Peso", "Normal", "Sobrepeso", "Obesidade I", "Obesidade II", "Obesidade III"]
        cores = ["blue", "green", "orange", "red", "darkred", "purple"]
        ax.barh(categorias, [18.5, 24.9, 29.9, 34.9, 39.9, 45], color=cores)
        ax.axvline(imc, color=cor, linestyle='--', label=f'Seu IMC: {imc:.2f}')
        ax.legend()
        st.pyplot(fig)
    else:
        st.write("Por favor, insira uma altura válida.")

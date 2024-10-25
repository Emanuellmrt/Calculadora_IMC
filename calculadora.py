import streamlit as st

def calcular_imc(peso, altura):
    return peso / (altura ** 2)

def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc < 24.9:
        return "Peso normal"
    elif 25 <= imc < 29.9:
        return "Sobrepeso"
    elif 30 <= imc < 34.9:
        return "Obesidade grau I"
    elif 35 <= imc < 39.9:
        return "Obesidade grau II"
    else:
        return "Obesidade grau III"

st.title("Calculadora de IMC")
st.write("Insira seu peso e altura para calcular seu IMC.")

peso = st.number_input("Peso (kg)", min_value=0.0, format="%.2f")
altura = st.number_input("Altura (m)", min_value=0.0, format="%.2f")

if st.button("Calcular IMC"):
    if altura > 0:
        imc = calcular_imc(peso, altura)
        classificacao = classificar_imc(imc)
        st.write(f"Seu IMC é: {imc:.2f}")
        st.write(f"Classificação: {classificacao}")
    else:
        st.write("Por favor, insira uma altura válida.")

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Simulação de Investimento")

# Parâmetros
investimento_inicial = st.number_input("Investimento inicial:", min_value=0)
taxa_juros = st.slider("Taxa de juros anual (%):", 0.0, 20.0, 5.0)
anos = st.slider("Duração (anos):", 1, 50, 10)

# Cálculo do investimento ao longo dos anos
valores = [investimento_inicial * (1 + taxa_juros / 100) ** i for i in range(anos + 1)]

# Gráfico
plt.figure(figsize=(10, 5))
plt.plot(range(anos + 1), valores)
plt.xlabel("Anos")
plt.ylabel("Valor acumulado")
plt.title("Simulação de Crescimento do Investimento")
st.pyplot(plt)

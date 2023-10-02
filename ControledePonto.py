import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Função para carregar a planilha de funcionários
# Função para carregar a planilha de funcionários
def load_funcionarios_data():
    df = pd.read_excel('funcionarios.xlsx', converters={'data_admissao': pd.to_datetime}, date_format='%d/%m/%Y')
    return df



# Função para carregar a planilha de registro de ponto
def load_registro_ponto_data():
    try:
        df = pd.read_excel('registroPonto.xlsx', parse_dates=['data', 'hora_entrada', 'hora_saida'])
    except FileNotFoundError:
        df = pd.DataFrame(columns=['codigo', 'nome', 'data', 'hora_entrada', 'hora_saida'])
    return df

# Define o título da página
st.title("ZP CONTABILIDADE")
st.divider()


# Adiciona uma barra lateral com as opções
page = st.sidebar.selectbox("Escolha uma página:", ("Página Inicial", "Registrar Entrada/Saída", "Consultar ponto", "Cadastrar Funcionário"))
# Variável para verificar se a senha está correta
senha_correta = False

# Verifica se a senha está correta para acessar a página "Consultar ponto"
if page == "Consultar ponto":
    senha = st.text_input("Digite a senha de acesso:", type="password")
    if senha == "1234":
        senha_correta = True
        st.empty()
    else:
        st.warning("Senha incorreta. Tente novamente.")

if senha_correta or page != "Consultar ponto":
    # Carrega os dados da planilha de funcionários
    df_funcionarios = load_funcionarios_data()

    # Carrega os dados da planilha de registro de ponto
    df_registro_ponto = load_registro_ponto_data()

    # Define o formato de data e hora
    data_hora_format = "%Y-%m-%d %H:%M:%S"

    if page == "Cadastrar Funcionário":
        senha = st.text_input("Digite a senha de acesso:", type="password")
        if senha == "1234":
            senha_correta = True
            st.empty()
        else:
            st.warning("Senha incorreta. Tente novamente.")

    if senha_correta or page != "Cadastrar Funcionário":
        # Carrega os dados da planilha de funcionários
        df_funcionarios = load_funcionarios_data()

        # Carrega os dados da planilha de registro de ponto
        df_registro_ponto = load_registro_ponto_data()

        # Define o formato de data e hora
        data_hora_format = "%Y-%m-%d %H:%M:%S"

    if page == "Página Inicial":
        st.info("Ontem foi embora. Amanhã ainda não veio. Temos somente hoje, comecemos! Qualquer ato de amor, por menor que seja, é um trabalho pela paz.")
        st.subheader("Controle de Ponto")

        # Mensagem de boas-vindas
        st.write("Bem-vindo ao sistema de controle de ponto da ZP CONTABILIDADE.")

        # Seção de Recados Importantes
        st.subheader("Recados Importantes")

        # Recado 1
        st.info("Lembrete: Os funcionários devem registrar sua entrada e saída todos os dias.")

        # Recado 2
        #st.warning("Dia da Reunião Mensal: A reunião mensal de equipe será realizada na próxima sexta-feira às 15h.")

        # Recado 3
        #st.error(
            #"Atualização de Política: A política de uso de dispositivos móveis foi atualizada. Leia-a em 'Políticas'.")

        # Rodapé
        st.write("© SevenTec - Bebedouro - Todos os direitos reservados.")

    elif page == "Registrar Entrada/Saída":
        st.write("Você está na página de registro de entrada/saída.")

        # Campo para inserir o código do funcionário
        codigo_funcionario = st.text_input("Digite o código do funcionário:")

        # Botão para limpar os dados e retornar à página "Registrar Entrada/Saída"
        if st.button("Limpar"):
            codigo_funcionario = ""

        if codigo_funcionario:
            funcionario = df_funcionarios[df_funcionarios['codigo_funcionario'] == int(codigo_funcionario)]

            if not funcionario.empty:
                # Mostrar os dados do funcionário
                st.write("Dados do funcionário:")
                st.write(f"Nome: {funcionario['nome'].values[0]}")
                st.write(f"Data Admissão: {funcionario['data_admissao'].dt.strftime('%d/%m/%Y').values[0]}")
                st.write(f"Setor: {funcionario['setor'].values[0]}")
                st.write(f"Função: {funcionario['funcao'].values[0]}")

                # Botão para confirmar o registro
                if st.button("Registrar Entrada"):
                    # Registra a hora de entrada atual
                    hora_entrada = datetime.now().strftime(data_hora_format)

                    # Cria um novo registro
                    novo_registro = pd.DataFrame({
                        'codigo': [int(codigo_funcionario)],
                        'nome': [funcionario['nome'].values[0]],
                        'data': [datetime.now().date()],
                        'hora_entrada': [hora_entrada],
                        'hora_saida': [None]
                    })

                    # Adiciona o novo registro à planilha de registro de ponto
                    df_registro_ponto = pd.concat([df_registro_ponto, novo_registro], ignore_index=True)
                    df_registro_ponto.to_excel('registroPonto.xlsx', index=False)

                    st.success(f"Entrada registrada para o funcionário {codigo_funcionario} às {hora_entrada}.")

                # Botão para registrar saída
                if st.button("Registrar Saída"):
                    # Registra a hora de saída atual
                    hora_saida = datetime.now().strftime(data_hora_format)

                    # Procura o índice do registro de entrada correspondente
                    index = df_registro_ponto[(df_registro_ponto['codigo'] == int(codigo_funcionario)) & (
                        df_registro_ponto['hora_saida'].isna())].index
                    if not index.empty:
                        # Atualiza a hora de saída no registro de entrada correspondente
                        df_registro_ponto.loc[index[-1], 'hora_saida'] = hora_saida
                        df_registro_ponto.to_excel('registroPonto.xlsx', index=False)
                        st.success(f"Saída registrada para o funcionário {codigo_funcionario} às {hora_saida}.")
                    else:
                        st.warning(
                            "Não foi possível encontrar um registro de entrada correspondente para este funcionário.")

            else:
                st.warning("Código de funcionário não encontrado.")


    elif page == "Consultar ponto":
        st.title("Consultar Ponto")
        st.write("Você está na página de consulta de ponto.")


        # Campo para inserir o mês desejado
        data_atual = datetime.now()
        mes_corrente = st.sidebar.selectbox("Selecione o mês:", range(1, 13), index=data_atual.month - 1)

        # Obtém a lista de usuários a partir dos dados da planilha de funcionários
        usuarios = df_funcionarios['nome'].unique()
        usuario_selecionado = st.sidebar.selectbox("Selecione o usuário:", usuarios)

        # Filtra os dados pelo mês e usuário selecionados
        dados_filtrados = df_registro_ponto[
            (df_registro_ponto['data'].dt.month == mes_corrente) & (df_registro_ponto['nome'] == usuario_selecionado)]
        if dados_filtrados.empty:
            st.warning(
                f"Nenhum registro de entrada/saída encontrado para o funcionário {usuario_selecionado} no mês {mes_corrente}.")

        else:
            # Exibe os dados filtrados
            st.write("Registros de ponto para o mês atual:")
            st.write(dados_filtrados)

            # Calcular o tempo decorrido entre entrada e saída
            dados_filtrados['tempo_decorrido'] = (
                    dados_filtrados['hora_saida'] - dados_filtrados['hora_entrada']).astype(str)

            # Exibe o tempo decorrido

            st.write("Tempo decorrido entre entrada e saída:")
            st.write(dados_filtrados[['hora_entrada', 'hora_saida', 'tempo_decorrido']])

            # Calcula o tempo total no mês corrente
            tempo_total = dados_filtrados['hora_saida'] - dados_filtrados['hora_entrada']
            tempo_total = tempo_total.sum()
            st.write(f"Tempo total no mês corrente para o usuário {usuario_selecionado}: {tempo_total}")


    elif page == "Cadastrar Funcionário":
        #senha = st.text_input("Digite a senha de acesso:", key="senha_cadastro")
        if senha == "1234":
            st.write("Você está na página de cadastro de funcionários.")

            # Formulário para cadastrar um novo funcionário
            codigo_funcionario = st.text_input("Código do Funcionário:", key="codigo_funcionario")
            nome = st.text_input("Nome:", key="nome_funcionario")
            data_admissao = st.text_input("Data de Admissão (dd/mm/aaaa):", key="data_admissao_funcionario")
            setor = st.text_input("Setor:", key="setor_funcionario")
            funcao = st.text_input("Função:", key="funcao_funcionario")

            # Botão para cadastrar o funcionário
            if st.button("Cadastrar", key="botao_cadastro"):
                if codigo_funcionario and nome and data_admissao and setor and funcao:
                    novo_funcionario = pd.DataFrame({
                        'codigo_funcionario': [codigo_funcionario],
                        'nome': [nome],
                        'data_admissao': [pd.to_datetime(data_admissao, format='%d/%m/%Y')],
                        'setor': [setor],
                        'funcao': [funcao]
                    })

                    # Carrega os dados existentes da planilha
                    df_funcionarios = load_funcionarios_data()
                    # Adiciona o novo funcionário aos dados existentes
                    df_funcionarios = pd.concat([df_funcionarios, novo_funcionario], ignore_index=True)
                    # Salva os dados atualizados na planilha funcionarios.xlsx
                    df_funcionarios.to_excel('funcionarios.xlsx', index=False)
                    st.success(f"Funcionário {nome} cadastrado com sucesso!")

                else:
                    st.warning("Por favor, preencha todos os campos.")
            # Exibir a tabela com os dados de todos os funcionários já cadastrados
            st.write("Funcionários cadastrados:")
            st.dataframe(df_funcionarios)

    else:
            st.info("Nenhum registro encontrado para o mês e usuário selecionados.")

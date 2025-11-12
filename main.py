from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
import pathlib
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    model="openai/gpt-oss-20b",
)

def bd_connect(path):
    """
    Verifica se o caminho do banco de dados existe.
    
    Args:
        path (str): Caminho para o arquivo do banco de dados
        
    Returns:
        pathlib.Path: Objeto Path do arquivo do banco
        
    Raises:
        FileNotFoundError: Se o caminho não existir
    """
    local_path = pathlib.Path(path)
    if local_path.exists():
        print(f"Conectado ao banco de dados em: {local_path}")
        return local_path
    else:
        raise FileNotFoundError(f"O caminho do banco de dados não foi encontrado: {local_path}")
    
def wrapper_bd(path):
    """
    Conecta ao banco de dados MySQL e retorna uma instância SQLDatabase.
    
    Args:
        path (str): Caminho de verificação do banco (usado para validação)
        
    Returns:
        SQLDatabase: Objeto de conexão com o banco de dados
    """
    # Conectar ao MySQL (banco 'empresa') usando pymysql
    bd_connect(path)
    data = SQLDatabase.from_uri("mysql+pymysql://root@localhost:3306/empresa")
    return data

def agent_sql_query():
    """
    Cria e configura um agente de IA para consultas SQL em linguagem natural.
    O agente interpreta perguntas em português e as converte em queries SQL,
    executando-as no banco de dados MySQL do ERP.
    Args:
        question (str): Pergunta em linguagem natural
    Returns:
        Agent: Agente configurado e pronto para processar consultas
    """

    db_info = wrapper_bd("c:/Users/asus/Documents/IA/projects/agent_bd/bd/empresa.db")

    toolkit = SQLDatabaseToolkit(db=db_info, llm=llm)

    tools = toolkit.get_tools()

    # for tool in tools:
    #     print(f"Nome da tool: {tool.name}")
    #     print(f"Descrição da tool: {tool.description}")
    #     print()


    system_prompt = """
    Você é um agente especializado em consultar banco de dados SQL de um ERP empresarial.
    Sua função é interpretar perguntas em português e fornecer respostas claras e objetivas.

    INSTRUÇÕES:
    1. Analise a pergunta do usuário em linguagem natural
    2. Examine as tabelas disponíveis no banco de dados
    3. Crie uma consulta SQL sintaticamente correta em {dialect}
    4. Execute a consulta e interprete os resultados
    5. SEMPRE responda em português de forma clara e amigável ao usuário

    REGRAS:
    - Limite suas consultas a no máximo {top_k} resultados
    - Ordene os resultados de forma relevante
    - Consulte apenas as colunas necessárias
    - Verifique a consulta duas vezes antes de executar
    - NÃO execute comandos DML (INSERT, UPDATE, DELETE, DROP)
    - SEMPRE forneça uma resposta final em linguagem natural ao usuário
    - Inclua valores monetários em formato brasileiro (R$ 1.000,00)

    IMPORTANTE: Após executar a consulta, SEMPRE forneça uma resposta final formatada
    e amigável ao usuário, não apenas mostre os dados brutos.
    """.format(dialect=toolkit.dialect, top_k=5)

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )

    while True:
        pergunta = input("\nDigite sua pergunta sobre o banco de dados (ou 'sair' para encerrar): \n")
        if pergunta.lower() == "sair":
            break
        for step in agent.stream(
            {"messages": [{"role": "user", "content": pergunta}]},
            stream_mode="values",
        ):
            step["messages"][-1].pretty_print()

if __name__=="__main__":
    agent_sql_query()
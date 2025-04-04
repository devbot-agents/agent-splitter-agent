from fastapi import APIRouter, HTTPException, Depends
from app.models.agent_model import InputModel, OutputModel, MicroagentSchema, Orchestrator, FlowStep
from typing import Dict, List, Any, Optional
import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Configurar logging
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Configurar o cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter(prefix="/api/v1", tags=["agent"])

def analyze_agent_complexity(input_data: InputModel) -> dict:
    """
    Analisa a complexidade do agente principal para determinar a melhor divisão.
    
    Args:
        input_data: Dados do agente principal
        
    Returns:
        Análise de complexidade e componentes potenciais
    """
    system_message = """Você é um especialista em análise de sistemas e arquitetura de microserviços.
    Sua tarefa é analisar a descrição e esquemas de um agente de IA e identificar componentes 
    lógicos que podem ser separados em microagentes independentes."""
    
    prompt = f"""
    # Análise de Complexidade do Agente

    ## Agente: {input_data.agent_name}
    
    ## Descrição:
    {input_data.agent_description}
    
    ## Schema de Entrada:
    ```json
    {input_data.input_schema}
    ```
    
    ## Schema de Saída:
    ```json
    {input_data.output_schema}
    ```
    
    ## Prompt do Agente (se disponível):
    {input_data.agent_prompt or "Não disponível"}
    
    # Tarefa:
    Analise este agente e identifique:
    1. Nível de complexidade geral (baixo, médio, alto)
    2. Componentes lógicos ou responsabilidades que podem ser separados
    3. Dependências entre esses componentes
    4. Fluxo de dados necessário entre componentes
    
    Retorne sua análise completa em formato JSON com esses quatro aspectos.
    """
    
    logger.info(f"Analisando complexidade do agente: {input_data.agent_name}")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        analysis = response.choices[0].message.content
        logger.info(f"Análise de complexidade concluída para o agente: {input_data.agent_name}")
        return analysis
        
    except Exception as e:
        logger.error(f"Erro ao analisar complexidade: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao analisar complexidade: {str(e)}")

def generate_microagents(input_data: InputModel, complexity_analysis: dict) -> List[MicroagentSchema]:
    """
    Gera a lista de microagentes com base na análise de complexidade.
    
    Args:
        input_data: Dados do agente principal
        complexity_analysis: Análise de complexidade do agente
        
    Returns:
        Lista de microagentes propostos
    """
    system_message = """Você é um especialista em design de agentes de IA e arquiteturas de microserviços.
    Sua tarefa é propor microagentes específicos com responsabilidades bem definidas para dividir
    um agente monolítico em componentes menores e mais gerenciáveis."""
    
    prompt = f"""
    # Geração de Microagentes
    
    ## Agente Principal: {input_data.agent_name}
    
    ## Descrição:
    {input_data.agent_description}
    
    ## Análise de Complexidade:
    {complexity_analysis}
    
    # Tarefa:
    Com base na análise de complexidade e na descrição do agente principal, defina uma lista 
    de microagentes. Para cada microagente, especifique:
    
    1. Nome (seguindo o padrão [função]-[contexto]-agent, usando kebab-case)
    2. Descrição clara da responsabilidade específica
    3. Schema de entrada (apenas os campos necessários para sua função)
    4. Schema de saída (o que este microagente produz)
    5. Dependências (nomes de outros microagentes dos quais este depende)
    
    Cada microagente deve ter uma única responsabilidade bem definida.
    Garanta que o conjunto de microagentes cubra toda a funcionalidade do agente principal.
    Retorne uma lista estruturada em formato JSON.
    """
    
    logger.info(f"Gerando propostas de microagentes para: {input_data.agent_name}")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        microagents_data = response.choices[0].message.content
        logger.info(f"Proposta de microagents concluída: {len(microagents_data)} microagentes definidos")
        return microagents_data
        
    except Exception as e:
        logger.error(f"Erro ao gerar microagentes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar microagentes: {str(e)}")

def generate_orchestrator(input_data: InputModel, microagents: List[MicroagentSchema]) -> Orchestrator:
    """
    Gera o orquestrador que coordena os microagentes.
    
    Args:
        input_data: Dados do agente principal
        microagents: Lista de microagentes propostos
        
    Returns:
        Definição do orquestrador
    """
    system_message = """Você é um especialista em orquestração de serviços e fluxos de trabalho.
    Sua tarefa é projetar um orquestrador que coordene a comunicação entre microagentes
    de forma eficiente, garantindo que o fluxo de dados seja adequado."""
    
    microagents_list = "\n".join([
        f"- {agent.name}: {agent.description}" 
        for agent in microagents
    ])
    
    prompt = f"""
    # Geração de Orquestrador
    
    ## Agente Principal: {input_data.agent_name}
    
    ## Descrição:
    {input_data.agent_description}
    
    ## Microagentes:
    {microagents_list}
    
    # Tarefa:
    Projete um orquestrador para coordenar a comunicação entre os microagentes listados.
    O orquestrador deve:
    
    1. Ter um nome adequado (seguindo o padrão orchestrate-[contexto]-agent)
    2. Ter uma descrição clara de seu papel
    3. Definir um fluxo de execução passo a passo (quais agentes são chamados em qual ordem)
    4. Incluir condições para etapas condicionais se necessário
    
    Retorne a definição do orquestrador em formato JSON.
    """
    
    logger.info(f"Gerando orquestrador para: {input_data.agent_name}")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        orchestrator_data = response.choices[0].message.content
        logger.info(f"Orquestrador gerado com sucesso para: {input_data.agent_name}")
        return orchestrator_data
        
    except Exception as e:
        logger.error(f"Erro ao gerar orquestrador: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar orquestrador: {str(e)}")

def generate_architecture_diagram(microagents: List[MicroagentSchema], orchestrator: Orchestrator) -> str:
    """
    Gera um diagrama de arquitetura em texto representando a relação entre os microagentes.
    
    Args:
        microagents: Lista de microagentes
        orchestrator: Definição do orquestrador
        
    Returns:
        Diagrama de arquitetura em texto
    """
    system_message = """Você é um especialista em criação de diagramas de arquitetura.
    Sua tarefa é criar um diagrama em ASCII art ou formato Mermaid que mostre claramente 
    a relação entre diferentes componentes de um sistema."""
    
    microagents_list = "\n".join([
        f"- {agent.name}: {agent.description}" 
        for agent in microagents
    ])
    
    dependencies = "\n".join([
        f"- {agent.name} depende de: {', '.join(agent.dependencies) if agent.dependencies else 'nenhum'}"
        for agent in microagents
    ])
    
    flow_steps = "\n".join([
        f"- Passo {step.step}: {step.agent} {f'(SE {step.condition})' if step.condition else ''}"
        for step in orchestrator.flow
    ])
    
    prompt = f"""
    # Criação de Diagrama de Arquitetura
    
    ## Microagentes:
    {microagents_list}
    
    ## Dependências:
    {dependencies}
    
    ## Fluxo de Orquestração:
    {flow_steps}
    
    # Tarefa:
    Crie um diagrama de arquitetura em formato Mermaid ou ASCII art que represente visualmente:
    
    1. Todos os microagentes como nós
    2. O orquestrador como nó central
    3. As relações de dependência entre os microagentes
    4. O fluxo de execução coordenado pelo orquestrador
    
    Se possível, organize os componentes de forma lógica, agrupando os relacionados.
    Para diagramas Mermaid, use a sintaxe de flowchart ou graph.
    """
    
    logger.info("Gerando diagrama de arquitetura")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        diagram = response.choices[0].message.content
        logger.info("Diagrama de arquitetura gerado com sucesso")
        return diagram
        
    except Exception as e:
        logger.error(f"Erro ao gerar diagrama de arquitetura: {str(e)}")
        # Retornamos None em vez de lançar exceção, pois o diagrama é opcional
        return None

@router.post("/execute", response_model=OutputModel)
async def execute(input_data: InputModel):
    """
    Endpoint principal para execução do agente splitter.
    Divide um agente principal em microagentes com responsabilidades específicas.
    """
    try:
        logger.info(f"Iniciando divisão do agente: {input_data.agent_name}")
        
        # Passo 1: Analisar a complexidade do agente
        complexity_analysis = analyze_agent_complexity(input_data)
        
        # Passo 2: Gerar propostas de microagentes
        microagents = generate_microagents(input_data, complexity_analysis)
        
        # Passo 3: Definir o orquestrador
        orchestrator = generate_orchestrator(input_data, microagents)
        
        # Passo 4: Gerar diagrama de arquitetura
        architecture_diagram = generate_architecture_diagram(microagents, orchestrator)
        
        # Passo 5: Compor a resposta final
        result = OutputModel(
            microagents=microagents,
            orchestrator=orchestrator,
            architecture_diagram=architecture_diagram
        )
        
        logger.info(f"Divisão concluída para o agente: {input_data.agent_name}")
        return result
        
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """
    Endpoint para verificar a saúde do serviço.
    """
    return {"status": "healthy"} 
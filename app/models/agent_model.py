from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

# Modelos para microagentes
class MicroagentSchema(BaseModel):
    name: str = Field(..., description="Nome do microagente")
    description: str = Field(..., description="Descrição da responsabilidade específica do microagente")
    input_schema: Dict[str, Any] = Field(..., description="Schema de entrada esperado pelo microagente")
    output_schema: Dict[str, Any] = Field(..., description="Schema de saída fornecido pelo microagente")
    dependencies: List[str] = Field(default_factory=list, description="Nomes dos microagentes dos quais este depende")

# Modelo para orquestrador
class FlowStep(BaseModel):
    step: int = Field(..., description="Número da etapa no fluxo")
    agent: str = Field(..., description="Nome do microagente a ser chamado nesta etapa")
    condition: Optional[str] = Field(None, description="Condição opcional para executar esta etapa")

class Orchestrator(BaseModel):
    name: str = Field(..., description="Nome do agente orquestrador")
    description: str = Field(..., description="Descrição da função do orquestrador")
    flow: List[FlowStep] = Field(..., description="Fluxo de execução dos microagentes")

# Modelo de entrada do agente
class InputModel(BaseModel):
    agent_name: str = Field(..., description="Nome do agente principal a ser dividido")
    agent_description: str = Field(..., description="Descrição completa do agente principal a ser dividido")
    input_schema: Dict[str, Any] = Field(..., description="Schema de entrada do agente principal")
    output_schema: Dict[str, Any] = Field(..., description="Schema de saída do agente principal")
    agent_prompt: Optional[str] = Field(None, description="Prompt detalhado do agente principal, se disponível")

# Modelo de saída do agente
class OutputModel(BaseModel):
    microagents: List[MicroagentSchema] = Field(..., description="Lista de microagentes que compõem o agente principal")
    orchestrator: Orchestrator = Field(..., description="Definição do agente orquestrador que coordena os microagentes")
    architecture_diagram: Optional[str] = Field(None, description="Diagrama de arquitetura em formato de texto representando a relação entre os microagentes") 
# Agent Splitter Agent

Uma solução para dividir um agente monolítico em microagentes com responsabilidades específicas, coordenados por um orquestrador.

## Visão Geral

O Agent Splitter Agent analisa agentes complexos e propõe uma divisão em componentes menores. Este enfoque traz diversas vantagens:

- **Redução no uso de tokens**: Cada microagente pode usar modelos menores e mais econômicos
- **Maior precisão**: Responsabilidades específicas levam a resultados mais precisos
- **Melhor manutenção**: Componentes pequenos e focados são mais fáceis de manter
- **Testes simplificados**: Unidades menores são mais fáceis de testar
- **Reusabilidade**: Microagentes podem ser compartilhados entre diferentes projetos

## Funcionalidades

- **Análise de Complexidade**: Avalia a complexidade do agente e identifica componentes lógicos
- **Geração de Microagentes**: Propõe microagentes com responsabilidades específicas
- **Design de Orquestrador**: Cria um orquestrador para coordenar os microagentes
- **Diagramas de Arquitetura**: Gera diagramas visuais mostrando a interação entre componentes

## Uso

```bash
# Instalação
pip install -r requirements.txt

# Execução
uvicorn app.main:app --reload
```

### Endpoint API

```
POST /api/v1/execute
```

### Modelo de Entrada

```json
{
  "agent_name": "nome-do-agente",
  "agent_description": "Descrição detalhada do agente a ser dividido",
  "input_schema": {
    "type": "object",
    "properties": {
      // Schema de entrada do agente original
    }
  },
  "output_schema": {
    "type": "object",
    "properties": {
      // Schema de saída do agente original
    }
  },
  "agent_prompt": "Prompt detalhado do agente original (opcional)"
}
```

### Modelo de Saída

```json
{
  "microagents": [
    {
      "name": "nome-do-microagente-1",
      "description": "Responsabilidade específica",
      "input_schema": { /* ... */ },
      "output_schema": { /* ... */ },
      "dependencies": []
    },
    // mais microagentes...
  ],
  "orchestrator": {
    "name": "orchestrate-contexto-agent",
    "description": "Coordena os microagentes",
    "flow": [
      {
        "step": 1,
        "agent": "nome-do-microagente-1",
        "condition": null
      },
      // mais passos...
    ]
  },
  "architecture_diagram": "Diagrama visual em formato Mermaid ou ASCII art"
}
```

## Exemplo de Uso

Considere um agente que calcula probabilidades de poker e recomenda ações. O `agent-splitter-agent` pode dividi-lo em microagentes como:

1. `calculate-hand-equity-agent`: Calcula probabilidade de vitória
2. `calculate-pot-odds-agent`: Calcula odds do pote 
3. `calculate-expected-value-agent`: Calcula valor esperado
4. `generate-recommendation-agent`: Gera recomendação com base nos valores calculados

Com um orquestrador `orchestrate-poker-decision-agent` coordenando o fluxo entre eles.

## Documentação da API

Após iniciar o servidor, acesse a documentação em:
http://localhost:8000/docs 
# ⏱️ Timesheet Processor

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-containerized-2496ED?style=flat&logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/status-validado%20✓-28a745?style=flat)

Aplicação containerizada que processa registros de timesheet a partir de um arquivo `data.json`, aplica regras de negócio e gera um resumo analítico em `result.json`.

Desenvolvida como desafio técnico com foco em **manipulação de dados**, **implementação de regras de negócio**, **tratamento de entradas inválidas** e **saída determinística**.

---

## ✨ Funcionalidades

| # | Funcionalidade | Detalhe |
|---|---|---|
| 1 | Filtragem de inválidos | Ignora registros com `minutes <= 0` e contabiliza o total descartado |
| 2 | Total por tarefa | Agrupa por `taskId` e soma os minutos |
| 3 | Tarefa mais trabalhada | Identifica a tarefa com maior total de minutos |
| 4 | Percentual por tarefa | Calcula a participação de cada tarefa sobre o total geral |
| 5 | Top 3 tarefas | Retorna as 3 tarefas com maior tempo, com percentual formatado |
| 6 | Top 3 funcionários | Ranking dos 3 usuários com maior total de minutos |
| 7 | Maior variedade de tarefas | Usuário com mais tarefas distintas trabalhadas |

---

## ⚙️ Como executar

> Requisito: [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução.

```bash
docker compose up --build
```

O arquivo `result.json` será gerado automaticamente na raiz do projeto ao final da execução.

✅ Nenhum passo manual adicional é necessário.

---

## 📁 Estrutura do projeto

```
.
├── data.json          # Dataset de entrada (300 registros)
├── process.py         # Script principal com toda a lógica de negócio
├── Dockerfile         # Definição da imagem Docker
├── docker-compose.yml # Orquestração do container e volume de saída
├── .gitignore         # Ignora o result.json gerado
└── README.md
```

---

## 📤 Exemplo de saída

Após a execução, o `result.json` gerado segue esta estrutura:

```json
{
  "totalMinutes": 28408,
  "tasks": [
    { "taskId": 103, "taskName": "Ajustar layout", "totalMinutes": 4047, "percentage": "14.25%" },
    { "taskId": 110, "taskName": "Criar endpoint relatório", "totalMinutes": 3500, "percentage": "12.32%" },
    ...
  ],
  "mostWorkedTask": {
    "taskId": 103, "taskName": "Ajustar layout", "totalMinutes": 4047, "percentage": "14.25%"
  },
  "top3TasksPercentage": [
    { "taskId": 103, "taskName": "Ajustar layout", "percentage": "14.25%" },
    { "taskId": 110, "taskName": "Criar endpoint relatório", "percentage": "12.32%" },
    { "taskId": 106, "taskName": "Criar testes unitários", "percentage": "10.74%" }
  ],
  "top3Employees": [
    { "userId": 5, "userName": "Eduardo", "totalMinutes": 4303 },
    { "userId": 1, "userName": "Ana", "totalMinutes": 4077 },
    { "userId": 3, "userName": "Carla", "totalMinutes": 3842 }
  ],
  "mostDistinctUserOnTasks": {
    "userId": 1, "userName": "Ana", "distinctTasks": 10,
    "taskIds": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
  },
  "ignoredRecords": 41
}
```

---

## 🧠 Decisão técnica — Por que Python?

A vaga é para desenvolvimento **JavaScript/TypeScript** — e essa é a stack que seria adotada em um ambiente de produção real. No entanto, para o escopo desta atividade, Python foi escolhido por razões objetivas:

**1. Zero dependências externas**
Toda a lógica foi implementada com stdlib nativa (`json`, `collections`, `pathlib`). Não há `npm install`, `package.json` ou etapa de build — o Dockerfile tem apenas 5 linhas.

**2. Container mais enxuto**
`python:3.12-slim` vs uma imagem Node com TypeScript exige transpilação (`tsc`) ou um runner como `ts-node`, adicionando camadas desnecessárias para uma CLI simples.

**3. Concisão na manipulação de dados**
Operações como `sorted()` com múltiplos critérios, `set()` para unicidade e `dict` para agrupamento são idiomáticas em Python — o código fica próximo da lógica de negócio, sem boilerplate.

---

### Como ficaria em TypeScript

```typescript
// Filtragem
const valid = records.filter(r => r.minutes > 0);

// Agrupamento por tarefa
const taskMap = new Map<number, { taskId: number; taskName: string; totalMinutes: number }>();
for (const r of valid) {
  const entry = taskMap.get(r.taskId) ?? { taskId: r.taskId, taskName: r.taskName, totalMinutes: 0 };
  entry.totalMinutes += r.minutes;
  taskMap.set(r.taskId, entry);
}

// Ordenação: totalMinutes desc, taskId asc em empate
const sorted = [...taskMap.values()].sort(
  (a, b) => b.totalMinutes - a.totalMinutes || a.taskId - b.taskId
);

// Persistência
import fs from "fs";
fs.writeFileSync("result.json", JSON.stringify(result, null, 2));
```

A lógica é equivalente (a escolha foi pragmática para o contexto, não por desconhecimento da stack).

---

## 🔒 Determinismo

A saída é **sempre idêntica** para a mesma entrada. Isso é garantido pelas regras de ordenação aplicadas em todos os agrupamentos:

- **Tarefas:** `totalMinutes DESC` → `taskId ASC` em empate
- **Funcionários:** `totalMinutes DESC` → `userId ASC` em empate
- **Tarefas distintas:** `distinctTasks DESC` → `userId ASC` em empate

---

## ✅ Validação

O `result.json` gerado foi comparado com o gabarito (`output.json`) e apresenta **equivalência estrutural e numérica completa** em todos os campos.
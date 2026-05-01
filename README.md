# ⏱️ Timesheet Processor

Aplicação containerizada responsável por processar registros de timesheet a partir de um arquivo `data.json`, aplicando regras de negócio e gerando um resumo analítico em `result.json`.

O projeto foi desenvolvido com foco em manipulação de dados, consistência de saída e execução determinística, conforme os requisitos do desafio técnico.

---

## ✨ Funcionalidades

A partir de um conjunto de registros de tempo, a aplicação:

- Filtra entradas inválidas (`minutes <= 0`)
- Agrupa dados por tarefa (`taskId`)
- Calcula o tempo total trabalhado
- Identifica a tarefa mais trabalhada
- Calcula o percentual de cada tarefa sobre o total
- Retorna o Top 3 tarefas e Top 3 funcionários
- Identifica o usuário com maior número de tarefas distintas
- Garante ordenação determinística conforme regras definidas

---

## ⚙️ Como executar

```bash
docker compose up --build
```

Após a execução, o arquivo `result.json` será gerado automaticamente na raiz do projeto.

✅ Nenhum passo manual adicional é necessário.

---

## 🧱 Estrutura do projeto

```
.
├── data.json
├── process.py
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 🧠 Decisão técnica

A aplicação foi implementada em Python por oferecer stdlib nativa para manipulação de JSON e dados (`json`, `collections`, `pathlib`), sem necessidade de dependências externas ou etapa de build — resultando em um container mais simples e um Dockerfile com apenas 5 linhas.

Em um ambiente alinhado à stack da empresa, TypeScript seria adotado para manter consistência tecnológica.

---

## ✅ Validação

O resultado gerado foi validado com base no arquivo de referência (`output.json`), garantindo equivalência estrutural e numérica, conforme exigido no desafio.

---

## 🔒 Determinismo

A aplicação garante saída determinística, assegurando que a mesma entrada sempre produzirá o mesmo resultado, respeitando rigorosamente as regras de ordenação especificadas.
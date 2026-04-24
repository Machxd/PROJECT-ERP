# ERP Analytics

Sistema de gestão de inventário para produtos perecíveis, com controle de validade, registro de movimentações (entradas, saídas e desperdícios) e dashboard analítico. Desenvolvido com Python puro (http.server + SQLite3) no back-end e HTML/CSS/JS com estética Glassmorphism e gráficos Chart.js no front-end, sem dependências externas.

## Como Rodar

1. Clone o repositório
2. Execute `python servidor.py`
3. Acesse `http://localhost:8080`
4. Login: `admin / admin123` ou `operador / op2024`

## Estrutura do Projeto

```
ERP_ANALYTICS/
├── database.py                     # Criação e estrutura das tabelas SQL
├── operacoes.py                    # Lógica de negócio (CRUD e Movimentações)
├── servidor.py                     # API HTTP com autenticação
├── login.html                      # Tela de login
├── index.html                      # Interface principal (SPA)
├── dados_exemplo.csv               # Arquivo CSV de exemplo para importação
├── relatorio_dados_estruturados.md # Relatório técnico do projeto
└── inventario.db                   # Banco de dados SQLite (gerado automaticamente)
```

## Funcionalidades

- CRUD completo de produtos (cadastro, edição, exclusão)
- Controle de validade com classificação automática (Válido, Alerta, Vencido)
- Registro de movimentações (Entrada, Saída, Desperdício)
- Dashboard analítico com 3 gráficos (Saúde do Estoque, Volume por Categoria, Fluxo de Movimentações)
- Importação de produtos via arquivo CSV
- Pesquisa em tempo real por nome, categoria e lote
- Filtro por mês de entrada
- Histórico completo de movimentações
- Sistema de login com sessão
- Tema claro e escuro

## Importação de Dados

O sistema aceita arquivos `.csv` com o seguinte formato:

```
Nome,Categoria,Lote,Quantidade,Validade,Entrada
Iogurte Grego,Laticínios,L-001/MAR,25,2026-04-15,2026-03-20
Arroz Integral 5kg,Mercearia,L-002/FEV,10,2027-10-01,2026-02-15
```

Um arquivo de exemplo (`dados_exemplo.csv`) está incluído no repositório.

## Tecnologias

- **Back-end:** Python 3 (http.server nativo)
- **Banco de Dados:** SQLite3
- **Front-end:** HTML5, CSS3, JavaScript Vanilla
- **Gráficos:** Chart.js
- **Ícones:** Lucide Icons

## Documentação

O relatório técnico com a análise de dados estruturados, variáveis do projeto e controle de fluxo está disponível no arquivo `relatorio_dados_estruturados.md`.
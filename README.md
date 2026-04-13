# 🏗️ Espaço Guto — Infraestrutura & DevOps

> Repositório central de infraestrutura para todos os projetos do espaço Guto na VPS Contabo.

---

## 📁 Estrutura do Repositório

```
ambiente_guto/
├── templates/
│   ├── docker-compose.template.yml   ← Template Docker reutilizável
│   ├── .env.template                 ← Template de variáveis de ambiente
│   └── deploy.yml                    ← Workflow GitHub Actions reutilizável
├── monitoring_Guto/
│   ├── docker-compose.yml            ← Stack: Prometheus + Grafana + exporters
│   ├── prometheus.yml                ← Config de scraping
│   └── .env.example                  ← Exemplo de credenciais (NÃO commitar .env)
├── scripts/
│   └── setup_new_project.sh          ← Setup automático de novos projetos na VPS
├── .gitignore
├── CHECKLIST_OPERACIONAL.md          ← Guia de comandos do dia a dia
└── README.md
```

---

## 🗺️ Espaço na VPS

```
/apps/Guto/
├── projeto_agendamento/    → porta 8000 ✅
├── agente_nutricionista/   → porta 8001
├── buscador_vagas/         → porta 8002
└── _templates/             → scripts de setup

/monitoring_Guto/           → Grafana :3000 | Prometheus :9090
```

---

## ⚡ Regra de Ouro

| Por Projeto        | Valor             |
|--------------------|-------------------|
| 1 repositório      | 1 pasta           |
| 1 repositório      | 1 `docker-compose`|
| 1 repositório      | 1 `.env`          |
| 1 repositório      | 1 porta única     |
| 1 repositório      | 1 pipeline CI/CD  |

---

## 🚀 Início Rápido

### Novo projeto
```bash
# Na VPS
bash /apps/Guto/_templates/setup_new_project.sh
```

### Subindo monitoramento
```bash
cd /monitoring_Guto
cp .env.example .env && nano .env
docker compose up -d
```

### Consultando guia completo
Ver [CHECKLIST_OPERACIONAL.md](./CHECKLIST_OPERACIONAL.md)

---

## 🔒 Segurança

- Credenciais **NUNCA** vão para o GitHub — use `.env` local na VPS
- GitHub Actions usa **SSH Key + Secrets** (sem senha hardcoded)
- Todos os containers usam prefixo `guto_` para isolamento
- Nenhum arquivo toca em projetos fora de `/apps/Guto`

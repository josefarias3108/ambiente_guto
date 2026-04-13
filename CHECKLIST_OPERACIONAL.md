# 📋 Checklist Operacional — Espaço Guto na VPS

> **Regra de Ouro:** 1 repo = 1 pasta = 1 docker-compose = 1 .env = 1 porta = 1 pipeline

---

## 🗺️ Mapa de Portas

| Projeto                | Porta | Status     |
|------------------------|-------|------------|
| `projeto_agendamento`  | 8000  | ✅ Ativo    |
| `agente_nutricionista` | 8001  | 🔲 Pendente |
| `buscador_vagas`       | 8002  | 🔲 Pendente |
| _(reserva)_            | 8003  | —          |
| _(reserva)_            | 8004  | —          |
| Grafana (monitoring)   | 3000  | 🔲 Pendente |
| Prometheus             | 9090  | 🔲 Pendente |
| node_exporter          | 9100  | 🔲 Pendente |
| cAdvisor               | 9200  | 🔲 Pendente |

---

## 🆕 Subir Projeto Existente do GitHub

```bash
# 1. Acesse a VPS
ssh guto@<VPS_IP>

# 2. Rode o script de setup
bash /apps/Guto/_templates/setup_new_project.sh
# (ele vai perguntar nome do repo, URL e porta)

# 3. Edite o .env com suas credenciais
nano /apps/Guto/<REPO_NAME>/.env

# 4. Suba o container
cd /apps/Guto/<REPO_NAME>
docker compose up -d --build

# 5. Verifique
docker compose ps
docker compose logs -f
```

---

## 🌱 Subir Projeto Novo (Futuro)

```bash
# 1. Crie o repositório no GitHub (local → push)
git init
git remote add origin https://github.com/josefarias3108/<REPO_NAME>.git
git push -u origin main

# 2. Adicione o Workflow de Deploy ao repositório
mkdir -p .github/workflows
cp /caminho/do/template/deploy.yml .github/workflows/deploy.yml
git add . && git commit -m "ci: add deploy workflow" && git push

# 3. Configure os GitHub Secrets no repositório:
#    → GitHub > Settings > Secrets and variables > Actions
#    VPS_HOST     = IP da VPS
#    VPS_USER     = guto
#    VPS_SSH_KEY  = (conteúdo da chave privada SSH)
#    VPS_PORT     = 22
#    APP_PORT     = (próxima porta disponível no mapa acima)

# 4. Na VPS, rode o setup:
bash /apps/Guto/_templates/setup_new_project.sh

# 5. A partir daí: todo push na main faz deploy automático ✅
```

---

## 🔄 Atualizar Projeto (Manual)

```bash
cd /apps/Guto/<REPO_NAME>
git pull
docker compose up -d --build
docker image prune -f
```

---

## ⏹️ Parar Projeto

```bash
cd /apps/Guto/<REPO_NAME>
docker compose down
```

---

## 📜 Ver Logs

```bash
# Últimas 100 linhas
cd /apps/Guto/<REPO_NAME>
docker compose logs --tail=100

# Logs em tempo real (streaming)
docker compose logs -f

# Logs de um container específico
docker logs guto_<REPO_NAME> -f
```

---

## 🗑️ Remover Projeto (CUIDADO)

```bash
cd /apps/Guto/<REPO_NAME>

# Para e remove containers + networks
docker compose down --volumes --remove-orphans

# Remove os arquivos (IRREVERSÍVEL)
rm -rf /apps/Guto/<REPO_NAME>

# Atualizar o registro de portas
nano /apps/Guto/_port_registry.txt
```

---

## 📊 Subir Stack de Monitoramento

```bash
# Primeira vez
cd /monitoring_Guto
cp .env.example .env
nano .env  # Troque a senha do Grafana!
docker compose up -d

# Acesse: http://<VPS_IP>:3000 (Grafana)
# Login: admin / senha_que_você_definiu

# Atualizar monitoramento
cd /monitoring_Guto
docker compose pull
docker compose up -d
```

---

## 🔧 Comandos Rápidos do Dia a Dia

```bash
# Ver todos os containers Guto rodando
docker ps --filter "label=guto.managed=true"

# Ver todos os containers (todos os usuários)
docker ps -a

# Ver uso de recursos
docker stats

# Ver registro de portas
cat /apps/Guto/_port_registry.txt

# Ver logs de todos projetos Guto simultaneamente
for dir in /apps/Guto/*/; do
  echo "=== $(basename $dir) ==="
  cd "$dir" && docker compose logs --tail=5 2>/dev/null
done
```

---

## 🔑 Gerar Chave SSH para GitHub Actions

```bash
# Na sua máquina LOCAL (Windows PowerShell):
ssh-keygen -t rsa -b 4096 -C "github-actions-guto" -f guto_deploy_key

# Copie a chave PÚBLICA para a VPS:
# cat guto_deploy_key.pub → adicione em ~/.ssh/authorized_keys na VPS

# Copie a chave PRIVADA para o GitHub Secret:
# cat guto_deploy_key → cole em VPS_SSH_KEY no GitHub Secrets de cada repo
```

---

*Última atualização: Abril/2026*

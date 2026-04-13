#!/bin/bash
# ============================================================
# SCRIPT: setup_new_project.sh
# Espaço Guto — VPS Contabo
# ============================================================
# EXECUÇÃO: Rode este script NA VPS como usuário guto:
#   bash /apps/Guto/_templates/setup_new_project.sh
#
# O script vai perguntar o nome do repo e a porta.
# ============================================================

set -e

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   🚀 Setup de Novo Projeto — Espaço Guto ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# === 1. ENTRADA DE DADOS ===
read -p "📌 Nome do repositório GitHub (ex: agente_nutricionista): " REPO_NAME
read -p "🌐 URL do repositório (ex: https://github.com/josefarias3108/agente_nutricionista.git): " REPO_URL
read -p "🔌 Porta da aplicação (ex: 8001): " APP_PORT

APP_DIR="/apps/Guto/${REPO_NAME}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📁 Diretório alvo : ${APP_DIR}"
echo "🔗 Repositório    : ${REPO_URL}"
echo "🔌 Porta          : ${APP_PORT}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# === 2. VERIFICAÇÕES DE SEGURANÇA ===

# Verificar se porta 8000 não está sendo reutilizada
if [ "${APP_PORT}" == "8000" ] && [ "${REPO_NAME}" != "projeto_agendamento" ]; then
  echo "❌ ERRO: Porta 8000 é reservada para projeto_agendamento!"
  exit 1
fi

# Verificar se diretório já existe
if [ -d "${APP_DIR}" ]; then
  echo "⚠️  Diretório ${APP_DIR} já existe."
  read -p "Deseja continuar mesmo assim? (s/N): " CONFIRM
  if [ "$CONFIRM" != "s" ] && [ "$CONFIRM" != "S" ]; then
    echo "Operação cancelada."
    exit 0
  fi
fi

# === 3. CRIAR DIRETÓRIO E CLONAR ===
echo "📂 Criando diretório..."
mkdir -p "${APP_DIR}"

echo "📥 Clonando repositório..."
git clone "${REPO_URL}" "${APP_DIR}" 2>/dev/null || (
  echo "   Repositório já clonado, atualizando..."
  cd "${APP_DIR}" && git pull
)

# === 4. CRIAR .env INICIAL ===
if [ ! -f "${APP_DIR}/.env" ]; then
  echo "📝 Criando .env inicial..."
  cat > "${APP_DIR}/.env" << EOF
# === GERADO AUTOMATICAMENTE — PREENCHA OS VALORES ===
APP_NAME=${REPO_NAME}
APP_ENV=production
APP_PORT=${APP_PORT}
LOG_LEVEL=INFO
DEBUG=false
TZ=America/Sao_Paulo

# Adicione aqui as variáveis específicas deste projeto:
EOF
  echo "⚠️  IMPORTANTE: Edite o arquivo ${APP_DIR}/.env com suas credenciais!"
else
  echo "ℹ️  .env já existe, mantendo."
fi

# === 5. LOG DO REGISTRO ===
LOG_FILE="/apps/Guto/_port_registry.txt"
echo "${APP_PORT} | ${REPO_NAME} | ${REPO_URL} | $(date '+%Y-%m-%d %H:%M:%S')" >> "${LOG_FILE}"

echo ""
echo "✅ PROJETO CONFIGURADO COM SUCESSO!"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo "   1. Edite o .env: nano ${APP_DIR}/.env"
echo "   2. Certifique-se que há um Dockerfile no repo"
echo "   3. Suba o projeto: cd ${APP_DIR} && docker compose up -d --build"
echo "   4. Verifique: docker compose ps"
echo ""

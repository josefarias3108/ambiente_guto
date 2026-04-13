# -*- coding: utf-8 -*-
"""
Script: setup_deploy_keys.py
- Conecta VPS via paramiko
- Gera par de chaves RSA 4096 na VPS
- Instala chave publica no authorized_keys
- Salva chave privada localmente para usar no GitHub Secrets
Credenciais lidas de variaveis de ambiente.
"""
import sys
import os
import time

# Forcar UTF-8 no stdout do Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import paramiko

# === CREDENCIAIS (lidas do ambiente) ===
HOST = os.environ.get("VPS_HOST", "194.147.58.150")
USER = os.environ.get("VPS_USER", "guto")
PASS = os.environ.get("VPS_PASS", "Aurora@22")
PORT = int(os.environ.get("VPS_PORT", "22"))

KEY_NAME       = "guto_deploy_key"
REMOTE_KEY_DIR = f"/home/{USER}/.ssh"
LOCAL_SAVE_DIR = os.path.expanduser(r"~\.ssh")


def run(ssh, cmd, wait=2):
    print(f"  >> {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    time.sleep(wait)
    out = stdout.read().decode("utf-8", errors="replace").strip()
    err = stderr.read().decode("utf-8", errors="replace").strip()
    if out:
        print(f"     {out}")
    if err:
        print(f"     [WARN] {err}")
    return out


def main():
    print("\n=== Setup de Chave SSH - Espaco Guto ===\n")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"[*] Conectando em {HOST}:{PORT} como {USER}...")
    ssh.connect(HOST, PORT, USER, PASS, timeout=15)
    print("[OK] Conectado!\n")

    # 1. Garantir .ssh existe na VPS
    print("[*] Verificando ~/.ssh na VPS...")
    run(ssh, f"mkdir -p {REMOTE_KEY_DIR} && chmod 700 {REMOTE_KEY_DIR}")

    # 2. Gerar par de chaves RSA 4096 na VPS (sem passphrase)
    priv_path = f"{REMOTE_KEY_DIR}/{KEY_NAME}"
    pub_path  = f"{priv_path}.pub"

    print("\n[*] Gerando par de chaves RSA 4096 na VPS...")
    # Remove chave antiga se existir para evitar conflito
    run(ssh, f"rm -f {priv_path} {pub_path}")
    run(ssh, f"ssh-keygen -t rsa -b 4096 -C 'github-actions-guto-deploy' -f {priv_path} -N '' -q", wait=4)
    print("[OK] Chaves geradas!")

    # 3. Instalar chave publica no authorized_keys
    print("\n[*] Instalando chave publica no authorized_keys...")
    run(ssh, f"cat {pub_path} >> {REMOTE_KEY_DIR}/authorized_keys")
    run(ssh, f"chmod 600 {REMOTE_KEY_DIR}/authorized_keys")
    # Remove duplicatas
    run(ssh, f"sort -u {REMOTE_KEY_DIR}/authorized_keys -o {REMOTE_KEY_DIR}/authorized_keys")
    print("[OK] Chave publica instalada!")

    # 4. Baixar chaves da VPS para maquina local
    print("\n[*] Baixando chaves da VPS para maquina local...")
    sftp = ssh.open_sftp()
    os.makedirs(LOCAL_SAVE_DIR, exist_ok=True)

    local_priv_path = os.path.join(LOCAL_SAVE_DIR, KEY_NAME)
    local_pub_path  = os.path.join(LOCAL_SAVE_DIR, f"{KEY_NAME}.pub")

    sftp.get(priv_path, local_priv_path)
    sftp.get(pub_path,  local_pub_path)
    sftp.close()

    # Permissao correta na chave privada local
    os.chmod(local_priv_path, 0o600)
    print(f"[OK] Salvas localmente!")

    # 5. Ler chave publica para exibir
    with open(local_pub_path, "r", encoding="utf-8") as f:
        pub_key = f.read().strip()

    print("\n" + "="*60)
    print("[OK] CHAVES GERADAS E INSTALADAS COM SUCESSO!")
    print("="*60)
    print(f"\n  Chave Privada : {local_priv_path}")
    print(f"  Chave Publica : {local_pub_path}")
    print(f"\n[CHAVE PUBLICA - ja instalada no authorized_keys da VPS]:")
    print(pub_key)
    print("\n" + "="*60)
    print("[PROXIMO PASSO - GitHub Secrets]")
    print("Vá em: GitHub repo > Settings > Secrets > Actions")
    print("Crie o secret: VPS_SSH_KEY")
    print("Cole o conteudo do arquivo:")
    print(f"  {local_priv_path}")
    print("="*60 + "\n")

    ssh.close()
    print("[OK] Conexao encerrada.")


if __name__ == "__main__":
    main()

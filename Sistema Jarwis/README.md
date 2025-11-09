 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/Sistema Jarwis/README.md b/Sistema Jarwis/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..2134428b3b31278c52db51a7afd6830e6a80cfb9
--- /dev/null
+++ b/Sistema Jarwis/README.md	
@@ -0,0 +1,35 @@
+# Sistema Jarwis (Compatibilidade Termux)
+
+Este diretório existe apenas para ajudar quem baixou o projeto em formato ZIP
+pelo celular e acabou dentro de uma pasta chamada `Sistema Jarwis` sem ver os
+arquivos principais do assistente.
+
+Os fontes verdadeiros ficam **um nível acima**, no diretório pai `Jarwis/`. Lá é
+que estão `main.py`, `jarwis/`, `scripts/` e os arquivos `requirements*.txt`.
+
+## Como usar a partir desta pasta
+
+Se você está no Termux e chegou até aqui com:
+
+```bash
+cd ~/Jarwis/Sistema\ Jarwis
+```
+
+basta executar os comandos adicionando `..` para acessar o diretório pai:
+
+```bash
+# Instalar dependências
+default_backend=".."
+pip install -r "$default_backend/requirements.txt"
+
+# Executar o assistente
+default_main="$default_backend/main.py"
+python "$default_main" --audio-backend termux --chunk-duration 1.5
+```
+
+> Dica: use `cd ..` para retornar ao diretório correto (`~/Jarwis`) e seguir as
+> instruções principais da documentação.
+
+Este diretório também fornece arquivos auxiliares para que os comandos funcionem
+mesmo que você permaneça aqui, mas recomendamos trabalhar sempre no diretório
+raiz do projeto.
 
EOF
)

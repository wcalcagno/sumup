#!/usr/bin/env bash
# Reemplaza el arbol de wcalcagno/sumup por este, limpio.
# Ejecutar DENTRO de esta carpeta. Requiere estar autenticado en GitHub.
set -e
git init -q 2>/dev/null || true
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/wcalcagno/sumup.git
git add -A
git commit -q -m "Estructura limpia del taller, sin solucionario"
git branch -M main
git push --force origin main
echo "Listo. Verifica en incognito: https://github.com/wcalcagno/sumup/archive/refs/heads/main.zip"

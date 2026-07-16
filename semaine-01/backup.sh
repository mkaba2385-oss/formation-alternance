#!/bin/bash
if [ -z "$1" ]; then
  echo "Usage: ./backup.sh <dossier>"
  exit 1
fi

DOSSIER="$1" 

# Vérifier que le dossier existe
if [ ! -d "$DOSSIER" ]; then
  echo "Erreur:$DOSSIER N EXISTE PAS "
  exit 1
fi
# Date au format YYYYMMDD
DATE=$(date +%Y%m%d)
#nom du zip
ZIP_NAME="${DOSSIER}-${DATE}.zip"
#creer le zip
zip -r  "$ZIP_NAME" "$DOSSIER" > /dev/null

echo "Sauvegarde créer : $ZIP_NAME"

# semaine-01/hello.py
import sys
import platform
 
print("Bonjour ! Je suis prêt à commencer.")
print(f"Python version : {sys.version}")
print(f"Système : {platform.system()} {platform.release()}")
 
# Petit calcul pour vérifier
total_heures = 35 * 11
print(f"Je vais travailler environ {total_heures} heures sur cette formation.")

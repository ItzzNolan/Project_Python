# backend/save_manager.py

import json
import os
from datetime import datetime


class SaveManager:
    """Gestionnaire de sauvegardes pour le jeu"""
    
    SAVE_DIR = "saves"
    QUICKSAVE_FILE = "quicksave.json"
    
    def __init__(self):
        if not os.path.exists(self.SAVE_DIR):
            os.makedirs(self.SAVE_DIR)
    
    def _get_path(self, filename):
        return os.path.join(self.SAVE_DIR, filename)
    
    def sauvegarder(self, jeu, filename=None):
        if filename is None:
            filename = self.QUICKSAVE_FILE
        
        filepath = self._get_path(filename)
        
        try:
            data = {
                'tour': jeu._tour,
                'carte': {
                    'largeur': jeu.carte.largeur,
                    'hauteur': jeu.carte.hauteur
                },
                'unites': [
                    {
                        'type': u.Unit,
                        'equipe': u.equipe,
                        'coords': list(u.coords) if u.coords else None,
                        'HP': u.HP,
                        'alive': u.alive,
                    }
                    for u in jeu.unites
                ],
                'metadata': {
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'version': '1.0'
                }
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"[SAVE] Partie sauvegardee: {filepath}")
            return True
            
        except Exception as e:
            print(f"[SAVE] Erreur: {e}")
            return False
    
    def charger(self, jeu, filename=None):
        from backend.carte import Carte
        from backend.Units import Unit
        
        if filename is None:
            filename = self.QUICKSAVE_FILE
        
        filepath = self._get_path(filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            jeu._tour = data['tour']
            jeu.carte = Carte(
                largeur=data['carte']['largeur'],
                hauteur=data['carte']['hauteur']
            )
            jeu.unites = []
            
            for u_data in data['unites']:
                unite = Unit(nomUnite=u_data['type'])
                unite.equipe = u_data['equipe']
                unite.coords = tuple(u_data['coords']) if u_data['coords'] else None
                unite.HP = u_data['HP']
                unite.alive = u_data['alive']
                jeu.unites.append(unite)
            
            date_str = data.get('metadata', {}).get('date', '?')
            print(f"[LOAD] Partie chargee: {filepath} ({date_str})")
            return True
            
        except FileNotFoundError:
            print(f"[LOAD] Aucune sauvegarde trouvee")
            return False
        except Exception as e:
            print(f"[LOAD] Erreur: {e}")
            return False
    
    def quicksave_existe(self):
        return os.path.exists(self._get_path(self.QUICKSAVE_FILE))

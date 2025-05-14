# Quarto AI - VoccamTheKiller

Cette intelligence artificielle joue au jeu **Quarto** en utilisant une stratégie basée sur l'analyse de l'état du plateau, l'anticipation des coups, et l'évitement des erreurs. Elle a été développée pour participer à un tournoi organisé via un serveur centralisé.

## 🔍 Fonctionnalités principales

- **Détection automatique d'une victoire** : si l'IA peut gagner en posant la pièce, elle le fait immédiatement.
- **Stratégie de défense** : évite de donner à l’adversaire une pièce permettant un coup gagnant direct.
- **Minimax avec élagage alpha-bêta (profondeur 2)** : simulation partielle des coups pour optimiser la décision sans dépasser le temps imparti.
- **Évaluation basée sur les lignes prometteuses** : favorise les coups qui mènent à des alignements.
- **Bonus de position** : encourage l’occupation de positions centrales.
- **Temps de réponse optimisé** : toutes les décisions sont prises en moins de 5 secondes pour éviter toute pénalité.

## 📁 Arborescence du dépôt

```
.
├── joueur.py         # Fichier principal contenant l’IA
├── requirements.txt  # Dépendances (optionnelles)
├── README.md         # Ce fichier
├── tests/            # Tests unitaires (logique IA et victoire)
└── docs/             # Documentation complémentaire (exemples, protocole)
```

## ⚙️ Dépendances

L'IA a été développée et testée sous **Python 3.10**, mais reste compatible avec toute version supérieure ou égale à **Python 3.8**.

Pour installer les éventuelles dépendances :

```bash
python -m pip install -r requirements.txt
```

> Aucune bibliothèque externe n’est requise par défaut.

## 🚀 Lancement de l’IA

Une fois le serveur de tournoi lancé et prêt :

```bash
python joueur.py localhost 3000
```

> L’IA se connectera automatiquement, s’inscrira, et répondra aux requêtes `ping` et `play`.

## 📤 Protocole de communication

L’IA utilise un protocole basé sur des requêtes JSON échangées via TCP :

### 🎯 Inscription

```json
{
  "request": "subscribe",
  "port": 8888,
  "name": "VoccamTheKiller",
  "matricules": ["23232"]
}
```

### 📡 Ping

- Requête : `{ "request": "ping" }`
- Réponse : `{ "response": "pong" }`

### 🧠 Coup à jouer

```json
{
  "request": "play",
  "lives": 3,
  "errors": [],
  "state": {
    "players": ["IA1", "IA2"],
    "current": 0,
    "board": [...],
    "piece": "BLEP"
  }
}
```

#### Réponse attendue :

```json
{
  "response": "move",
  "move": {
    "pos": 6,
    "piece": "SDFP"
  },
  "message": "À l’attaque !"
}
```

> Si aucun coup valable n’est possible, l’IA peut abandonner avec `{ "response": "giveup" }`.

## 🧪 Tests unitaires

Des tests sont disponibles dans le dossier `tests/`. Pour les exécuter :

```bash
python -m unittest discover tests
```

## 👥 Auteurs

- **Nom** : Mathis Lamborghini
- **Matricule** : 23232
- **Nom IA** : VoccamTheKiller

---

> Ce projet est développé dans le cadre du cours "Advanced Python 2BA", à l’ECAM.

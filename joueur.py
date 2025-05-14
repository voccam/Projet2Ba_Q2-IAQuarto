import socket
import threading
import json
import random
import sys

# === Configuration ===
PORT = 8888
NOM = "VoccamTheKiller"
MATRICULES = ["23232"]

# === Log fonctionnel ===
def log(msg):
    print(f"[LOG] {msg}", file=sys.stderr)

# === Liste complète des pièces ===
# Fonction générant l'ensemble des 16 pièces possibles du jeu
def toutes_les_pieces():
    traits = {
        "taille": ["B", "S"],
        "couleur": ["D", "L"],
        "trou": ["E", "F"],
        "forme": ["C", "P"]
    }
    return {t + c + tr + f for t in traits["taille"]
                              for c in traits["couleur"]
                              for tr in traits["trou"]
                              for f in traits["forme"]}

# === Vérifie si un coup est gagnant
# Vérifie si une position donnée sur le plateau permet de faire un Quarto
def is_winning_move(board, pos, piece):
    temp_board = board[:]
    temp_board[pos] = piece
    # Lignes gagnantes possibles (horizontales, verticales et diagonales)
    lines = [
        [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15],
        [0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15],
        [0, 5, 10, 15], [3, 6, 9, 12]
    ]
    for line in lines:
        line_pieces = [temp_board[i] for i in line if temp_board[i] is not None]
        if len(line_pieces) == 4:
            common = set(line_pieces[0])
            for p in line_pieces[1:]:
                common &= set(p)
            if common:
                return True
    return False

# === Évalue la qualité du plateau avec stratégie pondérée ===
# Fonction d'évaluation heuristique du plateau, favorise les lignes avec caractéristiques communes
def evaluate_board(board):
    CENTRAL_POSITIONS = {5, 6, 9, 10}
    score = 0
    for i, piece in enumerate(board):
        if piece is not None and i in CENTRAL_POSITIONS:
            score += 10  # bonus pour les positions centrales

    # Lignes gagnantes possibles (horizontales, verticales et diagonales)
    lines = [
        [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15],
        [0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15],
        [0, 5, 10, 15], [3, 6, 9, 12]
    ]
    for line in lines:
        line_pieces = [board[i] for i in line if board[i] is not None]
        if len(line_pieces) >= 2:
            common = set(line_pieces[0])
            for p in line_pieces[1:]:
                common &= set(p)
            score += len(common) * len(line_pieces)
    return score

# === Vérifie si une pièce donnée est dangereuse
# Vérifie si une pièce donnée permettrait à l'adversaire de gagner à son tour
def piece_dangereuse(board, piece):
    for i, v in enumerate(board):
        if v is None and is_winning_move(board, i, piece):
            return True
    return False

# === Minimax avec élagage alpha-bêta et stratégie rapide
# Algorithme Minimax avec élagage alpha-bêta, limité à une certaine profondeur pour respecter le temps
def minimax(board, played, current_piece, depth, alpha, beta, maximizing):
    if current_piece is None or depth == 0 or all(p is not None for p in board):
        return evaluate_board(board), None, None

    best_score = float("-inf") if maximizing else float("inf")
    best_pos = None
    best_piece = None

    positions = [i for i, v in enumerate(board) if v is None]
    remaining_pieces = list(toutes_les_pieces() - played - {current_piece})

    # Échantillonnage aléatoire pour limiter le nombre de branches à explorer
    positions = random.sample(positions, min(5, len(positions)))
    remaining_pieces = random.sample(remaining_pieces, min(5, len(remaining_pieces)))

    for pos in positions:
        new_board = board[:]
        new_board[pos] = current_piece
        new_played = played | {current_piece}

        for p in remaining_pieces:
            score, _, _ = minimax(new_board, new_played, p, depth - 1, alpha, beta, not maximizing)

            if is_winning_move(new_board, pos, current_piece):
                score += 1000 if maximizing else -1000
            if piece_dangereuse(new_board, p):
                score -= 500

            if maximizing:
                if score > best_score:
                    best_score = score
                    best_pos = pos
                    best_piece = p
                alpha = max(alpha, score)
            else:
                if score < best_score:
                    best_score = score
                    best_pos = pos
                    best_piece = p
                beta = min(beta, score)

            # Condition d'élagage alpha-bêta
            if beta <= alpha:
                break

    return best_score, best_pos, best_piece

# === Choix du coup
# Fonction principale de décision de l'IA (choix de la case + pièce à donner)
def choisir_coup(etat_jeu):
    board = etat_jeu["board"]
    pion_recu = etat_jeu["piece"]
    log(f"Pion reçu : {pion_recu}")
    log(f"Plateau actuel : {board}")

    cases_vides = [i for i, val in enumerate(board) if val is None]
    if not cases_vides:
        return {"response": "move", "move": {"pos": None, "piece": None}, "message": "Plus de place"}

    pieces_utilisees = set(filter(None, board))
    if pion_recu:
        pieces_utilisees.add(pion_recu)

    # === Donne "giveup" si plus aucun coup possible ===
    if not cases_vides or pion_recu is None and len(toutes_les_pieces() - pieces_utilisees) == 0:
        log("Plus aucun coup possible, abandon.")
        return {"response": "giveup"}

    score, pos, piece = minimax(board, pieces_utilisees, pion_recu, 2, float("-inf"), float("inf"), True)

    if pos is None:
        pos = random.choice(cases_vides)

    toutes = toutes_les_pieces()
    deja_jouees = set(filter(None, board))
    if pion_recu:
        deja_jouees.add(pion_recu)
    if piece is None or piece in deja_jouees:
        restants = list(toutes - deja_jouees)
        piece = random.choice(restants) if restants else None

    log(f"Position jouée : {pos}")
    log(f"Pièce donnée : {piece}")

    return {
        "response": "move",
        "move": {
            "pos": pos,
            "piece": piece
        },
        "message": "Amélioration finale IA"
    }

# === Serveur TCP ===
# Démarre un serveur TCP pour répondre aux requêtes du tournoi (ping et play)
def start_server():
    def handle_client(conn, addr):
        with conn:
            data = conn.recv(2048).decode().strip()
            if not data:
                return
            log(f"Message reçu : {data}")
            req = json.loads(data)

            if req["request"] == "ping":
                res = {"response": "pong"}
                conn.sendall((json.dumps(res) + "\n").encode())
                log("Réponse à ping envoyée.")

            elif req["request"] == "play":
                coup = choisir_coup(req["state"])
                conn.sendall((json.dumps(coup) + "\n").encode())
                log("Coup envoyé.")

    def loop():
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", PORT))
        server.listen()
        log(f"Serveur prêt sur le port {PORT}")
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

    threading.Thread(target=loop, daemon=True).start()

# === Client inscription ===
# Inscription de l'IA auprès du serveur du tournoi
def register(host, port):
    log(f"Connexion au serveur d’inscription {host}:{port}")
    s = socket.socket()
    s.connect((host, port))

    message = {
        "request": "subscribe",
        "port": PORT,
        "name": NOM,
        "matricules": MATRICULES
    }
    s.sendall((json.dumps(message) + "\n").encode())
    response = s.recv(1024).decode()
    log(f"Réponse du serveur : {response}")
    s.close()

# === Main ===
# Fonction principale lançant le serveur et gérant la boucle de vie de l'IA
def main():
    if len(sys.argv) != 3:
        print("Usage : python joueur.py <host> <port>")
        return

    host = sys.argv[1]
    port = int(sys.argv[2])

    start_server()
    register(host, port)

    log("IA en attente des requêtes…")
    while True:
        try:
            pass
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()

#14
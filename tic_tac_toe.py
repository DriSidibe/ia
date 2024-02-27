import pygame

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Tic Tac Toe")

# Fonction pour afficher le plateau de jeu
def afficher_plateau(plateau):
    screen.fill((255, 255, 255))
    for i in range(1, 3):
        pygame.draw.line(screen, (0, 0, 0), (200 * i, 0), (200 * i, 600), 5)
        pygame.draw.line(screen, (0, 0, 0), (0, 200 * i), (600, 200 * i), 5)
    for i in range(3):
        for j in range(3):
            if plateau[i][j] == 'X':
                pygame.draw.line(screen, (0, 0, 0), (j * 200 + 50, i * 200 + 50), (j * 200 + 150, i * 200 + 150), 5)
                pygame.draw.line(screen, (0, 0, 0), (j * 200 + 150, i * 200 + 50), (j * 200 + 50, i * 200 + 150), 5)
            elif plateau[i][j] == 'O':
                pygame.draw.circle(screen, (0, 0, 0), (j * 200 + 100, i * 200 + 100), 50, 5)
    pygame.display.update()

# Fonction pour vérifier s'il y a un gagnant
def verifier_gagnant(plateau):
    # Vérifier les lignes et les colonnes
    for i in range(3):
        if plateau[i][0] == plateau[i][1] == plateau[i][2] != ' ':
            return plateau[i][0]
        if plateau[0][i] == plateau[1][i] == plateau[2][i] != ' ':
            return plateau[0][i]

    # Vérifier les diagonales
    if plateau[0][0] == plateau[1][1] == plateau[2][2] != ' ':
        return plateau[0][0]
    if plateau[0][2] == plateau[1][1] == plateau[2][0] != ' ':
        return plateau[0][2]

    return None

# Fonction pour vérifier si le plateau est plein
def plateau_plein(plateau):
    for row in plateau:
        if ' ' in row:
            return False
    return True

# Fonction pour générer tous les coups valides possibles
def coups_possibles(plateau):
    coups = []
    for i in range(3):
        for j in range(3):
            if plateau[i][j] == ' ':
                coups.append((i, j))
    return coups

# Fonction pour simuler un coup sur le plateau
def jouer_coup(plateau, symbole, coup):
    plateau[coup[0]][coup[1]] = symbole

# Fonction pour annuler un coup sur le plateau
def annuler_coup(plateau, coup):
    plateau[coup[0]][coup[1]] = ' '

# Fonction pour évaluer le score du plateau
def evaluer_plateau(plateau):
    gagnant = verifier_gagnant(plateau)
    if gagnant == 'X':
        return 1
    elif gagnant == 'O':
        return -1
    else:
        return 0

# Algorithme Minimax
def minimax(plateau, profondeur, maximisant):
    if verifier_gagnant(plateau) is not None:
        return evaluer_plateau(plateau)

    if plateau_plein(plateau):
        return 0

    if maximisant:
        meilleur_score = float('-inf')
        for coup in coups_possibles(plateau):
            jouer_coup(plateau, 'X', coup)
            score = minimax(plateau, profondeur + 1, False)
            annuler_coup(plateau, coup)
            meilleur_score = max(meilleur_score, score)
        return meilleur_score
    else:
        meilleur_score = float('inf')
        for coup in coups_possibles(plateau):
            jouer_coup(plateau, 'O', coup)
            score = minimax(plateau, profondeur + 1, True)
            annuler_coup(plateau, coup)
            meilleur_score = min(meilleur_score, score)
        return meilleur_score

# Fonction pour que l'IA choisit le meilleur coup
def meilleur_coup(plateau):
    meilleur_score = float('-inf')
    meilleur_coup = None
    for coup in coups_possibles(plateau):
        jouer_coup(plateau, 'X', coup)
        score = minimax(plateau, 0, False)
        annuler_coup(plateau, coup)
        if score > meilleur_score:
            meilleur_score = score
            meilleur_coup = coup
    return meilleur_coup

# Fonction principale pour jouer au jeu
def jouer_tic_tac_toe():
    pygame.init()
    plateau = [[' ' for _ in range(3)] for _ in range(3)]
    tour = input("Qui commence (X our l'IA et O pour l'Humain) ? ")
    if tour != 'x' and tour != 'O':
        exit()

    while True:
        afficher_plateau(plateau)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                i, j = y // 200, x // 200
                if plateau[i][j] == ' ':
                    if tour == 'O':
                        jouer_coup(plateau, tour, (i, j))
                        tour = 'X'
                            

        if tour == 'X':
            coup = meilleur_coup(plateau)
            jouer_coup(plateau, 'X', coup)
            tour = 'O'

        gagnant = verifier_gagnant(plateau)
        if gagnant:
            afficher_plateau(plateau)
            print(f"Gagnant: {gagnant}")
            input("Appuyez sur Entrée pour quitter...")
            break

        if plateau_plein(plateau):
            afficher_plateau(plateau)
            print("Match nul!")
            input("Appuyez sur Entrée pour quitter...")
            break

if __name__ == "__main__":
    jouer_tic_tac_toe()

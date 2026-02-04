import pygame
import sys

# Pygame initialisieren
pygame.init()

# Fenstergröße
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Darts Scoreboard")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Schriftarten
font_large = pygame.font.SysFont('Arial', 48)
font_medium = pygame.font.SysFont('Arial', 36)
font_small = pygame.font.SysFont('Arial', 24)

class Player:
    def __init__(self, name, color):
        self.name = name
        self.score = 501  # Standard Startwert
        self.color = color
        self.history = []
        self.current_round = []
        self.wins = 0
        
    def add_score(self, points):
        if len(self.current_round) < 3:
            self.current_round.append(points)
            
    def finish_round(self):
        if self.current_round:
            round_total = sum(self.current_round)
            if self.score - round_total >= 0 and (self.score - round_total != 1):
                self.score -= round_total
                self.history.append(self.current_round.copy())
            elif self.score - round_total == 0:
                # Check für Double-Out
                if self.current_round[-1] % 2 == 0 or self.current_round[-1] == 50:
                    self.score = 0
                    self.history.append(self.current_round.copy())
            self.current_round.clear()
            
    def undo_last_throw(self):
        if self.current_round:
            self.current_round.pop()
        elif self.history:
            last_round = self.history.pop()
            self.score += sum(last_round)

class DartScoreboard:
    def __init__(self):
        self.players = [
            Player("Spieler 1", BLUE),
            Player("Spieler 2", RED)
        ]
        self.current_player = 0
        self.game_over = False
        self.winner = None
        
        # Tastatur-Input Zahlen
        self.input_value = ""
        self.active_input = False
        
        # Buttons für schnelle Eingabe
        self.quick_buttons = [
            ("20", 100, 450), ("19", 180, 450), ("18", 260, 450),
            ("17", 340, 450), ("16", 420, 450), ("15", 500, 450),
            ("Bull", 580, 450), ("25", 660, 450),
            ("x2", 100, 500), ("x3", 180, 500),
            ("Miss", 260, 500), ("Undo", 340, 500),
            ("Enter", 580, 500), ("Clear", 660, 500)
        ]
        
    def switch_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)
        
    def check_winner(self):
        for player in self.players:
            if player.score == 0:
                self.game_over = True
                self.winner = player
                return True
        return False
    
    def handle_click(self, pos):
        x, y = pos
        
        # Quick Buttons überprüfen
        for text, btn_x, btn_y in self.quick_buttons:
            btn_rect = pygame.Rect(btn_x, btn_y, 70, 40)
            if btn_rect.collidepoint(x, y):
                self.handle_button_click(text)
                return
        
        # Zahlen-Eingabe Bereich
        input_rect = pygame.Rect(300, 400, 200, 50)
        if input_rect.collidepoint(x, y):
            self.active_input = True
            self.input_value = ""
        else:
            self.active_input = False
            
    def handle_button_click(self, text):
        current = self.players[self.current_player]
        
        if text == "Enter":
            if self.input_value:
                try:
                    points = int(self.input_value)
                    if 0 <= points <= 180:
                        current.add_score(points)
                        self.input_value = ""
                except ValueError:
                    pass
                    
        elif text == "Clear":
            self.input_value = ""
            
        elif text == "Undo":
            current.undo_last_throw()
            
        elif text == "Miss":
            current.add_score(0)
            
        elif text == "x2":
            if self.input_value:
                try:
                    points = int(self.input_value) * 2
                    current.add_score(points)
                    self.input_value = ""
                except ValueError:
                    pass
                    
        elif text == "x3":
            if self.input_value:
                try:
                    points = int(self.input_value) * 3
                    current.add_score(points)
                    self.input_value = ""
                except ValueError:
                    pass
                    
        elif text == "Bull":
            current.add_score(50)
            
        elif text == "25":
            current.add_score(25)
            
        else:
            # Zahlen-Buttons (20, 19, 18, etc.)
            try:
                points = int(text)
                current.add_score(points)
            except ValueError:
                pass
    
    def handle_keypress(self, key):
        if self.active_input:
            if key == pygame.K_RETURN:
                if self.input_value:
                    try:
                        points = int(self.input_value)
                        current = self.players[self.current_player]
                        if 0 <= points <= 180:
                            current.add_score(points)
                            self.input_value = ""
                    except ValueError:
                        pass
            elif key == pygame.K_BACKSPACE:
                self.input_value = self.input_value[:-1]
            elif pygame.K_0 <= key <= pygame.K_9:
                self.input_value += chr(key)
    
    def draw(self, screen):
        screen.fill(WHITE)
        
        # Titel
        title = font_large.render("DARTS SCOREBOARD 501", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        
        # Spieler-Informationen anzeigen
        for i, player in enumerate(self.players):
            # Spieler-Box
            player_rect = pygame.Rect(50 + i*350, 100, 300, 250)
            pygame.draw.rect(screen, player.color, player_rect, 3)
            
            # Aktiver Spieler markieren
            if i == self.current_player and not self.game_over:
                pygame.draw.rect(screen, YELLOW, player_rect, 6)
            
            # Spielername
            name_text = font_medium.render(player.name, True, player.color)
            screen.blit(name_text, (50 + i*350 + 150 - name_text.get_width()//2, 120))
            
            # Aktueller Score
            score_text = font_large.render(str(player.score), True, BLACK)
            screen.blit(score_text, (50 + i*350 + 150 - score_text.get_width()//2, 180))
            
            # Aktuelle Runde
            round_text = font_small.render("Aktuelle Runde: " + " ".join(str(x) for x in player.current_round), True, BLACK)
            screen.blit(round_text, (50 + i*350 + 10, 250))
            
            # Gewinne
            wins_text = font_small.render(f"Siege: {player.wins}", True, BLACK)
            screen.blit(wins_text, (50 + i*350 + 10, 280))
        
        # Eingabe-Bereich
        pygame.draw.rect(screen, GRAY, (300, 400, 200, 50), 2)
        input_text = font_medium.render(self.input_value, True, BLACK)
        screen.blit(input_text, (310, 410))
        
        # Quick Buttons zeichnen
        for text, x, y in self.quick_buttons:
            btn_rect = pygame.Rect(x, y, 70, 40)
            pygame.draw.rect(screen, GRAY, btn_rect)
            pygame.draw.rect(screen, BLACK, btn_rect, 2)
            btn_text = font_small.render(text, True, BLACK)
            screen.blit(btn_text, (x + 35 - btn_text.get_width()//2, y + 20 - btn_text.get_height()//2))
        
        # Anweisungen
        instr = font_small.render("Klicke auf eine Zahl oder gib Punkte ein (0-180)", True, BLACK)
        screen.blit(instr, (WIDTH//2 - instr.get_width()//2, 370))
        
        # Runde beenden Button
        end_round_rect = pygame.Rect(WIDTH//2 - 100, 550, 200, 40)
        pygame.draw.rect(screen, GREEN, end_round_rect)
        pygame.draw.rect(screen, BLACK, end_round_rect, 2)
        end_text = font_medium.render("Runde beenden", True, BLACK)
        screen.blit(end_text, (WIDTH//2 - end_text.get_width()//2, 560))
        
        # Spiel beenden/Neustart Button
        if self.game_over:
            restart_rect = pygame.Rect(WIDTH//2 - 100, 480, 200, 40)
            pygame.draw.rect(screen, YELLOW, restart_rect)
            pygame.draw.rect(screen, BLACK, restart_rect, 2)
            restart_text = font_medium.render("Neues Spiel", True, BLACK)
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 490))
            
            # Gewinner anzeigen
            win_text = font_large.render(f"{self.winner.name} gewinnt!", True, GREEN)
            screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, 300))
        
        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    scoreboard = DartScoreboard()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                scoreboard.handle_keypress(event.key)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                scoreboard.handle_click(pos)
                
                # Runde beenden Button
                end_round_rect = pygame.Rect(WIDTH//2 - 100, 550, 200, 40)
                if end_round_rect.collidepoint(pos) and not scoreboard.game_over:
                    current_player = scoreboard.players[scoreboard.current_player]
                    current_player.finish_round()
                    if not scoreboard.check_winner():
                        scoreboard.switch_player()
                
                # Neues Spiel Button
                if scoreboard.game_over:
                    restart_rect = pygame.Rect(WIDTH//2 - 100, 480, 200, 40)
                    if restart_rect.collidepoint(pos):
                        # Gewinner bekommt einen Punkt
                        if scoreboard.winner:
                            scoreboard.winner.wins += 1
                        
                        # Spiel zurücksetzen
                        for player in scoreboard.players:
                            player.score = 501
                            player.history = []
                            player.current_round = []
                        scoreboard.game_over = False
                        scoreboard.winner = None
                        scoreboard.current_player = 0
        
        scoreboard.draw(screen)
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
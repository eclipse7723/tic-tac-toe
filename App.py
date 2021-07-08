from random import sample


EMPTY_CELL = '.'
MARKERS = ['X', 'O']


class Player:
    def __init__(self, name: str, marker: str):
        assert len(marker) == 1, f"Player's marker should be 1 character (you put {marker!r})"
        assert marker.upper() in ''.join(MARKERS), f"Invalid marker {marker!r}, only {MARKERS[0]!r} or {MARKERS[1]!r}"
        self.marker = marker
        self.name = name


class Desk:     # Model
    def __init__(self):
        self.__desk = [[EMPTY_CELL for i in range(3)] for i in range(3)]
        self.__players = []
        self.__step = 0             # четные для первого игрока, нечетные для второго

    def get_desk(self):
        return self.__desk

    def check_desk(self):
        """ TODO: Проверяет доску на предмет чьей-то победы """
        state = False, None     # Завершена ли игра, Победитель
        return state

    @property
    def players(self):
        return self.__players

    def add_player(self, player: Player):
        """ Добавляет игрока в базу """
        assert len(self.__players) < 2, 'Only 2 players allowed'
        self.__players.append(player)

    def fetch_player_by_marker(self, marker):
        assert marker.upper() in MARKERS, f'Unknown marker {marker!r}, it should be {MARKERS[0]!r} or {MARKERS[1]!r}'
        players = {player.marker: player for player in self.__players}
        return players[marker.upper()]

    def update_desk(self, marker: str, position: tuple):
        """ Устанавливает маркер в указаную позицию """
        if self.__desk[position[0]][position[1]] == EMPTY_CELL:
            self.__desk[position[0]][position[1]] = marker
            return True
        else:
            return False

    @property
    def step(self):
        return self.__step

    def next_step(self):
        self.__step += 1

    @staticmethod
    def get_allowed_moves():
        """ Возвращает координаты человеческим языком """
        table = {
            't1': (0, 0), 't2': (0, 1), 't3': (0, 2),
            'c1': (1, 0), 'c2': (1, 1), 'c3': (1, 2),
            'b1': (2, 0), 'b2': (2, 1), 'b3': (2, 2)
        }
        return table


class Controller:
    def __init__(self, desk, view):
        self.desk = desk
        self.view = view

    def init_players(self):
        """ Создаёт игроков """
        self.view.notify("Create your players")
        self.view.send("Enter 1st player's name")
        nameA = input("> ")
        self.view.send("Enter 2nd player's name")
        nameB = input("> ")
        markerA, markerB = sample(MARKERS, 2)
        playerA = Player(nameA, markerA)
        playerB = Player(nameB, markerB)
        self.view.notify(f"1st player's name is {playerA.name} and his marker is {playerA.marker}")
        self.view.notify(f"2nd player's name is {playerB.name} and his marker is {playerB.marker}")
        self.show_instruction()
        self.desk.add_player(playerA)
        self.desk.add_player(playerB)

    def read(self):
        """ Читает команды от пользователя """
        command = input("> ").replace(' ', '').lower()
        allowed_moves = self.desk.get_allowed_moves()
        if command in allowed_moves.keys():
            position = allowed_moves[command]
            player = self.get_current_player()
            self.move(player, position)
        elif command == 'help':
            self.show_instruction()
        elif command == 'who':
            self.show_current_player()
        elif command == 'stop':
            exit()
        else:
            self.view.notify("Unknown command, check 'help'")

    def show_desk(self):
        """ Отобразить доску """
        self.view.draw(self.desk.get_desk())

    def move(self, player: Player, position: tuple):
        """ Устанавливает значок игрока в указанное место """
        isMoved = self.desk.update_desk(player.marker, position)
        if isMoved is False:
            return self.view.notify('This position is already taken, try another')
        self.desk.next_step()
        self.view.notify(f"{player.name} makes a move:")
        self.view.draw(self.desk.get_desk())
        winner = self.desk.check_desk()
        if winner[0]:
            self.show_results(winner)

    def show_instruction(self):
        """ Отображает инструкцию для команды 'help' """
        self.view.instructions()

    def get_current_player(self):
        """ Возвращает текущего игрока, который делает ход """
        return self.desk.players[self.desk.step % 2]

    def show_current_player(self):
        """ Напоминает, кто сейчас ходит | для команды 'who' """
        current_player = self.get_current_player()
        self.view.notify(f"Current player is {current_player.name}")

    def show_results(self, winner):
        """ Уведомляет о резульатах игры """
        self.view.results(winner)


class View:
    @staticmethod
    def draw(desk):
        """
        Рисует доску такого вида:
              1  ┃  2  ┃  3
            ━━━━━╋━━━━━╋━━━━━
              4  ┃  5  ┃  6
            ━━━━━╋━━━━━╋━━━━━
              7  ┃  8  ┃  9
        """
        print("\t  {}  |  {}  |  {} \n".format(desk[0][0], desk[0][1], desk[0][2]),
              "\t—————+—————+—————\n",
              "\t  {}  |  {}  |  {} \n".format(desk[1][0], desk[1][1], desk[1][2]),
              "\t—————+—————+—————\n",
              "\t  {}  |  {}  |  {} \n".format(desk[2][0], desk[2][1], desk[2][2]))

    @staticmethod
    def notify(message):
        """ Отправка уведомлений """
        print(f"[!] {message}")

    @staticmethod
    def send(message):
        """ Отправка просто сообщений """
        print(f"[*] {message}")

    @staticmethod
    def instructions():
        print('='*30)
        print("You can make a move by entering the corresponding cell number:")
        print(f"\t  T1 |  T2 |  T3 \n",
              f"\t—————+—————+—————\n",
              f"\t  C1 |  C2 |  C3 \n",
              f"\t—————+—————+—————\n",
              f"\t  B1 |  B2 |  B3 \n")
        print("Type 'who' if you forgot who is current player")
        print("Type 'stop' to exit game...")
        print("Type 'help' to see that text again")
        print('='*30)

    def results(self, state):
        if state[1]:
            self.notify(f"Game over: {state[2].name} won this game!")
        else:
            self.notify(f"Game over: Draw!")


class Game:
    def __init__(self):
        self.controller = Controller(Desk(), View())
        self.run = False

    def play(self):
        """ Запуск игры """
        self.run = True
        self.controller.init_players()
        while self.run:
            self.controller.read()


if __name__ == "__main__":
    game = Game()
    game.play()

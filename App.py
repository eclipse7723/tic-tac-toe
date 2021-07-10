from random import sample


EMPTY_CELL = '.'        # Маркер пустой ячейки
MARKERS = ['X', 'O']    # Маркеры игроков
DESK_SIZE = 3           # Размер доски (поддерживается сейчас только 3)


class Player:
    def __init__(self, name: str, marker: str):
        assert len(marker) == 1, f"Player's marker should be 1 character (you put {marker!r})"
        assert marker.upper() in ''.join(MARKERS), f"Invalid marker {marker!r}, only {MARKERS[0]!r} or {MARKERS[1]!r}"
        self.marker = marker
        self.name = name


class Desk:
    def __init__(self):
        self.__desk = [[EMPTY_CELL for i in range(DESK_SIZE)] for i in range(DESK_SIZE)]
        self.__players = []
        self.__step = 0             # четные для первого игрока, нечетные для второго
        self.__state = False, None  # Завершена ли игра, Победитель

    def get_desk(self):
        """ Возвращает доску """
        return self.__desk

    def update_desk(self, marker: str, position: tuple):
        """ Устанавливает маркер в указаную позицию """
        if self.__desk[position[0]][position[1]] == EMPTY_CELL:
            self.__desk[position[0]][position[1]] = marker
            return True
        else:
            return False

    @property
    def state(self):
        return self.__state

    def check_combinations(self, lst: list):
        """ Проверка выигрышной комбинации """
        for row in lst:
            if row[0] == EMPTY_CELL:
                continue
            if len(set(row)) == 1:
                self.__state = True, self.fetch_player_by_marker(row[0])

    def check_desk(self):
        """ Проверяет доску на предмет чьей-то победы """
        # 1) Есть ли свободные ячейки
        isEmpty = False
        for row in self.__desk:
            if EMPTY_CELL in row:
                isEmpty = True
                break
        if isEmpty is False:
            # Игра завершена, но победителя нет
            self.__state = True, None

        # 2) Поиск выиграшных комбинаций
        rows = [row for row in self.__desk]
        columns = [[row[i] for row in self.__desk] for i in range(DESK_SIZE)]
        diagonals = [[self.__desk[i][i] for i in range(DESK_SIZE)],                 # Главная диагональ
                     [self.__desk[i][DESK_SIZE-i-1] for i in range(DESK_SIZE)]]     # Побочная диагональ
        self.check_combinations(rows)
        self.check_combinations(columns)
        self.check_combinations(diagonals)

        return self.__state

    @property
    def players(self):
        return self.__players

    def add_player(self, player: Player):
        """ Добавляет игрока в базу """
        assert len(self.__players) < 2, 'Only 2 players allowed'
        self.__players.append(player)

    def fetch_player_by_marker(self, marker):
        """ Возвращает игрока по указанному маркеру """
        assert marker.upper() in MARKERS, f'Unknown marker {marker!r}, it should be {MARKERS[0]!r} or {MARKERS[1]!r}'
        players = {player.marker: player for player in self.__players}
        return players[marker.upper()]

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
        """ Создаёт игроков и показывает инструкцию """
        self.view.notify("Create your players")
        self.view.send("Enter 1st player's name")
        nameA = input("> ")
        self.view.send("Enter 2nd player's name")
        nameB = input("> ")
        markerA, markerB = sample(MARKERS, 2)
        playerA = Player(nameA, markerA)
        playerB = Player(nameB, markerB)
        self.view.notify(f"1st player's name is {playerA.name} and his marker is {playerA.marker!r}")
        self.view.notify(f"2nd player's name is {playerB.name} and his marker is {playerB.marker!r}")
        self.show_instruction()
        self.desk.add_player(playerA)
        self.desk.add_player(playerB)

    def read(self):
        """ Читает команды от пользователя """
        if self.desk.state[0]:
            return False
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
        return True

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
        # Проверяем состояние игры (то есть доски)
        self.check_game_results()

    def show_instruction(self):
        """ Отображает инструкцию -> 'help' """
        self.view.instructions()

    def get_current_player(self):
        """ Возвращает текущего игрока, который делает ход """
        return self.desk.players[self.desk.step % 2]

    def show_current_player(self):
        """ Напоминает, кто сейчас ходит -> 'who' """
        current_player = self.get_current_player()
        self.view.notify(f"Current player is {current_player.name} (marker: {current_player.marker!r})")

    def check_game_results(self):
        """ Возвращает состояние доски """
        # Проверяем доску только после пятого хода, поскольку до этого выиграшных комбинаций не может быть
        if self.desk.step > 3:
            state = self.desk.check_desk()
            if state[0]:
                self.show_results(state)

    def show_results(self, state):
        """ Уведомляет о резульатах игры """
        self.view.results(state)


class View:
    @staticmethod
    def draw(desk):
        """
        Рисует доску такого вида (для поля любого размера):
              1  ┃  2  ┃  3
            ━━━━━╋━━━━━╋━━━━━
              4  ┃  5  ┃  6
            ━━━━━╋━━━━━╋━━━━━
              7  ┃  8  ┃  9
        """
        for i in range(DESK_SIZE):
            print("\t", end='')
            for j in range(DESK_SIZE):
                print(f"  {desk[i][j]}  ", end='')
                if j < DESK_SIZE-1:
                    print("|", end='')
            if i < DESK_SIZE-1:
                print(f"\n\t—————{'+—————'*(DESK_SIZE-1)}")
            else:
                print("")

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
            self.notify(f"Game over: {state[1].name} won this game!")
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
            self.run = self.controller.read()
        input()     # Чтобы окно не закрывалось моментально после итогов игры


if __name__ == "__main__":
    game = Game()
    game.play()

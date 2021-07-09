# Крестики-нолики
Консольная версия игры "крестики-нолики" паттерном MVC.

## Игра
#### Визуальная часть
```
      .  ┃  .  ┃  .         0  ┃  1  ┃  2  
    ━━━━━╋━━━━━╋━━━━━     ━━━━━╋━━━━━╋━━━━━
      .  ┃  .  ┃  .         3  ┃  4  ┃  5  
    ━━━━━╋━━━━━╋━━━━━     ━━━━━╋━━━━━╋━━━━━
      .  ┃  .  ┃  .         6  ┃  7  ┃  8  
```
#### Управление (как поставить значок)
```
      T1 ┃  T2 ┃  T3 
    ━━━━━╋━━━━━╋━━━━━
      C1 ┃  C2 ┃  C3
    ━━━━━╋━━━━━╋━━━━━
      B1 ┃  B2 ┃  B3
```
**Схема**: Top-Center-Bottom + 1-2-3.
Пример: **С2** - поставит маркер в центр решётки.
#### Команды
- **help** - вызвать подсказку
- **who** - показывает, кто сейчас ходит
- **stop** - прервать игру
#### Определение победы
В игре есть **8** вариантов победы (3 вертикально, 3 горизонтально и 2 по вертикали). Возможные ситуации:
```
      X  ┃  O  ┃  O         O  ┃  O  ┃  O  
    ━━━━━╋━━━━━╋━━━━━     ━━━━━╋━━━━━╋━━━━━
      .  ┃  X  ┃  .         .  ┃  X  ┃  .  
    ━━━━━╋━━━━━╋━━━━━     ━━━━━╋━━━━━╋━━━━━
      .  ┃  .  ┃  X         .  ┃  X  ┃  X  
```
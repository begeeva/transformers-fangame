# Transformers
Transformers - это простенькая игра в жанре раннер, в которой игроку предстоит управлять автоботом по имени Клиффджампер.
Протагонист бегает по Кибертрону, и периодически ему навстречу попадаются десептиконы,
при приближении которых надо прыгать, и тоннели, при приближении которых надо трансформироваться в автомобиль. Столкновение с ними приводит к проигрышу.
На экране поражения вы можете увидеть количество очков за данную игру и лучший результат за все игры. Задача игрока продержаться как можно дольше.

# Установка и запуск
- ``` pip3 install -r requirements.txt ```
- ``` python main.py ```

# Управление
Чтобы совершить прыжок нажмите на левую кнопку мыши или "пробел".

Чтобы трансформироваться нажмите на правую кнопку мыши или "LShift".

# Классы
Star - класс звёзд на заднем фоне в меню.
StartBtn - класс кнопки "START" в меню, нажатие на которую приводит к началу игры.
City - класс города на заднем плане в игре.
Player - анимированный класс игрока.
TunnelCeiling - класс потолка тоннеля, с которым может произойти столкновение.
TunnelWall - класс стены тоннеля, мимо которой игрок может пройти спокойно.
Enemy - класс врага.
(Подробнее о классах вы можете прочитать в пояснительной записке).

# Разработчик
Разработчик и художник данного проекта - Бегеева Абидат.

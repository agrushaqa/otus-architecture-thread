Домашнее задание 7

Домашнее задание

Многопоточное выполнение команд
Цель:

Разработка многопоточной системы выполнения команд на примере игры "Танки".
В результате выполнения ДЗ будет получен код, отвечающий за выполнение множества команд в несколько потоков, устойчивый к появлению новых видов команд и дополнительных ограничений, накладываемых на них.

Описание/Пошаговая инструкция выполнения домашнего задания:

Предположим, что у нас есть набор команд, которые необходимо выполнить. Выполнение команд организуем в несколько потоков.
Для этого будем считать, что у каждого потока есть своя потокобезопасная очередь.
Для того, чтобы выполнить команду, ее необходимо добавить в очередь. Поток читает очередную команду из очереди и выполняет ее.
Если выполнение команды прерывается выброшенным исключением, то поток должен отловить его и продолжить работу.
Если сообщений нет в очереди, то поток засыпает до тех пор, пока очередь пуста.
Последовательность шагов решения:

    Реализовать код, который запускается в отдельном потоке и делает следующее
    В цикле получает из потокобезопасной очереди команду и запускает ее.
    Выброс исключения из команды не должен прерывать выполнение потока.
    Написать команду, которая стартует код, написанный в пункте 1 в отдельном потоке.
    Написать команду, которая останавливает цикл выполнения команд из пункта 1, не дожидаясь их полного завершения (hard stop).
    Написать команду, которая останавливает цикл выполнения команд из пункта 1, только после того, как все команды завершат свою работу (soft stop).
    Написать тесты на команду запуска и остановки потока.


Критерии оценки:

За выполнение каждого пункта, перечисленного ниже начисляются баллы:

    ДЗ сдано на проверку - 2 балла
    Код решения опубликован на github/gitlab - 1 балл
    Настроен CI - 2 балла
    Код компилируется без ошибок - 1 балл.
    Написать тест, который проверяет, что после команды старт поток запущен - 1балл и 4 балла - если используются условные события синхронизации.
    Написать тест, который проверяет, что после команды hard stop, поток завершается - 1 балл
    Написать тест, который проверяет, что после команды soft stop, поток завершается только после того, как все задачи закончились - 2 балла
    Итого: 10 баллов
    Задание считается принятым, если набрано не менее 7 баллов.

# Реализация
смотри тесты в
tests\test_ioc_queue.py
# hard stop отличает тем, что не выполняет команды идующие после неё
пример:
        context_command_queue1.add_ioc_command("HardStop")
        context_command_queue1.add_ioc_command("Sleep", 12)
# soft stop выполняет команды идующие после неё
как видно в 
thread\features\steps\src\ioc_commands_queue.py
я на будущее добавил счётчик и интервал для того, чтобы SoftStop мог ждать 
подольше или поменьше

Домашнее задание 5

Реализация IoC контейнера
Цель:

Цель: Реализовать IoC контейнер, устойчивый к изменению требований.
В результате выполнения домашнего задания Вы получите IoC, который можно будет использовать в своих проектах.

Описание/Пошаговая инструкция выполнения домашнего задания:

В игре Космичекий бой есть набор операций над игровыми объектами: движение по прямой, поворот, выстрел. При этом содержание этих команд может отличаться для разных игр, в зависимости от того, какие правила игры были выбраны пользователями. Например, пользователи могут ограничить запас ход каждого корабля некоторым количеством топлива, а другой игре запретить поворачиваться кораблям по часовой стрелке и т.д.
IoC может помочь в этом случае, скрыв детали в стратегии разрешения зависимости.
Например,
IoC.Resolve("двигаться прямо", obj);
Возвращает команду, которая чаще всего является макрокомандой и осуществляет один шаг движения по прямой.
Реализовать IoC контейнер, который:

    Разрешает зависимости с помощью метода, со следующей сигнатурой:
    T IoC.Resolve(string key, params object[] args);
    Регистрация зависимостей также происходит с помощью метода Resolve
    IoC.Resolve("IoC.Register", "aaa", (args) => new A()).Execute();
    Зависимости можно регистрировать в разных "скоупах"
    IoC.Resolve("Scopes.New", "scopeId").Execute();
    IoC.Resolve("Scopes.Current", "scopeId").Exceute();
    Указание: Для работы со скоупами используйте ThreadLocal контейнер.


Критерии оценки:

    Интерфейс IoC устойчив к изменению требований. Оценка: 0 - 3 балла (0 - совсем не устойчив, 3 - преподаватель не смог построить ни одного контрпримера)
    IoC предоставляет ровно один метод для всех операций. 1 балл
    IoC предоставляет работу со скоупами для предотвращения сильной связности. 2 балла.
    Реализованы модульные тесты. 2 балла
    Реализованы многопоточные тесты. 2 балла
    Максимальная оценка 10 баллов.
    Задание принято, если будет набрано не менее 7 баллов.

Домашнее задание 3

Механизм обработки исключений в игре "Космическая битва"
Цель:

Научится писать различные стратегии обработки исключений так, чтобы соответствующий блок try-catсh не приходилось модифицировать каждый раз, когда возникает потребность в обработке исключительной ситуации по-новому.

Описание/Пошаговая инструкция выполнения домашнего задания:

Предположим, что все команды находятся в некоторой очереди. Обработка очереди заключается в чтении очередной команды и головы очереди и вызова метода Execute извлеченной команды. Метод Execute() может выбросить любое произвольное исключение.

    Обернуть вызов Команды в блок try-catch.
    Обработчик catch должен перехватывать только самое базовое исключение.
    Есть множество различных обработчиков исключений. Выбор подходящего обработчика исключения делается на основе экземпляра перехваченного исключения и команды, которая выбросила исключение.
    Реализовать Команду, которая записывает информацию о выброшенном исключении в лог.
    Реализовать обработчик исключения, который ставит Команду, пишущую в лог в очередь Команд.
    Реализовать Команду, которая повторяет Команду, выбросившую исключение.
    Реализовать обработчик исключения, который ставит в очередь Команду - повторитель команды, выбросившей исключение.
    С помощью Команд из пункта 4 и пункта 6 реализовать следующую обработку исключений:
    при первом выбросе исключения повторить команду, при повторном выбросе исключения записать информацию в лог.
    Реализовать стратегию обработки исключения - повторить два раза, потом записать в лог. Указание: создать новую команду, точно такую же как в пункте 6. Тип этой команды будет показывать, что Команду не удалось выполнить два раза.


Критерии оценки:

    ДЗ сдано на оценку - 2 балла
    Реализованы пункты 4-7. - 2 балла.
    Написаны тесты к пункту 4-7. - 2 балла
    Реализован пункт 8. - 1 балл
    Написаны тесты к пункту 8. - 1 балл
    Реализован пункт 9. - 1 балл
    Написаны тесты к пункту 9. - 1 балл
    Максимальная оценка за задание 10 баллов.
    Задание принимается, если задание оценено не менее, чем в 7 баллов.

# Замечания
## commands\__init__.py
При добавлении команды в
\thread\features\steps\src\commands
её нужно добавлять в
\thread\features\steps\src\commands\__init__.py

# requirements.txt
## create
pip freeze > requirements.txt
## use
pip install -r requirements.txt

# code style
## isort
python -m pip install isort
### run 
isort .
## mypy
python -m pip install mypy
### run 
mypy . --no-namespace-packages
## flake8
python -m pip install flake8
### run
flake8 --exclude venv,docs --ignore=F401
## code coverage
pip install coverage
### run
coverage run C:\Users\agrusha\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\behave\__main__.py
в файле .coveragerc нужно указать исходники

# Pytest
## install
```pip install pytest-xdist```

also:
https://pypi.org/project/pytest-parallel/
## run Tests in Parallel
```pytest -n 2 test_common.py```
## run one module
```
python -m pytest --rootdir=. tests\test_common.py
```
## run with allure
```
python -m pytest --rootdir=. tests --alluredir=reports/
```
# allure
```
allure generate report && allure open
```


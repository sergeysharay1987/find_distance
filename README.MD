#Описание приложения
Данное приложение позволяет рассчитать расстояние от МКАД до адреса, ввёднного пользователем в поле "адрес".



#Начальная настройка

1. Установите необходимые компоненты:
    ```
    apt update
    apt install git
    ```
2. Если вы не настроили его глобально, настройте git:
    ```
    git config user.name 'Имя Фамилия'
    git config user.email 'youremail@youremail_domain.com'
    ```
3. Установите необходимые компоненты (как указано на странице https://github.com/pyenv/pyenv/wiki/Common-build-problems:
4. Установите и настройте pyenv как указано на странице https://github.com/pyenv/pyenv#basic-github-checkout:

5. Установите самую низкую поддерживаемую версию Python:
    ```
    pyenv установить 3.7.0
    pyenv local 3.7.0 # запускать из корня этого репо (должен появиться файл `.python-version`)
    ```
6. Установите Docker согласно https://docs.docker.com/engine/install/ (известная работа: Docker версии 20.10.1, сборка 831ebea)

7. Добавьте своего пользователя в группу докеров:
    ```
    sudo usermod -aG docker ${USER}
    выход
    ```

8. Форк https://github.com/sergeysharay1987/find_distance репозиторий

9. Клонируем репозиторий:
    ```
    git clone git@github.com:sergeysharay1987/find_distance.git
    ```

10. Установить Poetry и все необходимые зависимости из poetry:
    ```
    pip install poetry 
    ```
11. Установить все необходимые зависимости:
    ```
    poetry install
    ```

##Docker
1. Для создания образа выполните команду:
    ```
    docker build -t find_distance .
    ```
2. Для создания и запуска контейнера на основе образа find_distance выполните команду:
    ```
    docker run --name distance -p 5000:5000 find_distance
    ```
3. Для остановки контейнера выполните команду:
    ```
    docker stop distance
    ```
4. Для повторного запуска контейнера с приложением выполните команлу:
    ```
    docker start distance
    ```

##Запуск

1. Для запуска приложения введите в отдельном терминале команду:
    ```
    python -m main
    ``` 
2. Для запуска приложения с помощью Docker выполните шаги, описанные в секции Docker.


# ml-pro HW1
## Основное
### Пункт 1
[Ссылка на зелёный прогон со всеми тремя job](https://github.com/Estomeee/ml-pro/actions/runs/39045207594)

[Ссылка на страницу пакета с образом, в теге
виден sha коммита](https://github.com/Estomeee/ml-pro/pkgs/container/iris-service%2Fsha-cb218f739e81d693c60033edf6ddbc871e4717f9)

### Пункт 2
[Ссылка на pull request, в истории которого виден красный прогон и затем зелёный.](https://github.com/Estomeee/ml-pro/pull/1)

### Пункт 3
1. Конфиг. Укажите в ConfigMap путь к несуществующей модели.

    [Ссылка на красный прогон](https://github.com/Estomeee/ml-pro/actions/runs/39047796733)

    [Ссылка на зелёный прогон](https://github.com/Estomeee/ml-pro/actions/runs/39050411921)

    В разделе с диагностикой указано: 
    ```
    FileNotFoundError: [Errno 2] No such file or directory: 'artifacts/no_model.joblib'

    ERROR:    Application startup failed. Exiting.
    ```
    Можно сделать вывод, что в конфиге задан неверный путь.
2. Секрет. Сделайте так, чтобы имя в secretRef не совпадало с именем секрета, который со‐
здаёт пайплайн.

    [Ссылка на красный прогон](https://github.com/Estomeee/ml-pro/actions/runs/39050726556)

    [Ссылка на зелёный прогон](https://github.com/Estomeee/ml-pro/actions/runs/39051165750)

    В диагностке для пода можно наблюдать статус:
    ``` CreateContainerConfigError```

3. Ресурсы. Поставьте в requests память, которой на узле заведомо нет, например 1000000000Mi.

    [Ссылка на красный прогон](https://github.com/Estomeee/ml-pro/actions/runs/39051653578)

    [Ссылка на зелёный прогон](https://github.com/Estomeee/ml-pro/actions/runs/39051767572)

    В разделе "база" указано, что под с базой пересоздается и по нему падает таймаут.

### Вопросы
1. Первый удачный build ([ссылка](https://github.com/Estomeee/ml-pro/actions/runs/39016040372)) занял 1 минуту и 6 секунд.
Второй ([ссылка](https://github.com/Estomeee/ml-pro/actions/runs/39026240965)) 25 секунд.
```
#11 [stage-0 4/8] COPY pyproject.toml uv.lock ./
#11 CACHED

#12 [stage-0 5/8] RUN uv sync --no-dev --no-install-project
#12 CACHED

#13 [stage-0 6/8] COPY src/ src/
#13 CACHED

#14 [stage-0 2/8] COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
#14 CACHED

#15 [stage-0 7/8] RUN uv sync --no-dev
#15 CACHED

#16 [stage-0 3/8] WORKDIR /app
#16 CACHED

#17 [stage-0 8/8] COPY artifacts/ artifacts/
#17 CACHED
```

2. ImagePullBackOff это ошибка конкретного пода, а не итоговая ошибка выката.
3. GitHub → Settings → Secrets and variables → Actions.
    
    Пароль сохраняем как секрет DB_PASSWORD. GitHub передаёт значение в процесс. K8s команда использует эту переменную и создаёт iris-secrets в кластере.
    
    ConfigMap предназначен для несекретных настроек вроде LOG_LEVEL
4. Без needs tests задания tests и build смогут запускаться параллельно при push в main. 

    Если в main попадает коммит с ошибкой. Тесты падают, обнаружив ошибку, но образ уже опубликован, а деплой мог уже начаться.

5. `if: github.ref == 'refs/heads/main'`

    Чтобы не публиковать ещё не принятый в main код.
6. Оба пода подключаются к одной базе и могут одновременно вызвать init() при запуске.
`pg_advisory_xact_lock` позволяет выполнить инициализацию по очереди. 
7. __Pending__(Pod ещё не назначен на узел, контейнер не запущен) → __CreateContainerConfigError__(Pod уже назначен на узел, но kubelet не может получить обязательный Secret) → __CrashLoopBackOff__(Контейнер запускается, приложение пытается загрузить модель и завершается с ошибкой.)

### Журнал

Было очень много опечаток, под конец отдавал yml(ы) на проверку ии. 

## Звездочки


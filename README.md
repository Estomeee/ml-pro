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

    [Ссылка на зелёный прогон]()

    В 

### Журнал

В моедли входных данных `Features` забыл прописать `model_config = {"extra": "forbid"}` из-за этого не проходили соответсвующие тесты, не сразу понял в чем дело.

## Звездочки


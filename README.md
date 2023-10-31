# cv_app
## Запуск приложения
### Локально
1. Скопировать `.env.sample` в `.env` и заполнить любыми значениями.
2. Запустить базу данных.

   ```shell
   make database
   ``` 
   или 
   ```shell 
   docker compose up database -d
   ```
3. Установить зависимости
   ```shell
   pip install -r requirements/requirements.txt 
   ```
4. Запустить приложение
    ```shell
    PYTHONPATH=$(pwd) python src/main.py
    ``` 
# Janus - IA Model to identify emotions in text

Los resultados del experimento de comparar diferentes modelos de llm para identificar emociones en textos concluyen que el mejor modelo para esta tarea es una versión Fine-Tuneada de `gpt-4o-mini-2024-07-18`.

Por lo tanto, se desarrolla y despliega un prototipo funcional que permite realizar una valoración cualitativa de la efecitvidad del modelo.

## Instrucciones de despliegue

Se debe crear el archivo .env con las variables:

- **OPENAI_API_KEY** donde debe configurar el API KEY de la cuenta donde se encuentre asociado el modelo fine-tuneado, adicionalmente, esta cuenta debe tener créditos disponibles, se debe tener cuidado con la divulgación de la aplicación dado que cada request realizado al API de OpenAI tiene costo.

- **ID_MODEL_OPENAI** con el identificador del modelo finetuneado en la plataformar de OpenAI,

## Instrucciones para poblar la base de datos

Se usa sqlite para tener una tabla de ususarios e intentos diponibles por ususario, para crear y poblar la tabla correr en la terminal

python sqlite_seeder_users.py

Para consultar la información creada:

- instala sqlite in terminal: `sudo apt install sqlite3`
- activar sqlite en la bd de interes: `sqlite3 users.db`
- query users table: `SELECT * FROM users;`
- salir de sqlite: `.exit`

## Instrucciones para levantar la aplicación

`stremlit run app.py`

## Desplegar la app

- instalar gcloud cli: https://cloud.google.com/sdk/docs/install?hl=es-419
- Se debe tener los archivos:

* app.yaml
* requierements.txt
* app.py

- desplegar: gcloud app deploy

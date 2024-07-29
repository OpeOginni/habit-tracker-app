## Setting up & Seeding DB

- Move to the `backend-flask` directory with the command

```bash
cd backend-flask
```

- Create a `.env` file and copy the value in the `.env.example` file into it.

- Create the DB and load the schema using the following command

```bash
python3 ./db/load-schema.py
```

- Seed the DB with Mock data for testing using the following command

```bash
python3 ./db/seed-db.py
```

- Notice a file `habit-tracker.db` was created this is the SQLite DB.

## Running the Flask Backend Service

- Make sure your terminal is running on the `backend-flask` directory.
- Then run the following command to start the Flask Server on local host

```bash
flask run
```

- The local server should be running on the this URL -> `http://127.0.0.1:5000`

## Testing the Flask Backend Service

- Make sure your terminal is currently on the `backend-flask` directory.
- Then run the following command to run the Unit Tests

```bash
pytest
```

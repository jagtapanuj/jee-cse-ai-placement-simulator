# Run Local App

## 1. Run without installing anything

```bash
python -m app.pure_http_server
```

Then open `http://127.0.0.1:8000`.

## 2. Run tests

```bash
python -m unittest discover -s tests -v
```

## 3. Try CLI simulator

```bash
python -m app.simulator_core --rank 300 --rank-type MHT_CET_MERIT
python -m app.simulator_core --rank 300 --rank-type MHT_CET_MERIT --include-partial
```

## 4. Run FastAPI version

```bash
pip install -r requirements.txt
uvicorn app.api_app:app --reload
```

Then open `http://127.0.0.1:8000/docs`.

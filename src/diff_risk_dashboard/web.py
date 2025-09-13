# FastAPI opcional: no se importa en tiempo de análisis para evitar fallos de mypy/CI.
# Uso local:
#   python -m pip install "fastapi>=0.110" "uvicorn[standard]>=0.27"
#   python -m diff_risk_dashboard.web
from __future__ import annotations

from typing import Any

from .core import summarize_apv_json
from .report import to_markdown


def create_app() -> Any:
    fastapi = __import__("fastapi")
    responses = __import__("fastapi.responses", fromlist=["HTMLResponse"])
    FastAPI = getattr(fastapi, "FastAPI")
    HTMLResponse = getattr(responses, "HTMLResponse")

    app = FastAPI(title="Diff Risk Dashboard")

    @app.get("/", response_class=HTMLResponse)
    def index() -> Any:
        return HTMLResponse(
            content="""
<!doctype html><html><body>
  <h1>Diff Risk Dashboard</h1>
  <form action="/summarize" method="post" enctype="multipart/form-data">
    <input type="file" name="file" accept=".json"/>
    <button type="submit">Summarize</button>
  </form>
</body></html>
""",
            status_code=200,
        )

    @app.post("/summarize", response_class=HTMLResponse)
    async def summarize(file: Any) -> Any:
        data = await file.read()
        text = data.decode("utf-8")
        summary = summarize_apv_json(text)
        md = to_markdown(summary).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return HTMLResponse(f"<pre>{md}</pre>", status_code=200)

    return app


def main() -> None:
    uvicorn = __import__("uvicorn")
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()

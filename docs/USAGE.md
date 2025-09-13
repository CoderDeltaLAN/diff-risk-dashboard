# Diff Risk Dashboard — Usage

## Short wrappers
- `drt <apv.json | raw-json>`: tabla a color (TTY)
- `drb <apv.json | raw-json>`: barras (logs)
- `drj <apv.json | raw-json>`: JSON (CI)
- `drmd <apv.json | raw-json>`: Markdown (stdout)

```bash
drt examples/sample_apv.json
drt '{"by_severity":{"CRITICAL":0,"HIGH":1,"MEDIUM":1,"LOW":1,"INFO":0}}'
APV="/ruta/real/a/tu_apv.json"; drt "$APV"
```

Agregar al PATH (opcional):
```bash
mkdir -p ~/.local/bin && ln -sf "$PWD/bin/"* ~/.local/bin/ && hash -r
```

CLI crudo:
```bash
poetry run diff-risk <input> -f table|bar|json|md --no-exit-by-risk
```

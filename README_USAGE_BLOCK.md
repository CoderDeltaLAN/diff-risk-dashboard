<!-- diff-risk:usage:start -->

## 🚀 Usage

### Short commands (recommended)

```bash
# Demo incluida (color bonito)
drt examples/sample_apv.json

# JSON inline (comilla simple afuera, dobles adentro)
drt '{"by_severity":{"CRITICAL":0,"HIGH":1,"MEDIUM":1,"LOW":1,"INFO":0}}'

# Tu archivo real
APV="/ruta/real/a/tu_apv.json"; drt "$APV"
```

**Otros formatos**
```bash
drb "$APV"                 # barras (logs)
drj "$APV"                 # JSON (CI)
drmd "$APV" > report.md    # Markdown a archivo
```

**Forzar color en capturas**
```bash
script -qfc 'drt "$APV"' /dev/null
```

**Añadir wrappers al PATH (opcional)**
```bash
mkdir -p ~/.local/bin && ln -sf "$PWD/bin/"* ~/.local/bin/ && hash -r
```

**CLI crudo (equivalentes)**
```bash
poetry run diff-risk examples/sample_apv.json -f table --no-exit-by-risk
poetry run diff-risk examples/sample_apv.json -f bar   --no-exit-by-risk
poetry run diff-risk examples/sample_apv.json -f json  --no-exit-by-risk
poetry run diff-risk examples/sample_apv.json -f md    --no-exit-by-risk > report.md
```

<!-- diff-risk:usage:end -->

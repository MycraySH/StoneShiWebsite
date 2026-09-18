# Stone Shi CV Website

Dependency-free Python portfolio site for Tong (Stone) Shi's CV, transportation/GIS resume, work samples, cover letter, and research proposal.

## Run locally

```bash
python app.py
```

Then open `http://127.0.0.1:8000`.

## Public website

https://mycraysh.github.io/StoneShiWebsite/

The public site is generated from the same Python page functions:

```bash
python build_site.py
```

Commit the updated `docs/` output along with source changes. GitHub Pages
publishes the `docs/` folder on the `main` branch.

## Pages

- `/` - CV homepage, profile, PDF downloads, and work samples.
- `/work/<slug>` - detailed work-sample preview pages.
- `/cover-letter` - generalized cover letter based on the supplied sample, with firm-specific language removed.
- `/research-proposal` - research interest proposal.

# thedivproject.com

Website for **The Div Project**, a coworking house in South Miami (5798 SW 68th Street).

- `docs/` — the live site (English at `/`, Spanish at `/es/`). GitHub Pages serves this folder.
- `build.py` — regenerates `docs/` from the copy and settings at the top of the file. Run `python3 build.py`.
- `src/images/` — photos and logo.

## Common changes
- **Offices available:** change `AVAILABLE_OFFICES` in `build.py`, run the build, commit.
- **HubSpot:** paste the form or meetings link into `HUBSPOT_URL` at the top of the `JS` block in `build.py` (it ends up in `docs/assets/site.js`). Until then, every "Book a visit" button opens an email to info@thedivproject.com.
- **Text:** edit the `T['en']` / `T['es']` dictionaries in `build.py`.

# gati2026

Sites and games from the Great American Teach-In 2026, live at **https://gati.alexhackney.com**.

## Adding a class
Everything served lives in `public/` (class folders, `_lib/`, and the generated `index.html`).

1. Create a folder named for the class inside `public/`, e.g. `public/mrs-smith-3rd/`, with an `index.html`. Its `<title>` tag is used as its name on the landing page.
2. Run `python3 scripts/build-index.py` to refresh the landing page.
3. `git add -A && git commit -m "Add mrs-smith-3rd" && git push`

Forge deploys on push. The class appears at `https://gati.alexhackney.com/mrs-smith-3rd/`.

## Forge setup (one time)
1. Forge → server → **New Site**: domain `gati.alexhackney.com`, project type **Static HTML**, web directory `/public`.
2. Site → **Git Repository**: provider GitHub, repo `<owner>/gati2026`, branch `main`, uncheck "Install Composer dependencies".
3. Site → **Deployments**: enable **Quick Deploy**. Deploy script:
   ```
   cd $FORGE_SITE_PATH
   git pull origin $FORGE_SITE_BRANCH
   ```
4. DNS: add an `A` record `gati` on `alexhackney.com` pointing to the server IP.
5. Site → **SSL**: Let's Encrypt for `gati.alexhackney.com`.

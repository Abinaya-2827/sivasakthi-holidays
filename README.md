# Sivasakthi Holidays

A Django travel agency website for Sivasakthi Holidays, Madurai — built with
Django, Bootstrap 5, and Bootstrap Icons.

## Setup (SQLite — zero setup, recommended for local dev)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # defaults work as-is for SQLite

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_site       # adds demo destinations, packages, hero slides, etc.
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`. Admin panel at `/admin/`.

## Using MySQL instead

In `.env`, set:
```
DB_ENGINE=mysql
DB_NAME=sivasakthi_holidays
DB_USER=root
DB_PASSWORD=your-password
```
Then create the database first: `CREATE DATABASE sivasakthi_holidays CHARACTER SET utf8mb4;`
and run the same `migrate` / `seed_site` / `runserver` steps above.

## What's implemented

- **Home** — hero image slider (Bootstrap carousel), welcome section, Why
  Choose Us, Popular Destinations, Gallery preview, Testimonials, CTA.
- **About** — company story and the 8 service points from the brief
  (safe travel, family/college/corporate/temple/honeymoon tours, drivers, buses).
- **Destinations** — all 19 destinations from the brief, searchable, no
  prices shown, each with a WhatsApp "Book Now" button that opens a
  prefilled message.
- **Packages** — Family / College / Corporate / Temple / Honeymoon / Weekend
  tours, filterable by type, showing destination + duration + facilities
  only (no prices), WhatsApp Book Now.
- **Gallery** — responsive grid with hover overlay.
- **Payment** — UPI ID display + QR placeholder + screenshot upload form.
- **Contact** — address/phone/WhatsApp/Instagram/email, Google Maps
  placeholder, working contact form.
- **Login / Register** — standard Django auth.
- **Admin panel** — manage destinations, packages, gallery, hero slides,
  testimonials, why-choose-us items, contact messages, and payment proofs.
- **Extras** — sticky navbar with scroll shadow, AOS scroll animations,
  WhatsApp floating button, back-to-top button, fully responsive.

## Adding your real images

Everything currently uses generated placeholder images (in `static/images/`)
labelled with the item name, so the site looks complete out of the box.

**Option A — the fast way (recommended for adding many at once):**

The project includes a `media_imports/` folder with subfolders already
set up: `destinations/`, `packages/`, `hero/`, `gallery/`. Drop your
photos in:

- `media_imports/destinations/` — filename must match the destination
  name (e.g. `Kerala.jpg`, `kodaikanal.png`, `all-local-tamil-nadu-tours.jpg`
  all work — matching ignores case, spaces, and dashes).
- `media_imports/packages/` — filename must match the tour type
  (e.g. `Family Tour.jpg`, `temple-tour.png`).
- `media_imports/hero/` — any filename; each image becomes a new
  hero slide (title = the filename).
- `media_imports/gallery/` — any filename; each image becomes a new
  gallery photo (caption = the filename).

Then run:

```bash
python manage.py import_media
```

It updates matching destinations/packages in place, adds new hero
slides and gallery photos, and tells you about any file it couldn't
match (so you can check the spelling). Safe to re-run — it won't
duplicate gallery/hero entries you've already imported.

**Option B — one at a time:** upload directly through the admin panel
(`/admin/`) — each destination, package, hero slide, and gallery photo
has an image field you can edit individually.

**Logo and bus photos** aren't database-backed — they're static files.
Replace `static/images/logo.png` and `static/images/bus-placeholder.jpg`
directly, and they'll update everywhere they're used.

## Project structure

```
config/         # settings, root urls
core/           # home, about, contact, payment + shared templates/base
accounts/       # login, register, logout
destinations/   # 19 destinations, search, seed_site command
packages/       # 6 tour package types
gallery/        # customer photo gallery
static/         # CSS, JS, placeholder images
media/          # uploaded images (created at runtime)
```

## Notes

- Prices are intentionally not shown anywhere per the brief — Book Now
  buttons open WhatsApp with a prefilled enquiry message instead.
- The UPI QR code is a placeholder graphic, not a real scannable code —
  replace `static/images/upi-qr-placeholder.png` with your actual QR
  image (generate one from your UPI app) before going live.
- Login/Register use Django's built-in auth system — there's no
  paid-feature gating tied to it currently, it's there because the
  brief's navbar calls for it.

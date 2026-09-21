# Emerald Table Restaurant 🍽️

![alt text](static/images/Am-I-Responsive.png)


### A Django restaurant website for **Emerald Table Restaurant**.

A responsive restaurant website built with Django, featuring a homepage, menu display, account registration and an online booking system. Signed-in users can create, view, edit and delete their own bookings. Server-side validation checks guest numbers, booking dates and booking times.

The repaired application has passed the documented local automated
tests and live manual checks. Heroku release v26 deployed commit
23311993, matching GitHub revision 2331199 at verification.
Subsequent documentation-only commits may have newer identifiers.

See TESTING.md for results, evidence and explicitly recorded limitations.

**Live Link:** [Emerald Table Restaurant](https://emerald-table-restaurant-8293c189fc58.herokuapp.com/)

> **Portfolio project:** Emerald Table Restaurant is fictional.
> Contact details are illustrative, and bookings are demonstrations,
> not real reservations. The map is included to demonstrate location
> integration. Social links lead to external platforms, not official
> restaurant accounts.

## Database Design

See the [Entity Relationship Diagram and schema explanation](ERD.md)
for the user-to-booking relationship, field definitions, validation
rules and handling of legacy bookings.

## Features
- Modern homepage with hero image + Google Maps embed
- Menu page with dish layout (grouped into categories)
- Online booking form with opening-hours validation
- Booking success confirmation page
- Django admin panel for managing menu items and bookings
- Bootstrap 5 styling + emerald theme
- Production deployment setup with:

  - Gunicorn

  - WhiteNoise (static files)

  - Heroku-ready config

## Tech Stack

 - Backend: Django (Python)

- Frontend: HTML, CSS, Bootstrap 5

- Database: SQLite for local development; PostgreSQL on Heroku for production

- Deployment: Heroku

- Static Files: WhiteNoise

- Version Control: Git + GitHub

## Wireframes

![alt text](static/images/wireframe-desktop.png)
![alt text](static/images/wireframe-mobile.png)

created with [Lucid](https://lucid.app/documents/#/home?folder_id=recent)

## Design & Colour Palette

The website uses an emerald green theme to reflect the restaurant’s identity: natural, fresh, elegant, and premium.

The palette is based around:

- Emerald Green — the primary brand colour used for headings, accents, buttons, and key UI elements

- Off-White / Light Backgrounds — used to keep the layout clean and readable

- Dark Text / Charcoal — for strong contrast and accessibility

- Light grey / bright green — used for hover effects and subtle highlights to give a luxury feel


![alt text](static/images/color-palette.png)

# Pages Overview

## Homepage

The homepage introduces visitors to **Emerald Table Restaurant** with a modern hero section, strong branding, and a welcoming atmosphere. Users can quickly understand the restaurant’s concept and navigate to the menu or booking pages.

The homepage includes an embedded Google Map to demonstrate location
integration for this fictional portfolio restaurant.


![alt text](static/images/home-top.png)
![alt text](static/images/home-bottom.png)

## Menu Page

The menu page displays dishes grouped by category for easy browsing.
Users can explore available meals, view pricing, and get a clear overview of the restaurant’s offerings.
All menu items are managed dynamically via the Django admin panel.

![alt text](static/images/menu.png)

## Booking Page

The booking page allows customers to reserve a table through a user-friendly form.

- Features include:

  - Opening hours validation

  - Required field validation

  - Booking confirmation page

  - Edit Booking

  - Delete Booking

  - Backend storage of reservations

  - Reservations are stored in the database and can be managed through the Django admin interface.

![alt text](static/images/book-a-table.png)
![alt text](static/images/confirmation-page.png)
![alt text](static/images/django-administration.png)
![alt text](static/images/all_bookings.png)
![alt text](static/images/delete_booking.png)
![alt text](static/images/edit_booking.png)

## Getting Started (Local Setup)

These instructions are for a new local checkout on Windows using
PowerShell. The repaired application has been tested locally with
Python 3.13.14 and Django 6.0.8.

### 1. Clone the repository

```powershell
git clone https://github.com/darrio-dk08/emerald_table_restaurant.git
cd emerald_table_restaurant
```


### 2. Create and activate a virtual environment

With Python 3.13 installed:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, allow scripts for the current terminal
session and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
python -m pip check
```

Expected dependency-check result:

```text
No broken requirements found.
```

### 4. Configure local environment variables

Create a file named `.env` beside `manage.py`.

For a new installation, generate a development secret:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated value into `.env`:

```dotenv
SECRET_KEY=replace-with-your-generated-development-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=
```

Replace the placeholder before running Django. Keep this development
secret private and use a different secret for production.

With `DEBUG=True` and an empty `DATABASE_URL`, the application uses
local SQLite. The configured timezone is `Europe/Dublin`.

Do not overwrite an existing `.env` without reviewing its configuration.
Do not commit `.env`, local databases or private backups.

### 5. Apply migrations and check the application

```powershell
python manage.py migrate
python manage.py check
python manage.py showmigrations restaurant
```

Expected Django check:

```text
System check identified no issues (0 silenced).
```

The restaurant migrations should show:

```text
restaurant
 [X] 0001_initial
 [X] 0002_booking_owner_validation
 [X] 0003_booking_guest_limit_eight
```

### 6. Create an administrator

```powershell
python manage.py createsuperuser
```

Follow the terminal prompts. A fresh database does not include the
existing development database's menu items or bookings.

### 7. Start the local server

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ in a browser.

The development-server warning is expected locally. Production must
use a production application server.

## Accounts and Bookings

- Register at `/accounts/signup/`.
- Sign in at `/accounts/login/`.
- Create a booking at `/booking/`.
- View your own bookings at `/bookings/`.
- Use the booking's Edit or Delete buttons to manage it.
- Deletion requires a confirmation POST.
- Logout uses a POST form with CSRF protection.

Online bookings accept 1–8 guests. Larger groups should contact the
restaurant directly.

Bookings require a future date and time in 15-minute intervals.
Available times are 12:00–14:45 and 17:00–21:45, using Europe/Dublin
local time.

Server-side validation applies to both booking creation and editing.
Submitting an unchanged edit displays an informational message rather
than claiming that the booking changed.

Legacy bookings may have no owner. They are excluded from ordinary
users' booking lists. Ownership must not be guessed or assigned to
an arbitrary account.

## Admin Panel

Visit `/admin/` and sign in with a staff account that has the necessary
permissions.

Menu items and bookings are registered with Django's administration
interface.

## Testing

See the [homepage HTML validation evidence](TESTING.md#homepage-html-validation--repaired-version).

See [TESTING.md](TESTING.md) for test coverage, manual results,
historical evidence and recorded testing limitations.

Run the three verified automated test modules:

```powershell
python manage.py test restaurant.test_booking_security restaurant.test_accounts_and_times restaurant.test_page_links --verbosity 1
```

The recorded local result is 21 tests passing.

These tests cover booking validation, authentication, ownership
restrictions, CSRF protection, selected internal links, static asset
discovery and booking labels.

They do not establish that the deployed website, production database,
all accessibility requirements or Git history are secure.

## Deployment Status and Requirements

The application is deployed on Heroku using PostgreSQL, Gunicorn
and WhiteNoise.

### Deployment configuration

- `.python-version` specifies Python 3.13.
- `requirements.txt` contains the pinned application dependencies.
- Production requires a strong, private `SECRET_KEY`.
- `DEBUG=False`.
- `ALLOWED_HOSTS` contains the exact deployed hostname.
- `DATABASE_URL` supplies the PostgreSQL connection.
- `DISABLE_COLLECTSTATIC` is absent so static collection can run.
- Static-file storage uses Django's `STORAGES` configuration.

The Procfile contains:

```text
release: python manage.py migrate --noinput
web: gunicorn emerald_table_restaurant.wsgi:application
```

### Deploying an update

1. Run the relevant local checks and tests.
2. Commit and push the changes to GitHub.
3. In the Heroku application's Deploy tab, select the connected
   repository's `main` branch and choose Deploy Branch.
4. Confirm the build and release succeed.
5. Compare the deployed revision with the intended GitHub commit.
6. Check the affected functionality on the live website.

Automatic deployments were disabled during the repair process.

### Recorded production verification

- PostgreSQL was confirmed as the production database.
- Restaurant migrations 0001, 0002 and 0003 were applied.
- Fifteen menu items and five legacy bookings were restored;
  restored fields matched the exported fixtures.
- A new customer booking remained present after refreshing.
- Documented registration, login and booking CRUD checks passed.
- Observed homepage resource requests returned HTTP 200 or 304.
- HTTP redirected to HTTPS.
- The HTTPS homepage returned HSTS, nosniff and DENY headers.
- A login POST without a CSRF token returned HTTP 403.
- Heroku v26 deployed 23311993, matching GitHub 2331199 at verification.
- The homepage and menu loaded after that deployment.

Django's production deployment check reported no errors and two
warnings: security.W005 and security.W021. HSTS was enabled, while
includeSubDomains and preload remained disabled. These warnings
were reviewed and retained.

See TESTING.md for the scope and limitations of each check.

## Security Status

The local and Heroku SECRET_KEY values were replaced.

The personal GitHub repository's history was rewritten to remove
.env, db.sqlite3 and Python cache files, and replace the identified
historical secret. A scan of the cleaned reachable Git objects found
no occurrences of that identified secret. The cleaned history was
pushed to the personal repository.

This does not establish removal from separate repositories, forks,
cached copies or private backups. The separate Code Institute
submission copy has not been confirmed cleaned.

Live cross-account edit/delete page requests returned 404.
Local automated ownership tests passed. Direct cross-account POST
requests were not manually tested on the live deployment.

Environment files, database credentials and private backup exports
must remain outside version control.
## Bugs and Repair Notes

See [bugs.md](bugs.md) for the bug log and
[repair notes](PROJECT_IMPROVEMETS.md) for the repair summary.

## Credits

[Django Community](http://djangoproject.com/community)

[Stack Overflow](http://stackoverflow.com)

[The Code City](https://www.youtube.com/@TheCodeCity)

[Free Code Camp](https://www.youtube.com/@freecodecamp)

[Bootstrap Components](https://getbootstrap.com/docs/5.3/examples/)

[Project Ideas](https://data-flair.training/blogs/django-project-ideas/)

[Booking System](https://blog.devgenius.io/django-tutorial-on-how-to-create-a-booking-system-for-a-health-clinic-9b1920fc2b78)



### Heroku Live Deployment / Live Site Link:

[Emerald Table Restaurant](https://emerald-table-restaurant-8293c189fc58.herokuapp.com/)


### GitHub Source Code / GitHub Repository / Repo Link:

[E.T.R. GitHub Repo](https://github.com/darrio-dk08/emerald_table_restaurant)
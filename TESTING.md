# Testing

## Current repair verification

The results below describe local testing of the repaired application.
They do not establish that the repaired version is deployed on Heroku.

### Test environment

- Windows with VS Code and PowerShell.
- Active Python virtual environment: `.venv`.
- Python version reported locally: 3.13.14.
- Django version: 6.0.8.
- Local database: SQLite.
- Application timezone: Europe/Dublin.
- Local development uses DEBUG=True.
- Automated tests use a separate temporary test database.

### Reproduce the automated tests

Run these commands from the folder containing `manage.py`, with the
project's virtual environment active and local development settings loaded:

```powershell
python manage.py check
python manage.py test restaurant.test_booking_security restaurant.test_accounts_and_times restaurant.test_page_links --verbosity 2
```

Expected:

```text
System check identified no issues (0 silenced).
Found 21 test(s).
...
Ran 21 tests in ...
OK
```

Django creates a temporary test database, applies migrations and destroys
that test database afterward. This does not delete the development database.

Use local settings for these instructions. Do not point the test suite at
the production database.

### Recorded automated results

On 20 September 2026, both captured runs completed successfully:

- 21 tests passed in 8.807 seconds.
- 21 tests passed in 8.854 seconds.
- No failures or errors were reported.

The tested working tree included the link-test file subsequently committed
as `2fd58bc`. After the homepage changes, another run passed all 21 tests in
8.819 seconds. Those homepage changes were subsequently committed as
`a2614e7`.

Durations will vary. The important result is that every test passes.

### Automated coverage

| Test file | Tests | Coverage |
|---|---:|---|
| restaurant/test_booking_security.py | 10 | Booking creation, editing, deletion, ownership, anonymous access, CSRF, guest limits, past dates, invalid times and unchanged-edit feedback |
| restaurant/test_accounts_and_times.py | 8 | Registration, password validation, login/logout, redirect safety, account CSRF protection and booking-time boundaries |
| restaurant/test_page_links.py | 3 | Rendered internal links, form-action route resolution, referenced local static files and booking-field labels |

### User stories and evidence

| User story | Verification | Local result |
|---|---|---|
| As a visitor, I can create an account and log in | Automated account tests and manual browser journey | PASS |
| As a customer, I can create and view my booking | Automated creation test and manual detail check | PASS |
| As a customer, I can change a booking | Automated update test and manual refresh check | PASS |
| As a customer, I receive accurate feedback when nothing changed | Automated unchanged-edit test and manual message check | PASS |
| As a customer, I can cancel deletion without losing the booking | Manual Cancel test; automated test confirms GET does not delete | PASS |
| As a customer, I can delete my booking | Automated deletion test and manual refresh check | PASS |
| As a customer, my bookings are private from other customers | Automated foreign-user GET/POST tests and two-account browser test | PASS |
| As a visitor, I must log in before accessing booking pages | Automated anonymous-route tests and manual login redirect | PASS |
| As a customer, I cannot submit an online booking for more than eight guests | Automated create/edit tests and manual 8-versus-9 checks | PASS |
| As a customer, I cannot submit past dates or invalid booking times | Automated create/edit validation tests | PASS |
| As a customer, I can navigate between the application's pages | Automated internal-link tests and manual navigation checks | PASS |

### Manual browser checks performed

These results were observed and reported during local repair testing.
Screenshots should be added where listed evidence is still pending.

| ID | Action | Expected result | Observed result |
|---|---|---|---|
| M01 | Open Book a Table while logged out | Redirect to login | PASS |
| M02 | Register, then log in with a new account | Registration succeeds; My Bookings initially empty | PASS |
| M03 | Create a valid future booking | Saved booking shows the submitted details | PASS |
| M04 | Edit guest count and refresh the list | Changed value remains saved | PASS |
| M05 | Submit an unchanged edit | Message says no changes were made | PASS |
| M06 | Open deletion confirmation and select Cancel | Booking remains | PASS |
| M07 | Confirm deletion and refresh | Booking remains deleted | PASS |
| M08 | As Account B, visit Account A's edit and delete URLs | Both return 404; A's booking remains unchanged | PASS |
| M09 | Create and edit with eight guests | Accepted | PASS |
| M10 | Create and edit with nine guests | Rejected; invalid value not saved | PASS |
| M11 | Click Name, Email and Phone labels | Corresponding input receives focus | PASS |
| M12 | Change an edit field, then select Cancel | Original saved value remains | PASS |
| M13 | Narrow browser and toggle navigation | Menu opens/closes and map fits its card | PASS at the tested size; exact viewport not recorded |
| M14 | Log out | Return to homepage; logged-in navigation disappears | PASS |

The local 404 responses for another user's booking are intentional.
They prevent access to that record and are not broken-link defects.

### Limitations of the current evidence

- Static-file tests check that referenced local source files exist.
  They do not verify Heroku or WhiteNoise delivery.
- Internal-link tests do not check external websites or every possible
  database state.
- Form-action tests check URL resolution. The separate security tests
  exercise the specific POST operations listed above.
- Label tests do not establish full accessibility compliance.
- The recorded narrow-browser test does not establish responsiveness at
  all viewport sizes.
- Passing tests cover the cases asserted; they are not proof that every
  possible input or workflow is correct.

### Checks still outstanding

| Check | Status |
|---|---|
| Current rendered HTML validation on all page types and error states | PENDING |
| Current CSS validation | PENDING |
| Full keyboard navigation and accessibility review | PENDING |
| Responsive checks at recorded mobile, tablet and desktop widths | PENDING |
| External map, social and CDN links | PENDING |
| Correctness of displayed business location and contact details | PENDING |
| Production static-file delivery | PENDING |
| Live PostgreSQL connection, migrations and persistence | PENDING |
| Actual exposed-key rotation and remote Git-history cleanup | PENDING |
| Deployed commit matches the final GitHub revision | PENDING |
| Repeat customer and security workflows on the repaired live site | PENDING |

Do not mark these checks PASS until they have been performed and recorded.

### Evidence to retain

For final manual evidence, record the tested commit, date, browser,
viewport where relevant, action, expected result and actual result.

Use synthetic account and booking data. Do not include passwords, .env
contents, database credentials or real customers' personal details.

### Homepage HTML validation — repaired version

The rendered HTML from the logged-out local homepage
(`http://127.0.0.1:8000/`) was copied from the browser's
View Source page and checked using the W3C Nu HTML Checker.

**Result:** No HTML errors reported.

**Scope:** This result covers the submitted homepage HTML only.
Other pages and the deployed website require separate validation.

![Homepage HTML validation result](static/testing_screenshots/homepage-html-validation.png)

### Menu HTML validation — repaired version

**Environment:** Local development.
**Page:** http://127.0.0.1:8000/menu/
**Tool:** W3C Nu HTML Checker.

The rendered page source was copied from the browser's View Source
page and submitted to the validator.

**Result:** No errors or warnings reported.
**Live deployment verification:** Pending.

![Local menu HTML validation result](static/testing_screenshots/menu-html-validation.png)

## Live HTML Validation

The deployed Heroku pages were checked using the
[W3C Nu HTML Checker](https://validator.w3.org/nu/).

These results record live-page checks reported during testing.
Earlier local validation results are documented separately.

| Page | Result |
|---|---|
| Homepage | PASS — no errors or warnings reported |
| Menu | PASS — no errors or warnings reported |
| Login | PASS — no errors or warnings reported |
| Signup before repair | FAIL — four HTML errors |
| Signup after repair | PASS — no errors or warnings reported |

### Live Homepage HTML Validation

Page checked: `/`

![Live homepage HTML validation](static/testing_screenshots/live-homepage-html-validation.png)

### Live Menu HTML Validation

Page checked: `/menu/`

![Live menu HTML validation](static/testing_screenshots/live-menu-html-validation.png)

### Live Login HTML Validation

Page checked: `/accounts/login/`

![Live login HTML validation](static/testing_screenshots/live-login-html-validation.png)

### Live Signup HTML Validation — Initial Failure

Page checked: `/accounts/signup/`

The initial check reported four errors:

1. End tag `p` implied, but there were open elements.
2. Unclosed element `span`.
3. Stray end tag `span`.
4. No `p` element in scope but a `p` end tag was seen.

The signup template used `{{ form.as_p }}`, which placed the
password-help list inside paragraph/span markup that produced
invalid HTML nesting.

![Live signup HTML validation before repair](static/testing_screenshots/live-signup-html-before-fix.png)

### Live Signup HTML Validation — After Repair

**File repaired:** `restaurant/templates/registration/signup.html`.

The template now renders individual fields inside div containers.
Labels, password guidance, field errors, non-field errors and CSRF
protection are retained.

The corrected page passed local validation. The subsequent live
retest was reported as having no errors or warnings.

![Live signup HTML validation after repair](static/testing_screenshots/live-signup-html-after-fix.png)

### Validation Scope

These results cover the homepage, menu, login and signup pages.
They do not establish full accessibility or functional correctness.

Authenticated booking pages and form-validation error states
require separate HTML checks.

## Historical validation evidence

The screenshots and notes below relate to earlier project versions.
They are retained as historical evidence and must not be treated as
validation of the current repaired revision.

Return back to the [README.md](README.md) file.

## Code Validation

HTML

Minor bugs fixed

Used [HTML W3C Validator](https://validator.w3.org/nu/#textarea) to test HTML file, code was pasted from web page view source

![alt text](static/images/Html.png)

- fixed bug

![alt text](static/images/Html-fixed.png)

## CSS

Used [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator/validator) pass with no errors 

![alt text](static/images/css-valid.png)

## JavaScript

Used [JShint Validator](https://jshint.com/)


![alt text](static/images/JShint-valid.png)

### Bug fixed after replacing *const* to *var*

![alt text](static/images/JShint-valid-fix.png)


## Python

Used [PEP8 CI Python Linter](https://pep8ci.herokuapp.com/) (**autopep8** document formatting)

### Validation for Emerald App

- asgi.py 

![alt text](static/images/Python-Linter.png)

- settings.py

![alt text](static/images/Python-Linter1.png)

- urls.py

![alt text](static/images/Python-urls.png)

- wsgi.py

![alt text](static/images/Python-wsgi.png)


### Validation for Restaurant App 

- 0001_initial.py

![alt text](static/images/Python-initial.png)

- admin.py

![alt text](static/images/Python-admin.png)

- apps.py

![alt text](static/images/Python-apps.png)

- forms.py

![alt text](static/images/Python-forms.png)

- models.py

![alt text](static/images/Python-models.png)

- views.py

![alt text](static/images/Python-views.png)

- manage.py

![alt text](static/images/Python-manage.png)


## Lighthouse 

- desktop 

![alt text](<static/images/lighthouse desktop.png>)


- mobile 

![alt text](<static/images/lighthouse mobile.png>)
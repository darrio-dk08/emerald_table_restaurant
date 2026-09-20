# Assessment Repair Notes

This document records the current repair status. It does not guarantee
an assessment pass.

## Booking Functionality

Local browser checks have exercised booking creation, listing, editing
and deletion.

- Booking routes require authentication.
- Ordinary users can access only their own bookings.
- Requests for another user's booking return 404.
- Deletion requires a confirmation POST.
- Unchanged edits display an informational message.
- Online bookings are limited to 1–8 guests.
- Server-side validation rejects past dates and invalid booking times.

See [TESTING.md](TESTING.md) for the scope and results of these checks.

## Authentication and Automated Testing

The three locally executed test modules contain 21 passing tests:

- `restaurant/test_booking_security.py`: 10 tests.
- `restaurant/test_accounts_and_times.py`: 8 tests.
- `restaurant/test_page_links.py`: 3 tests.

Coverage includes account registration, login, logout, booking ownership,
CSRF protection, guest limits, date and time boundaries, selected internal
links, static asset discovery and booking labels.

Passing these tests does not verify every assessment criterion or the
production deployment.

## Database Design

See [ERD.md](ERD.md) for the models, fields and relationships.

The booking owner relationship is nullable to preserve legacy records.
Legacy records without an owner are excluded from ordinary users'
booking lists. Deleting a user with related bookings is protected.

Restaurant migrations 0001, 0002 and 0003 have been applied locally.
Production migration status remains unverified.

## Security Remediation Status

The current tracked files no longer include `.env`, the local SQLite
database or Python cache files. Ignore rules help prevent these files
from being added again accidentally.

Earlier Git commits still contain sensitive material. Removing a file
from tracking does not remove it from Git history.

Secret rotation, repository-history cleanup and verification of the
affected remote repositories remain outstanding.

## Interface and Documentation Repairs

- Added account navigation and POST logout.
- Added booking feedback and an unchanged-edit message.
- Associated booking labels with their form inputs.
- Clarified guest limits and available booking times.
- Improved the homepage heading and responsive map styling.
- Removed an unused navigation script.
- Added the ERD and linked it from the README.
- Documented verified tests separately from pending checks.

Historical screenshots may show earlier versions. They must not be
treated as evidence of the repaired interface without comparison.

## Remaining Verification

- Production settings, database, migrations and static assets.
- Deployed commit identity and live booking behaviour.
- Secret rotation and sensitive Git-history remediation.
- Complete HTML, CSS and Python validation.
- Remaining accessibility and responsive-layout checks.
- External links and restaurant contact information.
- Updated screenshots and final assessor-criterion review.

A complete PEP 8 review and an overall assessment pass are not claimed.
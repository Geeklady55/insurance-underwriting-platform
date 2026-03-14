
# Known Issues and Future Improvements

## Current Limitations

- No user authentication
- No audit logging
- SQLite used instead of PostgreSQL
- Frontend is intentionally basic
- No containerization yet
- No automated test suite yet

## Planned Improvements

### Authentication
Add JWT-based login for admin or underwriter workflows.

### Audit Logging
Track who created or updated application records.

### Database Upgrade
Replace SQLite with PostgreSQL for a more production-like design.

### CI/CD
Add GitHub Actions to run linting and tests on push.

### Docker
Add Docker support for easier local and deployment workflows.

### Frontend Dashboard
Replace the HTML form with a cleaner React-based dashboard.

## Why These Matter

These improvements would make the project more aligned with enterprise engineering environments and real insurtech platform workflows.

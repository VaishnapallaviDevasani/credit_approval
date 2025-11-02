
This repository contains my solution for the Backend Internship Assessment at Alemeno Pvt. Ltd.  
The project demonstrates my skills in **backend development**, **Docker-based deployment**, and serves RESTful APIs using **Django**, **Django REST Framework**, and **PostgreSQL**.
- Containerized with Docker & Docker Compose
- Ready for cloud deployment or local testing
- Hands-on with migrations, admin, and scalable API design

## Technologies Used

- Python 3.11
- Django & Django REST Framework
- PostgreSQL
- Docker (Dockerfile, docker-compose.yml)
- Gunicorn (production WSGI server)
- Git & GitHub for version control
### 1. Clone the repository
```bash
git clone https://github.com/your-username/credit_approval.git
cd credit_approval
```
### 2. Build & Start using Docker Compose
```bash
docker compose build
docker compose up
```
App runs at: [http://localhost:8000](http://localhost:8000)
### 3. Run migrations and create superuser
```bash
docker compose run web python manage.py migrate
docker compose run web python manage.py createsuperuser
```
(for Django Admin access at `/admin/`)
## API Endpoints

- `POST /api/register/` : Register new user/customer
- `POST /api/login/` : Login to account
- `GET /api/view-loan/<amount>/` : Check loan eligibility
- `GET /api/view-customer/<phone>/` : See customer record
- (See full API docs in backend assignment PDF or code comments)
## Admin Dashboard

- Visit `/admin/` to manage data/models
- Login with superuser credentials created above
## About Me

This assessment reflects my ability to:
- Build production-grade APIs (Python, Django, REST)
- Set up Docker-based dev & prod environments
- Work with relational databases and ORM migrations
- Support cloud deployment, reliability, and DevOps best practices

I'm eager to contribute to Alemeno's engineering team, work on real-world ML integrations, and grow as a Software Developer.
## Submission Requirements
- All files required for review are included (`Dockerfile`, `docker-compose.yml`, `requirements.txt`, API source code).
- Setup steps and local test instructions are above.
- For any review/demo, please run `docker compose up` and test via the provided API endpoints or admin dashboard.

**Thank you for reviewing my submission. Looking forward to your feedback!**
E-mail:vaishnapallavidevasani@gmail.com

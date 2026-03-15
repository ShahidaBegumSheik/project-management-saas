# Project Management SaaS

A **full‑stack Project Management SaaS platform** built with:

- **FastAPI Backend**
- **React + Vite Frontend**
- **MySQL Database**
- **JWT Authentication**
- **Stripe‑ready Billing Architecture**
- **Docker for database setup**
- **Automated Backend Testing**

The application demonstrates **production‑style architecture, clean code organization, and scalable SaaS design**.

---

# Tech Stack

## Backend

- FastAPI
- SQLAlchemy ORM
- MySQL 8
- Alembic (database migrations)
- JWT Authentication
- Pytest (automated testing)
- Razorpay billing architecture

## Frontend

- React 18
- Vite
- TailwindCSS
- React Router
- Axios
- Stripe.js (frontend library)
- Node.js
- Recharts

---

# Architecture Overview

Client (React / Swagger)  
↓  
FastAPI Routers (API Layer)  
↓  
Service Layer (Business Logic)  
↓  
SQLAlchemy Models  
↓  
MySQL Database

---

## Project Structure

```text
project-management-saas/
├── backend
│   ├── app
│   │   ├── core
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── pagination.py
│   │   │   └── security.py
│   │   ├── dependencies
│   │   │   ├── auth.py
│   │   │   └── roles.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── audit_log.py
│   │   │   ├── notification.py
│   │   │   ├── project.py
│   │   │   ├── project_activity.py
│   │   │   ├── project_comment.py
│   │   │   ├── refresh_token.py
│   │   │   ├── subscription.py
│   │   │   ├── team.py
│   │   │   ├── team_invitation.py
│   │   │   ├── team_member.py
│   │   │   └── user.py
│   │   ├── routers
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── analytics.py
│   │   │   ├── auth.py
│   │   │   ├── billing.py
│   │   │   ├── notifications.py
│   │   │   ├── projects.py
│   │   │   └── teams.py
│   │   ├── schemas
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── analytics.py
│   │   │   ├── auth.py
│   │   │   ├── notification.py
│   │   │   ├── project.py
│   │   │   ├── subscription.py
│   │   │   ├── team.py
│   │   │   └── user.py
│   │   ├── services
│   │   │   ├── activity_service.py
│   │   │   ├── analytics_service.py
│   │   │   ├── audit_service.py
│   │   │   ├── cache_service.py
│   │   │   ├── email_service.py
│   │   │   ├── invoice_service.py
│   │   │   ├── notification_service.py
│   │   │   ├── rate_limit_service.py
│   │   │   ├── razorpay_service.py
│   │   │   ├── stripe_mock.py
│   │   │   └── subscription_service.py
│   │   └── main.py
│   ├── tests
│   │   ├── conftest.py
│   │   ├── test_admin.py
│   │   ├── test_auth.py
│   │   ├── test_billing.py
│   │   ├── test_health_and_audit.py
│   │   ├── test_pagination.py
│   │   ├── test_project_and_team_flow.py
│   │   ├── test_project_comments.py
│   │   └── test_projects.py
│   ├── .env
│   └── requirements.txt
└── frontend
    ├── public
    │   └── vite.svg
    ├── src
    │   ├── api
    │   │   └── client.js
    │   ├── assets
    │   │   └── react.svg
    │   ├── components
    │   │   ├── Badge.jsx
    │   │   ├── Button.jsx
    │   │   ├── Card.jsx
    │   │   ├── Charts.jsx
    │   │   ├── EmptyState.jsx
    │   │   ├── Loader.jsx
    │   │   ├── Modal.jsx
    │   │   ├── Sidebar.jsx
    │   │   ├── StatCard.jsx
    │   │   ├── ToastViewport.jsx
    │   │   └── Topbar.jsx
    │   ├── contexts
    │   │   ├── AuthContext.jsx
    │   │   └── ToastContext.jsx
    │   ├── guards
    │   │   ├── RequireAuth.jsx
    │   │   └── RequireRole.jsx
    │   ├── layouts
    │   │   ├── AdminLayout.jsx
    │   │   ├── AuthLayout.jsx
    │   │   └── UserLayout.jsx
    │   ├── pages
    │   │   ├── admin
    │   │   │   ├── AdminDashboard.jsx
    │   │   │   ├── AdminMappingPage.jsx
    │   │   │   ├── AdminNotificationsPage.jsx
    │   │   │   ├── AdminSubscriptionsPage.jsx
    │   │   │   └── AdminUsersPage.jsx
    │   │   ├── auth
    │   │   │   ├── LoginPage.jsx
    │   │   │   └── RegisterPage.jsx
    │   │   └── user
    │   │       ├── BillingPage.jsx
    │   │       ├── NotificationsPage.jsx
    │   │       ├── ProjectsPage.jsx
    │   │       ├── TeamsPage.jsx
    │   │       └── UserDashboard.jsx
    │   ├── utils
    │   │   ├── formatters.js
    │   │   └── useUnreadNotifications.js
    │   ├── App.css
    │   ├── App.jsx
    │   ├── index.css
    │   └── main.jsx
    ├── .env
    ├── index.html
    ├── package-lock.json
    ├── package.json
    └── vite.config.js
```

---

# Authentication

Supported authentication flows:

- User registration
- JWT login
- OAuth2 form login (Swagger)
- JSON login endpoint (React frontend)
- Role‑based access control

Endpoints

```
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/login-json
```

---

# Project Management Features

Users can:

- Create projects
- View their projects
- Delete projects
- Manage project data

Endpoints

```
POST /api/v1/projects
GET  /api/v1/projects
```

---

# Subscription System

The platform supports **SaaS subscription billing**.

Users can:

- Upgrade to Pro and Email will be sent after subscription
- Cancel subscription and email will be sent after cancellation
- View billing status
- Create and Delete their projects

User Endpoints

Projects

```
POST /api/v1/projects
DELETE /api/v1/projects/{project_id}
```

Billing Endpoints

```
GET  /api/v1/billing/me
POST /api/v1/billing/checkout/pro
POST /api/v1/billing/mock-webhook/success
POST /api/v1/billing/mock-webhook/cancel
POST /api/v1/billing/mock-webhook/downgrade
```

---

# Admin APIs

Admins can monitor platform activity.

Capabilities

- View users
- View subscriptions
- View user‑subscription mapping

Endpoints

```
GET /api/v1/admin/users
GET /api/v1/admin/subscriptions
GET /api/v1/admin/mapping
```

Admin has access to billing endpoints also

---

# Audit Logging

All major actions are logged:

- user registration
- login
- project creation
- subscription checkout
- subscription update

Audit data stored in **audit_logs table**.

---

# Running MySQL with Docker

Pull MySQL image

```bash
docker pull mysql:8
```

Run container

```bash
docker run -d --name pm_mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=pm_saas mysql:8
```

Verify container

```bash
docker ps
```

Connect to MySQL

```bash
docker exec -it pm_mysql mysql -uroot -proot
```

---

# Backend Installation

Clone repository

```bash
git clone <repo-url>
cd project-management-saas/backend
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create `.env`

```
DATABASE_URL=mysql+pymysql://root:root@127.0.0.1:3306/pm_saas

JWT_SECRET_KEY=your_secret
ACCESS_TOKEN_EXPIRE_MINUTES=60

SEED_ADMIN=true
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin1234
```

Run migrations

```bash
alembic upgrade head
```

Run backend

```bash
uvicorn app.main:app --reload
```

Backend runs at

```
http://127.0.0.1:8000
```

Swagger docs

```
http://127.0.0.1:8000/docs
```

---

# Frontend Installation

# 1. Install NVM (Node Version Manager)

NVM allows installing and switching between multiple Node versions.

Download **nvm-windows** from:

https://github.com/coreybutler/nvm-windows/releases

Download:

```
nvm-setup.exe
```

Run the installer and finsih the installation.

---

# 2. Verify NVM Installation

Open **Command Prompt** or **PowerShell** and run:

```
nvm version
```

# 3. Install Node.js using NVM

List available Node versions:

```
nvm list available
```

Install LTS version:

```
nvm install 20.11.1
```

Activate the installed version:

```
nvm use 20.11.1
```

---

# 4. Verify Node and npm

Check Node:

```
node -v
```

```
npm -v
```

npm installs automatically with Node.

---

# 5. Create Vite + React frontend for the project

Navigate to the project root folder where we want the frontend.

```

Run:

```
npm create vite@latest
```

---

# 6. Vite Interactive Setup

### Prompt 1 – Project Name

Example:

```
frontend
```

### Prompt 2 – Framework

Select:

```
React
```

### Prompt 3 – Variant

Choose one:

```
TypeScript
TypeScript + SWC
JavaScript
JavaScript + SWC
```

Most common choice:

```
JavaScript
```

---

# 7. Navigate to frontend

```
cd frontend
```

---

# 8. Install Dependencies

```
npm install
```

This installs:

```
react
react-dom
vite
```

---

# 9. Install Additional Libraries

### React Router

```
npm install react-router-dom
```

### Axios

```
npm install axios
```

### Charts

```
npm install recharts
```

### Icons

```
npm install lucide-react
```

---

Create `.env`

```
VITE_API_BASE=http://127.0.0.1:8000/api/v1
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_example
```

Intall tailwind CSS

    npm install tailwindcss @tailwindcss/vite


Modify vite.config.js

    import { defineConfig } from 'vite'
    import react from '@vitejs/plugin-react-swc'
    import tailwindcss from '@tailwindcss/vite'

    // https://vite.dev/config/
    export default defineConfig({
      plugins: [react(), tailwindcss()],
    })

Run development server

```bash
npm run dev
```

Frontend runs at

```
http://localhost:5173
```

---

# Running Backend Tests

Run tests

```bash
pytest -q
```

Tests cover:

- Authentication
- Projects
- Billing
- Admin APIs
- Audit logging
- Health endpoint

---

# Security Features

- JWT authentication
- Password hashing with bcrypt
- Role‑based authorization
- Input validation with Pydantic

---

# Performance Considerations

- Indexed database columns
- Optimized queries

---

# Implementation of comments module

## Step 1: Creating models and relationships

We need to create models for the entities that have properties.
For comment module, we create one model named ProjectComment and hence one new table in the DB named project_comments
Table creation
For ProjectComment, we create a table in DB using

```
__tablename__ = "project_comments"
```

For its properties we decide the data types.
i) id – uniquely identifies a comment, becomes the primary key - int
ii) project_id – the project for which the comment is associated with - int
iii) author_id – the user who added the comments to the project. - int
iv) content – the comment contents - string
v) created_at – the date and time when the comment was added

We have to create relationships of the model ProjectComment to other models or relationships.
Already we have Project and User models.
The relationships:
Since, project_id is a primary key in Project table, it becomes the foreign key in the ProjectComment model.
And similarly, author_id is the primary key in User table, it becomes the foreign key in the ProjectComment table.

```
project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
```

   

```
author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
```

ondelete=”CASCADE” is used when we want to delete the child rows for a matching parent if that parent row is deleted.
So, if particular project_id gets deleted in the “projects” table, the comments for that project_id get deleted from the “project_comments” table. If we want to prevent deletion of the parent row as long as its children are present in the other table, we need to use ondelete=”RESTRICT”. Example, if user leaves the project, then his id is not deleted if his comments are still present in the projects page as in future we may want to find out which user had made that comment.

1. From Project to ProjectComment - one-to-many, from ProjectComment to Project – many-to-one
2. From User to ProjectComment – one-to-many, from ProjectComment to User – many-to-one
   We have to add the relationships to the ProjectComment model as well as Project and User models.
   These relationships become attributes of the models and can be used to navigate through the relationship structure without using the complex join queries.

Relationships:

1. ProjectComment :
   i) project - related to Project model
   ii) author - related to User model
   project = relationship("Project", back_populates="comments")
       author = relationship("User", back_populates="project_comments")
   project and author - attributes added to ProjectComment
2. Project
   i) comments - related to ProjectComment model

```
comments = relationship("ProjectComment", back_populates="project", cascade="all, delete-orphan")
```

     comments  - attribute added to Project

3.  User
    i) project_comments - related to ProjectComment
    project_comments = relationship("ProjectComment", back_populates="author", cascade="all, delete-orphan")
    project_comments – attribute added to User

Once the relationships are added, we can access for queries like:

```
SELECT users.email
```

FROM project_comments
JOIN users
ON users.id = project_comments.author_id

As

```
comment.author.email
```

“comment” – object of ProjectComment SQLAlchemy model – comment = db.query(ProjectComment).first()
“author” – a relationship defined in the ProjectComment model - author = relationship("User", back_populates="project_comments") – this says SQLAlchemy that author_id is from users.id and SQLAlchemy can automatically load the User object associated with the “comment”
“email” – field in the User model - email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False)

to get both the comments and the author’s email id:

comments = (db.query(ProjectComment).filter(ProjectComment.project_id == project_id).all()
for comment in comments:
print(comment.content)
print(

```
comment.author.email
```

)

Indexing:
To make retrieval fast using an attribute, we have to make that attribute as Index
In ProjectComment model, we use two indexes:

```
__table_args__ = (
```

        Index("ix_project_comments_project_created", "project_id", "created_at"),
        Index("ix_project_comments_author_id", "author_id"),
    )
Frequent queries using project_id and created_at – the rows are grouped by project_id first, then sorted by time
Similarly, for “author_id” as index to sort internally on this field.

Why to use back_populates in relationships

```
comments = relationship("ProjectComment", back_populates="project", cascade="all, delete-orphan")
```

SQLAlchemy understands that “comments” and “project” attributes represent the same relationship. Navigation through the relationship becomes easy : comment.project or project.comments. And SQLAlchemy keeps both sides synchronized.
Example: when we use comment.project = project, SQLAlchemy automatically updates project.comments.
Without back_populates, we have to manually maintain both sides like:
comment.project = project
project.comments.append(commend)

## Step 2: Creating Schemas – pydantic models for APIs

Used for the request and response in APIs, what data can be sent and what data can be received via API calls
Also, for input validation.
For ProjectComment, we add two schemas
i) ProjectCommentCreate
ii) ProjectCommentOut
These schemas can also include the attributes from the models which have relationship with them. Example, we include author_email from User model in the ProjectCommentOut schema.
Schemas help in hiding the fields from the requests and responses as not all fields should be exposed in the API endpoints.
Pydantic models help in validating the inputs that are used in API requests and responses.

## Step 3: Creating routers

API prefix: /projects
Common for all the endpoints:
Check if the project_id is present in the db, if not present or if the user is not part of the team for this project, raise HTTP exception 404 – not found and return. user gets access to project when he accepts the invite sent by the owner of the project. Post acceptance, the user can post comments, delete and view the comments in the projects page.

GET: "/{project_id}/comments" – users can list all the comments for a project_id
list_project_comments (project_id: int, db: Session = Depends(get_db),
                          user=Depends(get_current_user)
We have various roles in the application:
for checking if it is the current logged in user and granting him access for this endpoint - get_current_user (app/dependencies/auth.py). When a new user registers, with an emailed and password, a token is generated and stored in the browser. This token is used when this user logs in in the future to verify that the user is an authenticated user. The token is extracted when the request arrives for login. And the token is passed to get_current_user() where it is decoded and verified. Once verified, the User is retrieved from the db matching the user_id retrieved from the payload of the request.
So, here for the currently logged in user, the endpoint /api/v1/projects/{project_id}/comments will list all the comments for the project_id if this user is part of the project.

POST: "/{project_id}/comments" – users can call this endpoint to add a comment for a project_id
add_project_comment (project_id: int, payload: ProjectCommentCreate, db: Session = Depends(get_db), user=Depends(require_end_user)
The role used here is : require_end_user (app/dependencies/roles.py) – this end point allows only users to post comments. There are two roles (user or admin) - app/models/user.py . So, comments cannot be posted by the admin.

If user is valid and the project_id is available, create a ProjectComment object and store in the db for ProjectComment table “project_comments”
We also log this post comment activity in two tables – “audit_logs” and “project_activities”
There is a function to invalidate the cache as a new entry is committed to db now. The cache usually returns the cached information rather than fetching from the db. Its necessary to invalidate the cache for a particular user. The

```
invalidate_prefix(f"projects:{user.id}:")
```

command invalidates cache entries matching by searching using the prefix as “projects:1” or “projects:2” where 1 or 2 represent a user id.

DELETE: "/{project_id}/comments/{comment_id}" – only users who added the comments can delete them. Select for a project_id a particular comment_id to delete
Role is require_end_user, as admin cannot delete the comments
Check if the project_id exists in the “projects” table and also the user is part of the team in this project
If not, raise HTTP error 404, project not found.
If passed, find the first comment in the “project_comments” table using filter with the comment_id and the project_id, and delete it if found.
If not found the comment with the comment_id, raise HTTP 404, comment not found
If comment is found, then check if its author is the user who requested the delete api.
If user id doesn’t match with the author_id of the comment, raise HTTP 403 – forbidden as only authors of the comment can delete the comment
If it matches, delete the comment from the db and commit it.
Log this activity in the “audit_logs”

## Step 4: Alembic migrations to update the db

Since new model is created – ProjectComments, we have to update the db with these changes.
We do this by creating a alembic revision:

```
alembic revision -m "add project comments table"
```

Check the upgrade() method for create_table and create_index methods and downgrade() method for drop_index() and drop_table() methods. The order in which we create and drop are significant. We create table followed by creating indexes. During downgrade, we drop the indexes first then at the end we drop the table itself.
Apply the alembic migrations using the command:

```
alembic upgrade head
```

               or by using the revision id:
                             alembic upgrade <revision_id>

## Step 5: Designing the front end.

Create a folder "api" under the "frontend" folder and inside it create a file client.js

client.js is used for creating a centralized HTTP client that the frontend uses to communicate with the backend API. Its implemented using axios. The app files imports this client. It provides centralized backend URL, attaching the jwt tokens to every request. When our app runs, and we check the console using the F12 key on the browser, we can use the localStorage methods to setItem, getItem, clear. We use these to set, get and clear tokens and users for the authorization session. The app attaches the login token to every request - `Bearer ${token}`
create a folder named “components” inside the “src” folder. Inside this we can add the reusable React components. Examples: Card for container layouts, Button, Charts, Modal (for pop up dialogs), We import these components in the pages we are displaying (like Projects page, or Notifications page) and call the methods on certain event handlers.
<button onClick={openProjectDetails}>View Project</button>
openProjectDetails is a event handler function called when the button is clicked where we can call the backend APIs and get the response from the API. This response can be then displayed in the various components.
Create “contexts” folder inside “src” folder. Inside this we create “AuthContext.jsx” file. It manages the authentication state across the entire application. Also, we have the “ToastContext.jsx” file inside the “contexts” folder. This is used to show temporary notification messages (toasts) across the app. These are small popup messages that appear briefly to inform the user about somethings like success message, error message, warnings, etc. In Comments module, small popup messages that notify about errors appear on the Projects page.
Create a “guard” folder and inside that add the two files “RequireAuth.jsx” ( for user authentication before accessing the page) and “RequireRole.jsx” (for restricting access based on user role). We use these inside the JavaScript for controlling the access to the page and authenticating the user when login.
“AuthLayout.jsx” provides 2-column screen and renders the child route with <Outlet />, child pages LoginPage.jsx and RegisterPage.jsx supply the actual form UI. “AuthLayout.jsx” is connected from frontend/src/App.jsx
“AuthContext.jsx” contains the authentication logic used by both LoginPage.jsx and RegisterPage.jsx
In the src/pages/user/ProjectPage.jsx, we have added two methods
i) handleAddComment(event)
ii) handleDeleteComment(commentId)

i) handleAddComment(event) :
Check if project is selected, if not selectedProject, we return as comments are associated with project
Trim the comment
Send a post request to /projects/${selectedProject.id}/comments and wait for the response
The response newcomment is appended to the list of comments

ii) handleDeleteComment(commentId):
If not selectedProject, return
If not confirmation of delete, return
Send a post request to /projects/${selectedProject.id}/comments/${commentId}. commentId is deleted from the list of comments
We set the comments to new list which doesn’t have the deleted comment
Array.isArray(prev)? prev.filter((comment) => comment.id !== commentId): []
For both add comment and delete comment , pop up toast messages are display to signify addition or deletion
push("Comment added", "success");
push("Comment deleted", "success");

Inside the react page that is returned, we call these handleAddComment and handleDeleteComment onSubmit. For adding comment we have a form inside which there is a textarea where the comment matter is entered and there is a button to submit. For handleDeleteComment we pass the comment.id and after that comment is deleted from the list, the modified list is returned which is then displayed.
Inside the routers for delete comment, we check for the author of the comment to allow for deletion of the comment :
@router.delete("/{project_id}/comments/{comment_id}")
def delete_project_comment(
    project_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_end_user),
    ):
…
…
if comment.author_id != user.id:
        raise HTTPException(status_code=403, detail="Only the comment owner can delete it")

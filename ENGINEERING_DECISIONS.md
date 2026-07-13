# Engineering Decisions — Task Manager API

## 1. Framework Selection: FastAPI
I chose FastAPI over traditional frameworks like Django or Flask for  benefits such as:
* **High Performance:** Built on top of Starlette and Uvicorn, making it one of the fastest Python frameworks available.
* **Asynchronous Support:** Native support for `async/await` syntax allows efficient handling of concurrent network requests.
* **Automatic Documentation:** Out-of-the-box generation of interactive OpenAPI (Swagger) documentation simplifies API testing.
* **Data Validation:** Seamless integration with **Pydantic v2** ensures strict data parsing and automatic error responses.

## 2. Database & ORM Strategy
* **PostgreSQL:** It was selected as the primary relational database (RDBMS) for its robust support for ACID compliance and structural data integrity.
* **SQLAlchemy:** Utilized as the Object-Relational Mapper (ORM) to interact with the database using clean, Pythonic object-oriented principles.
* **Alembic:** Integrated as the database migration tool to track changes dynamically without manual database manipulation.

## 3. Real-World Challenges & Resolved Bugs

During the containerization and deployment process, I hit and successfully resolved several structural hurdles:

* **Bug 1: The "Ghost Package" Linter Error (VS Code)**
  * *Issue:* Even though pip install sqlalchemy ran successfully in the terminal, VS Code threw bright yellow/red squiggly lines under my imports
  * *Resolution:* I understood that VS Code was just pointing to my computer's global Python interpreter instead of my virtual environment. Switching the interpreter to (venv) cleared the errors.

* **Bug 2: Uvicorn crash**
  * *Issue:* I moved my main.py file inside the app/ folder, but when I tried to start the server with uvicorn main:app, it crashed.
  * *Resolution:* I changed the command to uvicorn app.main:app --reload, which explicitly told Uvicorn exactly which folder to look inside.

* **Bug 3: NameError**
  * *Issue:* Alembic generated a script to build my tables but the script crashed with a NameError.This was because Alembic automatically wrote a piece of code using sqlmodel but it forgot to add import sqlmodel at the very top of its own script. It tried to use a tool it hadn't unpacked yet
  * *Resolution:* I manually added import sqlmodel to the top of the file which let the script run perfectly.

## 4. Database Design
* The project uses 8 tables. User is the base,everything else connects back to it. A User can be part of multiple Teams and the connection between them is stored in a separate TeamMembership table which also holds the user's Role in that team. This design means one user can be an Owner in one team and a Viewer in another.
A Team has multiple Projects, and each Project has multiple Tasks. Tasks can be assigned to multiple users through a TaskAssignment table which is a junction table that handles the many-to-many relationship between Tasks and Users. Each Task can have multiple Comments and every Comment knows which Task it belongs to and which User wrote it. Also, an ActivityLog table records important events across the team which stores a text description of what happened, who did it and which team it happened in.

## 5. Authentication Reasoning
I used JWT (JSON Web Tokens) over session-based authentication as the token itself carries the user's identity and expiry time signed with a secret key. This means the API can verify any request without hitting the database just to check if someone is logged in.

## 6. Authorization
* The system has four roles: Owner, Maintainer, Member and Viewer. Every user who joins a team gets one of these roles stored in the TeamMembership table.
All permission logic lives in a single file called permissions.py which contains a dictionary called ROLE_PERMISSIONS. This matrix maps every possible action to which roles are allowed to perform it. Before any sensitive action is executed in any route the code calls check_permission(role, action). If the role isn't allowed, it raises a 403 error immediately and the route code never runs.
The four roles work like this:
 * Owner — has full access to everything including deleting projects, changing roles and removing members
 * Maintainer — can manage projects and tasks and invite members but cannot change roles or remove members
* Member — can create and edit tasks but cannot delete them or manage team membership
* Viewer — read-only access plus the ability to add comments but cannot create or change anything else

## 7. Tradeoffs
* I chose JWT over session-based auth as it is simpler and statelessbut means tokens can't be instantly revoked before they expire.
* I skipped Redis/caching to keep the project simple for this timeline

## 8. Future Improvements
Some of the changes which I could've done:
* Add email notifications when a task is assigned to you
* Implement soft deletes so nothing is permanently lost
* Add a file attachment feature so users can attach documents to tasks

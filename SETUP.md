# Python Environment Setup Instructions

1. **Install Python 3.10+**
   - Download from https://www.python.org/downloads/

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```cmd
     venv\Scripts\activate
     ```

4. **Upgrade pip**
   ```bash
   pip install --upgrade pip
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Set up environment variables**
   - Create a `.env` file at the project root with your PostgreSQL and mail settings.

7. **Run migrations**
   ```bash
   flask db init
   flask db migrate -m "Initial schema"
   flask db upgrade
   ```

8. **Start the application**
   ```bash
   flask run
   ```

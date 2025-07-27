# 🎮 Dareora

![Dareora Logo Placeholder](https://placehold.co/400x150/00ffcc/000000?text=Dareora+Logo)

## ✨ Dare to Discover, Dare to Achieve!

Dareora is an exhilarating web application designed to be a vibrant community where users can challenge themselves and others with exciting dares. This platform provides a space to connect, compete, and conquer, pushing limits and finding new adventures together.

This project is being developed by a dedicated team, leveraging the power of Django for a robust backend and modern web technologies for a dynamic frontend.

## 🚀 Features (Current & Planned)

* *Post Dares:* Users can create and share their unique dares, with options for public visibility or private sharing.
* *Explore Dares:* Discover a wide variety of trending and challenging dares posted by other users.
* *Leaderboard:* A competitive ranking system based on points earned from completing dares.
* *Community Engagement:* Interact with other users through comments, likes, and follows.
* *User Reviews:* Provide feedback and ratings on completed dares.
* *User Authentication:* Secure user registration, login, and profile management.
* *Responsive Design:* A seamless and optimized experience across all devices (mobile, tablet, desktop).
* *Theme Toggle:* Switch between dark and light modes for personalized viewing, with preference saving.

## 🛠 Technologies Used

Dareora is built with a powerful combination of frontend and backend technologies:

### Frontend
* *HTML5:* For structuring the web content.
* *CSS3:* For styling, animations, and ensuring a fully responsive user interface.
* *JavaScript:* For interactive elements, dynamic content, and client-side logic (e.g., image sliders, theme toggling).

### Backend
* *Django:* A high-level Python web framework that encourages rapid development and clean, pragmatic design. It handles:
    * User authentication and authorization.
    * Database interactions (ORM).
    * API endpoints for dare management, user profiles, and more.
* *Python:* The programming language powering the Django backend.
* *PostgreSQL (Recommended):* A powerful, open-source object-relational database system for robust data storage. (Can be configured for SQLite for local development ease).

## ⚡ Getting Started

Follow these instructions to get your development environment set up and run the Dareora project locally.

### Prerequisites

Before you begin, ensure you have the following installed on your system:

* *Python 3.8+*
* *pip* (Python package installer)
* *Git*

### Installation

1.  *Clone the repository:*
    bash
    git clone [https://github.com/yashika0128/Dareora.git](https://github.com/yashika0128/Dareora.git)
    
    

2.  *Navigate to the project directory:*
    bash
    cd Dareora
    

3.  *Create and activate a Python virtual environment:*
    It's highly recommended to use a virtual environment to manage project dependencies.

    bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    

4.  *Install backend dependencies:*
    Install all required Python packages using pip.

    bash
    pip install -r requirements.txt
    
    *(Note: You will need to create a requirements.txt file by running pip freeze > requirements.txt after installing initial Django and other necessary packages.)*

5.  *Database Setup:*

    * *For local development (using SQLite, default Django):*
        No additional setup is usually required. Django will create a db.sqlite3 file automatically.

    * *For production or more robust local development (using PostgreSQL):*
        * Ensure PostgreSQL is installed and running.
        * Create a new database for Dareora (e.g., dareora_db).
        * Update your Dareora/settings.py file with your PostgreSQL database credentials.

6.  *Run Database Migrations:*
    Apply the initial database schema.

    bash
    python manage.py migrate
    

7.  *Create a Superuser (Optional but Recommended):*
    This allows you to access the Django admin panel.

    bash
    python manage.py createsuperuser
    
    Follow the prompts to create your superuser account.

8.  *Run the Development Server:*
    Start the Django development server.

    bash
    python manage.py runserver
    
    The application will typically be accessible at http://127.0.0.1:8000/.

## 💡 Usage

* *Access the Application:* Open your web browser and navigate to http://127.0.0.1:8000/.
* *Django Admin:* Access the administrative interface at http://127.0.0.1:8000/admin/ using the superuser credentials you created.
* *Frontend Interaction:*
    * Use the navigation links to explore various sections.
    * Interact with the theme toggle (moon/sun icon) to switch between light and dark modes.
    * The homepage slider will automatically advance, or you can use the dots for manual navigation.

## 🤝 Contributing

We welcome contributions from all team members! Here's a basic workflow:

1.  *Fork and Clone:* Ensure you have cloned the main repository.
2.  *Create a New Branch:* Always create a new branch for your features or bug fixes.
    bash
    git checkout -b feature/your-feature-name
    
3.  *Make Your Changes:* Implement your code, adhering to the project's coding standards.
4.  *Test Your Changes:* Ensure your new features work as expected and don't introduce regressions.
5.  *Commit Your Changes:* Write clear and concise commit messages.
    bash
    git commit -m "feat: Add new user profile page"
    
6.  *Push to Your Branch:*
    bash
    git push origin feature/your-feature-name
    
7.  *Create a Pull Request (PR):* Open a pull request from your branch to the main or develop branch of the main repository. Describe your changes thoroughly.
8.  *Code Review:* Participate in code reviews with your team.


## 📞 Contact

For any questions or collaboration inquiries, please reach out to the team leads or use the project's communication channels.

Project Link: [https://github.com/yashika0128/Dareora](https://github.com/yashika0128/Dareora)
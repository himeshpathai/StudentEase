# StudentEase
Introduction
The StudentEase project is a comprehensive Tkinter-based application designed to facilitate various functionalities required by both students and professors. The application aims to create a seamless and interactive environment for managing academic tasks such as assignment submissions, video lectures, file downloads, and chat interactions. This report provides an overview of the project's key features, modules, and implementation details.

Project Objective
The primary objective of the StudentEase project is to develop a user-friendly and efficient system for managing academic activities. The application allows teachers to post assignments, students to submit their work, and both parties to interact with the system in a streamlined manner. Additionally, the project includes functionalities for video lectures and database interactions.

Key Features
Login System:

Separate login pages for students (login_page_s.py) and professors (login_page_t.py).
Secure authentication mechanism to ensure only authorized users can access the system.
Dashboards:

Professor's Dashboard (pro2.py): Allows professors to manage their classes, post assignments, and view submissions.
Student's Dashboard (stu_dashboard.py): Provides students with access to assignments, lecture videos, and other academic resources.
Class Management:

Modules like d10a.py, d10b.py, and d10c.py handle different classes and subjects.
Each class module provides functionalities for viewing and managing class-specific tasks.
Assignment Submission:

GUI for teachers to post assignments with deadlines.
Interface for students to submit assignment files online.
Video Lectures:

Integration with an RFID system (server2.py) to start video recording based on valid RFID entries.
Upload and access video lectures from the database.
File Management:

Upload, display, and download files.
Data from the files table and announcements table are displayed together in the file_list_frame, ordered by timestamp.
Chat Feature:

Chatbox for students and professors to interact.
Messages stored in the 'announcements' database table.
GUI Navigation:

Seamless navigation between different canvases and frames.
Canvases and frames are managed across different files, allowing modular development and maintenance.
Implementation Details
Tkinter Framework:

The application utilizes the Tkinter framework for GUI development.
Multiple frames and canvases are used to create a dynamic and interactive interface.
Database Integration:

MySQL is used for database operations, ensuring robust data management.
Tables for storing user data, assignments, files, announcements, and video lecture metadata.
Modular Design:

Each module is designed to handle specific functionalities, promoting code reusability and modularity.
Modules like dash.py for login buttons, pro2.py for the professor's dashboard, and class-specific modules ensure a clean code structure.
RFID and Video Integration:

The server2 module integrates with an RFID system connected to an ESP8266.
Valid RFID entries trigger video recording, which is then uploaded to the database.
Challenges and Solutions
Login Loop Issue:

Initially, importing the stu_dashboard module caused the dashboard to appear before the login page.
The issue was resolved by ensuring proper control flow and module imports.
Global Variable Usage:

The global variable global_username is used to store and access the username across different functions and modules.
Ensured secure handling and accessibility of the variable without running the login loop repeatedly.
Database Synchronization:

Managing real-time updates and synchronization between different database tables.
Implemented efficient queries and data retrieval mechanisms to maintain consistency.
Conclusion
The StudentEase project successfully meets its objectives by providing a comprehensive platform for managing academic activities. With features like secure login, assignment submission, video lectures, and interactive chat, the application enhances the learning experience for both students and professors. The modular design and robust database integration ensure scalability and ease of maintenance. The project demonstrates effective use of Tkinter for GUI development and MySQL for backend operations, making it a valuable tool for educational institutions.

Future Enhancements
Enhanced Security:

Implementing advanced encryption for data transmission and storage.
Multi-factor authentication for user login.
Mobile Compatibility:

Developing a mobile version of the application for broader accessibility.
Additional Features:

Integration with online meeting platforms for live lectures.
Automated grading and feedback system for assignments.
Acknowledgments
This project was developed with the guidance and support of my professors and peers. Special thanks to all those who provided valuable feedback and suggestions during the development process

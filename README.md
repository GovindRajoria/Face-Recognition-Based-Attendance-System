
# Face Recognition-Based Attendance System  

## Overview  
The **Face Recognition-Based Attendance System** is an AI-powered application designed to automate attendance management. It utilizes real-time facial recognition technology to replace traditional methods like roll calls or sign-in sheets, ensuring accuracy, efficiency, and convenience.  

Key features include real-time face detection and recognition, user management (adding/removing users), and a web-based interface for easy interaction. Built with Python, Flask, OpenCV, and scikit-learn, this system offers a modern, scalable, and reliable solution for attendance tracking in educational and organizational settings.  

---

## Features  
- **Real-time Face Recognition**: Detects and identifies faces from a webcam feed.  
- **User Management**: Add, delete, or update users via the admin interface.  
- **Web-based Interface**: User-friendly interaction using a Flask-based web application.  
- **Attendance Recording**: Logs attendance with timestamps in CSV files.  
- **Robust Algorithms**: Uses Haar Cascade for detection and K-Nearest Neighbors (KNN) for recognition.  

---

## System Requirements  

### Hardware  
- **Computer**: Intel Core i5 or higher, 8GB+ RAM.  
- **Webcam**: 720p+ resolution, 30 fps or higher.  
- **Storage**: 256GB SSD (minimum).  

### Software  
- Python 3.6+  
- Flask  
- OpenCV  
- scikit-learn  
- Pandas  
- Jinja2  

---

## Installation  

1. **Clone the Repository**:  
   ```bash  
   git clone https://github.com/your-username/face-recognition-attendance.git  
   cd face-recognition-attendance  
   ```  

2. **Install Dependencies**:  
   Install the required Python libraries using pip:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. **Run the Application**:  
   Start the Flask server:  
   ```bash  
   python app.py  
   ```  
   Access the application at `http://localhost:5000`.  

---

## Usage  

1. **User Registration**:  
   Add new users by capturing their images via the admin interface.  
2. **Real-time Recognition**:  
   Start the webcam feed to detect and log attendance automatically.  
3. **Attendance Logs**:  
   Check attendance records saved as CSV files in the `Attendance` directory.  

---

## Challenges and Future Scope  

### Challenges  
- Low-light conditions may affect recognition accuracy.  
- Scalability for larger datasets requires optimization.  

### Future Improvements  
- Integration with mobile applications.  
- Use of advanced AI models like CNNs for enhanced performance.  
- Support for multi-location attendance tracking.  

---

## Author  
**Govind Kumar**  

Feel free to contribute to the project by submitting issues or pull requests.  

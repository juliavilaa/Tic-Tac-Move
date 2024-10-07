# Tic-Tac-Move

*Tic-Tac-Move* is a project that combines the classic Tic-Tac-Toe game with physical movement detection. The losing player must perform a physical exercise as a "penalty," choosing between running on a treadmill or doing military press repetitions. The application uses the camera to ensure the exercise is performed correctly through movement detection.

## 🚀 Features

- 🎮 Play *Tic-Tac-Toe* in a user-friendly graphical interface.
- 🏋‍♂ The losing player must perform one of two exercises as a penalty: running or military press.
- 📷 Physical movement detection using the camera, powered by technologies like mediapipe and opencv-python.
- 💻 Seamless hardware integration (camera) for automatic exercise verification.

## 📋 Requirements

- *Python 3.11*
- Libraries specified in requirements.txt
- A connected camera for movement detection

## ⚙ Installation

1. Clone the repository to your local machine:

    bash
    git clone https://github.com/your-username/tic-tac-move.git
    cd tic-tac-move
    

2. Create and activate a virtual environment:

    - On Windows:
      bash
      python -m venv venv
      venv\Scripts\activate
      

    - On MacOS/Linux:
      bash
      python3 -m venv venv
      source venv/bin/activate
      

3. Install the required dependencies:

    bash
    pip install -r requirements.txt
    

## ▶ Running the Application

To run the application, use the following command:

```bash
python main.py 
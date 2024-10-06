import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose

def detect_military_press(frame, pose):
    """Detecta si los brazos están en posición baja o alta en un military press."""
    results = pose.process(frame)
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y

        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y

        # Detectar la posición alta: cuando ambas muñecas están por encima de los hombros
        if left_wrist < left_shoulder and right_wrist < right_shoulder:
            return "up"  # Marcamos que los brazos están arriba
        # Detectar la posición baja: cuando ambas muñecas están debajo de los hombros
        elif left_wrist > left_elbow and right_wrist > right_elbow:
            return "down"  # Marcamos que los brazos están abajo
    
    return None  # No se detectó posición clara

def count_reps(cap):
    """Función que cuenta hasta 15 repeticiones del ejercicio military press."""
    count = 0
    current_position = "down"  # Iniciar asumiendo que los brazos están en posición baja
    is_going_up = False  # Controla si el movimiento actual es hacia arriba
    
    # Inicializar el detector de pose de MediaPipe
    with mp_pose.Pose() as pose:
        while count < 15:
            ret, frame = cap.read()
            if not ret:
                print("No se pudo acceder a la cámara")
                break

            # Detectar la posición de los brazos (arriba o abajo)
            new_position = detect_military_press(frame, pose)

            # Si estamos en posición baja y empezamos a subir
            if new_position == "up" and current_position == "down":
                is_going_up = True  # Los brazos están subiendo
                current_position = "up"  # Actualizamos la posición

            # Si hemos subido y ahora los brazos están bajando
            elif new_position == "down" and current_position == "up" and is_going_up:
                count += 1  # Contamos una repetición completa
                print(f"Repeticiones: {count}")
                is_going_up = False  # Reseteamos el estado
                current_position = "down"  # Actualizamos la posición

            # Mostrar el número de repeticiones en el video
            cv2.putText(frame, f"Reps: {count}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Mostrar el video
            cv2.imshow('Military Press', frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    print("¡15 repeticiones completadas!")
    cap.release()
    cv2.destroyAllWindows()

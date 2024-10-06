import time
import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils  # Para dibujar los puntos y el esqueleto

def detect_running(frame, pose, prev_knee_positions, min_movement=0.01):
    """Detecta si la persona está corriendo utilizando el movimiento de las rodillas."""
    results = pose.process(frame)
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Dibujar los puntos clave y el esqueleto en el frame
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))

        # Coordenadas de las rodillas (usamos solo estos puntos para correr)
        left_knee_y = landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y
        right_knee_y = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y

        # Comparar las posiciones actuales de las rodillas con las posiciones anteriores
        left_knee_moved_up = left_knee_y < prev_knee_positions[0] - min_movement
        left_knee_moved_down = left_knee_y > prev_knee_positions[0] + min_movement

        right_knee_moved_up = right_knee_y < prev_knee_positions[1] - min_movement
        right_knee_moved_down = right_knee_y > prev_knee_positions[1] + min_movement

        # Actualizar las posiciones previas
        prev_knee_positions[0] = left_knee_y
        prev_knee_positions[1] = right_knee_y

        # Verificar si ambas rodillas han subido y bajado
        if (left_knee_moved_up or right_knee_moved_up) and (left_knee_moved_down or right_knee_moved_down):
            return True  # Se detectó un ciclo de correr

    return False

def run_timer(cap):
    """Función para ejecutar un temporizador de 1 minuto cuando se detecta correr."""
    timer_started = False  # El temporizador no empieza hasta que se detecta correr
    start_time = None
    detection_threshold = 2  # Umbral para comenzar el temporizador (más detecciones consecutivas)
    detection_count = 0  # Contador de detecciones de correr
    prev_knee_positions = [0, 0]  # Posiciones previas de las rodillas

    # Inicializamos el detector de pose de MediaPipe
    with mp_pose.Pose() as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("No se pudo acceder a la cámara")
                break

            # Detectar si la persona está corriendo
            if detect_running(frame, pose, prev_knee_positions):
                detection_count += 1  # Incrementa si detecta movimiento de correr
                print(f"Detectado correr, conteo: {detection_count}")
            else:
                detection_count = 0  # Reseteamos el contador si no se detecta correr

            # Solo iniciar el temporizador si detecta varias veces correr consecutivamente
            if detection_count >= detection_threshold and not timer_started:
                print("Iniciando temporizador...")
                start_time = time.time()
                timer_started = True

            # Si el temporizador ya ha comenzado, mostrar el tiempo transcurrido
            if timer_started:
                elapsed_time = time.time() - start_time
                remaining_time = max(0, 60 - int(elapsed_time))  # Cuenta regresiva de 60 segundos
                print(f"Tiempo restante: {remaining_time} segundos")

                # Mostrar el temporizador en el frame de video
                cv2.putText(frame, f"Tiempo restante: {remaining_time}s", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                if elapsed_time >= 60:
                    print("¡Tiempo completo!")
                    break

            # Mostrar el video con esqueleto dibujado
            cv2.imshow('Correr en Caminadora', frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

import cv2

def show_frame(frame):
    cv2.imshow('Detección de Movimientos Corporales', frame)

def close_window():
    cv2.destroyAllWindows()

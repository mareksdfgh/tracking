import cv2
import keyboard

# Startposition und Größe des Quadrats
x, y = 300, 200
square_size = 100
step_size = 10

# Bildschirmbreite und -höhe abrufen
screen_width, screen_height = 640, 480  # Hier entsprechend der Bildschirmgröße anpassen

# Farben und Dicke definieren
retro_green = (0, 255, 0)
black = (0, 0, 0)
thickness = 2
border_thickness = thickness + 2

def draw_square_corners_and_lines(img, x, y, size, screen_width, screen_height, tracking):
    # Draw the square corners
    # Top-left corner
    cv2.line(img, (x, y), (x + 10, y), black, border_thickness)
    cv2.line(img, (x, y), (x, y + 10), black, border_thickness)
    cv2.line(img, (x, y), (x + 10, y), retro_green, thickness)
    cv2.line(img, (x, y), (x, y + 10), retro_green, thickness)

    # Top-right corner
    cv2.line(img, (x + size, y), (x + size - 10, y), black, border_thickness)
    cv2.line(img, (x + size, y), (x + size, y + 10), black, border_thickness)
    cv2.line(img, (x + size, y), (x + size - 10, y), retro_green, thickness)
    cv2.line(img, (x + size, y), (x + size, y + 10), retro_green, thickness)

    # Bottom-left corner
    cv2.line(img, (x, y + size), (x, y + size - 10), black, border_thickness)
    cv2.line(img, (x, y + size), (x + 10, y + size), black, border_thickness)
    cv2.line(img, (x, y + size), (x, y + size - 10), retro_green, thickness)
    cv2.line(img, (x, y + size), (x + 10, y + size), retro_green, thickness)

    # Bottom-right corner
    cv2.line(img, (x + size, y + size), (x + size - 10, y + size), black, border_thickness)
    cv2.line(img, (x + size, y + size), (x + size, y + size - 10), black, border_thickness)
    cv2.line(img, (x + size, y + size), (x + size - 10, y + size), retro_green, thickness)
    cv2.line(img, (x + size, y + size), (x + size, y + size - 10), retro_green, thickness)

    # Draw the lines
    center_x, center_y = x + size // 2, y + size // 2

    # Horizontal line (left of the square)
    cv2.line(img, (0, center_y), (x, center_y), black, border_thickness)
    cv2.line(img, (0, center_y), (x, center_y), retro_green, thickness)
    # Horizontal line (right of the square)
    cv2.line(img, (x + size, center_y), (screen_width, center_y), black, border_thickness)
    cv2.line(img, (x + size, center_y), (screen_width, center_y), retro_green, thickness)

    # Vertical line (above the square)
    cv2.line(img, (center_x, 0), (center_x, y), black, border_thickness)
    cv2.line(img, (center_x, 0), (center_x, y), retro_green, thickness)
    # Vertical line (below the square)
    cv2.line(img, (center_x, y + size), (center_x, screen_height), black, border_thickness)
    cv2.line(img, (center_x, y + size), (center_x, screen_height), retro_green, thickness)

    # Draw the circle if tracking
    if tracking:
        cv2.circle(img, (center_x, center_y), 5, black, border_thickness)
        cv2.circle(img, (center_x, center_y), 5, retro_green, thickness)

# Hauptfunktion
def main():
    global x, y, square_size  # Zugriff auf globale Variablen x, y, und square_size
    cap = cv2.VideoCapture(0)  # Öffnen der Kameraquelle

    tracker = cv2.TrackerCSRT_create()
    tracking = False
    enter_pressed = False

    while True:
        ret, frame = cap.read()  # Einzelbild von der Kamera erhalten

        # Überprüfen, ob das Einzelbild erfolgreich erfasst wurde
        if not ret:
            print("Fehler: Kein Kamerabild erhalten.")
            break

        if tracking:
            # Update the tracker
            success, bbox = tracker.update(frame)
            if success:
                x, y, w, h = [int(v) for v in bbox]
                draw_square_corners_and_lines(frame, x, y, square_size, screen_width, screen_height, True)
            else:
                tracking = False
                draw_square_corners_and_lines(frame, x, y, square_size, screen_width, screen_height, False)
        else:
            # Zeichnen des Quadrats auf dem Bild
            draw_square_corners_and_lines(frame, x, y, square_size, screen_width, screen_height, False)

            # Tastaturereignisse abfragen und Steuerung aktualisieren
            if keyboard.is_pressed('up') and y > 0:
                y -= step_size
            if keyboard.is_pressed('down') and y < screen_height - square_size:
                y += step_size
            if keyboard.is_pressed('left') and x > 0:
                x -= step_size
            if keyboard.is_pressed('right') and x < screen_width - square_size:
                x += step_size

            # Square size adjustment
            if keyboard.is_pressed('+') and square_size < 200:
                center_x, center_y = x + square_size // 2, y + square_size // 2
                square_size += step_size
                x, y = center_x - square_size // 2, center_y - square_size // 2
            if keyboard.is_pressed('-') and square_size > 30:
                center_x, center_y = x + square_size // 2, y + square_size // 2
                square_size -= step_size
                x, y = center_x - square_size // 2, center_y - square_size // 2

        # Start or stop tracking on Enter
        if keyboard.is_pressed('enter'):
            if not enter_pressed:
                if tracking:
                    tracking = False
                else:
                    bbox = (x, y, square_size, square_size)
                    tracker = cv2.TrackerCSRT_create()  # Re-initialize the tracker
                    tracker.init(frame, bbox)
                    tracking = True
                enter_pressed = True
        else:
            enter_pressed = False

        # Anzeige des Bildes
        cv2.imshow('Frame', frame)

        # ESC zum Beenden
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Freigeben der Ressourcen
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

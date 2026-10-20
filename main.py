import cv2
import mediapipe as mp
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities


def main():
    cam = cv2.VideoCapture(0)
    smoothed_brightness = None
    last_brightness = None

    if not cam.isOpened():
        print("Error: Could not open camera.")
        return

    try:
        devices = AudioUtilities.GetSpeakers()
        volume_control = devices.EndpointVolume

        last_volume = None
        control_mode = "brightness"

        mp_hands = mp.solutions.hands
        mp_draw = mp.solutions.drawing_utils

        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as hands:

            while True:
                success, frame = cam.read()

                if not success:
                    print("Error: Could not read frame.")
                    break
                frame = cv2.flip(frame, 1)

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb_frame)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_draw.draw_landmarks(
                            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                        )

                        thumb_tip = hand_landmarks.landmark[4]
                        index_tip = hand_landmarks.landmark[8]

                        height, width, _ = frame.shape

                        thumb_x = int(thumb_tip.x * width)
                        thumb_y = int(thumb_tip.y * height)
                        index_x = int(index_tip.x * width)
                        index_y = int(index_tip.y * height)

                        distance = (
                            (thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2
                        ) ** 0.5

                        min_distance = 30
                        max_distance = 200

                        percentage = int(
                            (distance - min_distance)
                            / (max_distance - min_distance)
                            * 100
                        )
                        percentage = max(0, min(100, percentage))

                        if smoothed_brightness is None:
                            smoothed_brightness = float(percentage)
                        else:
                            alpha = 0.20
                            smoothed_brightness = (
                                alpha * percentage + (1 - alpha) * smoothed_brightness
                            )
                        brightness = int(round(smoothed_brightness))

                        if control_mode == "brightness":
                            safe_brightness = max(10, brightness)
                            if (
                                last_brightness is None
                                or abs(safe_brightness - last_brightness) >= 5
                            ):
                                try:
                                    sbc.set_brightness(safe_brightness)
                                    last_brightness = safe_brightness
                                except Exception as e:
                                    print(
                                        f"Application error occurred while setting brightness: {e}"
                                    )
                        elif control_mode == "volume":
                            volume_percentage = brightness
                            if (
                                last_volume is None
                                or abs(volume_percentage - last_volume) >= 5
                            ):
                                try:
                                    volume_control.SetMasterVolumeLevelScalar(
                                        volume_percentage / 100.0, None
                                    )
                                    last_volume = volume_percentage
                                except Exception as e:
                                    print(
                                        f"Application error occurred while setting volume: {e}"
                                    )

                        cv2.circle(frame, (thumb_x, thumb_y), 10, (255, 0, 255), -1)
                        cv2.circle(frame, (index_x, index_y), 10, (255, 0, 255), -1)

                        cv2.line(
                            frame,
                            (thumb_x, thumb_y),
                            (index_x, index_y),
                            (255, 0, 255),
                            3,
                        )

                        bar_x = 20
                        bar_y = 150
                        bar_width = 250
                        bar_height = 20

                        cv2.rectangle(
                            frame,
                            (bar_x, bar_y),
                            (bar_x + bar_width, bar_y + bar_height),
                            (100, 100, 100),
                            2,
                        )

                        filled_width = int(bar_width * brightness / 100)
                        cv2.rectangle(
                            frame,
                            (bar_x, bar_y),
                            (bar_x + filled_width, bar_y + bar_height),
                            (0, 255, 0),
                            cv2.FILLED,
                        )

                        cv2.putText(
                            frame,
                            f"Mode: {control_mode.title()}",
                            (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (255, 255, 0),
                            2,
                        )

                else:
                    cv2.putText(
                        frame,
                        "No Hand Detected",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                    )
                cv2.putText(
                    frame,
                    "Press 'b' for Brightness, 'v' for Volume, 'q' to Quit",
                    (20, 460),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2,
                )
                cv2.imshow("Hand Gesture Control", frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                elif key == ord("b"):
                    control_mode = "brightness"
                    print("Control mode set to brightness.")
                elif key == ord("v"):
                    control_mode = "volume"
                    print("Control mode set to volume.")
    except Exception as e:
        print(f"Application error occurred: {e}")
    finally:
        cam.release()
        cv2.destroyAllWindows()
        print("Application closed.")


if __name__ == "__main__":
    main()

import time
from datetime import datetime
from multiprocessing import Process

from models import Booking, Room, User
from notification.email import send_email

for_notification = []


def add_to_notification(user_id, room_id):
    global for_notification
    for_notification.append((user_id, room_id))


class RoomChecker:
    @staticmethod
    def checking_available_rooms():
        global for_notification
        for room in Room.get_all():
            notifications_for_room = [
                t for t in for_notification if t[1] == room.id
            ]
            if notifications_for_room and not room.is_busy:
                for user_id, room_id in notifications_for_room:
                    for_notification.remove((user_id, room_id))
                    user = User.get("id", user_id)
                    send_email(
                        user.email,
                        "Office-booking-cli",
                        f"Комната {room.name} теперь свободна!",
                    )
            
            bookings = [b for b in Booking.get_all() if b.is_actual]
            for booking in bookings:
                if room.id == booking.room_id:
                    if datetime.strptime(booking.end_time + ':00', "%Y-%m-%d %H:%M:%S") < datetime.now():
                        room.update(room.id, is_busy=False)
                        user = User.get("id", booking.user_id)
                        if user is None:
                            user = "Пользователь удален"
                            return None
                        user_email = user.email
                        send_email(user_email, "Office-booking-cli", "время на бронирование истекло!")
                        booking.update(booking.id, is_actual=False)
                        print(booking)



def background_checker():
    while True:
        try:
            RoomChecker.checking_available_rooms()
            time.sleep(60)
        except Exception as e:
            print(f"Ошибка в фоновом процессе: {e}")
            time.sleep(60)


background_process = None


def start_background_checker():
    global background_process
    if background_process is None or not background_process.is_alive():
        background_process = Process(target=background_checker)
        background_process.daemon = True
        background_process.start()
        print("Фоновый процесс проверки комнат запущен")


def stop_background_checker():
    global background_process
    if background_process and background_process.is_alive():
        background_process.terminate()
        background_process.join()
        print("Фоновый процесс проверки комнат остановлен")

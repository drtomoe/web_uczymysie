import os


class Config:
    SECRET_KEY = "9fa4a357a8e67403dc5631d1806f9029"
    # konsola python --> import secrets --> secrets.token_hex(16) > to daje losowy ciąg 16 znaków potrzebny do bezpieczeństwa
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # adres /// oznacza, ze w db będzie w tym samym miejscu, co reszta plików
    MAIL_SERVER = 'smtp.gmail.com'  # ustawiamy maila, z którego będą wysyłane wiadomosci do resetu hasła
    MAIL_PORT = 465  # 587
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # żeby nie podawać w kodzie dancyh do konta(user/hasło), używamy funkcji z modułu os
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
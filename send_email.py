import smtplib
import os

GMAIL_USERNAME = os.getenv("GMAIL_USERNAME")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

def send_alert_email():
    try:
        # Configurar el servidor SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USERNAME, GMAIL_PASSWORD)

        message = 'Subject: Nota disponible\n\nNota disponible.'

        # Enviar el correo electrónico
        server.sendmail(GMAIL_USERNAME, GMAIL_USERNAME, message)
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
    finally:
        server.quit()
    
if __name__ == "__main__":
    send_alert_email()
    print("Correo enviado correctamente.")
import serial
import time

# Configuraci�n del puerto serial
arduino_port = 'COM8'  # Cambia esto seg�n el puerto de tu Arduino
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)

# L�mite de temperatura (defecto y serial)
temperatura_limite = 25
temperatura_limite_serial = -1

def enviar_limite_serial(limite):
    """Env�a el l�mite de temperatura al Arduino a trav�s del serial."""
    arduino.write(f"{limite}\n".encode())
    print(f"Valor enviado: {limite}")

def leer_temperatura():
    """Lee el valor de temperatura desde el Arduino y lo muestra en consola."""
    if arduino.in_waiting > 0:
        try:
            temp_data = arduino.readline().decode('utf-8').strip()
            temp_c = float(temp_data)
            print(f"Temperatura en C: {temp_c:.1f}")
            return temp_c
        except ValueError:
            print("Error en la conversi�n de datos de temperatura.")
            return None
    return None

def controlar_servo(temp_c, limite):
    """Controla el movimiento del servomotor seg�n la temperatura."""
    if temp_c > limite:
        print("Servo movido a 0�")
        time.sleep(1)
        print("Servo movido a 90�")
        time.sleep(1)
        print("Servo movido a 180�")
        time.sleep(1)
    else:
        print("Servo en posici�n 90�")
    time.sleep(5)  # Simula el delay entre mediciones

try:
    while True:
        # Env�a el l�mite si se recibe un valor desde el serial
        if arduino.in_waiting > 0:
            temperatura_limite_serial = int(arduino.readline().decode('utf-8').strip())
            print(f"Valor recibido desde el serial: {temperatura_limite_serial}")
            enviar_limite_serial(temperatura_limite_serial)

        # Lee la temperatura desde el Arduino
        temp_c = leer_temperatura()
        if temp_c is not None:
            # Decide qu� l�mite usar
            current_limit = temperatura_limite_serial if temperatura_limite_serial != -1 else temperatura_limite
            # Controla el servomotor seg�n la temperatura y el l�mite
            controlar_servo(temp_c, current_limit)

except KeyboardInterrupt:
    print("Programa detenido.")
finally:
    arduino.close()


import board
import busio
import digitalio
import adafruit_mcp230xx.mcp23017 as MCP
import RPi.GPIO as GPIO
from enum import Enum
from utils.logger import logger
import time

# Raspberry Pi GPIOs für Interrupts (IA, IB)
INTA_GPIO = 17  # z.B. GPIO17 für IA
INTB_GPIO = 27  # z.B. GPIO27 für IB


class InputName(Enum):
    UV = 0
    SALZ = 1
    WP = 2
    PUMPE = 3
    # ... weitere Namen/Indexe nach Bedarf


class OutputName(Enum):
    PUMPE = 0
    UV = 1
    SALZ = 2
    WP = 3
    # ... weitere Namen/Indexe nach Bedarf


class MCP23017IO:
    def __init__(self, i2c_address=0x20):
        # I2C initialisieren
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.mcp = MCP.MCP23017(self.i2c, address=i2c_address)

        # 8 Pins als Input, 8 Pins als Output
        self.input_pins = []
        self.output_pins = []

        for i in range(8):
            pin = self.mcp.get_pin(i)
            pin.direction = digitalio.Direction.INPUT
            pin.pull = digitalio.Pull.UP  # Optional: Pull-Up aktivieren
            self.input_pins.append(pin)

        for i in range(8, 16):
            pin = self.mcp.get_pin(i)
            pin.direction = digitalio.Direction.OUTPUT
            pin.value = False  # Standard: Ausgänge LOW
            self.output_pins.append(pin)

        # Interrupts konfigurieren
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(INTA_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(INTB_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Interrupt-Events registrieren
        GPIO.add_event_detect(
            INTA_GPIO, GPIO.FALLING, callback=self._interrupt_a_callback, bouncetime=200
        )
        GPIO.add_event_detect(
            INTB_GPIO, GPIO.FALLING, callback=self._interrupt_b_callback, bouncetime=200
        )

        logger.info("MCP23017 initialisiert: 8 Inputs, 8 Outputs, Interrupts aktiv.")

    def read_inputs(self, index=None):
        """
        Liest entweder alle 8 Eingänge (als Liste), einen einzelnen Eingang per Index (int), Namen (str) oder Enum.
        :param index: Optional, Index (0-7), Name (z.B. 'uv') oder Enum (InputName.UV)
        :return: Liste aller Eingänge oder einzelner bool-Wert
        """
        if index is None:
            states = [pin.value for pin in self.input_pins]
            logger.debug(f"MCP23017 Eingänge (alle): {states}")
            return states
        elif isinstance(index, int):
            if 0 <= index < 8:
                value = self.input_pins[index].value
                logger.debug(f"MCP23017 Eingang {index}: {value}")
                return value
            else:
                logger.error(f"Ungültiger Eingangs-Index: {index}")
                return None
        elif isinstance(index, str):
            try:
                idx = InputName[index.upper()].value
                value = self.input_pins[idx].value
                logger.debug(f"MCP23017 Eingang '{index}' (Index {idx}): {value}")
                return value
            except KeyError:
                logger.error(f"Unbekannter Eingangs-Name: {index}")
                return None
        elif isinstance(index, InputName):
            idx = index.value
            value = self.input_pins[idx].value
            logger.debug(f"MCP23017 Eingang '{index.name}' (Index {idx}): {value}")
            return value
        else:
            logger.error(f"Ungültiger Typ für index: {type(index)}")
            return None

    def set_output(self, index, value):
        """
        Setzt einen der 8 Ausgänge (index 0-7), per Index (int), Name (str) oder Enum (OutputName).
        :param index: Index (0-7), Name (z.B. 'pumpe') oder Enum (OutputName.PUMPE)
        :param value: True (HIGH) oder False (LOW)
        """
        if isinstance(index, int):
            if 0 <= index < 8:
                self.output_pins[index].value = value
                logger.info(f"MCP23017 Ausgang {index} auf {value} gesetzt.")
            else:
                logger.error(f"Ungültiger Ausgangs-Index: {index}")
        elif isinstance(index, str):
            try:
                idx = OutputName[index.upper()].value
                self.output_pins[idx].value = value
                logger.info(
                    f"MCP23017 Ausgang '{index}' (Index {idx}) auf {value} gesetzt."
                )
            except KeyError:
                logger.error(f"Unbekannter Ausgangs-Name: {index}")
        elif isinstance(index, OutputName):
            idx = index.value
            self.output_pins[idx].value = value
            logger.info(
                f"MCP23017 Ausgang '{index.name}' (Index {idx}) auf {value} gesetzt."
            )
        else:
            logger.error(f"Ungültiger Typ für Ausgangs-Index: {type(index)}")

    def read_outputs(self, index=None):
        """
        Liest entweder alle 8 Ausgänge (als Liste), einen einzelnen Ausgang per Index (int), Namen (str) oder Enum.
        :param index: Optional, Index (0-7), Name (z.B. 'pumpe') oder Enum (OutputName.PUMPE)
        :return: Liste aller Ausgänge oder einzelner bool-Wert
        """
        if index is None:
            states = [pin.value for pin in self.output_pins]
            logger.debug(f"MCP23017 Ausgänge (alle): {states}")
            return states
        elif isinstance(index, int):
            if 0 <= index < 8:
                value = self.output_pins[index].value
                logger.debug(f"MCP23017 Ausgang {index}: {value}")
                return value
            else:
                logger.error(f"Ungültiger Ausgangs-Index: {index}")
                return None
        elif isinstance(index, str):
            try:
                idx = OutputName[index.upper()].value
                value = self.output_pins[idx].value
                logger.debug(f"MCP23017 Ausgang '{index}' (Index {idx}): {value}")
                return value
            except KeyError:
                logger.error(f"Unbekannter Ausgangs-Name: {index}")
                return None
        elif isinstance(index, OutputName):
            idx = index.value
            value = self.output_pins[idx].value
            logger.debug(f"MCP23017 Ausgang '{index.name}' (Index {idx}): {value}")
            return value
        else:
            logger.error(f"Ungültiger Typ für Ausgangs-Index: {type(index)}")
            return None

    def _interrupt_a_callback(self, channel):
        logger.info("MCP23017 Interrupt A (IA) ausgelöst!")
        states = self.read_inputs()
        # Hier kannst du weitere Aktionen einbauen, z.B. Event an GUI/MQTT weitergeben

    def _interrupt_b_callback(self, channel):
        logger.info("MCP23017 Interrupt B (IB) ausgelöst!")
        states = self.read_inputs()
        # Hier kannst du weitere Aktionen einbauen, z.B. Event an GUI/MQTT weitergeben

    def cleanup(self):
        GPIO.cleanup([INTA_GPIO, INTB_GPIO])
        logger.info("MCP23017 GPIOs aufgeräumt.")


# Beispiel für Standalone-Test
if __name__ == "__main__":
    mcp = MCP23017IO()
    try:
        while True:
            print("Alle Eingänge:", mcp.read_inputs())
            print("UV-Eingang (Enum):", mcp.read_inputs(InputName.UV))
            print("SALZ-Eingang (String):", mcp.read_inputs("salz"))
            print("PUMPE-Eingang (Index):", mcp.read_inputs(3))
            print("Alle Ausgänge:", mcp.read_outputs())
            print("PUMPE-Ausgang (Enum):", mcp.read_outputs(OutputName.PUMPE))
            print("UV-Ausgang (String):", mcp.read_outputs("uv"))
            print("WP-Ausgang (Index):", mcp.read_outputs(3))
            # Beispiel: Ausgang 0 toggeln
            mcp.set_output(OutputName.PUMPE, not mcp.read_outputs(OutputName.PUMPE))
            time.sleep(1)
    except KeyboardInterrupt:
        print("Beende Test.")
    finally:
        mcp.cleanup()

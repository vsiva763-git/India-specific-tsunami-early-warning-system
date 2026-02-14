# Arduino Alert System (UNO + ESP8266 + LCD + Buzzer)

This sketch polls the project API and triggers a buzzer when a tsunami WARNING is active. Other alert levels are shown on the LCD.

## Uses
- API endpoint: `http://<server-ip>:5000/api/current-assessment`
- `alert_level` drives LCD and buzzer behavior

## Wiring (recommended)
- **Arduino UNO -> ESP8266 (ESP-01/ESP-12 AT firmware)**
  - UNO D2 (RX)  <- ESP TX
  - UNO D3 (TX)  -> ESP RX (use level shifter or divider to 3.3V)
  - ESP VCC/CH_PD -> 3.3V (stable regulator)
  - ESP GND -> GND
- **LCD 16x2 (parallel, HD44780)**
  - VSS -> GND
  - VDD -> 5V
  - V0 -> contrast (10k pot wiper)
  - RS -> D4
  - RW -> GND
  - E  -> D5
  - D4 -> D6
  - D5 -> D7
  - D6 -> D9
  - D7 -> D10
  - A (LED+) -> 5V (use resistor if needed)
  - K (LED-) -> GND
- **Active buzzer**
  - + -> D8 (use transistor if buzzer draws > 20mA)
  - - -> GND

## Libraries
Install in Arduino IDE:
- WiFiEspAT

## Setup
1. Edit `arduino_alert_system.ino`:
   - Set `WIFI_SSID`, `WIFI_PASS`, `API_HOST`
2. Upload to Arduino UNO.
3. Start the backend server and enable monitoring:
   - `POST /api/monitoring/start`
4. The LCD will show status; buzzer beeps for WARNING.

## Behavior
- WARNING: buzzer on (beeping), LCD shows WARNING
- ADVISORY/WATCH/NONE: LCD shows level, buzzer off
- No assessment yet: LCD shows NO DATA

## Notes
- The ESP8266 must run ESP-AT firmware.
- Keep the server reachable from the same WiFi network.
- Adjust the contrast potentiometer until text is visible.

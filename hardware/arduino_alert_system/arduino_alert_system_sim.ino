#include <LiquidCrystal.h>

// ---- Simulation-only hardware ----
const int BUZZER_PIN = 8; // Active buzzer

// LCD pins: RS, EN, D4, D5, D6, D7
const int LCD_RS = 4;
const int LCD_EN = 5;
const int LCD_D4 = 6;
const int LCD_D5 = 7;
const int LCD_D6 = 9;
const int LCD_D7 = 10;

LiquidCrystal lcd(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7);

// ---- Simulation state ----
const unsigned long SCREEN_INTERVAL_MS = 6000;
unsigned long lastScreenMs = 0;
int screenIndex = 0;

bool warningActive = false;
unsigned long lastBuzzerToggleMs = 0;
const unsigned long BUZZER_TOGGLE_MS = 300;
bool buzzerState = false;

struct AlertScreen {
  const char* line1;
  const char* line2;
  bool warning;
};

AlertScreen screens[] = {
  {"SAFE", "No threat", false},
  {"WATCH", "Monitor", false},
  {"ADVISORY", "Stay alert", false},
  {"WARNING", "Evacuate now", true},
  {"NO DATA", "Run check", false},
  {"UNKNOWN", "Check API", false}
};

const int SCREEN_COUNT = sizeof(screens) / sizeof(screens[0]);

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);

  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Tsunami Alert");
  lcd.setCursor(0, 1);
  lcd.print("SIM MODE");
  delay(1200);

  showScreen(0);
}

void loop() {
  unsigned long now = millis();

  if (now - lastScreenMs >= SCREEN_INTERVAL_MS) {
    lastScreenMs = now;
    screenIndex = (screenIndex + 1) % SCREEN_COUNT;
    showScreen(screenIndex);
  }

  updateBuzzer(now);
}

void showScreen(int index) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(screens[index].line1);
  lcd.setCursor(0, 1);
  lcd.print(screens[index].line2);
  warningActive = screens[index].warning;
}

void updateBuzzer(unsigned long now) {
  if (!warningActive) {
    digitalWrite(BUZZER_PIN, LOW);
    buzzerState = false;
    return;
  }

  if (now - lastBuzzerToggleMs >= BUZZER_TOGGLE_MS) {
    lastBuzzerToggleMs = now;
    buzzerState = !buzzerState;
    digitalWrite(BUZZER_PIN, buzzerState ? HIGH : LOW);
  }
}

#include <LiquidCrystal.h>
#include <WiFiEspAT.h>
#include <WiFiClient.h>
#include <SoftwareSerial.h>

// ---- User config ----
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASS = "YOUR_WIFI_PASSWORD";
const char* API_HOST = "192.168.1.50"; // Flask server IP or domain
const int API_PORT = 5000;
const char* API_PATH = "/api/current-assessment";

// ---- Hardware ----
const int ESP_RX_PIN = 2; // Arduino RX  <- ESP8266 TX
const int ESP_TX_PIN = 3; // Arduino TX  -> ESP8266 RX (use level shifter)
const int BUZZER_PIN = 8; // Active buzzer

// LCD pins: RS, EN, D4, D5, D6, D7
const int LCD_RS = 4;
const int LCD_EN = 5;
const int LCD_D4 = 6;
const int LCD_D5 = 7;
const int LCD_D6 = 9;
const int LCD_D7 = 10;

LiquidCrystal lcd(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7);
SoftwareSerial espSerial(ESP_RX_PIN, ESP_TX_PIN);
WiFiClient client;

// ---- State ----
unsigned long lastPollMs = 0;
const unsigned long POLL_INTERVAL_MS = 15000;

bool warningActive = false;
unsigned long lastBuzzerToggleMs = 0;
const unsigned long BUZZER_TOGGLE_MS = 300;
bool buzzerState = false;

void setup() {
	pinMode(BUZZER_PIN, OUTPUT);
	digitalWrite(BUZZER_PIN, LOW);

	lcd.begin(16, 2);
	lcd.clear();
	lcd.setCursor(0, 0);
	lcd.print("Tsunami Alert");
	lcd.setCursor(0, 1);
	lcd.print("Booting...");

	Serial.begin(9600);
	espSerial.begin(115200);
	WiFi.init(&espSerial);

	if (WiFi.status() == WL_NO_MODULE) {
		lcd.clear();
		lcd.print("ESP8266? NO");
		while (true) { delay(1000); }
	}

	connectWiFi();
}

void loop() {
	if (WiFi.status() != WL_CONNECTED) {
		connectWiFi();
	}

	unsigned long now = millis();
	if (now - lastPollMs >= POLL_INTERVAL_MS) {
		lastPollMs = now;
		pollAlert();
	}

	updateBuzzer(now);
}

void connectWiFi() {
	lcd.clear();
	lcd.setCursor(0, 0);
	lcd.print("WiFi connect");
	lcd.setCursor(0, 1);
	lcd.print(WIFI_SSID);

	while (WiFi.begin(WIFI_SSID, WIFI_PASS) != WL_CONNECTED) {
		delay(2000);
	}

	lcd.clear();
	lcd.setCursor(0, 0);
	lcd.print("WiFi OK");
	lcd.setCursor(0, 1);
	lcd.print(WiFi.localIP());
	delay(1000);
}

void pollAlert() {
	lcd.clear();
	lcd.setCursor(0, 0);
	lcd.print("Checking...");

	if (!client.connect(API_HOST, API_PORT)) {
		showError("Server down");
		warningActive = false;
		return;
	}

	client.print("GET ");
	client.print(API_PATH);
	client.println(" HTTP/1.1");
	client.print("Host: ");
	client.println(API_HOST);
	client.println("Connection: close");
	client.println();

	String response = readHttpResponse();
	client.stop();

	if (response.length() == 0) {
		showError("No response");
		warningActive = false;
		return;
	}

	handleAssessment(response);
}

String readHttpResponse() {
	unsigned long start = millis();
	String data = "";

	while (client.connected() && millis() - start < 5000) {
		while (client.available()) {
			char c = client.read();
			data += c;
		}
	}

	int jsonStart = data.indexOf("\r\n\r\n");
	if (jsonStart >= 0) {
		return data.substring(jsonStart + 4);
	}

	return data;
}

void handleAssessment(const String& body) {
	// Simple string match keeps SRAM usage low without JSON parser.
	if (body.indexOf("\"alert_level\":\"WARNING\"") >= 0) {
		warningActive = true;
		showAlert("WARNING", "Evacuate now");
		return;
	}

	warningActive = false;

	if (body.indexOf("\"alert_level\":\"ADVISORY\"") >= 0) {
		showAlert("ADVISORY", "Stay alert");
	} else if (body.indexOf("\"alert_level\":\"WATCH\"") >= 0) {
		showAlert("WATCH", "Monitor");
	} else if (body.indexOf("\"alert_level\":\"NONE\"") >= 0) {
		showAlert("SAFE", "No threat");
	} else if (body.indexOf("No assessment") >= 0) {
		showAlert("NO DATA", "Run check");
	} else {
		showAlert("UNKNOWN", "Check API");
	}
}

void showAlert(const char* line1, const char* line2) {
	lcd.clear();
	lcd.setCursor(0, 0);
	lcd.print(line1);
	lcd.setCursor(0, 1);
	lcd.print(line2);
}

void showError(const char* msg) {
	lcd.clear();
	lcd.setCursor(0, 0);
	lcd.print("Error");
	lcd.setCursor(0, 1);
	lcd.print(msg);
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
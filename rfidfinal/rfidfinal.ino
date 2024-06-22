#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <MFRC522.h>

const char* ssid = "himesh";
const char* password = "himeshpathai";
const char* serverIP = "192.168.160.183"; // Replace with your server's IP address
const int serverPort = 5000; // Replace with the port number your server is listening on
const String endpoint = "/validate_rfid"; // Endpoint to send RFID data to server

#define SS_PIN D4
#define RST_PIN D3

MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key;

byte nuidPICC[4]; // Init array that will store new NUID

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522

  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }

  Serial.println("RFID reader initialized");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected. Reconnecting...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");
  }

  if (scanRFID()) {
    Serial.println("RFID tag detected");
    delay(1000); // Delay for stability
  }

  delay(500); // Adjust delay as needed
}

bool scanRFID() {
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
    return false; // No card detected or reading failed
  }

  Serial.print("PICC type: ");
  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
  Serial.println(rfid.PICC_GetTypeName(piccType));

  if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&
      piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
      piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
    Serial.println("Your tag is not of type MIFARE Classic.");
    return false;
  }

  // Convert UID to decimal format
  String rfidData = "";
  for (byte i = 0; i < 4; i++) {
    rfidData += String(rfid.uid.uidByte[i]);
  }

  // Send RFID data to server
  bool success = sendRFIDData(rfidData);
  
  // Clear RFID data for the next reading
  rfidData = "";

  return success;
}

bool sendRFIDData(String data) {
  WiFiClient client;
  HTTPClient http;

  String url = "http://" + String(serverIP) + ":" + String(serverPort) + endpoint;
  Serial.println("Sending RFID data to server: " + data);

  http.begin(client, url); // Use the correct begin method
  http.addHeader("Content-Type", "text/plain");

  int httpResponseCode = http.POST(data);
  http.end();

  if (httpResponseCode == 200) {
    Serial.println("RFID data sent successfully to server.");
    return true;
  } else {
    Serial.print("Error sending RFID data. HTTP response code: ");
    Serial.println(httpResponseCode);
    return false;
  }
}

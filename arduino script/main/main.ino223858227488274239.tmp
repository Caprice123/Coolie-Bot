#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "WIFI_NAME";
const char* password = "WIFI_PASS";
const char* mqtt_server = "test.mosquitto.org";

// pin configuration for color sensor
int S0 = 15;
int S1 = 2;
int S2 = 18;
int S3 = 4;
int sensorOut = 35;
int frequency = 0;

// pin configuration for motor 
int motor2Pin1 = 25;
int motor2Pin2 = 26;
int enable2Pin = 13;

int motor1Pin1 = 32;
int motor1Pin2 = 33;
int enable1Pin = 14;

// configuration for motor driver
const int freq = 30000;
const int pwmChannel1 = 0;
const int pwmChannel2 = 0;
const int resolution = 8;
int dutyCycle = 255;
int delaytime = 750;

int mission = 0;
WiFiClient espClient;
PubSubClient client(espClient);


// connecting to wifi
void setup_wifi() {
    delay(10);
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
  
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    randomSeed(micros());
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}

// detect color based on RGB color
char* findColor(int colors[]){
    char* nameColor[] = {"Red", "Green", "Blue", "Yellow", "Black", "White"};
    if (colors[0] < 20 && colors[1] < 20 && colors[2] < 10){
        return nameColor[5];
    }
    else if (colors[0] <= 10 && colors[1] <= 10 && colors[2] < 20){
        return nameColor[3];
    }
    int min = colors[0];
    int index = 0;
    for (int x = 1; x < 3; x++){
        if (colors[x] < min && abs(colors[x] - min) > 2){
            min = colors[x];
            index = x;
        }
    }
    if (min > 50){
        return nameColor[4];
    }
   
    return nameColor[index];
}

// function so that color sensor can detect color
void detectColor(int colors[]){
    digitalWrite(S2, LOW);
    digitalWrite(S3, LOW);
    colors[0] = pulseIn(sensorOut, LOW);
    delay(50);

    digitalWrite(S2, HIGH);
    digitalWrite(S3, HIGH);
    colors[1] = pulseIn(sensorOut, LOW);
    delay(50);

    digitalWrite(S2, LOW);
    digitalWrite(S3, HIGH);
    colors[2] = pulseIn(sensorOut, LOW);
}

// function to move robot left
void turnleft(){
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, HIGH);
  
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, LOW);
}

// function to move robot forward
void forward(){
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, HIGH);
  
    digitalWrite(motor2Pin1, HIGH);
    digitalWrite(motor2Pin2, LOW);
}

// function to stop motor
void stop_motor(){
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, LOW);
  
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, LOW);
}

// going back to warehouse from destination target
void going_back_to_warehouse (int colors[]){
    detectColor(colors);
    Serial.print("Color Detected: ");
    Serial.println(findColor(colors));
    // going back to warehouse
    int yellow = 0;
    while (yellow < 2){
        detectColor(colors);
        
        // turning left when detect yellow
        if (findColor(colors) == "Yellow"){
            yellow += 1;
            Serial.println("Moving left");
            turnleft();
            delay(delaytime);
           
        }
        else{
            Serial.println("Moving Forward");
            forward();
        }
    }

    // sending information that it has done transporting
    client.publish("Line_Follower_Python", "Task Finished");
    stop_motor();
    delay(2000);
}

// function for detecting destination
int finding_color_message_based(String destination){
  char* location[] = {"A", "B", "C"};
  for (int x = 0; x < 3; x++){
      if (destination == location[x]){
          return x;
      }
  }
}

// function for receiving message
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  String destination;
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    destination += (char) payload[i];
  }
  Serial.println();

  if (String(topic) == "Line_Follower_ESP32"){
      int colors[3];
      
      // sending GUI that it is ready for transporting
      if (destination == "Ready?"){
          client.publish("Line_Follower_Python", "ESP32 Ready to Go");
          stop_motor();
         
      }
      // going to warehouse when it is getting message to back
      else if (destination == "Balik"){
          if (mission == 1){
              mission = 0;
              going_back_to_warehouse(colors);
          }
      }

      // going to destination based on GUI
      else if (destination == "A" || destination == "B" || destination == "C"){
          client.publish("Line_Follower_Python", "Message Received");
          mission = 1;
          Serial.print("Color Detected: ");
          Serial.println(findColor(colors));
          Serial.print("Setting Motor to ");
    
          char* matchColors[] = {"Blue", "Green", "Red"};
          int index = finding_color_message_based(destination);
          
          Serial.println(destination);
          Serial.println(matchColors[index]);
          int warna = 1;
          char* tmpColor = "Blank";
          
          // from warehouse go to destination based on color to turn left
          while (1){
                detectColor(colors);
                
                // found matched color, turn left
                if (findColor(colors) == tmpColor){
                  if (findColor(colors) == matchColors[index] && warna == 1){
                      warna = 0;
                      turnleft();
                      delay(delaytime);
                  }
                  
                  // Destination Reached
                  else if (findColor(colors) == "Black" && warna == 0){
                      turnleft();
                      delay(875);
                      stop_motor();
                      client.publish("Line_Follower_Python", "Reach Destination");
                      break;
                  }
                  
                  // go forward
                  else{
                     forward();
                    
                  }
                }
                else{
                  tmpColor = findColor(colors);
                  forward();
                }
            }
        }
    }
}

// reconnect to wifi when disconnect
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
     
      client.publish("Line_Follower_Python", "ESP32 Ready to Go");
      
      client.subscribe("Line_Follower_ESP32");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      
      delay(5000);
    }
  }
}

// setting all pin and configuration for esp32
void setup() {
    Serial.begin(115200);
    setup_wifi();
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
  
    // sets the pins as outputs
    pinMode(motor1Pin1, OUTPUT);
    pinMode(motor1Pin2, OUTPUT);
    pinMode(enable1Pin, OUTPUT);
    pinMode(motor2Pin1, OUTPUT);
    pinMode(motor2Pin2, OUTPUT);
    pinMode(enable2Pin, OUTPUT);
  
    // configure LED PWM functionalities
    ledcSetup(pwmChannel1, freq, resolution);
    ledcSetup(pwmChannel2, freq, resolution);
  
    // attach the channel to the GPIO to the controlled
    ledcAttachPin(enable1Pin, pwmChannel1);
    ledcAttachPin(enable2Pin, pwmChannel2);
  
    pinMode(S0, OUTPUT);
    pinMode(S1, OUTPUT);
    pinMode(S2, OUTPUT);
    pinMode(S3, OUTPUT);
    pinMode(sensorOut, INPUT);
  
  
    digitalWrite(S0, HIGH);
    digitalWrite(S1, HIGH);

    ledcWrite(pwmChannel1, dutyCycle);
    ledcWrite(pwmChannel2, dutyCycle);
}

void loop() {
  if (!client.connected()) {
      reconnect();
  }
  client.loop();

} 

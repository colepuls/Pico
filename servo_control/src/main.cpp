#include <Arduino.h>
#include <Servo.h>

Servo servo;
const int PIN = 9;
bool attached = false;

void setup()
{
    Serial.begin(115200);
    servo.attach(PIN);
}

void loop()
{
    if (!Serial.available())
    {
        return;
    }

    int angle = Serial.parseInt(); // reads first integer it sees

    if (angle >= 0 && angle <= 180)
    {
        servo.write(angle);
    }

    // clear rest of line
    while (Serial.available())
    {
        Serial.read();
    }

}
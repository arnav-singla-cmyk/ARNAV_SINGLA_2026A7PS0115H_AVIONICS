#include <LiquidCrystal.h>

const int BUTTON = 2;
const int LED = 3;
const int BUZZER = 4;
const int TRIG = 9;
const int ECHO = 10;
const int LDR = A0;

LiquidCrystal lcd(7, 8, 5, 6, 11, 12);

const int OPEN_SEA = 0;
const int ANCHOR_DROPPED = 1;
const int STORM = 2;
const int CHARYBDIS = 3;
const int WRECKED = 4;

int state = OPEN_SEA;

const int STORM_THRESHOLD = 27;
const float CHARYBDIS_THRESHOLD = 100.0;

const unsigned long WRECK_TIME = 5000;

unsigned long dangerStart = 0;
unsigned long lastBlink = 0;

bool lastButton = HIGH;
bool ledState = LOW;


float getDistance()
{
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG, LOW);

  long duration = pulseIn(ECHO, HIGH, 30000);

  if (duration == 0)
    return 999.0;

  return duration * 0.0343 / 2.0;
}


void displayState()
{
  lcd.clear();
  lcd.setCursor(0, 0);

  if (state == OPEN_SEA)
  {
    lcd.print("OPEN SEA");
  }
  else if (state == ANCHOR_DROPPED)
  {
    lcd.print("ANCHOR");
    lcd.setCursor(0, 1);
    lcd.print("DROPPED");
  }
  else if (state == STORM)
  {
    lcd.print("STORM");
  }
  else if (state == CHARYBDIS)
  {
    lcd.print("CHARYBDIS");
  }
  else if (state == WRECKED)
  {
    lcd.print("WRECKED");
    lcd.setCursor(0, 1);
    lcd.print("SHIP LOST!");
  }
}


void changeState(int newState)
{
  if (state != newState)
  {
    state = newState;
    displayState();

    Serial.print("STATE: ");

    if (state == OPEN_SEA)
      Serial.println("OPEN SEA");

    else if (state == ANCHOR_DROPPED)
      Serial.println("ANCHOR DROPPED");

    else if (state == STORM)
      Serial.println("STORM");

    else if (state == CHARYBDIS)
      Serial.println("CHARYBDIS");

    else if (state == WRECKED)
      Serial.println("WRECKED");
  }
}


void handleButton()
{
  bool buttonState = digitalRead(BUTTON);

  if (lastButton == HIGH && buttonState == LOW)
  {
    if (state != WRECKED)
    {
      if (state == ANCHOR_DROPPED)
        changeState(OPEN_SEA);
      else
        changeState(ANCHOR_DROPPED);

      dangerStart = 0;

      digitalWrite(LED, LOW);
      noTone(BUZZER);
    }

    delay(200);
  }

  lastButton = buttonState;
}


void setup()
{
  Serial.begin(9600);

  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  lcd.begin(16, 2);

  displayState();

  Serial.println("System Started");
}


void loop()
{
  int light = analogRead(LDR);
  float distance = getDistance();

  handleButton();

  Serial.print("Light: ");
  Serial.print(light);

  Serial.print(" | Distance: ");
  Serial.print(distance);

  Serial.print(" cm | State: ");


  if (state == WRECKED)
  {
    digitalWrite(LED, LOW);
    noTone(BUZZER);

    Serial.println("WRECKED");

    delay(100);
    return;
  }


  if (state == ANCHOR_DROPPED)
  {
    digitalWrite(LED, LOW);
    noTone(BUZZER);

    dangerStart = 0;

    Serial.println("ANCHOR DROPPED");

    delay(100);
    return;
  }


  bool stormDetected = light < STORM_THRESHOLD;
  bool charybdisDetected = distance < CHARYBDIS_THRESHOLD;


  if (state == OPEN_SEA)
  {
    digitalWrite(LED, LOW);
    noTone(BUZZER);

    if (stormDetected)
    {
      changeState(STORM);
      dangerStart = millis();
    }
    else if (charybdisDetected)
    {
      changeState(CHARYBDIS);
      dangerStart = millis();
    }
    else
    {
      Serial.println("OPEN SEA");
    }
  }


  else if (state == STORM)
  {
    noTone(BUZZER);

    if (!stormDetected)
    {
      digitalWrite(LED, LOW);

      changeState(OPEN_SEA);

      dangerStart = 0;
    }
    else
    {
      if (millis() - lastBlink >= 500)
      {
        lastBlink = millis();

        ledState = !ledState;

        digitalWrite(LED, ledState);
      }

      Serial.println("STORM");
    }
  }


  else if (state == CHARYBDIS)
  {
    digitalWrite(LED, LOW);

    if (!charybdisDetected)
    {
      noTone(BUZZER);

      changeState(OPEN_SEA);

      dangerStart = 0;
    }
    else
    {
      tone(BUZZER, 1000);

      Serial.println("CHARYBDIS");
    }
  }


  if (
    (state == STORM || state == CHARYBDIS) &&
    dangerStart != 0
  )
  {
    unsigned long elapsed = millis() - dangerStart;

    if (elapsed >= WRECK_TIME)
    {
      digitalWrite(LED, LOW);
      noTone(BUZZER);

      changeState(WRECKED);

      dangerStart = 0;
    }
  }

  delay(100);
}
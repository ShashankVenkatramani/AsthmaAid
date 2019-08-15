#define pin A0

long count = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  analogReference(INTERNAL);
}

void loop() {
  double inputValue;
  count = count + 1;
  inputValue = analogRead(pin);
  Serial.print(count);
  Serial.print(",");
  Serial.println(inputValue);
  delay(10);
}

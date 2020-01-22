#include <mcp_can.h>
#include <SPI.h>

// CAN Standard
#define CAN_STANDARD 0
#define CAN_EXTENDED 1

// Message Id for Elcon Charger
unsigned long int elconChargerId = 0x1806E5F4;
// Message Data to charge with 17A
byte elconMsg17A[8] = {0x04, 0x42, 0x00, 0xAA, 0x00, 0x00, 0x00, 0x00};
// Message Data to charge with 32A
byte elconMsg32A[8] = {0x04, 0x42, 0x01, 0x2C, 0x00, 0x00, 0x00, 0x00};

// Message Id for GWP Charger
unsigned int gwpChargerId = 0x300;
// Message Data to charge with 17A
byte gwpMsg05A[7] = {0x01, 0x38, 0x03, 0x44, 0x04, 0x05, 0x00};
// Message Data to charge with 17A
byte gwpMsg17A[7] = {0x01, 0x38, 0x03, 0x44, 0x04, 0xAA, 0x00};
// Message Data to charge with 32A
byte gwpMsg34A[7] = {0x01, 0x38, 0x03, 0x44, 0x04, 0x54, 0x01};

// Set CS to pin 10
MCP_CAN CAN0(10);

void setup()
{
  Serial.begin(115200);

  // Initialize MCP2515 running at 8MHz with a baudrate of 500kb/s and the masks and filters disabled.
  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK)
    Serial.println("MCP2515 Initialized Successfully!");
  else
    Serial.println("Error Initializing MCP2515...");
  
  // Change to normal mode to allow messages to be transmitted
  CAN0.setMode(MCP_NORMAL);
}



void loop()
{
  byte sndStat = CAN0.sendMsgBuf(elconChargerId, CAN_EXTENDED, 8, chargerMsg17A);
  if(sndStat == CAN_OK){
    Serial.println("Message Sent Successfully!");
  } else {
    Serial.println("Error Sending Message...");
  }
  delay(600);
}

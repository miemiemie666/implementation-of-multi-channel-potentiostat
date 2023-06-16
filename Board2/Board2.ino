/*
ad5933-test
    Reads impedance values from the AD5933 over I2C and prints them serially.
*/
#include <Arduino.h>
#include <Wire.h>
#include "AD5933.h"

#define TMUX1108_A0 2
#define TMUX1108_A1 3
#define TMUX1108_A2 9
#define ADG704_A0 0
#define ADG704_A1 1

//////////////Variable area//////////////////////
String inputString = "";         // a String to hold incoming data
bool stringComplete = false; 
short int showMode = 0;  
///////////////////////////////////////////////
int RrefNum = 4;
int RunkonwNum = 2;
///////////////////////////////////////////////////////////////////
long startFREQ = 10000;
int freqINCR = 1000;
int numINCR = 3;
long refRESIST = 1000;
///////////////////////////////////////////////////////////////////


double gain[511];
float phase[511];


void setup(void)
{
  //I2C
  Wire.begin();              
  //serial
  Serial.begin(115200);
  Serial1.begin(115200);
  inputString.reserve(200);  //string length

  //pin
  digitalWrite(LED_BUILTIN, HIGH);  //LED
  pinMode(ADG704_A0, OUTPUT);
  pinMode(ADG704_A1, OUTPUT);
  pinMode(TMUX1108_A0, OUTPUT);
  pinMode(TMUX1108_A1, OUTPUT);
  pinMode(TMUX1108_A2, OUTPUT);
  //pinMode(8, INPUT_PULLUP);
  //pinMode(7, INPUT_PULLUP);

}

void loop(void)
{
  seriaRead();
  
  if (stringComplete)  // print the string when a newline arrives:
  { 
    Serial.println("Received");
    //Serial1.println("Received1");
  //input command
    if (inputString.startsWith("LED"))
      {
        if (inputString.startsWith("LED OFF")||inputString.startsWith("LED off")||inputString.startsWith("LED 0"))
          {
            digitalWrite(LED_BUILTIN, HIGH);
            Serial1.println("LED OFF");
          }
        else
          {
            digitalWrite(LED_BUILTIN, LOW);
            Serial1.println("LED ON");
          }
      }

    else if(inputString.startsWith("MODE"))
      {
        if (inputString.startsWith("MODE A")||inputString.startsWith("STOP")||inputString.startsWith("stop"))
          {
            showMode = 0;                 
            Serial1.println("MODE A");
            Serial.println("MODE A");
            digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
            delay(100);                       // wait for a second
            digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
            delay(100); 
          }
        else if (inputString.startsWith("MODE B")) //scanSingle
          {
            showMode = 1;           
            Serial.println("MODE B");
            Serial1.println("MODE B");

            multiplexerADG704(RrefNum); //100k
            mutiplexerTMUX1108(6);//100k
            delay(10);
            int temporary_freqINCR = freqINCR; //if not "multiple" have bug
            freqINCR=0;
            scanInit(startFREQ,freqINCR,numINCR,refRESIST);
            freqINCR = temporary_freqINCR;
          }
        else if (inputString.startsWith("MODE C")) //scanMulti
          {
            showMode = 2;
            Serial.println("MODE C");
            Serial1.println("MODE C");

            multiplexerADG704(RrefNum);  //100k
            mutiplexerTMUX1108(8); //100k
            delay(10);
            scanInit(startFREQ,freqINCR,numINCR,refRESIST);
          }
        else if (inputString.startsWith("MODE D")) //Temperature
          {
            showMode = 3;
            Serial.println("MODE D");
            Serial1.println("MODE D");
          }
        else if(inputString.startsWith("MODE E"))  //realtime scan
          {
            showMode = 4;
            Serial.println("MODE E");
            Serial1.println("MODE E");

            multiplexerADG704(RrefNum);  //100k
            mutiplexerTMUX1108(8); //100k
            delay(10);
            scanInit(startFREQ,freqINCR,numINCR,refRESIST);
          }
        else if(inputString.startsWith("MODE F"))
          {
            showMode = 5;
            Serial.println("MODE F");
            Serial1.println("MODE F");
            //mutiplexerTMUX1108(8); //看你需要哪个口初始化，自己改
            multiplexerADG704(RrefNum);  

            delay(10);
            scanInit(startFREQ,freqINCR,numINCR,refRESIST);

          }
       
      }

    else if (inputString.startsWith("R_"))
      {
        if (inputString.startsWith("R_refNum"))
          {
            RrefNum = inputString.substring(8).toInt();
            multiplexerADG704(RrefNum);
            Serial.print("RrefNum=");
            Serial.println(RrefNum);
          }
        else if (inputString.startsWith("R_unkNum"))
          {
            RunkonwNum = inputString.substring(8).toInt();
            mutiplexerTMUX1108(RunkonwNum);
            Serial.print("RunkonwNum=");
            Serial.println(RunkonwNum);
          }
      }

    else if (inputString.startsWith("P_"))
      {
        if (inputString.startsWith("P_startFREQ"))
          {
            startFREQ = inputString.substring(11).toInt();
            Serial.print("startFREQ=");
            Serial.println(startFREQ);
          }
        else if (inputString.startsWith("P_freqINCR"))
          {
            freqINCR = inputString.substring(10).toInt();
            Serial.print("freqINCR=");
            Serial.println(freqINCR);
          }
        else if (inputString.startsWith("P_numINCR"))
          {
            numINCR = inputString.substring(9).toInt();
            Serial.print("numINCR=");
            Serial.println(numINCR);
          }
        else if (inputString.startsWith("P_refRESIST"))
          {
            refRESIST = inputString.substring(11).toInt();
            Serial.print("refRESIST=");
            Serial.println(refRESIST);
          }

          
      }      

    else if(inputString.startsWith("start")||inputString.startsWith("START")||inputString.startsWith("BEGIN")||inputString.startsWith("begin")) //set start frequency
      {
        if(showMode==1)
          {
            //mutiplexerTMUX1108(1);
            mutiplexerTMUX1108(RunkonwNum);
            scanSingle();
          }
        else if(showMode==2)
          {
            //mutiplexerTMUX1108(1);
            mutiplexerTMUX1108(RunkonwNum);
            scanMulti();
          }
        else if(showMode==3)
          {
            getTemprature_AD5933();
          }
        else if(showMode==4)
          {
            mutiplexerTMUX1108(RunkonwNum);
            scanRealtime();
          }
        else if(showMode==5)
          {
            scanMutichannel();
          }

      }
   
    inputString = ""; // clear the string:
    stringComplete = false;
  }
}

bool scanInit(long startFREQ_m,int freqINCR_m,int numINCR_m, long refRESIST_m)
{
  startFREQ = startFREQ_m;
  freqINCR = freqINCR_m;
  numINCR = numINCR_m;
  refRESIST = refRESIST_m;
  if (!(AD5933::reset() &&
        AD5933::setInternalClock(true) &&
        AD5933::setStartFrequency(startFREQ) &&
        AD5933::setIncrementFrequency(freqINCR) &&
        AD5933::setNumberIncrements(numINCR) &&       //only one test
        AD5933::setPGAGain(PGA_GAIN_X1)))
        {
            Serial.println("FAILED in initialization!");
            while (true) ;
        }
  // Perform calibration sweep
  if (AD5933::calibrate(gain, phase, refRESIST, numINCR+1))
    {
    Serial.println("Calibrated!");
    Serial1.println("Calibrated!");
    Wire.beginTransmission(4);
    Wire.write("OK");
    Wire.endTransmission();
    delay(1);
    return true;
   } 
  else
    {
    Serial.println("Calibration failed...");
    return false;
    }   
}


bool scanSingle()
{
  // Create arrays to hold the data
  int real[numINCR+1], imag[numINCR+1];
  float impedanceAverage = 0;
  float resistance = 0;
  float reactance = 0;
  // Perform the frequency sweep
  if (AD5933::frequencySweep(real, imag, numINCR+1)) 
  {
    for (int i = 0; i < numINCR+1; i++) {
      // Compute impedance
      float magnitude = sqrt(pow(real[i], 2) + pow(imag[i], 2));
      float impedance = 1/(magnitude*gain[i]);

      resistance = impedance * cos(((atan2(imag[i], real[i]))-phase[i]));
      reactance = impedance * sin(((atan2(imag[i], real[i]))-phase[i]));
      //if(reactance<0) reactance = -reactance;
        
      // Print raw frequency data
      //Serial.print("Fs=");
      //Serial.println(startFREQ);
      Serial.print("real=");
      Serial.print(real[i]);
      Serial.print("imag=");
      Serial.println(imag[i]);
      Serial.print("phase2=");
      Serial.println(atan2(imag[i], real[i]));
      Serial.print("phase=");
      Serial.println(phase[i]);
      Serial.print("Z1=");
      Serial.println(impedance);
      Serial.print("R1=");
      Serial.println(resistance);
      Serial.print("I1=");
      Serial.println(reactance);
      Serial.print("F1=");
      Serial.println(startFREQ);
 

      impedanceAverage += impedance;
    }
    //Serial1.print("F=");
    //Serial1.println(startFREQ);
    impedanceAverage /= (numINCR+1);
    //Serial1.print("Z=");
    //Serial1.println(impedanceAverage);
    // Send data to the master per I2C
    Wire.beginTransmission(4);
    Wire.write("Z1=");
    Wire.write((byte*)&impedanceAverage, sizeof(float));  // 发送float数据
    Wire.endTransmission();
    delay(5);
    Wire.beginTransmission(4);
    Wire.write("R1=");
    Wire.write((byte*)&resistance, sizeof(float));  // 发送float数据
    Wire.endTransmission();
    delay(5);
    Wire.beginTransmission(4);
    Wire.write("I1=");
    Wire.write((byte*)&reactance, sizeof(float));  // 发送float数据
    Wire.endTransmission();
    delay(5);
    char str[20];
    dtostrf(startFREQ, 2, 2, str);  // 将f转换为字符串，最小宽度为10，小数点后面保留6位
    Wire.beginTransmission(4);
    Wire.write("F1=");
    Wire.write(str);  // 发送float数据
    Wire.endTransmission();
    delay(5);
    Serial.println("Frequency sweep complete!(scanSingle)");
    return true;
  }
  else 
  {
    Serial.println("Frequency sweep failed...");
    return false;
  }

}  

bool scanMulti()
{
 // Create variables to hold the impedance data and track frequency
    int real, imag, i = 0, cfreq = startFREQ;
    long F=0;
    float resistance = 0, reactance = 0, impedance = 0;
    // Initialize the frequency sweep
    if (!(AD5933::setPowerMode(POWER_STANDBY) &&          // place in standby
          AD5933::setControlMode(CTRL_INIT_START_FREQ) && // init start freq
          AD5933::setControlMode(CTRL_START_FREQ_SWEEP))) // begin frequency sweep
         {
             Serial.println("Could not initialize frequency sweep...");
         }

    // Perform the actual sweep
    while ((AD5933::readStatusRegister() & STATUS_SWEEP_DONE) != STATUS_SWEEP_DONE) {
        // Get the frequency data for this frequency point
        if (!AD5933::getComplexData(&real, &imag)) {
            Serial.println("Could not get raw frequency data...");
        }

        // Print out the frequency data
        //Serial.print(cfreq);
        Serial.print("real=");
        Serial.println(real);
        Serial.print("imag=");
        Serial.println(imag);

        // Compute impedance
        float magnitude = sqrt(pow(real, 2) + pow(imag, 2));
        impedance = 1/(magnitude*gain[i]);
        
        resistance = impedance * cos(((atan2(imag, real))-phase[i]));
        reactance = impedance * sin(((atan2(imag, real))-phase[i]));
        //if(reactance<0) reactance = -reactance;
          
        Serial.print("Z1=");
        Serial.println(impedance);
        Serial.print("R1=");
        Serial.println(resistance);
        Serial.print("I1=");
        Serial.println(reactance);
        Serial.print("F1=");
        Serial.println(cfreq);

        // Send data to the master per I2C
        /*
        Wire.beginTransmission(4);
        Wire.write("Z=");
        Wire.write((byte*)&impedance, sizeof(float));  // 发送float数据
        Wire.endTransmission();
        delay(5);  //very important, otherwise the data will be lost
        Wire.beginTransmission(4);
        Wire.write("R=");
        Wire.write((byte*)&resistance, sizeof(float));  // 发送float数据
        Wire.endTransmission();
        delay(5);
        Wire.beginTransmission(4);
        Wire.write("I=");
        Wire.write((byte*)&reactance, sizeof(float));  // 发送float数据
        Wire.endTransmission();
        delay(5);
        */

        char str[20];
        dtostrf(impedance, 8, 2, str);  // 将f转换为字符串，最小宽度为10，小数点后面保留6位
        Wire.beginTransmission(4);
        Wire.write("Z1=");
        Wire.write(str);  // 发送float数据
        Wire.endTransmission();
        delay(5);
        dtostrf(resistance, 8, 2, str);  // 将f转换为字符串，最小宽度为10，小数点后面保留6位
        Wire.beginTransmission(4);
        Wire.write("R1=");
        Wire.write(str);  // 发送float数据
        Wire.endTransmission();
        delay(5);
        dtostrf(reactance, 8, 2, str);  // 将f转换为字符串，最小宽度为10，小数点后面保留6位
        Wire.beginTransmission(4);
        Wire.write("I1=");
        Wire.write(str);  // 发送float数据
        Wire.endTransmission();
        delay(5);

        dtostrf(cfreq, 8, 2, str);  // 将f转换为字符串，最小宽度为10，小数点后面保留6位
        Wire.beginTransmission(4);
        Wire.write("F1=");
        Wire.write(str);  // 发送float数据
        Wire.endTransmission();
        delay(5);
        // Increment the frequency
        i++;
        cfreq = startFREQ+freqINCR*i;
        AD5933::setControlMode(CTRL_INCREMENT_FREQ);
    }

    Serial.println("Frequency sweep complete!(Raw)");
    return true;

    // Set AD5933 power mode to standby when finished
    if (!AD5933::setPowerMode(POWER_STANDBY)){
      Serial.println("Could not set to standby...");
      return false;
    }
        

}

bool scanRealtime()
{
  while (1)
  {
    scanSingle();
  }

}  

bool scanMutichannel()
{
  int channelNum = 6;
  char buffer[20];
 for(int cNum=1;cNum<channelNum+1;cNum++)
 {
  multiplexerADG704(RrefNum);
  mutiplexerTMUX1108(cNum);
  delay(5);
  ////////////////////////////////scanMulti
    // Create variables to hold the impedance data and track frequency
    int real, imag, i = 0, cfreq = startFREQ;
    long F=0;
    float resistance = 0, reactance = 0, impedance = 0;
    // Initialize the frequency sweep
    if (!(AD5933::setPowerMode(POWER_STANDBY) &&          // place in standby
          AD5933::setControlMode(CTRL_INIT_START_FREQ) && // init start freq
          AD5933::setControlMode(CTRL_START_FREQ_SWEEP))) // begin frequency sweep
          {
              Serial.println("Could not initialize frequency sweep...");
          }

    // Perform the actual sweep
    while ((AD5933::readStatusRegister() & STATUS_SWEEP_DONE) != STATUS_SWEEP_DONE) {
        // Get the frequency data for this frequency point
        if (!AD5933::getComplexData(&real, &imag)) {
            Serial.println("Could not get raw frequency data...");
        }

        // Print out the frequency data
        //Serial.print(cfreq);
        sprintf(buffer, "real%d=", cNum); 
        Serial.print(buffer);
        //Serial.print("real=");
        Serial.println(real);
        sprintf(buffer, "imag%d=", cNum); 
        Serial.print(buffer);
        //Serial.print("imag=");
        Serial.println(imag);

        // Compute impedance
        float magnitude = sqrt(pow(real, 2) + pow(imag, 2));
        impedance = 1/(magnitude*gain[i]);
        
        resistance = impedance * cos(((atan2(imag, real))-phase[i]));
        reactance = impedance * sin(((atan2(imag, real))-phase[i]));
        //if(reactance<0) reactance = -reactance;
        sprintf(buffer, "Z%d=", cNum); 
        Serial.print(buffer);  
        //Serial.print("Z1=");
        Serial.println(impedance);
        sprintf(buffer, "R%d=", cNum); 
        Serial.print(buffer);
        //Serial.print("R1=");
        Serial.println(resistance);
        sprintf(buffer, "I%d=", cNum); 
        Serial.print(buffer);
        //Serial.print("I1=");
        Serial.println(reactance);
        sprintf(buffer, "F%d=", cNum); 
        Serial.print(buffer);
        //Serial.print("F1=");
        Serial.println(cfreq);

        char str[20];
        dtostrf(impedance, 8, 2, str);  // 将f转换为字符串，最小宽度为10，小数点后面保留6位
        Wire.beginTransmission(4);
        sprintf(buffer, "Z%d=", cNum); 
        Wire.write(buffer);
        //Wire.write("Z1=");
        Wire.write(str);  // 发送float数据
        Wire.endTransmission();
        delay(5);
        dtostrf(resistance, 8, 2, str);  // 将f转换为字符串，最小宽度为10，小数点后面保留6位
        Wire.beginTransmission(4);
        sprintf(buffer, "R%d=", cNum); 
        Wire.write(buffer);
        //Wire.write("R1=");
        Wire.write(str);  // 发送float数据
        Wire.endTransmission();
        delay(5);
        dtostrf(reactance, 8, 2, str);  // 将f转换为字符串，最小宽度为10，小数点后面保留6位
        Wire.beginTransmission(4);
        sprintf(buffer, "I%d=", cNum); 
        Wire.write(buffer);
        //Wire.write("I1=");
        Wire.write(str);  // 发送float数据
        Wire.endTransmission();
        delay(5);

        dtostrf(cfreq, 8, 2, str);  // 将f转换为字符串，最小宽度为10，小数点后面保留6位
        Wire.beginTransmission(4);
        sprintf(buffer, "F%d=", cNum); 
        Wire.write(buffer);
        //Wire.write("F1=");
        Wire.write(str);  // 发送float数据
        Wire.endTransmission();
        delay(5);
        // Increment the frequency
        i++;
        cfreq = startFREQ+freqINCR*i;
        AD5933::setControlMode(CTRL_INCREMENT_FREQ);
    }

    Serial.println("Frequency sweep complete!(Raw)");
    //return true;

    // Set AD5933 power mode to standby when finished
    if (!AD5933::setPowerMode(POWER_STANDBY)){
      Serial.println("Could not set to standby...");
      return false;
    }
  /////////////////////////////////////////
  }

}

void getTemprature_AD5933()
{
  //Temperature measurement
  AD5933::enableTemperature(1);
  float temperature = AD5933::getTemperature();
  Serial.print("Temperature: ");
  Serial.println(temperature);
  // Send data to the master per I2C 方法一指针有BUG //用方法二！！！各有优点
  char str[20];
  dtostrf(temperature, 2, 2, str);  // 将f转换为字符串，最小宽度为10，小数点后面保留6位
  Wire.beginTransmission(4);
  Wire.write("T1=");
  Wire.write(str);  // 发送float数据
  Wire.endTransmission();
  
}

void multiplexerADG704(int modeNum)
{
  switch(modeNum)
  {
    case 1:  //S1 1K
      digitalWrite(ADG704_A0, LOW);
      digitalWrite(ADG704_A1, LOW);
      break;
    case 2:  //S2 10K
      digitalWrite(ADG704_A0, HIGH);
      digitalWrite(ADG704_A1, LOW);
      break;
    case 3:  //S3 100K
      digitalWrite(ADG704_A0, LOW);
      digitalWrite(ADG704_A1, HIGH);
      break;
    case 4:  //S4 H2???
      digitalWrite(ADG704_A0, HIGH);
      digitalWrite(ADG704_A1, HIGH);
      break;
   
  }

}

void mutiplexerTMUX1108(int modeNum)
{
  //Multiplexer
  switch(modeNum)
    {
      case 1:  //S1 H9.1
        digitalWrite(TMUX1108_A0, LOW);
        digitalWrite(TMUX1108_A1, LOW);
        digitalWrite(TMUX1108_A2, LOW);
        break;
      case 2:  //S2 H9.2
        digitalWrite(TMUX1108_A0, HIGH);
        digitalWrite(TMUX1108_A1, LOW);
        digitalWrite(TMUX1108_A2, LOW);
        break;
      case 3:  //S3 H9.3
        digitalWrite(TMUX1108_A0, LOW);
        digitalWrite(TMUX1108_A1, HIGH);
        digitalWrite(TMUX1108_A2, LOW);
        break;
      case 4:  //S4  H9.4
        digitalWrite(TMUX1108_A0, HIGH);
        digitalWrite(TMUX1108_A1, HIGH);
        digitalWrite(TMUX1108_A2, LOW);
        break;
      case 5:  //S5  H9.5
        digitalWrite(TMUX1108_A0, LOW);
        digitalWrite(TMUX1108_A1, LOW);
        digitalWrite(TMUX1108_A2, HIGH);
        break;
      case 6:  //S6  H9.6
        digitalWrite(TMUX1108_A0, HIGH);
        digitalWrite(TMUX1108_A1, LOW);
        digitalWrite(TMUX1108_A2, HIGH);
        break;
      case 7:  //S7 20Kohm
        digitalWrite(TMUX1108_A0, LOW);
        digitalWrite(TMUX1108_A1, HIGH);
        digitalWrite(TMUX1108_A2, HIGH);
        break;
      case 8:  //S8 10Kohm
        digitalWrite(TMUX1108_A0, HIGH);
        digitalWrite(TMUX1108_A1, HIGH);
        digitalWrite(TMUX1108_A2, HIGH);
        break;
    }
}

void seriaRead()
{
  if (Serial.available()) {
    char inchar  = Serial.read();
    inputString += inchar; // make the string readString
    if (inchar == '\n') {
      stringComplete = true;     
    }
  }
  else if (Serial1.available()) {
    char inchar = Serial1.read();
    //Serial1.print(inchar);
    inputString += inchar; // make the string readString
    if (inchar == '\n') {
      stringComplete = true;
    }
  }
}


/*
 * 
 * 　　┏┓　　　┏┓+ +
 * 　┏┛┻━━━┛┻┓ + +
 * 　┃　　　　　　　┃ 　
 * 　┃　　　━　　　┃ ++ + + +
 *  ████━████ ┃+
 * 　┃　　　　　　　┃ +
 * 　┃　　　┻　　　┃
 * 　┃　　　　　　　┃ + +
 * 　┗━┓　　　┏━┛
 * 　　　┃　　　┃　　　　　　　　　　　
 * 　　　┃　　　┃ + + + +
 * 　　　┃　　　┃
 * 　　　┃　　　┃ +  Alpaca bless
 * 　　　┃　　　┃    Code without bug　　
 * 　　　┃　　　┃　　+　　　　　　　　　
 * 　　　┃　 　　┗━━━┓ + +
 * 　　　┃ 　　　　　　　┣┓
 * 　　　┃ 　　　　　　　┏┛
 * 　　　┗┓┓┏━┳┓┏┛ + + + +
 * 　　　　┃┫┫　┃┫┫
 * 　　　　┗┻┛　┗┻┛+ + + +
 * 
 */

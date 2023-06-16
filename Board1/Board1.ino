/********************************
 # Editor : miemie
 # Version: 2.0
 # Product: SSD1306 ADS1115 HC-05/06
 # Date:24.06.2022
**********************************/
#include <Arduino.h>
#include <U8x8lib.h>
#include <U8g2lib.h>
#include<ADS1115_WE.h> 
#include<Wire.h>
#include <Adafruit_MCP4725.h>

//////////////Definition area////////////////////
#define ADS1115_I2C_ADDRESS 0x48
#define LED 13
#define TMUX1108_EN 6  //TMUX1108
#define TMUX1108_A0 3
#define TMUX1108_A1 4
#define TMUX1108_A2 5
#define TMUX_S5_100 5
#define TMUX_S6_1k 6
#define TMUX_S7_10k 7
#define TMUX_S8_100k 8

//////////////Variable area//////////////////////
String inputString = "";         // a String to hold incoming data
bool stringComplete = false; 
short int showMode = 0;     //ssd1306 showMode
bool flagVoltammetry = false;         //cyclic flag
long int tmuxOhm = 100000;        //TMUX1108 Variable Resistors
int tmuxChannel = 7;         //TMUX1108 Channel


float E_supply = 4800;          //电位供电电压5V,实际4.8V
float E_begin = 1800;           //电位起始值  2.4-0.6V
float E_end = 3000;             //电位终止值  2.4+0.6V
float E_step = 10;            //电位步长  10mv
float E_scanrate = 100;          //扫描速率 50?100?150?200?
float E_pulse=200;                //DPV:5-250mv之间  
float E_Tpulse=20;               //DPV:时间要小于E_step/E_scanrate的一半,也就是周期的一半
float E_amplitude = 100;         //SWV:电位幅值  50mv?        
float E_frequency = 20;         //SWV:电位频率  50hz?100hz?150hz?200hz?
int E_numofscan = 2;            //number of scan

long E_time = 0;                //电位时间

//Board2
double Z_unknown=0;

int RrefNum = 2;
int RunkonwNum = 8;

long startFREQ = 80000;
int freqINCR = 1000;
int numINCR = 40;
long refRESIST = 10000;

//float k1 = 0, b1 = 0;           //kk斜率，bb截距
//float xConcentration[10] = {0}; //x轴浓度值
//float yPotential[10] = {0};     //y轴电位值
//int xnum = 0;           //x轴数据个数

//////////////Function area/////////////////////
ADS1115_WE adc = ADS1115_WE(ADS1115_I2C_ADDRESS);
U8X8_SSD1306_128X64_NONAME_HW_I2C u8x8(/* reset=*/ U8X8_PIN_NONE);//half buffer 用我就对了，丑是丑了点 
//U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);//full buffer
//U8G2_SSD1306_128X64_NONAME_1_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);//u8g2 1.19.1
Adafruit_MCP4725 dac;


void setup() 
  {
  pinMode(LED, OUTPUT);
  pinMode(TMUX1108_EN, OUTPUT);
  pinMode(TMUX1108_A0, OUTPUT);
  pinMode(TMUX1108_A1, OUTPUT);
  pinMode(TMUX1108_A2, OUTPUT);
  //////////////////////Enable area
  digitalWrite(TMUX1108_EN, LOW);

  //////////////////////Serial
  Serial.begin(115200);
  inputString.reserve(200);  //string length
  Serial.println("Serial begin");

  //////////////////////SSD1306
  //u8g2.begin();
  u8x8.begin();
  u8x8.setPowerSave(0);
  
  //////////////////////MCP4725 DAC
  // For MCP4725A0 the address is 0x60 or 0x61
  // For MCP4725A2 the address is 0x64 or 0x65
  dac.begin(0x61);

  //////////////////////I2C
  Wire.begin(4);  //adress 4
  Wire.onReceive(receiveEvent);
    //////////////////////ADS1115
  if(!adc.init())
    {Serial.println("ADS1115 not connected!");}

  /* Set the voltage range of the ADC to adjust the gain
   * Please note that you must not apply more than VDD + 0.3V to the input pins!
   * 
   * ADS1115_RANGE_6144  ->  +/- 6144 mV
   * ADS1115_RANGE_4096  ->  +/- 4096 mV
   * ADS1115_RANGE_2048  ->  +/- 2048 mV (default)
   * ADS1115_RANGE_1024  ->  +/- 1024 mV
   * ADS1115_RANGE_0512  ->  +/- 512 mV
   * ADS1115_RANGE_0256  ->  +/- 256 mV
   */
  adc.setVoltageRange_mV(ADS1115_RANGE_6144); //comment line/change parameter to change range

  /* Set the conversion rate in SPS (samples per second)
   * Options should be self-explaining: 
   * 
   *  ADS1115_8_SPS 
   *  ADS1115_16_SPS  
   *  ADS1115_32_SPS 
   *  ADS1115_64_SPS  
   *  ADS1115_128_SPS (default)
   *  ADS1115_250_SPS 
   *  ADS1115_475_SPS 
   *  ADS1115_860_SPS 
   */
   adc.setConvRate(ADS1115_64_SPS); //uncomment if you want to change the default

  /* Set continuous or single shot mode:
   * 
   *  ADS1115_CONTINUOUS  ->  continuous mode
   *  ADS1115_SINGLE     ->  single shot mode (default)
   */
  adc.setMeasureMode(ADS1115_CONTINUOUS); //comment line/change parameter to change mode

  /* Enable or disable permanent automatic range selection mode. If enabled, the range will
   * change if the measured values are outside of 30-80% of the maximum value of the current 
   * range.  
   * !!! Use EITHER this function once OR setAutoRange() whenever needed (see below) !!!
   */
  adc.setPermanentAutoRangeMode(true);
    

  /*初始化设置*/
  digitalWrite(LED, HIGH);  //LED
  u8x8.setFont(u8x8_font_chroma48medium8_r);
 // u8x8.drawString(0,0,"----------------");
 // u8x8.drawString(0,1,"Receive Command!");
 // u8x8.drawString(0,2,"----------------");
  }


void loop()
  { 
    SSD1306_DisplayMode(showMode); //0: A0-A4 Voltage display 
    
      if (stringComplete)  // print the string when a newline arrives:
        { 
          Serial.println("Received");

          //input command
          if (inputString.startsWith("LED"))
          {
            if (inputString.startsWith("LED OFF")||inputString.startsWith("LED off")||inputString.startsWith("LED 0"))
              {
                digitalWrite(LED_BUILTIN, HIGH);
                Serial.println("LED OFF");
              }
            else
              {
                digitalWrite(LED_BUILTIN, LOW);
                Serial.println("LED ON");
              }
          }
          else if (inputString.startsWith("ADC"))
            {
              int num = inputString.substring(4).toInt();
              showMode = 0;
              u8x8.clearDisplay();
              float value = 0;
              switch(num)
              {
                case 0:
                value = readChannel(ADS1115_COMP_0_GND);
                break;
                case 1:
                value = readChannel(ADS1115_COMP_1_GND);
                break;
                case 2:
                value = readChannel(ADS1115_COMP_2_GND);
                break;
                case 3:
                value = readChannel(ADS1115_COMP_3_GND);
                break;
            
              }
              Serial.println(value,5);
              u8x8.clearDisplay();
              u8x8.drawString(0,7,"ADC:");
              u8x8.setCursor(5,7);
              u8x8.print(value,5);
              delay(1000);
            }

          else if (inputString.startsWith("E_"))
            {
              showMode = 0;
              u8x8.clearDisplay();
              if (inputString.startsWith("E_begin"))
                {
                  E_begin=inputString.substring(7).toFloat()+(E_supply/2);//换算电压
                }
              else if (inputString.startsWith("E_end"))
                {
                  E_end=inputString.substring(5).toFloat()+(E_supply/2);
                }
              else if (inputString.startsWith("E_step"))
                {
                  E_step=inputString.substring(6).toFloat();
                }
              else if (inputString.startsWith("E_scanrate"))
                {
                  E_scanrate=inputString.substring(10).toFloat();
                }
              else if (inputString.startsWith("E_pulse"))
                {
                  E_pulse=inputString.substring(7).toFloat();
                }
              else if (inputString.startsWith("E_Tpulse"))
                {
                  E_Tpulse=inputString.substring(8).toFloat();
                }   
              else if (inputString.startsWith("E_amplitude"))
                {
                  E_amplitude=inputString.substring(11).toFloat();
                }
              else if (inputString.startsWith("E_frequency"))
                {
                  E_frequency=inputString.substring(11).toFloat();
                }      
              else if (inputString.startsWith("E_numofscan"))
                {
                  E_numofscan=inputString.substring(11).toFloat()+1;
                }    
              u8x8.drawString(0,0,"E_begin ");
              u8x8.setCursor(8,0);
              u8x8.print(E_begin,1); //不还原真实电压
              u8x8.drawString(0,1,"E_end   ");
              u8x8.setCursor(8,1);
              u8x8.print(E_end,1);
              u8x8.drawString(0,2,"E_step  ");
              u8x8.setCursor(8,2);
              u8x8.print(E_step,1);
              u8x8.drawString(0,3,"Scanrate");
              u8x8.setCursor(8,3);
              u8x8.print(E_scanrate,1);
              u8x8.drawString(0,4,"Pulse   ");
              u8x8.setCursor(8,4);
              u8x8.print(E_pulse,1);
              u8x8.drawString(0,5,"Tpulse  ");
              u8x8.setCursor(8,5);
              u8x8.print(E_Tpulse,1);
              u8x8.drawString(0,6,"Amplitude");
              u8x8.setCursor(8,6);
              u8x8.print(E_amplitude,1);
              u8x8.drawString(0,7,"Frequency");
              u8x8.setCursor(8,7);
              u8x8.print(E_frequency,1);

            }

          else if (inputString.startsWith("TMUX_"))
            {
              showMode = 0;
              u8x8.clearDisplay();

              if (inputString.startsWith("TMUX_100000")||inputString.startsWith("TMUX_100k"))
                {
                  tmuxChannel = TMUX_S8_100k; 
                  tmuxOhm=100000;
                  //Serial.println("TMUX_100k");
                }    
              else if (inputString.startsWith("TMUX_10000")||inputString.startsWith("TMUX_10k"))
                {
                  tmuxChannel = TMUX_S7_10k;
                  tmuxOhm=10000;
                  //Serial.println("TMUX_10k");
                }
              else if (inputString.startsWith("TMUX_1000")||inputString.startsWith("TMUX_1k"))
                {
                  tmuxChannel = TMUX_S6_1k;
                  tmuxOhm=1000;
                  //Serial.println("TMUX_1k");
                }       
              else if (inputString.startsWith("TMUX_100")||inputString.startsWith("tmux_100"))
                {
                  tmuxChannel = TMUX_S5_100;
                  tmuxOhm=100;  
                  //Serial.println("TMUX_100");
                }         
              u8x8.drawString(0,0,"tmuxChannel:");
              u8x8.setCursor(0,1);
              u8x8.print(tmuxChannel,1); 
              u8x8.drawString(0,2,"Ohm:");
              u8x8.setCursor(0,3);
              u8x8.print(tmuxOhm,1);
            }

          else if(inputString.startsWith("MODE"))
            {
              if (inputString.startsWith("MODE 0")||inputString.startsWith("STOP")||inputString.startsWith("stop"))
                {
                  showMode = 0;
                  u8x8.clearDisplay();
                  Serial.println("MODE 0");
                }
              else if (inputString.startsWith("MODE 1"))//potentiometry
                {
                  showMode = 1;
                  u8x8.clearDisplay();
                  Serial.println("MODE 1");
                }
              else if (inputString.startsWith("MODE 2")) //LSV
                {
                  showMode = 2;
                  u8x8.clearDisplay();
                  Serial.println("MODE 2");
                  flagVoltammetry = true;
                }
              else if (inputString.startsWith("MODE 3")) //CV
                {
                  showMode = 3;
                  u8x8.clearDisplay();
                  Serial.println("MODE 3");
                  flagVoltammetry = true;
                }
              else if (inputString.startsWith("MODE 4"))//DPV
                {
                  showMode = 4;
                  u8x8.clearDisplay();
                  Serial.println("MODE 4");
                  flagVoltammetry = true;
                }
              else if (inputString.startsWith("MODE 5"))//SWV
                {
                  showMode = 5;
                  u8x8.clearDisplay();
                  Serial.println("MODE 5");
                  flagVoltammetry = true;
                }
              else if (inputString.startsWith("MODE 6"))//NPV
                {
                  showMode = 6;
                  u8x8.clearDisplay();
                  Serial.println("MODE 6");
                  flagVoltammetry = true;
                }
              else if (inputString.startsWith("MODE A"))//clear
                {
                  showMode = 10;
                  u8x8.clearDisplay();
                  Serial.println("MODE A");               
                }
              else if (inputString.startsWith("MODE B"))//EIS single
                {
                  showMode = 7;
                  u8x8.clearDisplay();
                  Serial.println("MODE B");               
                }
              else if (inputString.startsWith("MODE C"))//EIS mutiple
                {
                  showMode = 8;
                  u8x8.clearDisplay();
                  Serial.println("MODE C");            
                }
              else if (inputString.startsWith("MODE D"))//EIS mutiple
                {
                  showMode = 8;
                  u8x8.clearDisplay();
                  Serial.println("MODE D");          
                }
            }
          
          else if(inputString.startsWith("START")||inputString.startsWith("start")||inputString.startsWith("BEGIN")||inputString.startsWith("begin"))
            {
              Serial.println("START"); //对应EIS，如果500个点，要等15s左右
            }

          else if (inputString.startsWith("R_")) //to board2 data
          {
            if (inputString.startsWith("R_refNum"))
              {
                RrefNum = inputString.substring(8).toInt();
                Serial.print("R_refNum");
                Serial.println(RrefNum);
              }
            else if (inputString.startsWith("R_unkNum"))
              {
                RunkonwNum = inputString.substring(8).toInt();
                Serial.print("R_unkNum");
                Serial.println(RunkonwNum);
              }
          }

          else if (inputString.startsWith("P_")) //to board2 data
          {
            if (inputString.startsWith("P_startFREQ"))
              {
                startFREQ = inputString.substring(11).toInt();
                Serial.print("P_startFREQ");
                Serial.println(startFREQ);
              }
            else if (inputString.startsWith("P_freqINCR"))
              {
                freqINCR = inputString.substring(10).toInt();
                Serial.print("P_freqINCR");
                Serial.println(freqINCR);
              }
            else if (inputString.startsWith("P_numINCR"))
              {
                numINCR = inputString.substring(9).toInt();
                Serial.print("P_numINCR");
                Serial.println(numINCR);
              }
            else if (inputString.startsWith("P_refRESIST"))
              {
                refRESIST = inputString.substring(11).toInt();
                Serial.print("P_refRESIST");
                Serial.println(refRESIST);
              }
          }
          

          /*
          else if (inputString.startsWith("DATA")) 
            {
              showMode = 0; //设置空白模式
              u8x8.clearDisplay();
              if(inputString[5]=='x'||inputString[5]=='X') //e.g. 发送格式DATA3x 1 2 3
              {
                int num=inputString.substring(4).toInt();//数据计数器
                xnum=inputString.substring(4).toInt();//数据计数器
                for(int i=0;i<num;i++)
                {
                  xConcentration[i]=inputString.substring(6+i*2).toFloat();
                }
                //for(int i=0;i<num;i++){Serial.println(xConcentration[i]);}
                u8x8.drawString(0,0,"X:"); //显示X轴数据
                for(int i=0;i<num;i++)
                {
                 u8x8.setCursor(2,i);
                 u8x8.print(xConcentration[i]);
                }

              }         
              else if(inputString[5]=='y'||inputString[5]=='Y')//e.g. 发送格式DAT4y 1.1234 2.1234 3.1456 0.1651 都是4位小数
              {
                int num=inputString.substring(4).toInt();//数据计数器
                for(int i=0;i<num;i++)
                {
                  yPotential[i]=inputString.substring(6+i*7).toFloat();
                }
                //for(int i=0;i<num;i++){Serial.println(yPotential[i],5);}
                u8x8.drawString(7,0,"Y:");
                u8x8.drawString(0,0,"X:");
                for(int i=0;i<num;i++)
                {
                 u8x8.setCursor(9,i);
                 u8x8.print(yPotential[i],4);
                 u8x8.setCursor(2,i);
                 u8x8.print(xConcentration[i]);
                }
              }
              else
              {
                for(int i=0;i<10;i++)//clear the array
                {
                  xConcentration[i]=0;
                  yPotential[i]=0;
                }

                Serial.println("no data");
              }
             
            }            
          */

          /*
          else if(inputString=="a\n")
            {
              u8x8.clearDisplay();
              u8x8.drawString(0,3,"Command:");
              u8x8.setCursor(0,4);
              u8x8.print(inputString);

            }
          */
          inputString = ""; // clear the string:
          stringComplete = false;
          //digitalWrite(LED,digitalRead(LED)^1); 
                   
        }

  }

void SSD1306_DisplayMode(int modeNum)
  {
    

    switch(modeNum)
    {
      case 0:

        break;

      case 1: //双电极系统,单传感器电位    
        {
          singlePotentiometry();
          break; 
        }        
      case 2: //三电极系统,单传感器电位  LSV  
        {
          if(flagVoltammetry==true)
            {
              u8x8.drawString(0,0, "MODE2: ");  
              //Serial.println("LSV");
              while(--E_numofscan && E_numofscan>0){
                voltammetryLSV();
              }
            }
          flagVoltammetry=false;
          break; 
        }  
      case 3: //三电极系统,单传感器电位  CV 
        {
          if(flagVoltammetry==true)
            {
              u8x8.drawString(0,0, "MODE3: ");  
              //Serial.println("CV");
              if(E_end>E_begin)
                {
                  while(--E_numofscan && E_numofscan>0){voltammetryCV();}
                }
              else
                {
                  while(--E_numofscan && E_numofscan>0){voltammetryCV2();}
                }
              
            }
          flagVoltammetry=false;
          break; 
        }  
      case 4: //三电极系统,单传感器电位  DPV 
        {
          if(flagVoltammetry==true)
            {
              u8x8.drawString(0,0, "MODE4: ");  
              //Serial.println("DPV");
            
              if(E_end>E_begin)
                {
                  while(--E_numofscan && E_numofscan>0){voltammetryDPV_HZC();}
                }
              else
                {
                  while(--E_numofscan && E_numofscan>0){voltammetryDPV2_HZC();}
                }
              
            }
          flagVoltammetry=false;
          break; 
        }
      case 5: //三电极系统,单传感器电位  SWV 
        {
          if(flagVoltammetry==true)
            {
              u8x8.drawString(0,0, "MODE5: ");  
              //Serial.println("SWV");
              if(E_end>E_begin)
                {
                  while(--E_numofscan && E_numofscan>0){voltammetrySWV_HZC();}
                }
              else
                {
                  while(--E_numofscan && E_numofscan>0){voltammetrySWV2_HZC();}
                }
              
            }
          flagVoltammetry=false;
          break; 
        }
      case 6: //三电极系统,单传感器电位  NPV 
        {
          if(flagVoltammetry==true)
            {
              u8x8.drawString(0,0, "MODE6: ");  
              //Serial.println("NPV");
              if(E_end>E_begin)
                {
                  while(--E_numofscan && E_numofscan>0){voltammetryNPV_CZC();}
                }
              else
                {
                  while(--E_numofscan && E_numofscan>0){voltammetryNPV_CZC();}
                }
              
            }
          flagVoltammetry=false;
          break; 
        }    

        
   /*   
      case 2: //均值滤波版本，直接显示S2-S8的放大后电压
        u8x8.setFont(u8x8_font_chroma48medium8_r);
        //u8x8.clearDisplay();
        u8x8.drawString(0,0,"Potential [V]:");

        for(int num=2;num<9;num++) //7个channal
        {
          TMUX1108_Mode(num);
          delay(10);
          voltage = 0;
          for(int i=0;i<20;i++)//求平均电压值，30个一组效果最好
          {
            voltage += readChannel(ADS1115_COMP_0_GND);
            delay(2);
          }
          voltage = voltage/20;
          //unsigned int voltageRange = adc.getVoltageRange_mV(); //查看分辨率
          //Serial.print("Channel0 Resolution >>>");
          //Serial.println(voltageRange);
          char buffer[20];
          sprintf(buffer, "Channel S%d [V]: ", num); 
          Serial.print(buffer);
          Serial.println(voltage,4);
          sprintf(buffer, "S%d: ", num);
          u8x8.drawString(0,num-1, buffer);
          u8x8.setCursor(4,num-1);
          u8x8.print(voltage,4);
          delay(10);
        }
        break;   

      case 3: //均值滤波版本，直接显示S2-S8的原电压，串口每次发1个点,对应串口调试助手波形显示
        u8x8.setFont(u8x8_font_chroma48medium8_r);
        //u8x8.clearDisplay();
        u8x8.drawString(0,0,"Potential [V]:");

        for(int num=2;num<9;num++) //7个channal
        {
          TMUX1108_Mode(num);
          delay(10);
          voltage = 0;
          for(int i=0;i<30;i++)//求平均电压值
          {
            voltage += readChannel(ADS1115_COMP_0_GND);
            delay(2);
          }
          voltage = voltage/30;
          //unsigned int voltageRange = adc.getVoltageRange_mV(); //查看分辨率
          //Serial.print("Channel0 Resolution >>>");
          //Serial.println(voltageRange);
          char buffer[20];
          //sprintf(buffer, "Channel S%d [V]: ", num); 
          sprintf(buffer, "S%d=", num); 
          Serial.print(buffer);
          Serial.println(voltage/2,4);
          sprintf(buffer, "S%d: ", num);
          u8x8.drawString(0,num-1, buffer);
          u8x8.setCursor(4,num-1);
          u8x8.print(voltage/2,4);
          delay(10);
        }
        break;  


      case 4: //均值滤波版本，直接显示S4的原电压，串口每次发1个点,对应串口调试助手波形显示，保留4位小数
        u8x8.setFont(u8x8_font_chroma48medium8_r);
        //u8x8.clearDisplay();
        u8x8.drawString(0,0,"Potential [V]:");

        //for(int num=1;num<7;num++) //6个channal
        //{
          int num=4;
          TMUX1108_Mode(num);
          delay(10);
          voltage = 0;
          for(int i=0;i<20;i++)//求平均电压值
          {
            voltage += readChannel(ADS1115_COMP_0_GND);
          }
          voltage = voltage/20;
          //unsigned int voltageRange = adc.getVoltageRange_mV(); //查看分辨率
          //Serial.print("Channel0 Resolution >>>");
          //Serial.println(voltageRange);
          char buffer[20];
          //sprintf(buffer, "Channel S%d [V]: ", num); 
          sprintf(buffer, "S%d=", num); 
          Serial.print(buffer);
          Serial.println(voltage/2,4);
          sprintf(buffer, "S%d: ", num);
          u8x8.drawString(0,num, buffer);
          u8x8.setCursor(4,num);
          u8x8.print(voltage/2,4);
          delay(10);
        //}
        break; 

      case 5://通过输入的点来拟合曲线
        u8x8.setFont(u8x8_font_chroma48medium8_r);
        LScurveFitting(xConcentration, yPotential, xnum, &k1, &b1);
        Serial.print("rSquare: ");
        Serial.println(LScurveFitting(xConcentration, yPotential, xnum, &k1, &b1),4);
        Serial.print("k1=");
        Serial.println(k1,4);
        Serial.print("b1=");
        Serial.println(b1,4);
        u8x8.drawString(0,6, "k=");
        u8x8.setCursor(4,6);
        u8x8.print(k1,4);
        u8x8.drawString(0,7, "b=");
        u8x8.setCursor(4,7);
        u8x8.print(b1,4);
        showMode =0;  //only show the result once
        delay(10);

        break;
*/
    }

  }

/*
//least square curve fitting y=kx+b
float LScurveFitting(float* x, float* y, int n, float* a, float* b)
{
	float sumx = 0.0;
	float sumy = 0.0;
	float sumx2 = 0.0;
  float sumy2 = 0.0;
	float sumxy = 0.0;
  float errorSquare = 0.0;
  float rSquare = 0.0;
	for (int i = 0; i < n; i++)
	{
		sumx += x[i];
		sumy += y[i];
		sumx2 += x[i] * x[i];
		sumxy += x[i] * y[i];
    sumy2 += y[i] * y[i];
	}
	*a = (n * sumxy - sumx * sumy) / (n * sumx2 - sumx * sumx);
	*b = (sumy - *a * sumx) / n;
  for(int i=0;i<n;i++)
  {
    errorSquare += (y[i]-(*a*x[i]+*b))*(y[i]-(*a*x[i]+*b));  //误差Q方,越小误差越小
  }
  rSquare = (n * sumxy - sumx * sumy) * (n * sumxy - sumx * sumy) / (n * sumx2 - sumx * sumx) / (n * sumy2 - sumy * sumy); //R方,决定系数越接近1越准确
  //Serial.print("errorSquare: ");
  //Serial.println(errorSquare,5);
  //Serial.print("rSquare: ");
  //Serial.println(rSquare,5);
  return rSquare;
}

*/


void TMUX1108_Mode(int modeNum)
  {
    digitalWrite(TMUX1108_EN, HIGH);
    switch(modeNum)
    {
      case 1:  //S1
        digitalWrite(TMUX1108_A0, LOW);
        digitalWrite(TMUX1108_A1, LOW);
        digitalWrite(TMUX1108_A2, LOW);
        break;
      case 2:  //S2
        digitalWrite(TMUX1108_A0, HIGH);
        digitalWrite(TMUX1108_A1, LOW);
        digitalWrite(TMUX1108_A2, LOW);
        break;
      case 3:  //S3
        digitalWrite(TMUX1108_A0, LOW);
        digitalWrite(TMUX1108_A1, HIGH);
        digitalWrite(TMUX1108_A2, LOW);
        break;
      case 4:  //S4
        digitalWrite(TMUX1108_A0, HIGH);
        digitalWrite(TMUX1108_A1, HIGH);
        digitalWrite(TMUX1108_A2, LOW);
        break;
      case 5:  //S5, 100ohm
        digitalWrite(TMUX1108_A0, LOW);
        digitalWrite(TMUX1108_A1, LOW);
        digitalWrite(TMUX1108_A2, HIGH);
        tmuxOhm=100;
        break;
      case 6:  //S6, 1Kohm
        digitalWrite(TMUX1108_A0, HIGH);
        digitalWrite(TMUX1108_A1, LOW);
        digitalWrite(TMUX1108_A2, HIGH);
        tmuxOhm=1000;
        break;
      case 7:  //S7, 10Kohm
        digitalWrite(TMUX1108_A0, LOW);
        digitalWrite(TMUX1108_A1, HIGH);
        digitalWrite(TMUX1108_A2, HIGH);
        tmuxOhm=10000;
        break;
      case 8:  //S8, 100Kohm
        digitalWrite(TMUX1108_A0, HIGH);
        digitalWrite(TMUX1108_A1, HIGH);
        digitalWrite(TMUX1108_A2, HIGH);
        tmuxOhm=100000;
        break;
    }
  }

float readChannel(ADS1115_MUX channel) {
  float voltage = 0.0;
  adc.setCompareChannels(channel);
  voltage = adc.getResult_V(); // alternative: getResult_mV for Millivolt
  return voltage;
}

void serialEvent() 
{
  while (Serial.available()) 
  {   
    char inChar = (char)Serial.read();// get the new byte:    
    inputString += inChar;// add it to the inputString:
    if (inChar == '\n') 
    {
      stringComplete = true;// if the incoming character is a newline, set a flag so the main loop can
    }
  }
}

void receiveEvent(int byteCount) //I2C receive data
{
  String receivedData = "";
  while (Wire.available()) {
    char c = Wire.read();
    receivedData += c;
  }
  
  // 检查接收到的数据类型
  /*
  if (receivedData.startsWith("Z=")) 
  {  
    byte buffer[sizeof(float)];
    receivedData.remove(0, 2);
    for (int i = 0; i < sizeof(float); i++) {
      buffer[i] = receivedData[i];
    }
    float receivedFloat;
    memcpy(&receivedFloat, buffer, sizeof(float));
    Serial.println("Z=" + String(receivedFloat));
  }
  else if (receivedData.startsWith("R=")) 
  {  
    byte buffer[sizeof(float)];
    receivedData.remove(0, 2);
    for (int i = 0; i < sizeof(float); i++) {
      buffer[i] = receivedData[i];
    }
    float receivedFloat;
    memcpy(&receivedFloat, buffer, sizeof(float));
    Serial.println("R=" + String(receivedFloat));
  }
  else if (receivedData.startsWith("I=")) 
  {  
    byte buffer[sizeof(float)];
    receivedData.remove(0, 2);
    for (int i = 0; i < sizeof(float); i++) {
      buffer[i] = receivedData[i];
    }
    float receivedFloat;
    memcpy(&receivedFloat, buffer, sizeof(float));
    Serial.println("I=" + String(receivedFloat));
  }

  */
  if (receivedData.startsWith("Z1=")) 
  {  
    receivedData.remove(0, 3);
    Serial.println("Z1=" + String(receivedData));
  }
  else if (receivedData.startsWith("R1=")) 
  {  
    receivedData.remove(0, 3);
    Serial.println("R1=" + String(receivedData));
  }
  else if (receivedData.startsWith("I1=")) 
  {  
    receivedData.remove(0, 3);
    Serial.println("I1=" + String(receivedData));
  }
  
  else if (receivedData.startsWith("F1=")) 
  {  
    receivedData.remove(0, 3);
    Serial.println("F1=" + String(receivedData));
  }
  else if (receivedData.startsWith("T1=")) 
  {  
    receivedData.remove(0, 3);
    Serial.println("T1=" + String(receivedData));
  }
  else if (receivedData.startsWith("OK")) 
  {     
    Serial.println("OK");
  }
}

void singlePotentiometry()
{
  float voltage = 0.0;
  float voltage_S1_Plus = 0.0, voltage_S1_Minus = 0.0;
  //unsigned int voltageRange = adc.getVoltageRange_mV(); //查看分辨率//
  //Serial.print("Channel0 Resolution >>>");//
  //Serial.println(voltageRange);      //
  voltage_S1_Plus = readChannel(ADS1115_COMP_2_GND);
  voltage_S1_Minus = readChannel(ADS1115_COMP_3_GND);
  if(voltage_S1_Minus >0.8) //理论上S1_Minus是1，但是实际会小，0.97左右
    {
      voltage = (voltage_S1_Plus/2)-voltage_S1_Minus;
    }
  else
    {
      voltage = voltage_S1_Plus/2;
    }
  //Serial.print("v_S+=");
  //Serial.println(voltage_S1_Plus,4);         
  //Serial.print("v_S-=");
  //Serial.println(voltage_S1_Minus,4);
  Serial.print("S2=");
  Serial.println(voltage,4);
  u8x8.drawString(0,0, "MODE1: ");        
  u8x8.drawString(0,1, "v_S+: ");
  u8x8.drawString(0,2, "v_S-: ");
  u8x8.drawString(0,3, "volt: ");
  u8x8.setCursor(5,1);
  u8x8.print(voltage_S1_Plus,4);
  u8x8.setCursor(5,2);
  u8x8.print(voltage_S1_Minus,4);
  u8x8.setCursor(5,3);
  u8x8.print(voltage,4);  

  //delay(500);///可不需要
}

float voltammetryLSV()
{
  //dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
  TMUX1108_Mode(tmuxChannel);
  float stepNum = ((E_end - E_begin) / E_step)+1;
  float T_interval = (E_step/E_scanrate)*1000;
  unsigned long previousMillis = 0;
  
  for (int i = 0; i < stepNum; )
  {
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= T_interval)
    {
      previousMillis = currentMillis;
      float counter = ((i*E_step + E_begin)/(E_supply/4096)); //1.1499为电压转换系数,4.71V/4096
      dac.setVoltage(counter, false);
      i ++;

      //float reVoltage = readChannel(ADS1115_COMP_1_GND);
      float weVoltage = readChannel(ADS1115_COMP_0_GND);
      Serial.print("ce=");
      Serial.println(-((i*E_step + E_begin)/1000-(E_supply/1000/2))); //mV to V ,set 2.4V to 0V to middle
      //Serial.print("re=");
      //Serial.println(reVoltage);
      Serial.print("we=");
      Serial.println(weVoltage);

    }
  }
//dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V

}

float voltammetryCV()
{
  //dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
  TMUX1108_Mode(tmuxChannel);
  float stepNum = ((E_end - E_begin) / E_step)+1;
  float T_interval = (E_step/E_scanrate)*1000;
  unsigned long previousMillis = 0;

  for (int i = 0; i < stepNum; )
  {
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= T_interval)
    {
      previousMillis = currentMillis;
      float counter = ((i*E_step + E_begin)/(E_supply/4096)); //1.1499为电压转换系数,4.71V/4096
      dac.setVoltage(counter, false);
      i ++;

      //float reVoltage = readChannel(ADS1115_COMP_1_GND);
      float weVoltage = readChannel(ADS1115_COMP_0_GND);
      //Serial.print("re=");
      //Serial.println(reVoltage);
      Serial.print("we=");
      Serial.println((weVoltage-2.4),4);
      Serial.print("ce=");
      Serial.println(-((i*E_step + E_begin)/1000-(E_supply/1000/2)),4);
    }

  }
    for (int i = 1; i < stepNum; )
  {
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= T_interval)
    {
      previousMillis = currentMillis;
      float counter = ((E_end - i*E_step)/(E_supply/4096)); 
      dac.setVoltage(counter, false);
      i++;

      //float reVoltage = readChannel(ADS1115_COMP_1_GND);
      float weVoltage = readChannel(ADS1115_COMP_0_GND);
      Serial.print("we=");
      Serial.println((weVoltage-2.4),4);
      Serial.print("ce=");
      Serial.println(-((E_end - i*E_step)/1000-(E_supply/1000/2)),4);
    }
  }
  //dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
}

float voltammetryCV2()
{
  //dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
  TMUX1108_Mode(tmuxChannel);
  float stepNum = ((E_begin - E_end) / E_step)+1;
  float T_interval = (E_step/E_scanrate)*1000;
  unsigned long previousMillis = 0;

  for (int i = 1; i < stepNum; )
  {
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= T_interval)
    {
      previousMillis = currentMillis;
      float counter = ((E_begin - i*E_step)/(E_supply/4096)); 
      dac.setVoltage(counter, false);
      i++;

      //float reVoltage = readChannel(ADS1115_COMP_1_GND);
      float weVoltage = readChannel(ADS1115_COMP_0_GND);
      Serial.print("we=");
      Serial.println((weVoltage-2.4),4);
      Serial.print("ce=");
      Serial.println(-((E_begin - i*E_step)/1000-(E_supply/1000/2)),4);
    }
  }
  for (int i = 0; i < stepNum; )
  {
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= T_interval)
    {
      previousMillis = currentMillis;
      float counter = ((i*E_step + E_end)/(E_supply/4096)); //1.1499为电压转换系数,4.71V/4096
      dac.setVoltage(counter, false);
      i ++;

      //float reVoltage = readChannel(ADS1115_COMP_1_GND);
      float weVoltage = readChannel(ADS1115_COMP_0_GND);
      //Serial.print("re=");
      //Serial.println(reVoltage);
      Serial.print("we=");
      Serial.println((weVoltage-2.4),4);
      Serial.print("ce=");
      Serial.println(-((i*E_step + E_end)/1000-(E_supply/1000/2)),4);
    }

  }
  //dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
}

float voltammetryDPV()
{
  dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
  delay(1000);
  TMUX1108_Mode(tmuxChannel);
  float stepNum = (E_end - E_begin) / E_step+1;
  float T_interval = (E_step/E_scanrate)*1000;
  float E_diff = E_pulse - E_step;
  float counter1 ,counter2;
  unsigned long previousMillis = 0;
  for (int i = 0; i < stepNum; )
  {    
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= T_interval)
    {
      previousMillis = currentMillis;
      counter1 = (((i*E_step + E_begin)+E_diff)/(E_supply/4096)); 
      dac.setVoltage(counter1, false);
      delay(E_Tpulse); 
      counter2 = ((i*E_step + E_begin)/(E_supply/4096)); 
      dac.setVoltage(counter2, false);
      i ++;
    

      float weVoltage = readChannel(ADS1115_COMP_0_GND);
      Serial.print("ce=");
      //Serial.println((i*E_step + E_begin)/1000);
      Serial.println(-((i*E_step + E_begin)/1000-(E_supply/1000/2)),4);
      Serial.print("we=");
      Serial.println(weVoltage,4);
    }

  }
  dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
}

float voltammetryDPV2()
{
  dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
  delay(1000);
  TMUX1108_Mode(tmuxChannel);
  float stepNum = (E_begin - E_end) / E_step+1;  //改为E_begin - E_end
  float T_interval = (E_step/E_scanrate)*1000;
  float E_diff = E_pulse - E_step;
  float counter1 ,counter2;
  unsigned long previousMillis = 0;
  for (int i = 0; i < stepNum; )
  {    
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= T_interval)
    {
      previousMillis = currentMillis;
      counter1 = (((E_begin - i*E_step)-E_diff)/(E_supply/4096)); 
      dac.setVoltage(counter1, false);
      delay(E_Tpulse); 
      counter2 = ((E_begin - i*E_step)/(E_supply/4096)); 
      dac.setVoltage(counter2, false);
      i ++;
    

      float weVoltage = readChannel(ADS1115_COMP_0_GND);
      Serial.print("ce=");
      //Serial.println((i*E_step + E_begin)/1000);
      Serial.println(-((i*E_step + E_begin)/1000-(E_supply/1000/2)),4);//-E_step 系统偏差
      Serial.print("we=");
      Serial.println(weVoltage,4);
    }

  }
  dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
}

float voltammetrySWV()
{
  dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
  TMUX1108_Mode(tmuxChannel);
  float stepNum = (E_end - E_begin) / E_step+1;
  float T_interval = 1/E_frequency*1000;
  float T_wait = T_interval/2;
  float counter1 ,counter2;
  unsigned long previousMillis = 0;
  for (int i = 0; i < stepNum; )
  {    
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= T_interval)
    {
      previousMillis = currentMillis;
      counter1 = ((i*E_step + E_begin+(E_amplitude*2))/(E_supply/4096)); 
      dac.setVoltage(counter1, false);
      delay(T_wait); 
      counter2 = ((i*E_step + E_begin)/(E_supply/4096)); 
      dac.setVoltage(counter2, false);
      i ++;

      float weVoltage = readChannel(ADS1115_COMP_0_GND);
      Serial.print("ce=");
      Serial.println(-((i*E_step + E_begin)/1000-(E_supply/1000/2)));
      Serial.print("we=");
      Serial.println(weVoltage);
    }

  }
  dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
}

float voltammetrySWV2()
{
  dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
  TMUX1108_Mode(tmuxChannel);
  float stepNum = (E_begin - E_end) / E_step+1;
  float T_interval = 1/E_frequency*1000;
  float T_wait = T_interval/2;
  float counter1 ,counter2;
  unsigned long previousMillis = 0;
  for (int i = 0; i < stepNum; )
  {    
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= T_interval)
    {
      previousMillis = currentMillis;
      counter1 = ((E_begin - i*E_step -(E_amplitude*2))/(E_supply/4096)); 
      dac.setVoltage(counter1, false);
      delay(T_wait); 
      counter2 = ((E_begin - i*E_step)/(E_supply/4096)); 
      dac.setVoltage(counter2, false);
      i ++;

      float weVoltage = readChannel(ADS1115_COMP_0_GND);
      Serial.print("ce=");
      Serial.println(-((i*E_step + E_begin)/1000-(E_supply/1000/2)));
      Serial.print("we=");
      Serial.println(weVoltage);
    }

  }
  dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
}

float voltammetryNPV()
{
  dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
  TMUX1108_Mode(tmuxChannel);
  float stepNum = (E_end - E_begin) / E_step+1;
  float T_interval = (E_step/E_scanrate)*1000;
  //float T_wait = T_interval-E_Tpulse;
  unsigned long previousMillis = 0;
  for (int i = 0; i < stepNum; )
  {
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= T_interval)
    {
      previousMillis = currentMillis;
      float counter = ((i*E_step + E_begin)/(E_supply/4096)); 
      dac.setVoltage(counter, false);
      delay(E_Tpulse);
      dac.setVoltage((E_supply/2)/(E_supply/4096), false);
      //delay(T_wait);
      i ++;
     
      float weVoltage = readChannel(ADS1115_COMP_0_GND);
      Serial.print("ce=");
      Serial.println(-((i*E_step + E_begin)/1000-(E_supply/1000/2)));
      Serial.print("we=");
      Serial.println(weVoltage);
    }

  }
  dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
}

float voltammetryNPV2()//dai xiugai
{
  dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
  TMUX1108_Mode(tmuxChannel);
  float stepNum = (E_begin - E_end) / E_step+1;
  float T_interval = (E_step/E_scanrate)*1000;
  //float T_wait = T_interval-E_Tpulse;
  unsigned long previousMillis = 0;
  for (int i = 0; i < stepNum; )
  {
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= T_interval)
    {
      previousMillis = currentMillis;
      float counter = ((E_begin - i*E_step)/(E_supply/4096)); 
      dac.setVoltage(counter, false);
      delay(E_Tpulse);
      dac.setVoltage((E_supply/2)/(E_supply/4096), false);
      //delay(T_wait);
      i ++;
     
      float weVoltage = readChannel(ADS1115_COMP_0_GND);
      Serial.print("ce=");
      Serial.println(-((i*E_step + E_begin)/1000-(E_supply/1000/2)));
      Serial.print("we=");
      Serial.println(weVoltage);
    }

  }
  dac.setVoltage((E_supply/2)/(E_supply/4096), false);//set Voltage to 2.4V
}

float voltammetryDPV_HZC()//right to left
{
  E_time = (unsigned long) E_step /E_scanrate*1000;
  float counter1 ,Voltage_out;
  float weVoltage, weVoltage0, weVoltage1;
  for (Voltage_out = E_begin; Voltage_out < E_end; Voltage_out += E_step)//right to left
  {
    Serial.print("ce=");
    Serial.println(-(Voltage_out/1000-(E_supply/1000/2)),4);
    weVoltage0 = readChannel(ADS1115_COMP_0_GND);
    Voltage_out = Voltage_out + E_pulse;
    dac.setVoltage(Voltage_out/(E_supply/4096), false);
    delay(E_Tpulse);
    weVoltage1 = readChannel(ADS1115_COMP_0_GND);
    weVoltage = (weVoltage1-weVoltage0);
    Serial.print("we=");
    Serial.println(weVoltage,4);
    Voltage_out = Voltage_out - E_pulse; 
    dac.setVoltage(Voltage_out/(E_supply/4096), false);
    delay(E_time - E_Tpulse);

  }
}

float voltammetryDPV2_HZC()//left to right
{
  E_time = (unsigned long) E_step /E_scanrate*1000;
  float counter1 ,Voltage_out;
  float weVoltage, weVoltage0, weVoltage1;
  for (Voltage_out = E_begin; Voltage_out > E_end; Voltage_out -= E_step)//left to right
  {
    Serial.print("ce=");
    Serial.println(-(Voltage_out/1000-(E_supply/1000/2)),4);
    weVoltage0 = readChannel(ADS1115_COMP_0_GND);
    Voltage_out = Voltage_out - E_pulse;
    dac.setVoltage(Voltage_out/(E_supply/4096), false);
    delay(E_Tpulse);
    weVoltage1 = readChannel(ADS1115_COMP_0_GND);
    weVoltage = (weVoltage1-weVoltage0);
    Serial.print("we=");
    Serial.println(weVoltage,4);
    Voltage_out = Voltage_out + E_pulse; 
    dac.setVoltage(Voltage_out/(E_supply/4096), false);
    delay(E_time - E_Tpulse);

  }


}

float voltammetrySWV_HZC()//right to left
{
  E_time = (unsigned long) 1000/(2*E_frequency);
  float counter1 ,Voltage_out;
  float weVoltage, weVoltage0, weVoltage1;
  for (Voltage_out = E_begin; Voltage_out < E_end; Voltage_out += E_step)
  {
   
    dac.setVoltage((Voltage_out + E_amplitude)/(E_supply/4096), false);
    delay(E_time);
    Serial.print("ce=");
    Serial.println(-(Voltage_out/1000-(E_supply/1000/2)),4);
    weVoltage0 = readChannel(ADS1115_COMP_0_GND);
    dac.setVoltage((Voltage_out - E_amplitude)/(E_supply/4096), false);
    delay(E_time);
    weVoltage1 = readChannel(ADS1115_COMP_0_GND);
    weVoltage = weVoltage0 - weVoltage1;
    Serial.print("we=");
    Serial.println(weVoltage,4);

  }


}

float voltammetrySWV2_HZC()//left to right
{
  E_time = (unsigned long) 1000/(2*E_frequency);
  float counter1 ,Voltage_out;
  float weVoltage, weVoltage0, weVoltage1;
  for (Voltage_out = E_begin; Voltage_out > E_end; Voltage_out -= E_step)
  {
    
    dac.setVoltage((Voltage_out - E_amplitude)/(E_supply/4096), false);
    delay(E_time);
    Serial.print("ce=");
    Serial.println(-(Voltage_out/1000-(E_supply/1000/2)),4);
    weVoltage0 = readChannel(ADS1115_COMP_0_GND);
    dac.setVoltage((Voltage_out + E_amplitude)/(E_supply/4096), false);
    delay(E_time);
    weVoltage1 = readChannel(ADS1115_COMP_0_GND);
    weVoltage = weVoltage0 - weVoltage1;
    Serial.print("we=");
    Serial.println(weVoltage,4);

  }

}

float voltammetryNPV_CZC()//left to right
{
  E_time = (unsigned long) E_step /E_scanrate*1000;
  float Voltage_out0 ,Voltage_out;
  float weVoltage, weVoltage0, weVoltage1;
  for (Voltage_out = E_begin+E_step,Voltage_out0=E_begin; Voltage_out < E_end; Voltage_out += E_step)//right to left
  {
    dac.setVoltage(Voltage_out/(E_supply/4096), false);
    delay(E_Tpulse);
    Serial.print("ce=");
    Serial.println(-(Voltage_out/1000-(E_supply/1000/2)),4);
    weVoltage0 = readChannel(ADS1115_COMP_0_GND);

    dac.setVoltage(Voltage_out0/(E_supply/4096), false);
    delay(E_time -E_Tpulse);

    Voltage_out = Voltage_out+E_step;
    dac.setVoltage(Voltage_out/(E_supply/4096), false);
    delay(E_Tpulse);
    weVoltage1 = readChannel(ADS1115_COMP_0_GND);
    weVoltage = (weVoltage1-weVoltage0);
    Serial.print("we=");
    Serial.println(weVoltage,4);

    dac.setVoltage(Voltage_out0/(E_supply/4096), false);
    delay(E_time -E_Tpulse);

  }
}

float voltammetryNPV2_CZC()//right to left
{
  E_time = (unsigned long) E_step /E_scanrate*1000;
  float Voltage_out0 ,Voltage_out;
  float weVoltage, weVoltage0, weVoltage1;
  for (Voltage_out = E_begin-E_step,Voltage_out0=E_begin; Voltage_out > E_end; Voltage_out -= E_step)//right to left
  {
    dac.setVoltage(Voltage_out/(E_supply/4096), false);
    delay(E_Tpulse);
    Serial.print("ce=");
    Serial.println(-(Voltage_out/1000-(E_supply/1000/2)),4);
    weVoltage0 = readChannel(ADS1115_COMP_0_GND);

    dac.setVoltage(Voltage_out0/(E_supply/4096), false);
    delay(E_time -E_Tpulse);

    Voltage_out = Voltage_out-E_step;
    dac.setVoltage(Voltage_out/(E_supply/4096), false);
    delay(E_Tpulse);
    weVoltage1 = readChannel(ADS1115_COMP_0_GND);
    weVoltage = (weVoltage1-weVoltage0);
    Serial.print("we=");
    Serial.println(weVoltage,4);

    dac.setVoltage(Voltage_out0/(E_supply/4096), false);
    delay(E_time -E_Tpulse);

  }
}



















/*
 *                        _oo0oo_
 *                       o8888888o
 *                       88" . "88
 *                       (| -_- |)
 *                       0\  =  /0
 *                     ___/`---'\___
 *                   .' \\|     |// '.
 *                  / \\|||  :  |||// \
 *                 / _||||| -:- |||||- \
 *                |   | \\\  - /// |   |
 *                | \_|  ''\---/''  |_/ |
 *                \  .-\__  '-'  ___/-. /
 *              ___'. .'  /--.--\  `. .'___
 *           ."" '<  `.___\_<|>_/___.' >' "".
 *          | | :  `- \`.;`\ _ /`;.`/ - ` : | |
 *          \  \ `_.   \_ __\ /__ _/   .-` /  /
 *      =====`-.____`.___ \_____/___.-`___.-'=====
 *                        `=---='
 * 
 * 
 *      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 * 
 *            BUddha bless never without BUG
 */

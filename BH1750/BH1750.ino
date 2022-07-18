#include <SparkFunTSL2561.h>

 #include <Wire.h>


  int BH1750_Device = 0x23;                                       // I2C address for BH1720 light sensor
  float lux, Scaled_FtCd;
  float lux_av, lux_av2; 
  float  FtCd, wattsm2;
  int    iteration = 0;
  int    iteration_time = 20;
 // unsigned myTime;   
void setup() {

   Serial.begin (9600);
  // Serial.println("BH1750");

   Wire.begin ();
   Wire.beginTransmission (BH1750_Device);
   Wire.write (0x10);                                                  // sets resolution to 1 Lux
   Wire.endTransmission ();
   delay (100);
   

}

void loop() 
{
   iteration++;
   const float mov_avg_alpha = 0.1;
   static float mov_avg = -100;
   
   lux = BH1750_Read();
   lux_av= (lux_av + lux)/2;
   lux_av2=(lux_av2 + lux_av+ lux)/3;
   if (mov_avg == -100) mov_avg = lux;
   mov_avg= (mov_avg_alpha*lux + (1- mov_avg_alpha)*lux);
  
   //FtCd = lux_av/10.764;
   //wattsm2 = lux_av/683.0;
//   myTime = millis();
  // Serial.print ("iteration: ");
  // Serial.println (iteration);  
  // Serial.print ("Watts per square meter: ");
  // Serial.println (wattsm2,4); 
  // Serial.print ("lux = ");
   //Serial.print(60);
   //Serial.print(" ");
   //Serial.print(20);    
   Serial.print(" ");
   Serial.print(lux_av);
   //Serial.print(" ");
   //Serial.print(round(mov_avg));
   Serial.println ();
   
   delay (iteration_time);
   
}

// subroutine

 unsigned int BH1750_Read() {

   unsigned int i=0;
   Wire.beginTransmission (BH1750_Device);
   Wire.requestFrom (BH1750_Device, 2);
   while(Wire.available ()) 
   {
     i <<=8;
     i|= Wire.read();  
   }
   Wire.endTransmission();  
   return i/1.2;  // Convert to Lux
}

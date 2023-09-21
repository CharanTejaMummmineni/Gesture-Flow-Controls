#include <Servo.h>
#define inputs 7
#define inputlen 4
Servo thumb;
Servo index;
Servo middle;
Servo ring;
Servo small;
Servo elbow;
Servo Shoulder;
int valsrec[7];
int stringlen = (7*inputlen) + 1;
int counter = 0;
bool counterstart = false;
String received;


int temp1=0;
int temp2=0;
int temp3=0;
int temp4=0;

void setup()
{
  Serial.begin(9600);
  thumb.attach(6);
  index.attach(2);
  middle.attach(3);
  ring.attach(4);
  small.attach(5);
  elbow.attach(9);
  Shoulder.attach(10);
}

void program()
{  
  while(Serial.available())
  {
    char c = Serial.read();
    if (c == '$')
    {
      counterstart = true;
    }
    if(counterstart == true);
    {
      if(counter < stringlen)
      {
       received = String(received + c); 
       counter++;
      }
    }
    if(counter >= stringlen)
    {
      for(int i=0; i<7; i++)
      {
        int k=(i*4)+1;
        valsrec[i] = received.substring(k,k+4) .toInt();
      }
      received = "";
      counter = 0;
      counterstart = false;
    }
  }
}

void loop()
{
  program();
  if(valsrec[0]==1)
  {
    thumb.write(180);
  }
  else
  {
    thumb.write(0);
  }
  if(valsrec[1]==1)
  {
    index.write(180);
  }
  else
  {
    index.write(0);
  }
  if(valsrec[2]==1)
  {
    middle.write(180);
  }
  else
  {
    middle.write(0);
  }
  if(valsrec[3]==1)
  {
    ring.write(180);
  }
  else
  {
    ring.write(0);
  }
  if(valsrec[4]==1)
  {
    small.write(180);
  }
  else
  {
    small.write(0);
  }
  temp2 = temp1;
  temp1 = valsrec[5];
  if(temp1 >= temp2)
  {
    for(int pos=temp2;pos<=temp1;pos++)
    {
      elbow.write(pos);
    }
  }
  else
  {
    for(int pos=temp1;pos>=temp2;pos++)
    {
      elbow.write(pos);
    }
  }
  temp4 = temp3;
  temp3 = valsrec[6];
  if(temp3 >= temp4)
  {
    for(int pos=temp4;pos<=temp3;pos++)
    {
      Shoulder.write(pos);
    }
  }
  else
  {
    for(int pos=temp3;pos>=temp4;pos++)
    {
      Shoulder.write(pos);
    }
  }
}

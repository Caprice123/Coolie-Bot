# Coolie Bot (Robot for Transporting using MQTT)
 Coolie Bot is a robot that is used for transporting things from one place to other place. This robot is still prototype using arduino as the microcontroller.
 
## Table of contents

- [Overview](#overview)
  - [Description](#description)
  - [The challenge](#the-challenge)
  - [Screenshot](#screenshot)
- [Our process](#our-process)
  - [Built with](#built-with)
  - [What We learned](#what-we-learned)
  - [Continued development](#continued-development)
  - [Useful resources](#useful-resources)
- [Author](#author)


## Overview

### Description
 In this era, robot is not a strange things for us. Robot helps us many things, such as helping someone to lift something. In this project, we make a prototype robot using ESP32 and we want to control it from far away. The target for this project is for factory so that it will help the workers to transport some part from one place to another. In this project, we only use three place that are represented as place A, place B, place C. For the robot reach place A or B or C, the robot need sensor that can sense the indication whether it is already in place, so we use color sensor to indicate that.
 
### The challenge
  - How to make color sensor as the indicator for the robot
  - How to control it from far away.
 
### Screenshot
![GUI](result/gui.png)

Demo Prototype : [Here](https://drive.google.com/file/d/173ATPo9UnvM3lJuPyt6W0aknh30r3qm-/view?usp=sharing)


## Our process

### Built with
  - ESP32
  - MQTT
  - Python (tkinter)

### What we learned
 From this project, we learn how to control something from far away using MQTT publish and subscribe. 
```
void callback(char* topic, byte* payload, unsigned int length) {
  // do something

  if (String(topic) == "Line_Follower_ESP32"){
   // do something
  }

```

### Continued development
 In the future, we will try to use MQTT for IoT because it is so powerful to make some machine can communicate with other machine

### Useful resources
- [MQTT in ESP32](https://randomnerdtutorials.com/esp32-mqtt-publish-subscribe-arduino-ide/) - This helped us to understand how to configure ESP32 with mqtt
- [MQTT in Python](http://www.steves-internet-guide.com/into-mqtt-python-client/) - This helped us to understand how to configure python with mqtt

### Author
- [Kelvin Cendra](https://github.com/Caprice123)
- [Raymond Winsher](https://github.com/Raywinsher21)
- [Ardhian Mahendar]()
- [Irvine]()
- [Richie Eviendy]()

#include <Arduino.h>
#include <Wire.h>
#include <MotorController.h>

#include <CMPS12.h>
#include <VL53L0X.h>

// Addresses
#define TCAADDR 0x70

#define TILE_SIZE 300

enum{
	TOF_FRONT = 0,
	TOF_FRONT_RIGHT,
	TOF_FRONT_LEFT,
	TOF_BACK_RIGHT,
	TOF_BACK,
	TOF_BACK_LEFT,
	TOF_END
};

VL53L0X tof[TOF_END];
uint16_t tof_distance[TOF_END];

uint8_t motor_pins[4] = { 17, 5, 16, 4 };
uint8_t pwm_pins[4] = { 2, 13, 26, 27 };


MotorController Motors(motor_pins, pwm_pins);

CMPS12 cmps12;

void tcaselect(uint8_t i) {
	if (i > 7) return;

	Wire.beginTransmission(TCAADDR);
	Wire.write(1 << i);
	Wire.endTransmission();  
}

void GetTOF(){
	for(int i = 0; i < TOF_END; i++){
		tcaselect(i);
		tof_distance[i] = tof[i].readRangeContinuousMillimeters();

		Serial.print("Distance [");
		Serial.print(i);
		Serial.print("]: ");
		Serial.print(tof_distance[i]);
		Serial.println("mm");
	}
}

uint32_t GetTile(uint16_t distance){
		uint16_t tile = 0;

		while (distance >= TILE_SIZE){
			++tile;
			distance -= TILE_SIZE;
		}

		return ((distance << 16) + tile);
}

void RotateDeg(float deg){
	deg = fmod(deg, 360.0);

	float FinalAngle = 180.0f;
	float Margin = 0.5f;

	float Offset = deg - cmps12.GetBearing3599();

	while(1){
		float CurrentAngle = cmps12.GetBearing3599() + Offset;

		if (CurrentAngle < 0)
			CurrentAngle += 360.0f;

		CurrentAngle = fmod(CurrentAngle, 360.0);

		uint32_t speed = 50.0 + abs(180.0 - CurrentAngle) / 180.0 * 205.0;// 50-255% Speed

		if (CurrentAngle < FinalAngle - Margin)
			Motors.Right(speed);
		else if (CurrentAngle > FinalAngle + Margin){
			Motors.Left(speed);
		}else{
			Motors.Break();
			break;
		}
	}
}

void MoteTile(int Ammount){
	uint8_t laser;

	GetTOF();

	if (tof_distance[TOF_FRONT] == 0xFFFF){
		laser = TOF_BACK;
	}
	else if (tof_distance[TOF_FRONT] > tof_distance[TOF_BACK]){
		laser = TOF_BACK;
	}
	else
	{
		laser = TOF_FRONT;
	}
	

	uint32_t tiles = GetTile(tof_distance[laser]);

	uint16_t tile = tiles & 0xFFFF;

	int final_tile = tile;

	if (laser == TOF_FRONT){
		final_tile -= Ammount;
	}
	else
	{
		final_tile += Ammount;
	}

	if (final_tile < 0)
		final_tile = 0;

	while(1){
		GetTOF();

		tiles = GetTile(tof_distance[laser]);
		tile = tiles & 0xFFFF;
    	uint32_t distance = tiles >> 16;

		if (laser == TOF_BACK){
			distance = TILE_SIZE - distance;
		}

		if ( (tile == final_tile && distance < 50) || ((tile < final_tile && laser == TOF_FRONT) || (tile > final_tile && laser == TOF_BACK)) ) {
			Motors.Backward(50); 
		}
		else if ( ((tile > final_tile && laser == TOF_FRONT) || (tile < final_tile && laser == TOF_BACK)) ){
			uint32_t base_speed = 255;

			Motors.Forward(base_speed, base_speed);
		}
		else if (tile == final_tile && distance > 65){
			uint32_t base_speed = 50.f + ( (distance - 65.f) / (300.f - 65.f) * (255.f - 50.f));

			Motors.Forward(base_speed, base_speed);
		}else{
			Motors.Break(255);
			break;
		}
	}
}

void setup() {
	Serial.begin(115200);
	Wire.begin(SDA, SCL);

	delay(1000);

	Serial.println("Started");

	for(int i = 0; i < TOF_END; i++){
		tcaselect(i);

		tof[i].init();
		tof[i].setTimeout(25);

		// lower the return signal rate limit (default is 0.25 MCPS)
		tof[i].setSignalRateLimit(0.175);
		// increase laser pulse periods (defaults are 14 and 10 PCLKs)
		tof[i].setVcselPulsePeriod(VL53L0X::VcselPeriodPreRange, 16);
		tof[i].setVcselPulsePeriod(VL53L0X::VcselPeriodFinalRange, 12);

		tof[i].setMeasurementTimingBudget(20000);

		tof[i].startContinuous();
	}

	Serial.println("TOF Started");
}

void loop() {
	MoteTile(1);
	delay(1000);
	RotateDeg(-90);
	Motors.Break();
	delay(1000);
}
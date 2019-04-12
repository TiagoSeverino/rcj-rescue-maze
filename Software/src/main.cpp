#include <Arduino.h>
#include <Wire.h>
#include <MotorController.h>

#include <CMPS12.h>
#include <VL53L0X.h>

// Addresses
#define TCAADDR 0x70

#define TILE_SIZE 300
#define ALIGN_GAP 5

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

void AlignToWall(){

	uint32_t speed = 80;
	bool useLeft = false;
	bool useRight = false;

	GetTOF();

	uint32_t backLeft = GetTile(tof_distance[TOF_BACK_LEFT]);
	uint16_t backLeftTile = backLeft & 0xFFFF;
    uint16_t backLeftDist = backLeft >> 16;

	uint32_t frontLeft = GetTile(tof_distance[TOF_FRONT_LEFT]);
	uint16_t frontLeftTile = frontLeft & 0xFFFF;
    uint16_t frontLeftDist = frontLeft >> 16;

	uint32_t backRight = GetTile(tof_distance[TOF_BACK_RIGHT]);
	uint16_t backRightTile = backRight & 0xFFFF;
    uint16_t backRightDist = backRight >> 16;

	uint32_t frontRight = GetTile(tof_distance[TOF_FRONT_RIGHT]);
	uint16_t frontRightTile = frontRight & 0xFFFF;
    uint16_t frontRightDist = frontRight >> 16;

	if (frontLeftTile == backLeftTile)
		useLeft = true;

	if (frontRightTile == backRightTile)
		useRight = true;

	if (useLeft && useRight)
		if (backLeftTile > backRightTile)
			useLeft = false;
		else if (backLeftTile < backRightTile)
			useRight = false;

	if (useLeft == false && useRight == false)
		useLeft = true;

	int i = 0;

	while(1){

		if (i > 60)
			break;

		++i;

		GetTOF();

		backLeft = GetTile(tof_distance[TOF_BACK_LEFT]);
		backLeftTile = backLeft & 0xFFFF;
		backLeftDist = backLeft >> 16;

		frontLeft = GetTile(tof_distance[TOF_FRONT_LEFT]);
		frontLeftTile = frontLeft & 0xFFFF;
		frontLeftDist = frontLeft >> 16;

		backRight = GetTile(tof_distance[TOF_BACK_RIGHT]);
		backRightTile = backRight & 0xFFFF;
		backRightDist = backRight >> 16;

		frontRight = GetTile(tof_distance[TOF_FRONT_RIGHT]);
		frontRightTile = frontRight & 0xFFFF;
		frontRightDist = frontRight >> 16;

		float gap = ALIGN_GAP;

		if (useLeft){
			gap = ALIGN_GAP * (frontLeftTile * 1.25 + 1);
			if (backLeftDist > frontLeftDist - gap && backLeftDist < frontLeftDist + gap)
				break;
		}

		if (useRight){
			gap = ALIGN_GAP * (frontRightTile * 1.25 + 1);
			if (backRightDist > frontRightDist - gap && backRightDist < frontRightDist + gap)
				break;
		}

		if (useLeft == useRight)
			if (backLeftDist > frontLeftDist + gap && backRightDist < frontRightDist - gap)
				Motors.Right(speed);
			else if (backLeftDist < frontLeftDist - gap && backRightDist > frontRightDist + gap)
				Motors.Left(speed);
			else if (backLeftDist > frontLeftDist + gap && backRightDist > frontRightDist + gap)
				Motors.Forward(speed);
			else
				Motors.Backward(speed);
		else if (useLeft)
			if (backLeftDist > frontLeftDist + gap)
				Motors.Right(speed);
			else // backLeftDist < frontLeftDist - gap:
				Motors.Right(speed);
		else
			if (backRightDist < frontRightDist - gap)
				Motors.Right(speed);
			else // backRightDist > frontRightDist + gap:
				Motors.Left(speed);
	}
	Motors.Break();
	delay(100);
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

void MoteTile(int Ammount = 1){
	uint8_t laser;

	GetTOF();

	if (tof_distance[TOF_FRONT] == 0xFFFF)
	{
		laser = TOF_BACK;
	}
	else if (tof_distance[TOF_FRONT] > tof_distance[TOF_BACK])
	{
		laser = TOF_BACK;
	}
	else
	{
		laser = TOF_FRONT;
	}

	uint32_t tiles = GetTile(tof_distance[laser]);

	uint16_t tile = tiles & 0xFFFF;

	int final_tile = tile;

	if (laser == TOF_FRONT)
	{
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
    	uint16_t distance = tiles >> 16;


		Serial.print("Distance: ");
		Serial.println(distance);
		
		Serial.print("Tiles: ");
		Serial.println(tile);

		if ( (tile <= final_tile && distance < 45 && laser == TOF_FRONT) || (tile >= final_tile && distance > 55 && laser == TOF_BACK) ) {
			Motors.Backward(50);

			Serial.print("Backward");			
		}
		else if ( ((tile > final_tile && laser == TOF_FRONT) || (tile < final_tile && laser == TOF_BACK)) ){
			uint32_t base_speed = 255;

			Serial.println("Forward");

			Motors.Forward(base_speed, base_speed);
		}
		else if (tile == final_tile && ((distance > 55 && laser == TOF_FRONT) || (distance < 45 && laser == TOF_BACK)) ){
			uint32_t base_speed;

			if (laser == TOF_FRONT)
			{
				base_speed = 50.f + ( (distance - 55.f) / (300.f - 55.f) * (255.f - 50.f));
			}
			else
			{
				base_speed = 50.f + ( (45.f - distance) / 300.f * (255.f - 50.f));
			}

			Serial.print("Forward ");
			Serial.print("Base_Speed: ");
			Serial.println(base_speed);

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
	AlignToWall();
	//RotateDeg(-90
	//Motors.Break();
	//delay(1000);
}
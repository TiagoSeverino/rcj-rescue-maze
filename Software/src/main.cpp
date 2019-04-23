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

enum{
	DIRECTION_UP = 0,
	DIRECTION_RIGHT,
	DIRECTION_BOTTOM,
	DIRECTION_LEFT
};

VL53L0X tof[TOF_END];
uint16_t tof_distance[TOF_END];

uint8_t motor_pins[4] = { 17, 5, 16, 4 };
uint8_t pwm_pins[4] = { 2, 13, 26, 27 };

float Bear3599OffSet;

uint8_t DIRECTION = DIRECTION_UP;

MotorController Motors(motor_pins, pwm_pins);

CMPS12 compass;

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

		/*
		Serial.print("Distance [");
		Serial.print(i);
		Serial.print("]:");
		Serial.println(tof_distance[i]);
		*/
	}
}

float GetBearing(){
	float bear = compass.GetBearing3599();

	bear -= Bear3599OffSet;

	if (bear > 360.f)
		bear -= 360.f;
	else if (bear < 0.f)
		bear += 360.f;

	return bear;
}

uint32_t GetTile(uint16_t distance){
		uint16_t tile = 0;

		while (distance >= TILE_SIZE){
			++tile;
			distance -= TILE_SIZE;
		}

		return ((distance << 16) + tile);
}

void AlignToWall1(){

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

		if (i > 30)
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
			gap = ALIGN_GAP * (frontLeftTile * 1.1f + 1);
			if (backLeftDist > frontLeftDist - gap && backLeftDist < frontLeftDist + gap)
				break;
		}

		if (useRight){
			gap = ALIGN_GAP * (frontRightTile * 1.1f + 1);
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

// NOT TESTED
void AlignToWall(){
		uint32_t base_speed = 80;
		bool useLeft = false;
		bool useRight = false;

		uint16_t gap = 2;

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

		
		int i = 0;

		while(1){

			if (i > 30)
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

			if (useLeft)
				if (backLeftDist > frontLeftDist - gap && backLeftDist < frontLeftDist + gap)
					break;
			
			if (useRight)
				if (backRightDist > frontRightDist - gap && backRightDist < frontRightDist + gap)
					break;

			if (useLeft == useRight)
				if (backLeftDist > frontLeftDist + gap && backRightDist < frontRightDist - gap)
					Motors.Right(base_speed);
				else if (backLeftDist < frontLeftDist - gap && backRightDist > frontRightDist + gap)
					Motors.Left(base_speed);
				else if (backLeftDist > frontLeftDist + gap && backRightDist > frontRightDist + gap)
					Motors.Forward(base_speed);
				else
					Motors.Backward(base_speed);
			else if (useLeft)
				if (backLeftDist > frontLeftDist + gap)
					Motors.Right(base_speed);
				else //if backLeftDist < frontLeftDist - gap:
					Motors.Left(base_speed);
			else
				if (backRightDist < frontRightDist - gap)
					Motors.Right(base_speed);
				else //if backRightDist > frontRightDist + gap:
					Motors.Left(base_speed);
		}

		Motors.Break(base_speed);
		delay(100);
}

void RotateDeg(float deg, bool _Offset = true){
	deg = fmod(deg, 360.0);

	float FinalAngle = 180.0f;
	float Margin = 0.5f;

	float Offset = deg - GetBearing();

	if (_Offset == false){
		Offset = 0;
	}

	while(1){
		float CurrentAngle = GetBearing() + Offset;

		delay(5);

		if (CurrentAngle < 0)
			CurrentAngle += 360.0f;

		CurrentAngle = fmod(CurrentAngle, 360.0);

		uint32_t speed = 100.0f + (abs(180.0f - CurrentAngle) / 180.0f * 150.0f);// 100-255 Speed

		if (CurrentAngle < FinalAngle - Margin)
			Motors.Right(speed);
		else if (CurrentAngle > FinalAngle + Margin){
			Motors.Left(speed);
		}else{
			Motors.Break();
			break;
		}
	}
	delay(100);
}

void MoteTile(int Ammount = 1){
	uint8_t laser;

	GetTOF();

	laser = TOF_FRONT;

	uint32_t tiles = GetTile(tof_distance[laser]);
	uint16_t tile = tiles & 0xFFFF;
	uint16_t distance = tiles >> 16;

	if (distance >= (TILE_SIZE - (TILE_SIZE / 4.f))){
			tile += 1;
			distance = 0;
	}

	int final_tile = tile;

	final_tile -= Ammount;

	if (final_tile < 0)
		final_tile = 0;

	int i = 0;

	int gap = 4;


	float deg = DIRECTION * 90;
	float FinalAngle = 180.0f;
	float Margin = .5f;
	float Offset = deg - GetBearing();

	while(1){
		GetTOF();

		tiles = GetTile(tof_distance[laser]);
		tile = tiles & 0xFFFF;
    	distance = tiles >> 16;


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



		float CurrentAngle = GetBearing() + Offset;

		if (CurrentAngle < 0)
			CurrentAngle += 360.0f;

		CurrentAngle = fmod(CurrentAngle, 360.0);


		if ( tile <= final_tile && distance < 60 ) {
			Motors.Backward(50);

			//Serial.print("Backward");			
		}
		else if ( tile > final_tile ){
			uint32_t base_speed_left = 200;
			uint32_t base_speed_right = 200;

			if (frontLeftDist > frontRightDist + gap)
				base_speed_left -= 25;
			else if (frontLeftDist < frontRightDist - gap)
				base_speed_right -= 25;

			if (CurrentAngle < FinalAngle - Margin)
				base_speed_right -= 25;
			else if (CurrentAngle > FinalAngle + Margin)
				base_speed_left -= 25;

			Motors.Forward(base_speed_left, base_speed_right);
			
			//Serial.println("Forward");
		}
		else if ( tile == final_tile && distance > 65 ){
			uint32_t base_speed = 50.f + ( (distance - 65.f) / (300.f - 65.f) * (255.f - 100.f));
			uint32_t base_speed_left = base_speed;
			uint32_t base_speed_right = base_speed;

			if (frontLeftDist > frontRightDist + gap)
				base_speed_left *= 0.8f;
			else if (frontLeftDist < frontRightDist - gap)
				base_speed_right *= 0.8f;

			if (CurrentAngle < FinalAngle - Margin)
				base_speed_right *= 0.8f;
			else if (CurrentAngle > FinalAngle + Margin)
				base_speed_left *= 0.8f;

			Motors.Forward(base_speed_left, base_speed_right);

			/*
			Serial.print("Forward ");
			Serial.print("Base_Speed: ");
			Serial.println(base_speed);
			*/
		}else{
			Motors.Break(255);
			break;
		}
	}

	delay(100);

	AlignToWall();
}

void UpdateCompassOffset(){
	Bear3599OffSet = compass.GetBearing3599() + (DIRECTION * 90.f);
}

void RotateLeft(){
	RotateDeg(-90);
	AlignToWall();

	if (DIRECTION > DIRECTION_UP)
		--DIRECTION;
	else
		DIRECTION = DIRECTION_LEFT;

	UpdateCompassOffset();
}

void RotateRight(){
	RotateDeg(90);
	AlignToWall();

	if (DIRECTION < DIRECTION_LEFT)
		++DIRECTION;
	else
		DIRECTION = DIRECTION_UP;

	UpdateCompassOffset();
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
		tof[i].setSignalRateLimit(0.1);
		// increase laser pulse periods (defaults are 14 and 10 PCLKs)
		tof[i].setVcselPulsePeriod(VL53L0X::VcselPeriodPreRange, 18);
		tof[i].setVcselPulsePeriod(VL53L0X::VcselPeriodFinalRange, 14);

		tof[i].setMeasurementTimingBudget(20000);

		tof[i].startContinuous();
	}

	Serial.println("TOF Started");

	UpdateCompassOffset();
}

void loop() {

	MoteTile(1);
	AlignToWall();
	UpdateCompassOffset();
	
	if (tof_distance[TOF_FRONT] < 200){
		RotateLeft();
	}

	delay(1000);
	//Motors.Break();
	//delay(1000);
}
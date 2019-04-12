#include <CMPS12.h>
#include <Wire.h>

#define CMPS12_DEFAULT_ADDRESS 0x60

CMPS12::CMPS12(void)
	: address(CMPS12_DEFAULT_ADDRESS)
{
	
}
uint8_t CMPS12::readReg(uint8_t reg){
	uint8_t value;

	Wire.beginTransmission(address);
	Wire.write(reg);
	Wire.endTransmission();

	Wire.requestFrom(address, (uint8_t) 1);
	value = Wire.read();

	return value;
}

uint32_t CMPS12::readReg32Bit(uint8_t reg)
{
	uint32_t value;

	Wire.beginTransmission(address);
	Wire.write(reg);
	Wire.endTransmission();

	Wire.requestFrom(address, (uint8_t) 4);
	value  = (uint32_t)Wire.read() << 24; // value highest byte
	value |= (uint32_t)Wire.read() << 16;
	value |= (uint16_t)Wire.read() <<  8;
	value |=           Wire.read();       // value lowest byte

	return value;
}

uint8_t CMPS12::GetBearing255(){
	return readReg(BEARING_255);
}

float CMPS12::GetBearing3599(){
	return ((readReg(BEARING_3599_H) << 8) + readReg(BEARING_3599_L)) / 10.;
}

uint8_t CMPS12::GetPitch(){
	return readReg(PITCH);
}

uint8_t CMPS12::GetRoll(){
	return readReg(ROLL);
}

uint32_t CMPS12::Get3Axis(){
	return readReg32Bit(BEARING_3599_H);
}
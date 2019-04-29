#include <TPA81.h>
#include <Wire.h>

#define TPA81_DEFAULT_ADDRESS 0x68

TPA81::TPA81(void)
	: address(TPA81_DEFAULT_ADDRESS)
{
	
}
uint8_t TPA81::readReg(uint8_t reg){
	uint8_t value;

	Wire.beginTransmission(address);
	Wire.write(reg);
	Wire.endTransmission();

	Wire.requestFrom(address, (uint8_t) 1);
	value = Wire.read();

	return value;
}

uint8_t TPA81::PixelTemp(uint8_t pixel){
	return readReg(TPA81_PIXEL + pixel);
}

uint8_t TPA81::AmbientTemperature(){
	return readReg(TPA81_AMBTEMP);
}

uint8_t TPA81::HighestTemp(){
	uint8_t highest = 0;

	for (int i = 0; i < 8; ++i){
		uint8_t temp = readReg(TPA81_PIXEL + i);

		if (temp > highest)
			highest = temp;
	}

	return highest;
}
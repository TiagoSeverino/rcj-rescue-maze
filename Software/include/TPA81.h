#ifndef _TPA81_H_
#define _TPA81_H_

#include <Arduino.h>

class TPA81
{
	public:
		enum regAddr
    	{
			TPA81_SOFTVER = 0,
			TPA81_REGADDR = 0, // Same as TPA81_SOFTVER
			TPA81_AMBTEMP = 1, //
			TPA81_PIXEL = 2 //Register for pixels fr	
		};

		TPA81(void);

		uint8_t AmbientTemperature();
		uint8_t PixelTemp(uint8_t pixel);
		uint8_t HighestTemp();

		uint8_t readReg(uint8_t reg);

	private:
		uint8_t address;
};

#endif
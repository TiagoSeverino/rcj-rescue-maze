#ifndef _CMPS12_H_
#define _CMPS12_H_

#include <Arduino.h>

class CMPS12
{
	public:
		enum regAddr
    	{
			COMMAND_REGISTER = 0x00, // Command register (write)
			SOFTWARE_VERSION = 0x00, // Software version (read)
			BEARING_255 = 0x01, // Compass Bearing 8 bit, i.e. 0-255 for a full circle
			BEARING_3599_H = 0x02,
			BEARING_3599_L = 0x03, // Compass Bearing 16 bit, i.e. 0-3599, representing 0-359.9 degrees. register 2 being the high byte. This is calculated by the processor from quaternion outputs of the BNO055
			PITCH = 0x04, // Pitch angle - signed byte giving angle in degrees from the horizontal plane (+/- 90°)
			ROLL = 0x05, // Roll angle - signed byte giving angle in degrees from the horizontal plane (+/- 90°)
			RAW_MAGNETOMETER_X_H = 0x06,
			RAW_MAGNETOMETER_X_L = 0x07, // Magnetometer X axis raw output, 16 bit signed integer (register 0x06 high byte)
			RAW_MAGNETOMETER_Y_H = 0x08,
			RAW_MAGNETOMETER_Y_L = 0x09, // Magnetometer Y axis raw output, 16 bit signed integer (register 0x08 high byte)
			RAW_MAGNETOMETER_Z_H = 0x0A,
			RAW_MAGNETOMETER_Z_L = 0x0B, // Magnetometer Z axis raw output, 16 bit signed integer (register 0x0A high byte)
			RAW_ACCELEROMETER_X_H = 0x0C,
			RAW_ACCELEROMETER_X_L = 0x0D, // Accelerometer X axis raw output, 16 bit signed integer (register 0x0C high byte)
			RAW_ACCELEROMETER_Y_H = 0x0E,
			RAW_ACCELEROMETER_Y_L = 0x0F, // Accelerometer Y axis raw output, 16 bit signed integer (register 0x0E high byte)
			RAW_ACCELEROMETER_Z_H = 0x10,
			RAW_ACCELEROMETER_Z_L = 0x11, // Accelerometer Z axis raw output, 16 bit signed integer (register 0x10 high byte)
			RAW_GYRO_X_H = 0x12,
			RAW_GYRO_X_L = 0x13, // Gyro X axis raw output, 16 bit signed integer (register 0x12 high byte)
			RAW_GYRO_Y_H = 0x14,
			RAW_GYRO_Y_L = 0x15, // Gyro Y axis raw output, 16 bit signed integer (register 0x14 high byte)
			RAW_GYRO_Z_H = 0x16,
			RAW_GYRO_Z_L = 0x17, // Gyro Z axis raw output, 16 bit signed integer (register 0x16 high byte)
			TEMPERATURE_H = 0x18,
			TEMPERATURE_L = 0x19, // Temperature of the BNO055 in degrees centigrade (register 0x18 high byte)
			BNO055_BEARING_H = 0x1A,
			BNO055_BEARING_L = 0x1B, // Compass Bearing 16 bit This is the angle Bosch generate in the BNO055 (0-5759), divide by 16 for degrees
			BNO055_PITCH_H = 0x1C,
			BNO055_PITCH_L = 0x1D, // Pitch angle 16 bit - signed byte giving angle in degrees from the horizontal plane (+/- 180°)
			CALIBRATION_STATE = 0x1E // Calibration state, bits 0 and 1 reflect the calibration status (0 un-calibrated, 3 fully calibrated)
		};

		CMPS12(void);

		uint8_t GetBearing255();
		float GetBearing3599();
		uint8_t GetPitch();
		uint8_t GetRoll();
		uint32_t Get3Axis();

		uint8_t readReg(uint8_t reg);
		uint32_t readReg32Bit(uint8_t red);

	private:
		uint8_t address;
};

#endif
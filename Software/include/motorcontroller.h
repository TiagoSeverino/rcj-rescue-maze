#ifndef _MotorController_H_
#define _MotorController_H_

#include <Arduino.h>

class MotorController
{
	private:
		uint8_t motor_pins[4];
		uint8_t pwm_pins[4];
		uint32_t pwm_values[4];

		void SetPwmValues(uint32_t pwm_values[4]);

	public:
		MotorController(uint8_t motor_pins[4], uint8_t pwm_pins[4]);

		void Forward();
		void Forward(uint32_t PWM);
		void Forward(uint32_t PWM_L, uint32_t PWM_R);
		void Forward(uint32_t pwm_values[4]);

		void Backward();
		void Backward(uint32_t PWM);
		void Backward(uint32_t PWM_L, uint32_t PWM_R);
		void Backward(uint32_t pwm_values[4]);

		void Left();
		void Left(uint32_t PWM);
		void Left(uint32_t PWM_L, uint32_t PWM_R);
		void Left(uint32_t pwm_values[4]);

		void Right();
		void Right(uint32_t PWM);
		void Right(uint32_t PWM_L, uint32_t PWM_R);
		void Right(uint32_t pwm_values[4]);

		void Break();
		void Break(uint32_t PWM);
		void Break(uint32_t PWM_L, uint32_t PWM_R);
		void Break(uint32_t pwm_values[4]);

		void Stop();
};

#endif
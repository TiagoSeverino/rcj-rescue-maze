#include <motorcontroller.h>

MotorController::MotorController(uint8_t motor_pins[4], uint8_t pwm_pins[4])
{
	// Setting PWM properties
	const int freq = 30000;
	const int resolution = 8;

	for(size_t i = 0; i < 4; i++)
	{
		this->motor_pins[i] = motor_pins[i];
		this->pwm_pins[i] = pwm_pins[i];

		pinMode(this->motor_pins[i], OUTPUT);
		pinMode(this->pwm_pins[i], OUTPUT);

		digitalWrite(this->motor_pins[i], LOW);
		digitalWrite(this->pwm_pins[i], LOW);

		ledcSetup(i + 2, freq, resolution);
		ledcAttachPin(this->pwm_pins[i], i + 2);
	}

	SetPwmValues(new uint32_t[4]  { 255, 255, 255, 255 } );
	
}

void MotorController::SetPwmValues(uint32_t pwm_values[4]){
	for(size_t i = 0; i < 4; i++)
		this->pwm_values[i] = pwm_values[i];
}

void MotorController::Forward()
{
	for(size_t i = 0; i < 4; i++)
	{
		digitalWrite(this->motor_pins[i], i % 2);
		ledcWrite(i + 2, this->pwm_values[i]);
	}
}

void MotorController::Forward(uint32_t PWM)
{
	this->SetPwmValues(new uint32_t[4] { PWM, PWM, PWM, PWM });
	this->Forward();
}

void MotorController::Forward(uint32_t PWM_L, uint32_t PWM_R)
{
	this->SetPwmValues(new uint32_t[4] { PWM_L, PWM_L, PWM_R, PWM_R });
	this->Forward();
}

void MotorController::Forward(uint32_t pwm_values[4])
{
	this->SetPwmValues(pwm_values);
	this->Forward();
}

void MotorController::Backward()
{
	for(size_t i = 0; i < 4; i++)
	{
		digitalWrite(this->motor_pins[i], !(i % 2));
		ledcWrite(i + 2, this->pwm_values[i]);
	}
}

void MotorController::Backward(uint32_t PWM)
{
	this->SetPwmValues(new uint32_t[4] { PWM, PWM, PWM, PWM });
	this->Backward();
}

void MotorController::Backward(uint32_t PWM_L, uint32_t PWM_R)
{
	this->SetPwmValues(new uint32_t[4] { PWM_L, PWM_L, PWM_R, PWM_R });
	this->Backward();
}

void MotorController::Backward(uint32_t pwm_values[4])
{
	this->SetPwmValues(pwm_values);
	this->Backward();
}

void MotorController::Left()
{
	for(size_t i = 0; i < 4; i++)
	{
		digitalWrite(this->motor_pins[i], (i < 2) ? !(i % 2) : (i % 2));
		ledcWrite(i + 2, this->pwm_values[i]);
	}
}

void MotorController::Left(uint32_t PWM)
{
	this->SetPwmValues(new uint32_t[4] { PWM, PWM, PWM, PWM });
	this->Left();
}

void MotorController::Left(uint32_t PWM_L, uint32_t PWM_R)
{
	this->SetPwmValues(new uint32_t[4] { PWM_L, PWM_L, PWM_R, PWM_R });
	this->Left();
}

void MotorController::Left(uint32_t pwm_values[4])
{
	this->SetPwmValues(pwm_values);
	this->Left();
}

void MotorController::Right()
{
	for(size_t i = 0; i < 4; i++)
	{
		digitalWrite(this->motor_pins[i], (i < 2) ? (i % 2) : !(i % 2));
		ledcWrite(i + 2, this->pwm_values[i]);
	}
}

void MotorController::Right(uint32_t PWM)
{
	this->SetPwmValues(new uint32_t[4] { PWM, PWM, PWM, PWM });
	this->Right();
}

void MotorController::Right(uint32_t PWM_L, uint32_t PWM_R)
{
	this->SetPwmValues(new uint32_t[4] { PWM_L, PWM_L, PWM_R, PWM_R });
	this->Right();
}

void MotorController::Right(uint32_t pwm_values[4])
{
	this->SetPwmValues(pwm_values);
	this->Right();
}

void MotorController::Break()
{
	for(size_t i = 0; i < 4; i++)
	{
		digitalWrite(this->motor_pins[i], HIGH);
		ledcWrite(i + 2, this->pwm_values[i]);
	}
}

void MotorController::Break(uint32_t PWM)
{
	this->SetPwmValues(new uint32_t[4] { PWM, PWM, PWM, PWM });
	this->Break();
}

void MotorController::Break(uint32_t PWM_L, uint32_t PWM_R)
{
	this->SetPwmValues(new uint32_t[4] { PWM_L, PWM_L, PWM_R, PWM_R });
	this->Break();
}

void MotorController::Break(uint32_t pwm_values[4])
{
	this->SetPwmValues(pwm_values);
	this->Break();
}

void MotorController::Stop()
{
	for(size_t i = 0; i < 4; i++)
	{
		digitalWrite(this->motor_pins[i], LOW);
		ledcWrite(i + 2, this->pwm_values[i]);
	}
}
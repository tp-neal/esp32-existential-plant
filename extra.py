# def play_tone(dac, freq, duration_ms, amplitude):
#     """Plays a square wave tone at a given frequency and duration."""
#     print(f"Playing {freq}Hz for {duration_ms}ms")

#     # Calculate the delay for one "half" of the wave in microseconds
#     # 1 second = 1,000,000 microseconds
#     # 1 cycle = 1,000,000 / freq
#     # 1/2 cycle (high or low) = (1,000,000 / freq) / 2
#     half_period_us = int(500000 / freq)

#     # Calculate how long to run the loop
#     end_time = utime.ticks_add(utime.ticks_ms(), duration_ms)

#     half_freq = 128
#     high_freq = min(255, half_freq + amplitude)
#     low_freq = max(0, half_freq - amplitude)
                    
#     # Run the loop until the duration is over
#     while utime.ticks_diff(end_time, utime.ticks_ms()) > 0:
#         dac.write(high_freq) # Wave goes HIGH
#         utime.sleep_us(half_period_us)
        
#         dac.write(low_freq)   # Wave goes LOW
#         utime.sleep_us(half_period_us)
        
        


# def moisture_sensor_init() -> None:
#     adc = ADC(Pin(32))
    
#     adc.atten(ADC.ATTN_11DB)
    
#     adc.width(ADC.WIDTH_12BIT)
    
#     while True:
#         raw_value = adc.read()
        
#         voltage = (raw_value / 4095) * 3.3
        
#         print(raw_value)
        
#         utime.sleep(0.5)
# wika-temperature-probe
Python class for reading temperature from Wika CTH7000 temperature probe.

![cth7000_en_co (1)](https://github.com/pao3007/wika-temperature-probe/assets/35431691/c097def2-9743-420a-a5d0-2ff043370c17)

Init class with COM port on which Wika temperature probe is connected:
```python
temp_probe = WikaTempProbe('COM3')
```

Connect to the device:
```python
temp_probe.connect()
```

Read measured temperature from device, selecting channel:
```python
res = temp_probe.measure_channel('B')
temp = None
if res == -1:
    print("ERROR")
elif res == -2:
    print("Wrong Channel Selected")
else:
    temp = float(res)
print(temp)
```

End communication with device:
```python
temp_probe.disconnect()
```

Other functions:

Set device to remote or local control, disabling keypad:
```python
temp_probe.set_system_remote(True)
```
Set unit of device to Celsius:
```python
temp_probe.set_unit_celsius()
```
Ask for identification of device:
```python
temp_probe.ident()
```

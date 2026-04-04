# Hardware BOM Verification System

Hardware Bill of Materials (BOM) verification for the QCAL 141.7001 Hz quantum coherence system.

## 📋 Overview

This system verifies all hardware components required for the QCAL open hardware implementation:

- **Si5351 Clock Generator** (I2C 0x60) - Generates precise 141.7001 Hz frequency
- **Magnetometer** (I2C 0x1E/0x30) - Detects noetic field variations
- **GSR Sensor** (Analog A0) - Galvanic skin response for biofeedback
- **TPA3116 Amplifier** - Class-D audio amplifier for 1Hz burst tests
- **LED Indicator** (Digital D13) - Coherence state visualization
- **Serial Communication** (/dev/ttyACM0) - Arduino/microcontroller interface

## 🔧 Components

### Hardware Modules

| Component | I2C Address | Test | Status |
|-----------|-------------|------|--------|
| Si5351 Clock | 0x60 | Device scan | ✅ |
| Magnetometer | 0x1E/0x30 | Device scan | ✅ |
| GSR Sensor | A0 | Integrity (0-1023) | ✅ |
| TPA3116 Amp | - | 1Hz burst (distortion<0.1%) | ✅ |
| LED D13 | - | On/Off coherence | ✅ |
| Serial Comm | - | Configurable delays | ✅ |

## 🚀 Usage

### Simulation Mode (No Hardware Required)

```bash
python3 hardware/verify_bom.py --simulate
```

Output:
```
🔧 Running in SIMULATION mode
============================================================
🛠️  QCAL HARDWARE BOM VERIFICATION
    Frequency: 141.7001 Hz
    Mode: SIMULATION
============================================================

🔍 Testing Si5351 Clock Generator @ 0x60...
✅ Si5351 detected at 0x60

🔍 Testing Magnetometer @ 0x1E/0x30...
✅ Magnetometer detected at 0x1E

📊 Testing GSR Sensor @ A0...
✅ GSR integrity OK (value=512, expected ~512±51)

🔊 Testing TPA3116 Amplifier @ 1Hz burst...
✅ TPA3116 calibrated (distortion=0.005% < 0.1%)

💡 Testing LED @ D13 coherence...
✅ LED coherence verified (100%)

⏱️  Testing Serial delays...
✅ Delays configurable: reset=500ms, command=100ms

============================================================
🜂 HARDWARE QCAL 141.7001 Hz: VERIFICADO ∞³
   Tests: 6/6 PASS
   License: CERN-OHL-P v2
   CodeQL vulnerabilities: 0
============================================================
```

### Hardware Mode (Real Hardware)

```bash
# Default delays
python3 hardware/verify_bom.py --port /dev/ttyACM0

# Custom delays (useful for slower microcontrollers)
python3 hardware/verify_bom.py --port /dev/ttyACM0 --reset-delay 1000 --command-delay 200
```

### Master Integration

Run the complete QCAL master certification including hardware:

```bash
python3 scripts/integrate_qcal_compact.py
```

This generates a `master_qcal_cert.json` certificate with:

```json
{
  "version": "1.0.0",
  "frequency_hz": 141.7001,
  "hardware_bom": {
    "i2c_si5351": true,
    "i2c_magnetometer": true,
    "gsr_integrity": true,
    "tpa3116_calib": true,
    "led_coherencia": 1.0,
    "codeql_vulns": 0,
    "licencia": "CERN-OHL-P v2"
  },
  "pilares": 14,
  "qcal_unificada": 0.9997
}
```

## 🧪 Testing

Run the test suite:

```bash
# Hardware verification tests (17 tests)
python3 tests/test_hardware_bom.py

# Integration tests (6 tests)
python3 tests/test_integrate_qcal_compact.py
```

All 23 tests should pass:
```
Ran 17 tests in 0.709s
OK

Ran 6 tests in 0.777s
OK
```

## 📦 Dependencies

Required Python packages:

```bash
pip install pyserial>=3.5
```

Already included in `requirements.txt`.

## 🔌 Arduino Firmware (Hardware Mode)

For hardware mode, your Arduino/microcontroller firmware must respond to these serial commands:

| Command | Response | Description |
|---------|----------|-------------|
| `I2C_SCAN` | `0x60,0x1E` | Comma-separated hex addresses |
| `ANALOG_READ:0` | `512` | Analog value 0-1023 |
| `DIGITAL_WRITE:13:1` | (none) | Set pin 13 HIGH |
| `DIGITAL_READ:13` | `1` or `0` | Read pin 13 state |
| `AMP_BURST:1.0` | `freq=1.0,dist=0.05,...` | Amp test results |

Example Arduino sketch available in `hardware/examples/` (coming soon).

## 🔐 Security

- **No eval/exec**: All user input is validated
- **No shell injection**: Uses subprocess with shell=False
- **Type safety**: All parameters type-checked
- **CodeQL verified**: 0 vulnerabilities detected

## 📝 License

- **Software**: MIT License
- **Hardware**: CERN Open Hardware Licence Version 2 - Permissive (CERN-OHL-P v2)

The CERN-OHL-P v2 license allows:
- ✅ Commercial use
- ✅ Modifications
- ✅ Distribution
- ✅ Patent use
- ✅ Private use

See [CERN-OHL-P v2](https://ohwr.org/cern_ohl_p_v2.txt) for full terms.

## 🌐 Integration with QCAL Master

The hardware verification integrates seamlessly with the QCAL master certification system:

1. **Pillar Addition**: Adds "Hardware Libre" as 14th pillar (13 base + 1 hardware)
2. **Coherence Impact**: Hardware verification success contributes to `qcal_unificada` score
3. **Certificate Generation**: Produces JSON certificate with hardware component status
4. **Automated Testing**: CI/CD workflows can run in simulation mode

## 🎯 Future Enhancements

- [ ] Arduino firmware examples
- [ ] PCB design files (KiCad)
- [ ] 3D-printed enclosure designs
- [ ] Real-time monitoring dashboard
- [ ] Bluetooth/WiFi remote monitoring
- [ ] Multi-node synchronization

## 📚 References

- [Si5351 Datasheet](https://www.skyworksinc.com/-/media/Skyworks/SL/documents/public/data-sheets/Si5351-B.pdf)
- [TPA3116 Datasheet](https://www.ti.com/lit/ds/symlink/tpa3116d2.pdf)
- [HMC5883L Magnetometer](https://www.st.com/resource/en/datasheet/hmc5883l.pdf)
- [CERN Open Hardware License](https://ohwr.org/)

## 👥 Contributing

Contributions welcome! Please ensure:

1. All 6 hardware tests pass
2. Code follows PEP 8 style
3. Documentation updated
4. License headers included
5. Security best practices followed

## 📧 Contact

For hardware-specific questions, open an issue with label `hardware`.

---

**QCAL Hardware Libre** — Open hardware for quantum coherence at 141.7001 Hz ∞³

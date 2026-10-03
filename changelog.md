# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses calendar-based versioning in the form `YEAR.MONTH.RELEASE`
(e.g. `2026.9.1` is the first release in September 2026).


## [Unreleased]

### Added

- `SerialMixin` for devices with serial I/O (`read()`, `readline()`, `write()`, `any()`).


## [2026.9.1] - 2026-09-27

First release.

### Added

- State machine implemented with the _State_ design pattern: `Context` and the
  `Init`, `Configuration`, `FactoryReset`, `ServiceTerminal`, `ConnectNetwork`,
  `Measurement`, `Publish`, `Sleep`, `OTA`, `Advertisement` (BLE, work in
  progress) and `Error` states.
- Short and long press of the control button at startup to enter
  configuration or factory reset; service button to enter the service terminal.
- `DeviceManager` for registering devices and looking them up by type or by
  one or more aliases; `BaseDevice` as a common ancestor of all devices.
- Device mixins for sensors, actuators, buttons, network adapters and power
  management.
- Device drivers: `WS2812B` diagnostic LED, `DHT11` temperature and humidity
  sensor, `CYW43439` WiFi adapter, `DS3231` real-time clock (skeleton),
  buttons and power monitor.
- Service terminal over UART with the whole REPL redirected using
  `os.dupterm()`.
- Command parser using the _Registry_ design pattern and commands using the
  _Command_ design pattern.
- Service terminal commands `blink`, `commands`, `devices`, `help`, `i2c`,
  `measurements`, `net`, `power`, `reset`, `rtc`, `settings`, `sysinfo`,
  `uptime` and `version`.
- User settings stored in `/data/settings.json` with encrypted passwords,
  including WiFi, MQTT and NTP server configuration.
- MQTT client with last will; measurements stored in a file.
- `BaseModel` for declarative data models with field validation.


[Unreleased]: https://github.com/bletvaska/mastering-iot-the-things/compare/2026.9.1...HEAD
[2026.9.1]: https://github.com/bletvaska/mastering-iot-the-things/releases/tag/2026.9.1

## About
Python code for HC-SR501 PIR Motion Detector

## Items
* HC SR501 PIR board
* RaspberryPi
* 3 x Dupont jumpers F-F

## Wiring Diagram
[https://www.sensoranalytics.com.au/image/shared/WiringDiag.png](https://www.sensoranalytics.com.au/image/shared/WiringDiag.png)

## Install
* Copy `ctrl-pir`, `driver-pir.py`, and `pir.py` files to `~/src/pir`

## Run
`cd ~/src/pir` <br>
```./ctrl-pir start```

## View Alerts
`screen -r pir`

## Issues
Install `screen`. Install missing python packages used by `pir.py`.

## Good Ideas
Adding `ctrl-pir start` to start on boot to crontab. For extra cautious, `ctrl-pir restart` once a day at some off peak hour.

## Phone Alerts and Notifications
Register with [pushover.net](https://pushover.net). Then add your app and user tokens in `pir.py` and set `Mute = 1`. Now phone will sound and display notifications.
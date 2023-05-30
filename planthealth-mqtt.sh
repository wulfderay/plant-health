#!/bin/bash
### BEGIN INIT INFO
# Provides:          plant_health
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Plant Health
# Description:       Publishes the health of my plant over mqtt
### END INIT INFO

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting plant_health"
    python3 /usr/local/bin/planthealth-mqtt.py &
    ;;
  stop)
    echo "Stopping plant_health"
    pkill -f /usr/local/bin/planthealth-mqtt.py
    ;;
  restart)
    echo "Restarting plant_health"
    pkill -f /usr/local/bin/planthealth-mqtt.py
    python3 /usr/local/bin/planthealth-mqtt.py &
    ;;
  *)
    echo "Usage: /etc/init.d/plant_health {start|stop|restart}"
    exit 1
    ;;
esac

exit 0

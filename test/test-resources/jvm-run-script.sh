#!/bin/bash
# run script for service

. /lib/lsb/init-functions

SERVICE_NAME="$service_name"
JVM_JAVA_HOME=$java_home
JVM_MAX_MEMORY=$jvm_max_memory
JVM_MAIN_CLASS="$java_main_class"
JVM_SERVICE_JAR="$jvm_service_jar"


JAVA_BIN=$JVM_JAVA_HOME/bin/java

JVM_OPTS="-Xms128m -Xmx$JVM_MAX_MEMORY -XX:+UseConcMarkSweepGC -server"

LOG_PATH="log"
LOG_FILE="$LOG_PATH/$SERVICE_NAME.log"

PID_PATH="pid"
PID_FILE="$PID_PATH/$SERVICE_NAME.pid"

TIME_NOW=`date`

start() {
    echo "starting $SERVICE_NAME ..."
    if [ ! -d $PID_PATH ]; then
        mkdir $PID_PATH
    fi
    if [ ! -d $LOG_PATH ]; then
        mkdir $LOG_PATH
    fi
    if [ ! -f $PID_FILE ]; then
        echo -e "\n[$TIME_NOW] starting $SERVICE_NAME" >> $LOG_FILE
        echo "running command: nohup $JAVA_BIN $JVM_OPTS -cp "$JVM_SERVICE_JAR:lib/*" $JVM_MAIN_CLASS >> $LOG_FILE 2>&1 &" >> $LOG_FILE

        nohup $JAVA_BIN $JVM_OPTS -cp "$JVM_SERVICE_JAR:lib/*" $JVM_MAIN_CLASS >> $LOG_FILE 2>&1 &

        echo $! > $PID_FILE
        echo "$SERVICE_NAME started"
    else
        echo "$SERVICE_NAME is already running ..."
    fi
}

stop() {
    if [ -f $PID_FILE ]; then
        PID=$(cat $PID_FILE);
        echo "stopping $SERVICE_NAME ..."
        kill $PID;
        echo "$SERVICE_NAME stopped!"
        rm $PID_FILE
        echo "[$TIME_NOW] stopping $SERVICE_NAME" >> $LOG_FILE
    else
        echo "$SERVICE_NAME is not running ..."
    fi
}

status() {
    if [ -f $PID_FILE ]; then
        echo "$SERVICE_NAME is started"
    else
        echo "$SERVICE_NAME is stopped"
    fi
}

case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  status)
        status
        ;;
  restart)
        stop
        start
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart|status}"
        exit 1
esac
exit 0

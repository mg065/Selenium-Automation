#!/usr/bin/bash
today_is="weekday"
case "$(date +%a)" in
  Sat|Sun) today_is="weekend";;
esac

if [ "${today_is}" == "weekday" ]; then
	# Tachometer run
	/home/developer/Tahometer/tahometer.sh

	# Pycharm open
	/snap/pycharm-community/286/bin/pycharm.sh

	if ! ${1}; then
		read -rp "Enter your task id: " task_id
	else
		task_id=${1}
		hv-py sign-in "${task_id}"
	fi
fi


lunch_time_start="01:05"
lunch_time_end="02:05"
lunch_time_start_fri="12:30"
lunch_time_end_fri="02:30"

function get_current_time(){
	current_time=$(date | awk '{ print $5}' | awk -F ':' '{print $1":"$2}')
	echo "${current_time}"
}

if [ "$(date | awk '{print $1}')" == "Fri" ];
	then
		while [ get_current_time !=  "${lunch_time_start_fri}" ]
			do
				sleep 1m
			done
else
	while [ get_current_time !=  "${lunch_time_start}" ]
			do
				sleep 1m
			done
fi

hv-py stop

if [ "$(date | awk '{print $1}')" == "Fri" ];
	then
		while [ get_current_time !=  "${lunch_time_end_fri}" ]
			do
				sleep 1m
			done
else
	while [ get_current_time !=  "${lunch_time_end}" ]
			do
				sleep 1m
			done
fi

hv-py continue

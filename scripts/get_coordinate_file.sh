#!/usr/bin/expect -f

# Set variables
set user "nvidia"
set url "192.168.1.120"
set remoteFile "$user@$url:/home/nvidia/.GPS_Coordinate_Loader_GUI/gps_data.json"
set localDestination "./"
set password "jetsonmini"

# Run scp and pass password
spawn scp $remoteFile $localDestination
expect {
    "password:" {
        send "$password\r"
        exp_continue
    }
    eof
}

# Close the spawned process
wait


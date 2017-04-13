#!/bin/bash
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2017 - Dario Ostuni <dario.ostuni@gmail.com>
#

while true
do
    dialog --inputbox "Inserisci la velocità del serpente (da 1.0 a 10.0, consigliata 5.0):" 8 72 2> /tmp/__snakespeed_magic42
    printf "exit" > /tmp/__snakespeed_magic43
    diff /tmp/__snakespeed_magic43 /tmp/__snakespeed_magic42
    if [[ "$?" == "0" ]]
    then
        break
    fi
    sudo python3 unihatsnake.py $(cat /tmp/__snakespeed_magic42)
done
reset

#!/usr/bin/env bash
# Parallel Shopify harvests (one chain per host). Logs in work/_all/harvest_logs.
H="python3 /home/user/lumera/scripts/brands/harvest_shopify.py"; W=/home/user/lumera/work; L=$W/_all/harvest_logs; mkdir -p $L
( $H https://buyriteelectric.com $W/ELCO_Lighting/catalog_1_buyrite.json --collection elco-lighting > $L/elco.log 2>&1
  $H https://buyriteelectric.com $W/Panasonic/catalog_1_buyrite.json --collection panasonic > $L/panasonic.log 2>&1 ) &
( $H https://lightingsupply.com $W/Lutron/catalog_1_lightingsupply.json --collection lutron > $L/lutron.log 2>&1
  $H https://lightingsupply.com $W/Westgate/catalog_2_lightingsupply.json --collection westgate-manufacturing > $L/westgate2.log 2>&1 ) &
( $H https://sonicelectric.com $W/Orbit/catalog_1_sonic.json --collection orbit > $L/orbit.log 2>&1
  $H https://sonicelectric.com $W/Westgate/catalog_1_sonic.json --collection westgate > $L/westgate1.log 2>&1 ) &
( $H https://www.bulbamerica.com $W/Satco/catalog_1_bulbamerica_nuvo.json --collection nuvo-lighting > $L/satco1.log 2>&1
  $H https://www.bulbamerica.com $W/Satco/catalog_2_bulbamerica_satco.json --collection satco > $L/satco2.log 2>&1 ) &
( $H https://breakeroutlet.com $W/_all/breakeroutlet.json > $L/breakeroutlet.log 2>&1 ) &
( $H https://umage.us $W/UMAGE/catalog_1_umage_us.json > $L/umage.log 2>&1
  $H https://www.umage.com $W/UMAGE/catalog_2_umage_com.json > $L/umage2.log 2>&1 ) &
wait
echo ALL_HARVESTS_DONE

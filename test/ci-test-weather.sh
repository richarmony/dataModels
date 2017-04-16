#!/bin/sh

# Tests the Weather datamodels

testWeatherObserved(){
<<<<<<< HEAD
   # 1. check that the JSON Schema is a valid JSON Schema
   result=`ajv compile --v5 -s Weather/WeatherObserved/schema.json -r common-schema.json -r geometry-schema.json -r Weather/weather-schema.json`
   assertEquals "schema Weather/WeatherObserved/schema.json is valid" "${result}"

   # 2. check that the JSON example is valid according to the JSON Schema
   result=`ajv test --v5 -s Weather/WeatherObserved/schema.json -r common-schema.json -r geometry-schema.json -r Weather/weather-schema.json -d Weather/WeatherObserved/example.json --valid`
   assertEquals "Weather/WeatherObserved/example.json passed test" "${result}"
=======
   result = ajv compile --v5 -s ../Weather/WeatherObserved/schema.json -r ../common-schema.json -r ../geometry-schema.json -r ../Weather/weather-schema.json
   assertEquals "../Weather/WeatherObserved/example.json valid" "${result}"
   result = ajv test --v5 -s ../Weather/WeatherObserved/schema.json -r ../common-schema.json -r ../geometry-schema.json -r ../Weather/weather-schema.json -d ../Weather/WeatherObserved/example.json --valid
   assertEquals "schema ../Weather/WeatherObserved/schema.json is valid" "${result}"
>>>>>>> 960f08a... added example ci-test
}

# load shunit2
. shunit2

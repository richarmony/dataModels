#!/bin/sh

# Tests the WasteManagement datamodels

testWasteContainerIsle(){
   result=`ajv compile --v5 -s WasteManagement/WasteContainerIsle/schema.json -r common-schema.json -r geometry-schema.json`
   assertEquals "schema WasteManagement/WasteContainerIsle/schema.json is valid" "${result}"
   result=`ajv test --v5 -s WasteManagement/WasteContainerIsle/schema.json -r common-schema.json -r geometry-schema.json -d WasteManagement/WasteContainerIsle/example.json --valid`
   assertEquals "WasteManagement/WasteContainerIsle/example.json passed test" "${result}"
}

testWasteContainer(){
   result=`ajv compile --v5 -s WasteManagement/WasteContainer/schema.json -r common-schema.json -r geometry-schema.json`
   assertEquals "schema WasteManagement/WasteContainer/schema.json is valid" "${result}"
   result=`ajv test --v5 -s WasteManagement/WasteContainer/schema.json -r common-schema.json -r geometry-schema.json -d WasteManagement/WasteContainer/example.json --valid`
   assertEquals "WasteManagement/WasteContainer/example.json passed test" "${result}"
}

testWasteContainerModel(){
   result=`ajv compile --v5 -s WasteManagement/WasteContainerModel/schema.json -r common-schema.json -r geometry-schema.json`
   assertEquals "schema WasteManagement/WasteContainerModel/schema.json is valid" "${result}"
   result=`ajv test --v5 -s WasteManagement/WasteContainerModel/schema.json -r common-schema.json -r geometry-schema.json -d WasteManagement/WasteContainerModel/example.json --valid`
   assertEquals "WasteManagement/WasteContainerModel/example.json passed test" "${result}"
}

# load shunit2
. shunit2

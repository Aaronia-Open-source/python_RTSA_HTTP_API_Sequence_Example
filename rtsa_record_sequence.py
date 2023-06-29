import requests
import json
import time

#################### Setup endpoints & Block names. Open RTSA_Python_remote_automation.rmix to run this sample code
m_base_url = "http://localhost:54665/remoteconfig"
m_v6_block_name = "Block_Spectran_V6B_0"
m_filewriter_block_name = "Block_FileWriter_0"

def main():
    #################### list of measurements:
    measurement_tasks = [
    {
        "CenterFrequency": 105.3e6,
        "FileName": "/tmp/f_#f___#t_duration_#rd.rtsa", # Linux file path. Windows would be e.g. "c:\yourpath\to\store\records\myfile_#f___#t_duration_#rd.rtsa"
        "RecordDuration": 3.6  # in seconds
    },
    {
        "CenterFrequency": 433.050e6,
        "FileName": "/tmp/f_#f___#t_duration_#rd.rtsa",
        "RecordDuration": 3.5  # in seconds
    },
    {
        "CenterFrequency": 105.6e6,
        "FileName": "/tmp/f_#f___#t_duration_#rd.rtsa",
        "RecordDuration": 5  # in seconds
    },
    {
        "CenterFrequency": 144.8e6,
        "FileName": "/tmp/f_#f___#t_duration_#rd.rtsa",
        "RecordDuration": 2.3  # in seconds
    },]

    #################### OPTIONAL: query and print remote config
    
    #print("Querying and print remote config:")
    #print(query_remote_config())

    #################### OPTIONAL: query and print remote config

    #print("Starting V6:")
    #set_v6_active(True, m_v6_block_name)
    #print("Give V6 Time to boot")
    #time.sleep(5);

    #################### device setup

    print("Set AMPs, Reference level & span")
    set_v6_amp_to_auto(m_v6_block_name)
    set_v6_ref_level(m_v6_block_name, -35)
    set_v6_span(m_v6_block_name, "1 / 128");
    time.sleep(0.5);


    #################### start mesurement sequence
    for measurement in measurement_tasks:
        print(f'Recording at fCenter: {measurement["CenterFrequency"]}')

        set_v6_center_frequency(m_v6_block_name, measurement["CenterFrequency"])

        filename = measurement["FileName"]
        filename = filename.replace("#f", str(measurement["CenterFrequency"]))
        filename = filename.replace("#t", str(int(time.time())))
        filename = filename.replace("#rt", str(measurement["RecordDuration"]))

        set_filewriter_file_name(filename, m_filewriter_block_name);
        set_filewriter_active(True, m_filewriter_block_name)
        time.sleep(measurement["RecordDuration"])
        set_filewriter_active(False, m_filewriter_block_name)

        print(filename)

    
    #################### OPTIONAL: stop devices
    #print("Stopping V6:")
    #set_v6_active(False, m_v6_block_name)


def eval_response_ok( pResponse ):
    if pResponse.status_code is not 200:
        pResponse.raise_for_status()

def query_remote_config():
    response = requests.get(m_base_url)
    eval_response_ok(response)
    return response.json()

def set_v6_active( pActive, pBlock ):
    data = {
        "request": 11,
        "receiverName": pBlock,
        "config": {
            "type": "group",
            "items": [
                {
                    "type": "group",
                    "name": "main",
                    "items": [
                        {
                            "type": "bool",
                            "name": "run",
                            "value": pActive
                        }
                    ]
                }
            ]
        }
    }

    response = requests.put(m_base_url, data=json.dumps(data))
    eval_response_ok(response);
    return response.json()

def set_filewriter_file_name(pName, pBlock):
    data = {
        "flags": "",
        "receiverName": pBlock,
        "config": {
            "type": "group",
            "name": pBlock,
            "label": "File Writer",
            "flags": "",
            "items": [
                {
                    "type": "file",
                    "name": "filename",
                    "file": pName        
                }
            ]
        }
    }
    response = requests.put(m_base_url, data=json.dumps(data))
    eval_response_ok(response);
    return response.json()

def set_filewriter_active(pActive, pBlock):
    data = {
        "receiverName": pBlock,
        "config": {
            "type": "group",
            "name": pBlock,
            "label": "File Writer",
            "flags": "",
            "items": [
                {
                    "type": "bool",
                    "name": "filerecord",
                    "value": pActive      
                }
            ]
        }
    }
    response = requests.put(m_base_url, data=json.dumps(data))
    eval_response_ok(response)
    return response.json()

def set_v6_amp_to_auto(pBlock):
    data = {
        "request": 11,
        "receiverName": pBlock,
        "config": {
            "type": "group",
            "items": [
            {
                "type": "group",
                "name": "calibration",
                "items": [
                {
                    "type": "string",
                    "name": "preamp",
                    "value": "Auto"
                }
                ]
            }
            ]
        }
        }
    
    response = requests.put(m_base_url, data=json.dumps(data))
    eval_response_ok(response);
    return response.json()
    
def set_v6_ref_level(pBlock, pRefLevel):
  data =  {
    "request": 11,
    "receiverName": pBlock,
    "config": {
        "type": "group",
        "items": [
        {
            "type": "group",
            "name": "main",
            "items": [
            {
                "type": "float",
                "name": "reflevel",
                "value": pRefLevel
            }
            ]
        }
        ]
    }
    }
  
  response = requests.put(m_base_url, data=json.dumps(data))
  eval_response_ok(response);
  return response.json()
  

def set_v6_center_frequency(pBlock, pFrequency):
  data = {
    "request": 11,
    "receiverName": pBlock,
    "config": {
        "type": "group",
        "items": [
        {
            "type": "group",
            "name": "main",
            "items": [
            {
                "type": "float",
                "name": "centerfreq",
                "value": pFrequency
            }
            ]
        }
        ]
    }
    }
  
  response = requests.put(m_base_url, data=json.dumps(data))
  eval_response_ok(response);
  return response.json()

def set_v6_span(pBlock, pSpan):
  data = {
    "request": 11,
    "receiverName": pBlock,
    "config": {
        "type": "group",
        "items": [
        {
            "type": "group",
            "name": "main",
            "items": [
            {
                "type": "string",
                "name": "decimation",
                "value": pSpan
            }
            ]
        }
        ]
    }
    }
  
  response = requests.put(m_base_url, data=json.dumps(data))
  eval_response_ok(response);
  return response.json()

if __name__ == "__main__":
    main()

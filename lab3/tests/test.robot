*** Settings ***
Library  Process
Library  String

Test Setup    Run CLI    directory  create  root  2  None
Test Teardown   Run CLI    directory  delete  root
*** Variables ***
${APP NAME}    /home/anya/Desktop/qa-potapchuk-kp01/lab3/ui.py
${PATH}         ../dir
${FILE PATH}         ./dir
${INVALID PATH}         ../dir22222222222
${INVALID FILE PATH}         ./dir22222222222
*** Test Cases ***
Create valid directory
    ${root id}=     Get Root Id
    ${stdout}=    Run CLI    directory  create  dir  10  ${root id}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty    ${body["dir_id"]}
    Should Be Equal    ${status code}   200

Create two root folder
    ${stdout}=    Run CLI    directory  create  dir  10  None
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty    ${body["exception"]}
    Should Be Equal    ${status code}   400

Create invalid directory that already exist
    ${root id}=     Get Root Id
    Run CLI    directory  create  dir  10  ${root id}
    ${stdout}=    Run CLI    directory  create  dir  10  ${root id}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body["exception"]}
    Should Be Equal    ${status code}   400

Create more than max items in folder
    ${root id}=     Get Root Id
    Run CLI    directory  create  dir  10  ${root id}
    Run CLI    directory  create  dir2  10  ${root id}
    ${stdout}=  Run CLI    directory  create  dir3  10  ${root id}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body["exception"]}
    Should Be Equal    ${status code}   400

Delete folder that does not exist
    ${root id}=     Get Root Id
    Run CLI    directory   delete  ${root id}
    ${stdout}=  Run CLI    directory   delete  ${root id}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body["exception"]}
    Should Be Equal    ${status code}   400

Delete valid folder
    ${root id}=     Get Root Id
    ${stdout}=  Run CLI    directory   delete  ${root id}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Be Empty   ${body}
    Should Be Equal    ${status code}   200

Move to the valid path
    ${root id}=     Get Root Id
    Run CLI    directory    create      dir     10      ${root id}
    ${response}=    Run CLI    directory        create      dir1    10      ${root id}
    ${response body}=    Parse Response Body    ${response}
    ${stdout}=  Run CLI    directory   move     ${response body["dir_id"]}    ${PATH}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Be Empty   ${body}
    Should Be Equal    ${status code}   200

Move to invalid path
    ${root id}=     Get Root Id
    ${response}=    Run CLI    directory  create  dir  10  ${root id}
    ${response body}=    Parse Response Body    ${response}
    ${stdout}=  Run CLI    directory   move     ${response body["dir_id"]}    ${INVALID PATH}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body}
    Should Be Equal    ${status code}   404

Get all items in directiry
    ${root id}=     Get Root Id
    ${response}=    Run CLI    directory  create  dir  10  ${root id}
    ${response body}=    Parse Response Body    ${response}
    ${stdout}=  Run CLI    directory    get-items   ${response body["dir_id"]}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body}
    Should Be Equal    ${status code}   200

Create valid binaryfile
    ${root id}=     Get Root Id
    ${stdout}=    Run CLI    binaryfile  create  bin    something    ${root id}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty    ${body["file_id"]}
    Should Be Equal    ${status code}   200

Create invalid binaryfile that already exist
    ${root id}=     Get Root Id
    Run CLI    binaryfile  create  bin    something    ${root id}
    ${stdout}=    Run CLI    binaryfile  create  bin    something    ${root id}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body["exception"]}
    Should Be Equal    ${status code}   400


Delete binaryfile that does not exist
    ${root id}=     Get Root Id
    ${response}=    Run CLI     binaryfile  create  bin    something    ${root id}
    ${response body}=    Parse Response Body    ${response}
    Run CLI    binaryfile   delete  ${response body["file_id"]}
    ${stdout}=  Run CLI    binaryfile   delete  ${response body["file_id"]}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body["exception"]}
    Should Be Equal    ${status code}   404

Delete valid binaryfile
    ${root id}=     Get Root Id
    ${response}=    Run CLI     binaryfile  create  bin    something    ${root id}
    ${response body}=    Parse Response Body    ${response}
    ${stdout}=  Run CLI    binaryfile   delete  ${response body["file_id"]}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Be Empty   ${body}
    Should Be Equal    ${status code}   200

Move binaryfile to the valid path
    ${root id}=     Get Root Id
    Run CLI    directory    create      dir     10      ${root id}
    ${response}=    Run CLI     binaryfile  create  bin    something    ${root id}
    ${response body}=    Parse Response Body    ${response}
    ${stdout}=  Run CLI    binaryfile   move     ${response body["file_id"]}    ${FILE PATH}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Be Empty   ${body}
    Should Be Equal    ${status code}   200

Move binaryfile to invalid path
    ${root id}=     Get Root Id
    ${response}=    Run CLI     binaryfile  create  bin    something    ${root id}
    ${response body}=    Parse Response Body    ${response}
    ${stdout}=  Run CLI    binaryfile   move     ${response body["file_id"]}   ${INVALID FILE PATH}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body}
    Should Be Equal    ${status code}   400

Can read binaryfile
    ${root id}=     Get Root Id
    ${response}=    Run CLI     binaryfile  create  bin    something    ${root id}
    ${response body}=    Parse Response Body    ${response}
    ${stdout}=  Run CLI    binaryfile   read     ${response body["file_id"]}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body["text"]}
    Should Be Equal    ${status code}   200

Create valid logtextfile
    ${root id}=     Get Root Id
    ${stdout}=    Run CLI    logtextfile  create  bin    something    ${root id}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty    ${body["file_id"]}
    Should Be Equal    ${status code}   200

Create invalid logtextfile that already exist
    ${root id}=     Get Root Id
    Run CLI    logtextfile  create  bin    something    ${root id}
    ${stdout}=    Run CLI    logtextfile  create  bin    something    ${root id}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body["exception"]}
    Should Be Equal    ${status code}   400


Delete logtextfile that does not exist
    ${root id}=     Get Root Id
    ${response}=    Run CLI     logtextfile  create  bin    something    ${root id}
    ${response body}=    Parse Response Body    ${response}
    Run CLI    logtextfile   delete  ${response body["file_id"]}
    ${stdout}=  Run CLI    logtextfile   delete  ${response body["file_id"]}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body["exception"]}
    Should Be Equal    ${status code}   404

Delete valid logtextfile
    ${root id}=     Get Root Id
    ${response}=    Run CLI     logtextfile  create  bin    something    ${root id}
    ${response body}=    Parse Response Body    ${response}
    ${stdout}=  Run CLI    logtextfile   delete  ${response body["file_id"]}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Be Empty   ${body}
    Should Be Equal    ${status code}   200

Move logtextfile to the valid path
    ${root id}=     Get Root Id
    Run CLI    directory    create  dir     10      ${root id}
    ${response}=    Run CLI     logtextfile     create     bin    something    ${root id}
    ${response body}=    Parse Response Body    ${response}
    ${stdout}=  Run CLI    logtextfile   move     ${response body["file_id"]}    ${FILE PATH}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Be Empty   ${body}
    Should Be Equal    ${status code}   200

Move logtextfile to invalid path
    ${root id}=     Get Root Id
    ${response}=    Run CLI     logtextfile  create  bin    something    ${root id}
    ${response body}=    Parse Response Body    ${response}
    ${stdout}=  Run CLI    logtextfile   move     ${response body["file_id"]}   ${INVALID FILE PATH}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body}
    Should Be Equal    ${status code}   400

Can read logtextfile
    ${root id}=     Get Root Id
    ${response}=    Run CLI     logtextfile  create  bin    something    ${root id}
    ${response body}=    Parse Response Body    ${response}
    ${stdout}=  Run CLI    logtextfile   read     ${response body["file_id"]}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body["text"]}
    Should Be Equal    ${status code}   200

Create valid bufferfile
    ${root id}=     Get Root Id
    ${stdout}=    Run CLI    bufferfile  create  bin    something    ${root id}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty    ${body["file_id"]}
    Should Be Equal    ${status code}   200

Create invalid bufferfile that already exist
    ${root id}=     Get Root Id
    Run CLI    bufferfile  create  bin    something    ${root id}
    ${stdout}=    Run CLI    bufferfile  create  bin    something    ${root id}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body["exception"]}
    Should Be Equal    ${status code}   400


Delete bufferfile that does not exist
    ${root id}=     Get Root Id
    ${response}=    Run CLI     bufferfile  create  bin    something    ${root id}
    ${response body}=    Parse Response Body    ${response}
    Run CLI    bufferfile   delete  ${response body["file_id"]}
    ${stdout}=  Run CLI    bufferfile   delete  ${response body["file_id"]}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body["exception"]}
    Should Be Equal    ${status code}   404

Delete valid bufferfile
    ${root id}=     Get Root Id
    ${response}=    Run CLI     bufferfile  create  bin    something    ${root id}
    ${response body}=    Parse Response Body    ${response}
    ${stdout}=  Run CLI    bufferfile   delete  ${response body["file_id"]}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Be Empty   ${body}
    Should Be Equal    ${status code}   200

Move bufferfile to the valid path
    ${root id}=     Get Root Id
    Run CLI    directory    create      dir     10      ${root id}
    ${response}=    Run CLI     bufferfile  create  bin    something    ${root id}
    ${response body}=    Parse Response Body    ${response}
    ${stdout}=  Run CLI    bufferfile   move     ${response body["file_id"]}    ${FILE PATH}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Be Empty   ${body}
    Should Be Equal    ${status code}   200

Move bufferfile to invalid path
    ${root id}=     Get Root Id
    ${response}=    Run CLI     bufferfile  create  bin    something    ${root id}
    ${response body}=    Parse Response Body    ${response}
    ${stdout}=  Run CLI    bufferfile   move     ${response body["file_id"]}   ${INVALID FILE PATH}
    Log To Console    ${stdout}
    ${status code}=     Parse Status Code   ${stdout}
    ${body}=    Parse Response Body    ${stdout}
    Should Not Be Empty   ${body}
    Should Be Equal    ${status code}   400


*** Keywords ***
Run CLI
    [Arguments]    @{varargs}
    ${result}=  Run Process  python3  ${APP NAME}  @{varargs}
    [Return]    ${result.stdout}

Parse status code
    [Arguments]    ${stdout}
    ${split response} =    Split String   ${stdout}   ;
    [Return]    ${split response}[0]

Parse response body
    [Arguments]    ${stdout}
    ${split response} =    Split String   ${stdout}   ;
    ${json}=             evaluate        json.loads('''${split response}[1]''')    json
    [Return]    ${json}

Get root id
     ${stdout}=    Run CLI    directory  get_root
     ${body}=    Parse Response Body    ${stdout}
     [Return]    ${body["root_id"]}
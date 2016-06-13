# Ansible Modules for Java Flight Recorder

## Attention
**Ansible Modules for Java Flight Recorder is NOT Oracle product. If you would like to know the license of Java Flight Recorder, please check the BCL For Java SE or, please contact the Oracle. **  
BCL For Java SE  
http://www.oracle.com/technetwork/java/javase/terms/license/index.html  
Contact Oracle  
https://www.oracle.com/corporate/contact/index.html  
  
Check Java Flight Recorder on all java process.
```yml
- hosts: localhost
  tasks:
    - name: Get Java process id
      shell: jps -mlv | grep Sleep | awk '{print $1}'
      register: pids
    - name: Check JFR
      jfr:
         pid={{ item }}
         cmd=check
      register: jfr_output
      with_items: '{{pids.stdout_lines}}'
    - debug: msg='{{ jfr_output.results|map(attribute='stdout')|list }}'
```
Output is following
```shell
TASK [Get Java process id] *****************************************************
changed: [localhost]

TASK [Check JFR] ***************************************************************
ok: [localhost] => (item=2166)
ok: [localhost] => (item=32427)

TASK [debug] *******************************************************************
ok: [localhost] => {
    "msg": [
        "2166:Recording: recording=1 name='myrecording.jfr' duration=1m filename='myrecording.jfr' compress=false (stopped)",
        "32427:Recording: recording=1 name='myrecording.jfr' duration=1m filename='myrecording.jfr' compress=false (stopped)Recording: recording=2 name='Recording 2' (running)"
    ]
}
```

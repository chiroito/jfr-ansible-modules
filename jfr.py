#!/usr/bin/python

DOCUMENTATION = '''
---
module: jfr
short_description: Control Java Flight Recorder on OracleJDK
description:
     - This module controls Java Flight Recorder on OracleJDK using jcmd command.
     - Parameter details see https://docs.oracle.com/javacomponents/jmc-5-5/jfr-runtime-guide/comline.htm
version_added: "2.1"
options:
  pid:
    description:
      - "PID of OracleJDK process."
    required: true
  cmd:
    description:
        - "Operation to Java Flight Recorder."
    required: true
    choices: [ "start", "stop", "check", "dump" ]
  name:
    description:
      - "Name of recording"
    required: false
  settings:
    description:
      - "Server-side template"
    required: false
  defaultrecording:
    description:
      - "Starts default recording"
    required: false
  delay:
    description:
      - "Delay start of recording"
    required: false
  duration:
    description:
      - "Duration of recording"
    required: false
  filename:
    description:
      - "Resulting recording filename"
    required: false
  compress:
    description:
      - "GZip compress the resulting recording file"
    required: false
  maxage:
    description:
      - "Maximum age of buffer data"
    required: false
  maxsize:
    description:
      - "Maximum size of buffers in bytes"
    required: false
  recording:
    description:
      - "Recording id"
    required: false
  verbose:
    description:
      - "Print verbose data"
    required: false
  discard:
    description:
      - "Discards the recording data"
    required: false
  copy_to_file:
    description:
      - "Copy recording data to file"
    required: false
  compress_copy:
    description:
      - "GZip compress copy_to_file destination"
    required: false
author:
    - Chihiro Ito
requirements:
   - jcmd (command line binary)
notes:
   - see also https://docs.oracle.com/javacomponents/jmc-5-5/jfr-runtime-guide/comline.htm
'''

EXAMPLES = '''
# Start Java Flight Recorder on OracleJDK that PID is 1234.
- jfr: pid=1234 cmd=start

# Stop recording 1 of Java Flight Recorder on OracleJDK that PID is 1234.
- jfr: pid=1234 cmd=stop recording=1

# Dump Java Flight Recorder (recording id=1) to ~/dump.jfr file.
- jfr: pid=1234 cmd=dump recording=1 copy_to_file=~/dump.jfr
'''


def main():
    module = AnsibleModule(
        argument_spec=dict(
            pid=dict(type='int', required=True),
            cmd=dict(type='str', required=True,
                     choices=['start', 'stop', 'check', 'dump']),
            name=dict(type='str', required=False),
            settings=dict(type='str', required=False),
            defaultrecording=dict(type='bool', required=False),
            delay=dict(type='int', required=False),
            duration=dict(type='int', required=False),
            filename=dict(type='str', required=False),
            compress=dict(type='bool', required=False),
            maxage=dict(type='int', required=False),
            maxsize=dict(type='int', required=False),
            recording=dict(type='int', required=False),
            verbose=dict(type='bool', required=False),
            discard=dict(type='bool', required=False),
            copy_to_file=dict(type='str', required=False),
            compress_copy=dict(type='bool', required=False),
        ),
        supports_check_mode=True
    )

    jfr_option = dict(
        start={'name', 'settings', 'defaultrecording', 'delay',
               'duration', 'filename', 'compress', 'maxage', 'maxsize'},
        stop={'name', 'recording', 'verbose'},
        check={'name', 'recording', 'discard',
               'copy_to_file', 'compress_copy'},
        dump={'name', 'recording', 'copy_to_file', 'compress_copy'}
    )

    pid = module.params['pid']
    cmd = module.params['cmd']

    jcmd_path = module.get_bin_path('jcmd', required=True)

    param = []
    for _param in jfr_option[cmd]:
        if module.params[_param] is not None:
            param.append('%s=%s' % (_param, module.params[_param]))

    param_str = ' '.join(param)

    (rc, out, err) = module.run_command(
        '%s %s JFR.%s %s' % (jcmd_path, pid, cmd, param_str),
        check_rc=True
    )

    module.exit_json(changed=True, rc=rc, stdout=out, stderr=err)

from ansible.module_utils.basic import *


if __name__ == '__main__':
    main()

#!/usr/bin/python
DOCUMENTATION = '''
'''

EXAMPLES = '''
'''

def main():
    module = AnsibleModule(
        argument_spec=dict(
            pid=dict(type='int',  required=True),
            cmd=dict(type='str', required=True, choices=['start', 'stop', 'check', 'dump']),
            name=dict(type='str', required=False),
            settings=dict(type='str',  required=False),
            defaultrecording=dict(type='bool',  required=False),
            delay=dict(type='int',  required=False),
            duration=dict(type='int',  required=False),
            filename=dict(type='str',  required=False),
            compress=dict(type='bool',  required=False),
            maxage=dict(type='int',  required=False),
            maxsize=dict(type='int',  required=False),
            recording=dict(type='int',  required=False),
            verbose=dict(type='bool',  required=False),
            discard=dict(type='bool',  required=False),
            copy_to_file=dict(type='str',  required=False),
            compress_copy=dict(type='bool',  required=False),
        ),
        supports_check_mode=True,
    )

    jfr_option = dict(
        start={'name','settings','defaultrecording','delay','duration','filename','compress','maxage','maxsize'},
        stop={'name','recording','verbose'},
        check={'name','recording','discard','copy_to_file','compress_copy'},
        dump={'name','recording','copy_to_file','compress_copy'}
    )

    pid = module.params["pid"]
    cmd = module.params["cmd"]

    jcmd_path = module.get_bin_path('jcmd', required=True)

    param=[]
    for _param in jfr_option[cmd]:
        if module.params[_param] is not None:
            param.append('%s=%s' % (_param, module.params[_param]))

    param_str = " ".join(param)
    (rc, out, err) = module.run_command('%s %s JFR.%s %s' % (jcmd_path, pid, cmd, param_str), check_rc=True)

    module.exit_json(changed=True, rc=rc, stdout=out, stderr=err)

from ansible.module_utils.basic import *

main()

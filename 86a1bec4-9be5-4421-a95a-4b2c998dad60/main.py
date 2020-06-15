#!/usr/bin/env python3

# Seluxit - License agreement
#
# TERMS AND CONDITIONS FOR USE AND MODIFICATION OF THE PROGRAM
#
# 0. Preamble.
# This License applies to any program or other work which contains it. The
# "Program", below, refers to any such program or work, and a "work based on the
# Program" means either the Program or any derivative work under copyright law:
# that is to say, a work containing the Program or a portion of it, either
# verbatim or with modifications and/or translated into another language.
# (Hereinafter, translation is included without limitation in the term
# "modification".) The licensee is addressed as "you". “Parties” shall refer to
# both Seluxit and you.
#
# 1. Acceptance.
# You are not required to accept this License, since you have not signed it.
# However, nothing else grants you permission to use or modify the Program or
# its derivative works. These actions are prohibited by law if you do not accept
# this License. Therefore, by using or modifying the Program (or any work based
# on the Program), you indicate your acceptance of this License to do so, and
# all its terms and conditions for using, or modifying the Program or works
# based on it.
#
# 2. Proprietary Rights.
# The Program is and shall remain the sole property of Seluxit and its
# licensors. Except for the license rights granted herein, Seluxit and its
# licensors retain all right, title and interest in and to the Program,
# including all intellectual property rights therein and thereto.
# You may modify the Program or any portion of it, thus forming a work based on
# the Program, and send such modifications to us for approval. You must cause
# the modified files to carry prominent notices stating that you changed the
# files and the date of any change. You furthermore agree and understand that
# all modifications and derivatives of the Program including new functionalities
# are Seluxit’s propriety. Except for the license rights granted herein, Seluxit
# and its licensors retain all right, title and interest in and to such
# modifications and derivatives Program, including all intellectual property
# rights therein and thereto.
# You may use and modify the Program in object code or executable form only
# under the terms of this agreement. The source code for a work means the
# preferred form of the work for making modifications to it. Any attempt
# otherwise to use or modify the Program is void and will automatically
# terminate your rights under this License.
#
# 2.1 License Grant as to Free Licenses.
# A “Free License” is allowed for a personal, non-commercial use of the Program.
# As personal use we understand any use of the Program for purposes that are
# neither directly nor indirectly paid. It is not about whether the service
# itself is paid but whether the service is rendered within the context of the
# creation of an added value with some kind of financial compensation.
# Subject to your compliance with the terms and conditions herein, Seluxit
# grants to you a world-wide, non-exclusive, revocable, non-transferable,
# non-sublicensable, non-fee bearing license to use and modify the Program only
# for your own internal use, related to your solutions. If, at any time, you
# start using the Program commercially, your rights under this Agreement are
# terminated. If you wish to continue to use the Program you acknowledge that a
# separate Enterprise License needs to be agreed upon in writing by the Parties.
#
# 2.2 License Grant as to Enterprise Licenses.
# An “Enterprise License” is required if you make any commercial use of the
# Program. Subject to your compliance with the terms of the Enterprise License,
# Seluxit may grant you a world-wide, non-exclusive, revocable,
# non-transferable, non-sublicensable, fee bearing license to only use and/or
# modify the Program according with the terms and conditions of such separate
# Enterprise License, which has to be agreed upon by the Parties.
# Seluxit has no obligation to provide any type of support or service in
# connection to the Program irrespective of the type of license used by you,
# unless otherwise agreed to in writing by the Parties.
#
# 3. Restrictions.
# You will not:
# (a) use or modify the Program in any manner except as expressly permitted in
# this Agreement;
# (c) transfer, sell, rent, lease, lend, distribute, or sublicense the Program
# to any third party;
# (d) use the Program for other purposes than the ones it has been shared with
# you for, as described above.
# (g) alter or remove any proprietary notices in the Program;
#
# 4. No warranty.
# There is no warranty for the Program, to the extent permitted by applicable
# law. The Program is provided "as is" without warranty of any kind, either
# expressed or implied, including, but not limited to, the implied warranties of
# merchantability and fitness for a particular purpose. The entire risk as to
# the quality of any performance of the program is with you. Should the program
# prove defective, you assume the cost of all necessary servicing, repair or
# correction.
#
# 5. Liability.
# In no event will Seluxit be liable to you for damages, including any general,
# special, incidental or consequential damages arising out of the use or
# inability to use the program (including but not limited to loss of data or
# data being rendered inaccurate or losses sustained by you or third parties or
# a failure of the program to operate with any other programs).
#
# 6. Term and Termination.
# The Agreement shall apply at soon as the Program has been shared with you and
# shall remain in effect until terminated. Our blocking of your access to the
# Program shall constitute the termination of your rights but not your
# obligations and restrictions under this Agreement, which shall survive the
# termination of this Agreement.
# If you do not comply with the terms of the Agreement or the restrictions
# herein, we may terminate your license to the Program or, at our sole
# discretion, suspend your license to the Program until you come into compliance
# with such terms and restrictions.
from threading import Event
import logging
import signal
import sys
import time
import SimpleMFRC522

try:
    import wappsto
except ImportError:
    print("Failed to import the Wappsto package.")
    print("Please install it using 'pip3 install wappsto'")
    sys.exit(-1)

exit_code = 0
killed = Event()
reader = SimpleMFRC522.SimpleMFRC522()

stop_cb = (lambda *args: killed.set())

signal.signal(signal.SIGINT, stop_cb)
signal.signal(signal.SIGTERM, stop_cb)

logging.basicConfig(
    level=logging.DEBUG,  # or .INFO
    format="%(asctime)s - %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

wapp_log = logging.getLogger(__name__)

service = wappsto.Wappsto(json_file_name='86a1bec4-9be5-4421-a95a-4b2c998dad60.json')


def status_callback(status):
    wapp_log.info("Current status: {}".format(status.current_status))


def network_callback(network, event):
    wapp_log.info("network event: {}".format(event))
    global exit_code
    exit_code = 181
    stop_cb()


def pump_value_callback(value, action_type):
    parent_device = value.get_parent_device()
    if action_type == 'refresh':
        msg = "Refreshing value: {} of a device [{}]".format(
            value.name,
            parent_device.name,
        )
        wapp_log.info(msg)
        value.update(value.report_state.data)
    elif action_type == 'set':
        '''
        msg = "The value: {} of a device [{}] has been changed to {}.".format(
            value.name,
            parent_device.name,
            value.report_state.data
        )
        wapp_log.info(msg)
        value.update(value.report_state.data)
        '''


status_service = service.get_status()
status_service.set_callback(status_callback)

service.get_network().set_callback(network_callback)

pump_device = service.get_device("pump")
pump_value = pump_device.get_value("nfc_reader")
pump_value.set_callback(pump_value_callback)

def read():
    id, text = self.reader.read()
    self.pump_value.report_state.data = text;
    self.pump_value.update(text)
    self.read()

if __name__ == "__main__":
    try:
        service.start(address="collector.wappsto.com", port=443)

        try:
            #while not killed.is_set():
            #    time.sleep(1)
            self.read()
        except BaseException:
            pass

        service.stop()
    except Exception as e:
        wapp_log.error("Failed to start: {}".format(e))

    sys.exit(exit_code)

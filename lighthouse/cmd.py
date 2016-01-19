#!/usr/bin/env python2

import sys
import random
import re
from time import sleep
import logging
from multiprocessing import Process, Value, Manager, Array
from ctypes import c_char, c_char_p
import subprocess
import json
import os

try:
    import xdg.BaseDirectory
    import xdg.DesktopEntry
    import xdg.IconTheme
    HAS_XDG = True
except ImportError:
    HAS_XDG = False

if "XDG_CONFIG_HOME" in os.environ:
    XDG_CONFIG_HOME = os.environ["XDG_CONFIG_HOME"]
else:
    XDG_CONFIG_HOME = os.path.expanduser("~/.config")

ICON_THEME_CONFIG_FILES = (
    os.path.expanduser("~/.gtkrc-2.0"),
    os.path.expanduser("~/.config/gtkrc-2.0"),
    "/etc/gtk-2.0/gtkrc",
    "%s/gtk-3.0/settings.ini" % XDG_CONFIG_HOME,
    "/etc/gtk-3.0/settings.ini",
)

TERMINAL = "terminator"
MAX_OUTPUT = 100 * 1024
result_buf = Array(c_char, MAX_OUTPUT);

# Output management
def clear_output():
    result_buf.value = json.dumps([])

def update_output():
    results = json.loads(result_buf.value)
    print("".join(results))
    sys.stdout.flush()

def append_output(title, action):
    result = create_result(title, action)
    results = json.loads(result_buf.value)

    if len(results) < 2:
        results.append(result)
    else: # Ignore the bottom two default option
        results.insert(-2, result)

    result_buf.value = json.dumps(results)

def prepend_output(title, action):
    results = json.loads(result_buf.value)
    results.insert(0, create_result(title, action))
    result_buf.value = json.dumps(results)

def get_process_output(process, string, action):
    process_out = str(subprocess.check_output(process))
    out_str = ((string % (process_out) if ("%s" in string) else string))
    out_act = ((action % (process_out) if ("%s" in action) else action))
    return (out_str, out_act)

# XDG functions
def xdg_find_desktop_entry(cmd):
    files = list(xdg.BaseDirectory.load_data_paths(\
            "applications", "%s.desktop" % (cmd)))

    if files:
        # Earlier paths take precedence
        return xdg.DesktopEntry.DesktopEntry(files[0])

def xdg_get_icon_theme():
    for fn in ICON_THEME_CONFIG_FILES:
        try:
            for line in file(fn, 'r').readlines():
                # Extract icon theme and remove quotes
                match = re.match(r'^\s*gtk-icon-theme-name\s*=\s*("?)(.*)\1\s*', line)
                if match:
                    return match.group(2)
        except:
            pass

    # Fallback icon theme, required to be present
    return "hicolor"

def xdg_get_icon(desktop_entry):
    icon = desktop_entry.getIcon()
    if icon:
        fn = xdg.IconTheme.getIconPath(icon, theme=xdg_get_icon_theme())

        if fn.endswith(".svg"):
            return xdg.IconTheme.getIconPath(icon)
        else:
            return fn

def xdg_get_exec(desktop_entry):
    # Since the exec path may contain subsitution parameters such as %f,
    # we need to remove them.
    exec_spec = desktop_entry.getExec()
    return re.sub(r"%.", "", exec_spec).strip()

def xdg_get_cmd(cmd):
    if not HAS_XDG:
        return

    desktop_entry = xdg_find_desktop_entry(cmd)
    if not desktop_entry:
        return

    exec_path = xdg_get_exec(desktop_entry)
    if not exec_path:
        return

    icon = xdg_get_icon(desktop_entry)
    if icon:
        menu_entry = "%%I%s%%%s" % (icon, cmd)
    else:
        menu_entry = cmd

    return (menu_entry, exec_path)

# Helper functions
def sanitize(string):
    return string.replace("{", "\\{") \
                 .replace("}", "\\}") \
                 .replace("|", "\\|") \
                 .replace("\n", " ")

def create_result(title, action):
    return "{%s |%s }" % \
        (sanitize(title),
         sanitize(action))

# Main function
def parse_line():
    line = sys.stdin.readline()[:-1]
    clear_output()

    if not line:
        update_output()
        return

    try:
        complete = subprocess.check_output("compgen -c %s" % (line), shell=True, executable="/bin/bash")
        complete = complete.split('\n')

        for cmd_num in range(min(len(complete), 5)):
                # Look for XDG applications of the given name.
                xdg_cmd = xdg_get_cmd(complete[cmd_num])
                if xdg_cmd:
                    append_output(*xdg_cmd)
    except:
        pass

    finally:
        # Could be bash...
        prepend_output("run '%s' in a shell" % (line),
                      "%s -e %s" % (TERMINAL, line))
        # Could be a command...
        prepend_output("execute '%s'" % line, line)

        update_output()

# Main loop
if __name__ == "__main__":
    while True:
        parse_line()


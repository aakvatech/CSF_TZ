# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import importlib

import frappe

__version__ = "2.1.0"
patches_loaded = False


def console(*data):
    frappe.publish_realtime("out_to_console", data, user=frappe.session.user)


def load_monkey_patches():
    global patches_loaded

    if (
        patches_loaded
        or not getattr(frappe, "conf", None)
        or not "csf_tz" in frappe.get_installed_apps()
    ):
        return

    for module_name in os.listdir(frappe.get_app_path("csf_tz", "monkey_patches")):
        if not module_name.endswith(".py") or module_name == "__init__.py":
            continue

        importlib.import_module("csf_tz.monkey_patches." + module_name[:-3])

    patches_loaded = True



connect = frappe.connect


def custom_connect(*args, **kwargs):
    out = connect(*args, **kwargs)

    if frappe.conf.auto_commit_on_many_writes:
        frappe.db.auto_commit_on_many_writes = 1

    load_monkey_patches()
    return out


frappe.connect = custom_connect

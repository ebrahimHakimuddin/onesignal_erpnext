import frappe
import requests
import re

def get_onesignal_settings():
    return {
        "app_id": frappe.db.get_single_value("OneSignal Settings", "app_id"),
        "api_key": frappe.db.get_single_value("OneSignal Settings", "rest_api_key"),
    }

def send_onesignal_from_log(doc, method):
    settings = {
	"app_id": YOUR-APP-ID,
	"api_key": YOUR-API-KEY,
    }
    if not settings["app_id"] or not settings["api_key"]:
        frappe.log_error("OneSignal Settings not configured")
        return

    recipients = []

    # Case 1: Notification to a specific user
    if doc.for_user:
        recipients = [doc.for_user]

    # Case 2: Notification to a role
    elif doc.for_role:
        role_users = frappe.get_all(
            "Has Role",
            filters={"role": doc.for_role},
            fields=["parent as user"]
        )
        recipients = [
            r.user for r in role_users
            if r.user and r.user not in ("Administrator", "Guest")
        ]

    # Case 3: Notification to everyone
    else:
        all_users = frappe.get_all(
            "User",
            filters={"enabled": 1},
            pluck="name"
        )
        recipients = [
            u for u in all_users
            if u not in ("Administrator", "Guest")
        ]

    if not recipients:
        return

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {settings['api_key']}",
    }
    # Split into chunks of 2000
    chunk_size = 2000
    for i in range(0, len(recipients), chunk_size):
        chunk = recipients[i:i + chunk_size]

        payload = {
            "app_id": settings["app_id"],
            "include_external_user_ids": chunk,
            "headings": {"en": frappe.utils.strip_html(doc.subject) or "ERPNext Notification"},
            "contents": {"en": frappe.utils.strip_html(doc.email_content or doc.subject)},
	    "url": frappe.utils.get_url_to_form(doc.doctype, doc.name).replace("http://","https://")
        }

        try:
            res = requests.post(
                "https://onesignal.com/api/v1/notifications",
                headers=headers,
                json=payload,
                timeout=10,
            )
            res.raise_for_status()
        except Exception as e:
            frappe.log_error(f"OneSignal push failed for chunk {i//chunk_size+1}: {str(e)}")

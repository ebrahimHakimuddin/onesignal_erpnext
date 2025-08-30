import("https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js");

window.OneSignalDeferred = window.OneSignalDeferred || [];

// Option 1: jQuery (always available in Frappe)
$(document).ready(() => {
  OneSignalDeferred.push(async function (OneSignal) {
    if (frappe.session.user === "Guest") {
      await OneSignal.logout();
    } else {
      await OneSignal.login(frappe.session.user);
    }
  });
});

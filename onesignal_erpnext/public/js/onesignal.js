import("https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js");

window.OneSignalDeferred = window.OneSignalDeferred || [];

$(document).ready(() => {
 
  OneSignalDeferred.push(async function (OneSignal) {
     await OneSignal.init({
         appId: "YOUR_ONESIGNAL_APP_ID",
       });
    if (frappe.session.user === "Guest") {
      await OneSignal.logout();
    } else {
      await OneSignal.login(frappe.session.user);
    }
  });
});

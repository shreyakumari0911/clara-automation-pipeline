# Changelog

### Account Memo Changes

- **after_hours_flow_summary** changed:
```diff
--- v1
+++ v2
@@ -0,0 +1 @@
+After hours, if the situation matches that emergency definition, Clara should capture the same details and then page the on‑call technician by transferring to the on‑call number. If the transfer rings more than 60 seconds, Clara should return to the caller, apologize, and promise a callback as soon as the technician receives the page. Non‑emergency calls after hours can be logged with all details and clearly tagged as next‑business‑day follow up.
```

- **business_hours** changed:
```diff
--- v1
+++ v2
@@ -9,5 +9,5 @@
   "start": "09:00",
   "end": "17:00",
   "timezone": "ET",
-  "raw": "Our office hours are 9 AM to 5 PM Eastern, Monday through Friday. During that time, calls about billing or new installs go to the office, while service calls go to the service queue."
+  "raw": "Mon–Fri 9:00 AM–5:00 PM ET"
 }
```

- **call_transfer_rules** changed:
```diff
--- v1
+++ v2
@@ -1,5 +1,5 @@
 {
-  "raw": "",
+  "raw": "For qualifying fire alarm emergencies, transfer to the on-call alarm technician. If the transfer rings for more than 60 seconds, return to the caller, apologize, and confirm the technician will call back quickly.",
   "timeout_seconds": null,
   "retries": null,
   "what_to_say_if_fails": ""
```

- **emergency_routing_rules** changed:
```diff
--- v1
+++ v2
@@ -1,6 +1,8 @@
 {
-  "raw": "For emergencies, we only want Clara to escalate if the monitoring center has already called them and they are following up, or if there is an active trouble on the fire alarm panel that is beeping continuously and they cannot silence it.",
+  "raw": "For emergencies we only want Clara to escalate when either the monitoring center has already contacted the customer about an alarm or when there is a continuous trouble on the fire alarm panel that the customer cannot silence. Those should be called out as high priority. After hours, if the situation matches that emergency definition, Clara should capture the same details and then page the on‑call technician by transferring to the on‑call number. If the transfer rings more than 60 seconds, Clara should return to the caller, apologize, and promise a callback as soon as the technician receives the page. Non‑emergency calls after hours can be logged with all details and clearly tagged as next‑business‑day follow up.",
   "steps": [
-    "For emergencies, we only want Clara to escalate if the monitoring center has already called them and they are following up, or if there is an active trouble on the fire alarm panel that is beeping continuously and they cannot silence it."
+    "For emergencies we only want Clara to escalate when either the monitoring center has already contacted the customer about an alarm or when there is a continuous trouble on the fire alarm panel that the customer cannot silence. Those should be called out as high priority.",
+    "After hours, if the situation matches that emergency definition, Clara should capture the same details and then page the on‑call technician by transferring to the on‑call number. If the transfer rings more than 60 seconds, Clara should return to the caller, apologize, and promise a callback as soon as the technician receives the page.",
+    "Non‑emergency calls after hours can be logged with all details and clearly tagged as next‑business‑day follow up."
   ]
 }
```

- **integration_constraints** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-We use our own internal ticketing system, not ServiceTrade. Clara should not try to log into anything; just capture the situation clearly so our team can open a ticket.
+Use internal alarm ticketing only; Clara must not reference or depend on any external system.
```

- **notes** changed:
```diff
--- v1
+++ v2
@@ -1 +1,5 @@
-[]
+[
+  "Structured form override for 'business_hours': 'raw' overridden: previous='Our standard hours are Monday through Friday, 9:00 AM to 5:00 PM Eastern Time. Billing and sales calls go to the main office line; service issues go to the service queue.', new='Mon–Fri 9:00 AM–5:00 PM ET'.",
+  "Structured form override for 'call_transfer_rules': 'raw' overridden: previous='After hours, if the situation matches that emergency definition, Clara should capture the same details and then page the on‑call technician by transferring to the on‑call number. If the transfer rings more than 60 seconds, Clara should return to the caller, apologize, and promise a callback as soon as the technician receives the page.', new='For qualifying fire alarm emergencies, transfer to the on-call alarm technician. If the transfer rings for more than 60 seconds, return to the caller, apologize, and confirm the technician will call back quickly.'.",
+  "Structured form override for 'integration_constraints': previous value='We use our own internal ticketing system, not ServiceTrade. Clara should not try to log into anything; just capture the situation clearly so our team can open a ticket.', new value='Use internal alarm ticketing only; Clara must not reference or depend on any external system.'."
+]
```

- **office_hours_flow_summary** changed:
```diff
--- v1
+++ v2
@@ -0,0 +1 @@
+During office hours, Clara should collect caller name, site name, callback number, panel type if they know it, and whether the monitoring center has called. Then route to the service queue.
```

- **questions_or_unknowns** changed:
```diff
--- v1
+++ v2
@@ -1,8 +1,5 @@
 [
   "Missing office address (not found or unclear in transcript).",
   "Missing services supported (not found or unclear in transcript).",
-  "Missing emergency definition (not found or unclear in transcript).",
-  "Missing call transfer rules (not found or unclear in transcript).",
-  "Missing after-hours flow summary (not found or unclear in transcript).",
-  "Missing office-hours flow summary (not found or unclear in transcript)."
+  "Missing emergency definition (not found or unclear in transcript)."
 ]
```

### Agent Spec Changes

- **agent_name** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-CityLine Alarm & Monitoring – Clara Answers Agent v1
+CityLine Alarm & Monitoring – Clara Answers Agent v2
```

- **call_transfer_protocol** changed:
```diff
--- v1
+++ v2
@@ -1,5 +1,5 @@
 {
-  "raw": "",
+  "raw": "For qualifying fire alarm emergencies, transfer to the on-call alarm technician. If the transfer rings for more than 60 seconds, return to the caller, apologize, and confirm the technician will call back quickly.",
   "timeout_seconds": null,
   "retries": null,
   "what_to_say_if_fails": ""
```

- **key_variables** changed:
```diff
--- v1
+++ v2
@@ -12,14 +12,16 @@
     "start": "09:00",
     "end": "17:00",
     "timezone": "ET",
-    "raw": "Our office hours are 9 AM to 5 PM Eastern, Monday through Friday. During that time, calls about billing or new installs go to the office, while service calls go to the service queue."
+    "raw": "Mon–Fri 9:00 AM–5:00 PM ET"
   },
   "office_address": "",
   "timezone": "ET",
   "emergency_routing": {
-    "raw": "For emergencies, we only want Clara to escalate if the monitoring center has already called them and they are following up, or if there is an active trouble on the fire alarm panel that is beeping continuously and they cannot silence it.",
+    "raw": "For emergencies we only want Clara to escalate when either the monitoring center has already contacted the customer about an alarm or when there is a continuous trouble on the fire alarm panel that the customer cannot silence. Those should be called out as high priority. After hours, if the situation matches that emergency definition, Clara should capture the same details and then page the on‑call technician by transferring to the on‑call number. If the transfer rings more than 60 seconds, Clara should return to the caller, apologize, and promise a callback as soon as the technician receives the page. Non‑emergency calls after hours can be logged with all details and clearly tagged as next‑business‑day follow up.",
     "steps": [
-      "For emergencies, we only want Clara to escalate if the monitoring center has already called them and they are following up, or if there is an active trouble on the fire alarm panel that is beeping continuously and they cannot silence it."
+      "For emergencies we only want Clara to escalate when either the monitoring center has already contacted the customer about an alarm or when there is a continuous trouble on the fire alarm panel that the customer cannot silence. Those should be called out as high priority.",
+      "After hours, if the situation matches that emergency definition, Clara should capture the same details and then page the on‑call technician by transferring to the on‑call number. If the transfer rings more than 60 seconds, Clara should return to the caller, apologize, and promise a callback as soon as the technician receives the page.",
+      "Non‑emergency calls after hours can be logged with all details and clearly tagged as next‑business‑day follow up."
     ]
   }
 }
```

- **system_prompt** changed:
```diff
--- v1
+++ v2
@@ -2,13 +2,13 @@
 
 === Business Hours Call Flow ===
 Business hours description:
-Our office hours are 9 AM to 5 PM Eastern, Monday through Friday. During that time, calls about billing or new installs go to the office, while service calls go to the service queue.
+Mon–Fri 9:00 AM–5:00 PM ET
 During business hours, follow **exactly** this sequence. Do not skip steps, and do not add new ones:
 1. Greeting: Greet the caller on behalf of the business and state that you are an AI assistant.
 2. Ask purpose: Ask the caller for the reason for their call.
 3. Collect name and number: Collect the caller's name and callback phone number early in the call.
 4. Determine routing: Based only on the rules below and the memo:
-   - Office-hours flow summary: [UNKNOWN: office hours call flow summary – if caller asks, say you do not have this information yet and collect it for a human follow-up.]
+   - Office-hours flow summary: During office hours, Clara should collect caller name, site name, callback number, panel type if they know it, and whether the monitoring center has called. Then route to the service queue.
    - Do not guess routes that are not specified.
 5. Transfer or route: If routing requires a live person, follow the transfer protocol section.
 6. Fallback if transfer fails: If the transfer fails, drops, or no one answers, follow the 'Transfer Failure Handling' section.
@@ -17,7 +17,7 @@
 
 === After-Hours Call Flow ===
 After-hours flow description:
-[UNKNOWN: after-hours flow summary – if caller asks, say you do not have this information yet and collect it for a human follow-up.]
+After hours, if the situation matches that emergency definition, Clara should capture the same details and then page the on‑call technician by transferring to the on‑call number. If the transfer rings more than 60 seconds, Clara should return to the caller, apologize, and promise a callback as soon as the technician receives the page. Non‑emergency calls after hours can be logged with all details and clearly tagged as next‑business‑day follow up.
 During after-hours, follow **exactly** this sequence. Do not skip steps, and do not add new ones:
 1. Greeting: Greet the caller on behalf of the business and clarify that it is after hours.
 2. Ask purpose: Ask the caller for the reason for their call.
@@ -35,17 +35,12 @@
 Definition / examples of emergencies:
 [UNKNOWN: emergency definition – if caller asks, say you do not have this information yet and collect it for a human follow-up.]
 Routing rules for emergencies:
-For emergencies, we only want Clara to escalate if the monitoring center has already called them and they are following up, or if there is an active trouble on the fire alarm panel that is beeping continuously and they cannot silence it.
+For emergencies we only want Clara to escalate when either the monitoring center has already contacted the customer about an alarm or when there is a continuous trouble on the fire alarm panel that the customer cannot silence. Those should be called out as high priority. After hours, if the situation matches that emergency definition, Clara should capture the same details and then page the on‑call technician by transferring to the on‑call number. If the transfer rings more than 60 seconds, Clara should return to the caller, apologize, and promise a callback as soon as the technician receives the page. Non‑emergency calls after hours can be logged with all details and clearly tagged as next‑business‑day follow up.
 Routing rules for non-emergencies:
 A lot of our calls are non-emergency: low-priority troubles, beeping keypads on security systems, and programming questions. Those can wait until office hours.
 
 === Call Transfer Protocol ===
-{
-  "raw": "",
-  "timeout_seconds": null,
-  "retries": null,
-  "what_to_say_if_fails": ""
-}
+For qualifying fire alarm emergencies, transfer to the on-call alarm technician. If the transfer rings for more than 60 seconds, return to the caller, apologize, and confirm the technician will call back quickly.
 If you initiate a transfer, clearly tell the caller who you are transferring to and why.
 
 === Transfer Failure Handling ===
@@ -69,6 +64,3 @@
 - Missing office address (not found or unclear in transcript).
 - Missing services supported (not found or unclear in transcript).
 - Missing emergency definition (not found or unclear in transcript).
-- Missing call transfer rules (not found or unclear in transcript).
-- Missing after-hours flow summary (not found or unclear in transcript).
-- Missing office-hours flow summary (not found or unclear in transcript).
```

- **version** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-v1
+v2
```

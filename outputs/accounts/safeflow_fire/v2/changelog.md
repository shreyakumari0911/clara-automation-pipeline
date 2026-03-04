# Changelog

### Account Memo Changes

- **after_hours_flow_summary** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-After hours we have a simple rotation: one tech is on call each week. Right now callers leave a voicemail, and the on-call tech has to listen to all of them. With Clara we’d like the on-call tech to get a much clearer summary of what’s going on.
+After hours, Clara needs to decide if it is an emergency based on that definition. For emergencies, collect full details and then transfer to the on‑call technician. If the transfer rings longer than 60 seconds, cancel the transfer, return to the caller, apologize, and confirm that the tech will call back as soon as they receive the page. For non‑emergency calls after hours, log all the information and let the caller know that the office will follow up during the next business day.
```

- **business_hours** changed:
```diff
--- v1
+++ v2
@@ -9,5 +9,5 @@
   "start": "07:00",
   "end": "15:30",
   "timezone": "PT",
-  "raw": "Office hours are Monday through Friday, 7:00 AM to 3:30 PM Pacific. Most inspection scheduling calls are non-urgent and can go to voicemail, but we’d like Clara to grab the basics and propose a callback during office hours."
+  "raw": "Mon–Fri 7:00 AM–3:30 PM PT"
 }
```

- **call_transfer_rules** changed:
```diff
--- v1
+++ v2
@@ -1,5 +1,5 @@
 {
-  "raw": "",
+  "raw": "For qualifying fire protection emergencies, transfer to the on-call technician. If the transfer rings longer than 60 seconds, go back to the caller, apologize, and confirm details for dispatch.",
   "timeout_seconds": null,
   "retries": null,
   "what_to_say_if_fails": ""
```

- **emergency_routing_rules** changed:
```diff
--- v1
+++ v2
@@ -1,4 +1,7 @@
 {
-  "raw": "",
-  "steps": []
+  "raw": "After hours, Clara needs to decide if it is an emergency based on that definition. For emergencies, collect full details and then transfer to the on‑call technician. If the transfer rings longer than 60 seconds, cancel the transfer, return to the caller, apologize, and confirm that the tech will call back as soon as they receive the page. For non‑emergency calls after hours, log all the information and let the caller know that the office will follow up during the next business day.",
+  "steps": [
+    "After hours, Clara needs to decide if it is an emergency based on that definition. For emergencies, collect full details and then transfer to the on‑call technician. If the transfer rings longer than 60 seconds, cancel the transfer, return to the caller, apologize, and confirm that the tech will call back as soon as they receive the page.",
+    "For non‑emergency calls after hours, log all the information and let the caller know that the office will follow up during the next business day."
+  ]
 }
```

- **integration_constraints** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-We use ServiceTrade too, but we do not want Clara to create jobs automatically yet.
+ServiceTrade is required for all work. Clara should not create or modify jobs directly.
```

- **notes** changed:
```diff
--- v1
+++ v2
@@ -1 +1,5 @@
-[]
+[
+  "Structured form override for 'business_hours': 'raw' overridden: previous='Our business hours are Monday through Friday, 7:00 AM to 3:30 PM Pacific Time. After that we switch to an on‑call rotation.', new='Mon–Fri 7:00 AM–3:30 PM PT'.",
+  "Structured form override for 'call_transfer_rules': 'raw' overridden: previous='During business hours, Clara should gather caller name, callback number, building name, and address. If the call is about inspections or testing, taking a message and putting it in the inspection work queue is fine. If the call is about a known system impairment, Clara should flag it as high priority and transfer to the coordinator.', new='For qualifying fire protection emergencies, transfer to the on-call technician. If the transfer rings longer than 60 seconds, go back to the caller, apologize, and confirm details for dispatch.'.",
+  "Structured form override for 'integration_constraints': previous value='We use ServiceTrade for all fire protection work. Clara must never create jobs or change schedules in ServiceTrade; only capture information for our staff.', new value='ServiceTrade is required for all work. Clara should not create or modify jobs directly.'."
+]
```

- **office_hours_flow_summary** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-Office hours are Monday through Friday, 7:00 AM to 3:30 PM Pacific. Most inspection scheduling calls are non-urgent and can go to voicemail, but we’d like Clara to grab the basics and propose a callback during office hours.
+During business hours, Clara should gather caller name, callback number, building name, and address. If the call is about inspections or testing, taking a message and putting it in the inspection work queue is fine. If the call is about a known system impairment, Clara should flag it as high priority and transfer to the coordinator.
```

- **questions_or_unknowns** changed:
```diff
--- v1
+++ v2
@@ -2,7 +2,5 @@
   "Missing office address (not found or unclear in transcript).",
   "Missing services supported (not found or unclear in transcript).",
   "Missing emergency definition (not found or unclear in transcript).",
-  "Missing emergency routing rules (not found or unclear in transcript).",
-  "Missing non-emergency routing rules (not found or unclear in transcript).",
-  "Missing call transfer rules (not found or unclear in transcript)."
+  "Missing non-emergency routing rules (not found or unclear in transcript)."
 ]
```

### Agent Spec Changes

- **agent_name** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-SafeFlow Fire Protection – Clara Answers Agent v1
+SafeFlow Fire Protection – Clara Answers Agent v2
```

- **call_transfer_protocol** changed:
```diff
--- v1
+++ v2
@@ -1,5 +1,5 @@
 {
-  "raw": "",
+  "raw": "For qualifying fire protection emergencies, transfer to the on-call technician. If the transfer rings longer than 60 seconds, go back to the caller, apologize, and confirm details for dispatch.",
   "timeout_seconds": null,
   "retries": null,
   "what_to_say_if_fails": ""
```

- **key_variables** changed:
```diff
--- v1
+++ v2
@@ -12,12 +12,15 @@
     "start": "07:00",
     "end": "15:30",
     "timezone": "PT",
-    "raw": "Office hours are Monday through Friday, 7:00 AM to 3:30 PM Pacific. Most inspection scheduling calls are non-urgent and can go to voicemail, but we’d like Clara to grab the basics and propose a callback during office hours."
+    "raw": "Mon–Fri 7:00 AM–3:30 PM PT"
   },
   "office_address": "",
   "timezone": "PT",
   "emergency_routing": {
-    "raw": "",
-    "steps": []
+    "raw": "After hours, Clara needs to decide if it is an emergency based on that definition. For emergencies, collect full details and then transfer to the on‑call technician. If the transfer rings longer than 60 seconds, cancel the transfer, return to the caller, apologize, and confirm that the tech will call back as soon as they receive the page. For non‑emergency calls after hours, log all the information and let the caller know that the office will follow up during the next business day.",
+    "steps": [
+      "After hours, Clara needs to decide if it is an emergency based on that definition. For emergencies, collect full details and then transfer to the on‑call technician. If the transfer rings longer than 60 seconds, cancel the transfer, return to the caller, apologize, and confirm that the tech will call back as soon as they receive the page.",
+      "For non‑emergency calls after hours, log all the information and let the caller know that the office will follow up during the next business day."
+    ]
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
-Office hours are Monday through Friday, 7:00 AM to 3:30 PM Pacific. Most inspection scheduling calls are non-urgent and can go to voicemail, but we’d like Clara to grab the basics and propose a callback during office hours.
+Mon–Fri 7:00 AM–3:30 PM PT
 During business hours, follow **exactly** this sequence. Do not skip steps, and do not add new ones:
 1. Greeting: Greet the caller on behalf of the business and state that you are an AI assistant.
 2. Ask purpose: Ask the caller for the reason for their call.
 3. Collect name and number: Collect the caller's name and callback phone number early in the call.
 4. Determine routing: Based only on the rules below and the memo:
-   - Office-hours flow summary: Office hours are Monday through Friday, 7:00 AM to 3:30 PM Pacific. Most inspection scheduling calls are non-urgent and can go to voicemail, but we’d like Clara to grab the basics and propose a callback during office hours.
+   - Office-hours flow summary: During business hours, Clara should gather caller name, callback number, building name, and address. If the call is about inspections or testing, taking a message and putting it in the inspection work queue is fine. If the call is about a known system impairment, Clara should flag it as high priority and transfer to the coordinator.
    - Do not guess routes that are not specified.
 5. Transfer or route: If routing requires a live person, follow the transfer protocol section.
 6. Fallback if transfer fails: If the transfer fails, drops, or no one answers, follow the 'Transfer Failure Handling' section.
@@ -17,7 +17,7 @@
 
 === After-Hours Call Flow ===
 After-hours flow description:
-After hours we have a simple rotation: one tech is on call each week. Right now callers leave a voicemail, and the on-call tech has to listen to all of them. With Clara we’d like the on-call tech to get a much clearer summary of what’s going on.
+After hours, Clara needs to decide if it is an emergency based on that definition. For emergencies, collect full details and then transfer to the on‑call technician. If the transfer rings longer than 60 seconds, cancel the transfer, return to the caller, apologize, and confirm that the tech will call back as soon as they receive the page. For non‑emergency calls after hours, log all the information and let the caller know that the office will follow up during the next business day.
 During after-hours, follow **exactly** this sequence. Do not skip steps, and do not add new ones:
 1. Greeting: Greet the caller on behalf of the business and clarify that it is after hours.
 2. Ask purpose: Ask the caller for the reason for their call.
@@ -35,10 +35,7 @@
 Definition / examples of emergencies:
 [UNKNOWN: emergency definition – if caller asks, say you do not have this information yet and collect it for a human follow-up.]
 Routing rules for emergencies:
-{
-  "raw": "",
-  "steps": []
-}
+After hours, Clara needs to decide if it is an emergency based on that definition. For emergencies, collect full details and then transfer to the on‑call technician. If the transfer rings longer than 60 seconds, cancel the transfer, return to the caller, apologize, and confirm that the tech will call back as soon as they receive the page. For non‑emergency calls after hours, log all the information and let the caller know that the office will follow up during the next business day.
 Routing rules for non-emergencies:
 {
   "raw": "",
@@ -46,12 +43,7 @@
 }
 
 === Call Transfer Protocol ===
-{
-  "raw": "",
-  "timeout_seconds": null,
-  "retries": null,
-  "what_to_say_if_fails": ""
-}
+For qualifying fire protection emergencies, transfer to the on-call technician. If the transfer rings longer than 60 seconds, go back to the caller, apologize, and confirm details for dispatch.
 If you initiate a transfer, clearly tell the caller who you are transferring to and why.
 
 === Transfer Failure Handling ===
@@ -75,6 +67,4 @@
 - Missing office address (not found or unclear in transcript).
 - Missing services supported (not found or unclear in transcript).
 - Missing emergency definition (not found or unclear in transcript).
-- Missing emergency routing rules (not found or unclear in transcript).
 - Missing non-emergency routing rules (not found or unclear in transcript).
-- Missing call transfer rules (not found or unclear in transcript).
```

- **version** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-v1
+v2
```

# Changelog

### Account Memo Changes

- **after_hours_flow_summary** changed:
```diff
--- v1
+++ v2
@@ -0,0 +1 @@
+After hours, if the issue matches that emergency definition, Clara should collect full details and attempt to reach the on‑call electrician. If no one answers within 60 seconds, Clara must go back to the caller, apologize, and clearly state that the on‑call electrician will return their call as soon as possible. Non‑emergency calls after hours should still be logged with the same information, but Clara should promise only a next‑business‑day callback.
```

- **business_hours** changed:
```diff
--- v1
+++ v2
@@ -9,5 +9,5 @@
   "start": "08:00",
   "end": "16:00",
   "timezone": "MT",
-  "raw": "During the day we’re open from 8 AM to 4 PM Mountain Time, Monday to Friday. Calls should be answered, basic info taken, and then routed to whichever estimator or journeyman is handling that customer."
+  "raw": "Mon–Fri 8:00 AM–4:00 PM MT"
 }
```

- **call_transfer_rules** changed:
```diff
--- v1
+++ v2
@@ -1,5 +1,5 @@
 {
-  "raw": "",
+  "raw": "For emergencies transfer to the on-call electrician. If there is no answer within 60 seconds, return to the caller, apologize, and confirm that the on-call will call back as soon as possible.",
   "timeout_seconds": null,
   "retries": null,
   "what_to_say_if_fails": ""
```

- **emergency_definition** changed:
```diff
--- v1
+++ v2
@@ -1,6 +1,3 @@
 [
-  "any situation with visible arcing",
-  "burning smell from an electrical panel",
-  "main power out to an entire building",
-  "anything the fire department tells them is unsafe"
+  "unsafe"
 ]
```

- **emergency_routing_rules** changed:
```diff
--- v1
+++ v2
@@ -1,6 +1,7 @@
 {
-  "raw": "We do small commercial electrical service work: panel issues, breaker trips, outlet problems, and lighting repairs. The reason we’re interested in Clara is to make sure after-hours emergency calls don’t go to voicemail.",
+  "raw": "After hours, if the issue matches that emergency definition, Clara should collect full details and attempt to reach the on‑call electrician. If no one answers within 60 seconds, Clara must go back to the caller, apologize, and clearly state that the on‑call electrician will return their call as soon as possible. Non‑emergency calls after hours should still be logged with the same information, but Clara should promise only a next‑business‑day callback.",
   "steps": [
-    "We do small commercial electrical service work: panel issues, breaker trips, outlet problems, and lighting repairs. The reason we’re interested in Clara is to make sure after-hours emergency calls don’t go to voicemail."
+    "After hours, if the issue matches that emergency definition, Clara should collect full details and attempt to reach the on‑call electrician. If no one answers within 60 seconds, Clara must go back to the caller, apologize, and clearly state that the on‑call electrician will return their call as soon as possible.",
+    "Non‑emergency calls after hours should still be logged with the same information, but Clara should promise only a next‑business‑day callback."
   ]
 }
```

- **integration_constraints** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-We don’t have any fancy integrations yet. Everything gets written down and later entered into QuickBooks and our shared calendar.
+QuickBooks and internal calendar only. Clara cannot book appointments or create jobs directly.
```

- **notes** changed:
```diff
--- v1
+++ v2
@@ -1 +1,5 @@
-[]
+[
+  "Structured form override for 'business_hours': 'raw' overridden: previous='Confirming hours: we are open Monday through Friday, 8:00 AM to 4:00 PM Mountain Time. We do not run a weekend office.', new='Mon–Fri 8:00 AM–4:00 PM MT'.",
+  "Structured form override for 'call_transfer_rules': 'raw' overridden: previous='During business hours Clara should capture the caller name, company, callback number, and service address. If the reason is panel issues, repeated breaker trips, or building-wide outages, the call should be transferred to the service lead. For simple outlet or lighting issues, taking a message is fine.', new='For emergencies transfer to the on-call electrician. If there is no answer within 60 seconds, return to the caller, apologize, and confirm that the on-call will call back as soon as possible.'.",
+  "Structured form override for 'integration_constraints': previous value='We use QuickBooks and a shared calendar internally. Clara should not promise appointment times or say that a job has been booked; just that our office will schedule and confirm.', new value='QuickBooks and internal calendar only. Clara cannot book appointments or create jobs directly.'."
+]
```

- **office_hours_flow_summary** changed:
```diff
--- v1
+++ v2
@@ -0,0 +1 @@
+During business hours Clara should capture the caller name, company, callback number, and service address. If the reason is panel issues, repeated breaker trips, or building-wide outages, the call should be transferred to the service lead. For simple outlet or lighting issues, taking a message is fine.
```

- **questions_or_unknowns** changed:
```diff
--- v1
+++ v2
@@ -1,8 +1,5 @@
 [
   "Missing office address (not found or unclear in transcript).",
   "Missing services supported (not found or unclear in transcript).",
-  "Missing non-emergency routing rules (not found or unclear in transcript).",
-  "Missing call transfer rules (not found or unclear in transcript).",
-  "Missing after-hours flow summary (not found or unclear in transcript).",
-  "Missing office-hours flow summary (not found or unclear in transcript)."
+  "Missing non-emergency routing rules (not found or unclear in transcript)."
 ]
```

### Agent Spec Changes

- **agent_name** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-Prime Electric Service – Clara Answers Agent v1
+Prime Electric Service – Clara Answers Agent v2
```

- **call_transfer_protocol** changed:
```diff
--- v1
+++ v2
@@ -1,5 +1,5 @@
 {
-  "raw": "",
+  "raw": "For emergencies transfer to the on-call electrician. If there is no answer within 60 seconds, return to the caller, apologize, and confirm that the on-call will call back as soon as possible.",
   "timeout_seconds": null,
   "retries": null,
   "what_to_say_if_fails": ""
```

- **key_variables** changed:
```diff
--- v1
+++ v2
@@ -12,14 +12,15 @@
     "start": "08:00",
     "end": "16:00",
     "timezone": "MT",
-    "raw": "During the day we’re open from 8 AM to 4 PM Mountain Time, Monday to Friday. Calls should be answered, basic info taken, and then routed to whichever estimator or journeyman is handling that customer."
+    "raw": "Mon–Fri 8:00 AM–4:00 PM MT"
   },
   "office_address": "",
   "timezone": "MT",
   "emergency_routing": {
-    "raw": "We do small commercial electrical service work: panel issues, breaker trips, outlet problems, and lighting repairs. The reason we’re interested in Clara is to make sure after-hours emergency calls don’t go to voicemail.",
+    "raw": "After hours, if the issue matches that emergency definition, Clara should collect full details and attempt to reach the on‑call electrician. If no one answers within 60 seconds, Clara must go back to the caller, apologize, and clearly state that the on‑call electrician will return their call as soon as possible. Non‑emergency calls after hours should still be logged with the same information, but Clara should promise only a next‑business‑day callback.",
     "steps": [
-      "We do small commercial electrical service work: panel issues, breaker trips, outlet problems, and lighting repairs. The reason we’re interested in Clara is to make sure after-hours emergency calls don’t go to voicemail."
+      "After hours, if the issue matches that emergency definition, Clara should collect full details and attempt to reach the on‑call electrician. If no one answers within 60 seconds, Clara must go back to the caller, apologize, and clearly state that the on‑call electrician will return their call as soon as possible.",
+      "Non‑emergency calls after hours should still be logged with the same information, but Clara should promise only a next‑business‑day callback."
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
-During the day we’re open from 8 AM to 4 PM Mountain Time, Monday to Friday. Calls should be answered, basic info taken, and then routed to whichever estimator or journeyman is handling that customer.
+Mon–Fri 8:00 AM–4:00 PM MT
 During business hours, follow **exactly** this sequence. Do not skip steps, and do not add new ones:
 1. Greeting: Greet the caller on behalf of the business and state that you are an AI assistant.
 2. Ask purpose: Ask the caller for the reason for their call.
 3. Collect name and number: Collect the caller's name and callback phone number early in the call.
 4. Determine routing: Based only on the rules below and the memo:
-   - Office-hours flow summary: [UNKNOWN: office hours call flow summary – if caller asks, say you do not have this information yet and collect it for a human follow-up.]
+   - Office-hours flow summary: During business hours Clara should capture the caller name, company, callback number, and service address. If the reason is panel issues, repeated breaker trips, or building-wide outages, the call should be transferred to the service lead. For simple outlet or lighting issues, taking a message is fine.
    - Do not guess routes that are not specified.
 5. Transfer or route: If routing requires a live person, follow the transfer protocol section.
 6. Fallback if transfer fails: If the transfer fails, drops, or no one answers, follow the 'Transfer Failure Handling' section.
@@ -17,7 +17,7 @@
 
 === After-Hours Call Flow ===
 After-hours flow description:
-[UNKNOWN: after-hours flow summary – if caller asks, say you do not have this information yet and collect it for a human follow-up.]
+After hours, if the issue matches that emergency definition, Clara should collect full details and attempt to reach the on‑call electrician. If no one answers within 60 seconds, Clara must go back to the caller, apologize, and clearly state that the on‑call electrician will return their call as soon as possible. Non‑emergency calls after hours should still be logged with the same information, but Clara should promise only a next‑business‑day callback.
 During after-hours, follow **exactly** this sequence. Do not skip steps, and do not add new ones:
 1. Greeting: Greet the caller on behalf of the business and clarify that it is after hours.
 2. Ask purpose: Ask the caller for the reason for their call.
@@ -33,12 +33,9 @@
 
 === Emergency Handling ===
 Definition / examples of emergencies:
-- any situation with visible arcing
-- burning smell from an electrical panel
-- main power out to an entire building
-- anything the fire department tells them is unsafe
+- unsafe
 Routing rules for emergencies:
-We do small commercial electrical service work: panel issues, breaker trips, outlet problems, and lighting repairs. The reason we’re interested in Clara is to make sure after-hours emergency calls don’t go to voicemail.
+After hours, if the issue matches that emergency definition, Clara should collect full details and attempt to reach the on‑call electrician. If no one answers within 60 seconds, Clara must go back to the caller, apologize, and clearly state that the on‑call electrician will return their call as soon as possible. Non‑emergency calls after hours should still be logged with the same information, but Clara should promise only a next‑business‑day callback.
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
+For emergencies transfer to the on-call electrician. If there is no answer within 60 seconds, return to the caller, apologize, and confirm that the on-call will call back as soon as possible.
 If you initiate a transfer, clearly tell the caller who you are transferring to and why.
 
 === Transfer Failure Handling ===
@@ -75,6 +67,3 @@
 - Missing office address (not found or unclear in transcript).
 - Missing services supported (not found or unclear in transcript).
 - Missing non-emergency routing rules (not found or unclear in transcript).
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

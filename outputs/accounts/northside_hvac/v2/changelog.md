# Changelog

### Account Memo Changes

- **after_hours_flow_summary** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-After hours today we have a basic answering service. They take a message and then text our on-call tech, but they almost never ask enough questions. We want Clara to do a better job collecting details and confirming whether it is truly urgent.
+To lock this in: business hours are Monday through Friday, 7:30 AM to 5:00 PM Central Time. Outside those hours we treat everything as after hours. After hours, for true emergencies Clara should confirm that definition, then take full details and attempt to transfer to the on‑call dispatcher. If no one answers within 45 seconds, return to the caller, apologize, and confirm that a tech will call back as soon as possible. For non‑emergency calls after hours, collect the details and clearly state that our office will follow up during business hours.
```

- **business_hours** changed:
```diff
--- v1
+++ v2
@@ -9,5 +9,5 @@
   "start": "07:30",
   "end": "17:00",
   "timezone": "CT",
-  "raw": "Business hours are Monday to Friday, 7:30 AM to 5:00 PM Central. During those hours, calls should go to the dispatcher if possible, otherwise to any available coordinator."
+  "raw": "Mon–Fri 7:30 AM–5:00 PM CT"
 }
```

- **call_transfer_rules** changed:
```diff
--- v1
+++ v2
@@ -1,5 +1,5 @@
 {
-  "raw": "",
+  "raw": "During business hours transfer emergency unit-down calls to the dispatcher queue. After hours transfer emergencies to the on-call dispatcher; if no answer within 45 seconds, return to caller, apologize, and take a full message.",
   "timeout_seconds": null,
   "retries": null,
   "what_to_say_if_fails": ""
```

- **emergency_routing_rules** changed:
```diff
--- v1
+++ v2
@@ -1,6 +1,7 @@
 {
-  "raw": "We handle commercial HVAC maintenance and emergency calls for office buildings and small retail. Most of our pain is that the receptionist can only take one call at a time, so overflow callers hang up.",
+  "raw": "After hours, for true emergencies Clara should confirm that definition, then take full details and attempt to transfer to the on‑call dispatcher. If no one answers within 45 seconds, return to the caller, apologize, and confirm that a tech will call back as soon as possible. For non‑emergency calls after hours, collect the details and clearly state that our office will follow up during business hours.",
   "steps": [
-    "We handle commercial HVAC maintenance and emergency calls for office buildings and small retail. Most of our pain is that the receptionist can only take one call at a time, so overflow callers hang up."
+    "After hours, for true emergencies Clara should confirm that definition, then take full details and attempt to transfer to the on‑call dispatcher. If no one answers within 45 seconds, return to the caller, apologize, and confirm that a tech will call back as soon as possible.",
+    "For non‑emergency calls after hours, collect the details and clearly state that our office will follow up during business hours."
   ]
 }
```

- **integration_constraints** changed:
```diff
--- v1
+++ v2
@@ -0,0 +1 @@
+Internal HVAC ticketing system only; Clara should not log into or modify any external systems.
```

- **notes** changed:
```diff
--- v1
+++ v2
@@ -1 +1,4 @@
-[]
+[
+  "Structured form override for 'business_hours': 'raw' overridden: previous='To lock this in: business hours are Monday through Friday, 7:30 AM to 5:00 PM Central Time. Outside those hours we treat everything as after hours.', new='Mon–Fri 7:30 AM–5:00 PM CT'.",
+  "Structured form override for 'call_transfer_rules': 'raw' overridden: previous='During business hours, Clara should always collect caller name, callback number, company name, and site address. If the reason is a unit down, no heating, or no cooling, transfer to the dispatcher queue. If the issue is routine maintenance or filter changes, just take a message for the coordinators.', new='During business hours transfer emergency unit-down calls to the dispatcher queue. After hours transfer emergencies to the on-call dispatcher; if no answer within 45 seconds, return to caller, apologize, and take a full message.'."
+]
```

- **office_hours_flow_summary** changed:
```diff
--- v1
+++ v2
@@ -0,0 +1 @@
+During business hours, Clara should always collect caller name, callback number, company name, and site address. If the reason is a unit down, no heating, or no cooling, transfer to the dispatcher queue. If the issue is routine maintenance or filter changes, just take a message for the coordinators. For non‑emergency calls after hours, collect the details and clearly state that our office will follow up during business hours.
```

- **questions_or_unknowns** changed:
```diff
--- v1
+++ v2
@@ -1,7 +1,5 @@
 [
   "Missing office address (not found or unclear in transcript).",
   "Missing non-emergency routing rules (not found or unclear in transcript).",
-  "Missing call transfer rules (not found or unclear in transcript).",
-  "Missing integration constraints (not found or unclear in transcript).",
-  "Missing office-hours flow summary (not found or unclear in transcript)."
+  "Missing integration constraints (not found or unclear in transcript)."
 ]
```

### Agent Spec Changes

- **agent_name** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-Northside HVAC & Cooling – Clara Answers Agent v1
+Northside HVAC & Cooling – Clara Answers Agent v2
```

- **call_transfer_protocol** changed:
```diff
--- v1
+++ v2
@@ -1,5 +1,5 @@
 {
-  "raw": "",
+  "raw": "During business hours transfer emergency unit-down calls to the dispatcher queue. After hours transfer emergencies to the on-call dispatcher; if no answer within 45 seconds, return to caller, apologize, and take a full message.",
   "timeout_seconds": null,
   "retries": null,
   "what_to_say_if_fails": ""
```

- **key_variables** changed:
```diff
--- v1
+++ v2
@@ -12,14 +12,15 @@
     "start": "07:30",
     "end": "17:00",
     "timezone": "CT",
-    "raw": "Business hours are Monday to Friday, 7:30 AM to 5:00 PM Central. During those hours, calls should go to the dispatcher if possible, otherwise to any available coordinator."
+    "raw": "Mon–Fri 7:30 AM–5:00 PM CT"
   },
   "office_address": "",
   "timezone": "CT",
   "emergency_routing": {
-    "raw": "We handle commercial HVAC maintenance and emergency calls for office buildings and small retail. Most of our pain is that the receptionist can only take one call at a time, so overflow callers hang up.",
+    "raw": "After hours, for true emergencies Clara should confirm that definition, then take full details and attempt to transfer to the on‑call dispatcher. If no one answers within 45 seconds, return to the caller, apologize, and confirm that a tech will call back as soon as possible. For non‑emergency calls after hours, collect the details and clearly state that our office will follow up during business hours.",
     "steps": [
-      "We handle commercial HVAC maintenance and emergency calls for office buildings and small retail. Most of our pain is that the receptionist can only take one call at a time, so overflow callers hang up."
+      "After hours, for true emergencies Clara should confirm that definition, then take full details and attempt to transfer to the on‑call dispatcher. If no one answers within 45 seconds, return to the caller, apologize, and confirm that a tech will call back as soon as possible.",
+      "For non‑emergency calls after hours, collect the details and clearly state that our office will follow up during business hours."
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
-Business hours are Monday to Friday, 7:30 AM to 5:00 PM Central. During those hours, calls should go to the dispatcher if possible, otherwise to any available coordinator.
+Mon–Fri 7:30 AM–5:00 PM CT
 During business hours, follow **exactly** this sequence. Do not skip steps, and do not add new ones:
 1. Greeting: Greet the caller on behalf of the business and state that you are an AI assistant.
 2. Ask purpose: Ask the caller for the reason for their call.
 3. Collect name and number: Collect the caller's name and callback phone number early in the call.
 4. Determine routing: Based only on the rules below and the memo:
-   - Office-hours flow summary: [UNKNOWN: office hours call flow summary – if caller asks, say you do not have this information yet and collect it for a human follow-up.]
+   - Office-hours flow summary: During business hours, Clara should always collect caller name, callback number, company name, and site address. If the reason is a unit down, no heating, or no cooling, transfer to the dispatcher queue. If the issue is routine maintenance or filter changes, just take a message for the coordinators. For non‑emergency calls after hours, collect the details and clearly state that our office will follow up during business hours.
    - Do not guess routes that are not specified.
 5. Transfer or route: If routing requires a live person, follow the transfer protocol section.
 6. Fallback if transfer fails: If the transfer fails, drops, or no one answers, follow the 'Transfer Failure Handling' section.
@@ -17,7 +17,7 @@
 
 === After-Hours Call Flow ===
 After-hours flow description:
-After hours today we have a basic answering service. They take a message and then text our on-call tech, but they almost never ask enough questions. We want Clara to do a better job collecting details and confirming whether it is truly urgent.
+To lock this in: business hours are Monday through Friday, 7:30 AM to 5:00 PM Central Time. Outside those hours we treat everything as after hours. After hours, for true emergencies Clara should confirm that definition, then take full details and attempt to transfer to the on‑call dispatcher. If no one answers within 45 seconds, return to the caller, apologize, and confirm that a tech will call back as soon as possible. For non‑emergency calls after hours, collect the details and clearly state that our office will follow up during business hours.
 During after-hours, follow **exactly** this sequence. Do not skip steps, and do not add new ones:
 1. Greeting: Greet the caller on behalf of the business and clarify that it is after hours.
 2. Ask purpose: Ask the caller for the reason for their call.
@@ -37,7 +37,7 @@
 - loss of cooling in a critical area like a server room
 - medical space
 Routing rules for emergencies:
-We handle commercial HVAC maintenance and emergency calls for office buildings and small retail. Most of our pain is that the receptionist can only take one call at a time, so overflow callers hang up.
+After hours, for true emergencies Clara should confirm that definition, then take full details and attempt to transfer to the on‑call dispatcher. If no one answers within 45 seconds, return to the caller, apologize, and confirm that a tech will call back as soon as possible. For non‑emergency calls after hours, collect the details and clearly state that our office will follow up during business hours.
 Routing rules for non-emergencies:
 {
   "raw": "",
@@ -45,12 +45,7 @@
 }
 
 === Call Transfer Protocol ===
-{
-  "raw": "",
-  "timeout_seconds": null,
-  "retries": null,
-  "what_to_say_if_fails": ""
-}
+During business hours transfer emergency unit-down calls to the dispatcher queue. After hours transfer emergencies to the on-call dispatcher; if no answer within 45 seconds, return to caller, apologize, and take a full message.
 If you initiate a transfer, clearly tell the caller who you are transferring to and why.
 
 === Transfer Failure Handling ===
@@ -73,6 +68,4 @@
 The following items are not yet clearly defined from the account materials. If they come up, collect information and flag for human review, and do NOT guess:
 - Missing office address (not found or unclear in transcript).
 - Missing non-emergency routing rules (not found or unclear in transcript).
-- Missing call transfer rules (not found or unclear in transcript).
 - Missing integration constraints (not found or unclear in transcript).
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

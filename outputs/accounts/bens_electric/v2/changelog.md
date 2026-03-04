# Changelog

### Account Memo Changes

- **after_hours_flow_summary** changed:
```diff
--- v1
+++ v2
@@ -0,0 +1 @@
+After hours, first confirm if this is an emergency. Non-emergency calls after hours should be collected and followed up during the next business day.
```

- **business_hours** changed:
```diff
--- v1
+++ v2
@@ -8,6 +8,6 @@
   ],
   "start": "08:00",
   "end": "17:00",
-  "timezone": "",
-  "raw": "We are open Monday to Friday 8am to 5pm."
+  "timezone": "PT",
+  "raw": "Mon–Fri 8:00 AM–5:00 PM PT"
 }
```

- **call_transfer_rules** changed:
```diff
--- v1
+++ v2
@@ -1,6 +1,6 @@
 {
-  "raw": "transfer the call to dispatch.",
-  "timeout_seconds": null,
+  "raw": "For emergencies, transfer to dispatch phone tree. If transfer does not connect within 60 seconds, return to caller, take a message (name, callback number, service address), and notify dispatch.",
+  "timeout_seconds": 60,
   "retries": null,
   "what_to_say_if_fails": ""
 }
```

- **emergency_definition** changed:
```diff
--- v1
+++ v2
@@ -1 +1,6 @@
-[]
+[
+  "any electrical issue that causes sparking",
+  "burning smell",
+  "loss of power to critical systems",
+  "immediate safety risk"
+]
```

- **emergency_routing_rules** changed:
```diff
--- v1
+++ v2
@@ -1,7 +1,6 @@
 {
-  "raw": "If it's an emergency, transfer the call to dispatch. Transfer the call to dispatch for emergencies.",
+  "raw": "All emergencies should be transferred to the phone tree for dispatch.",
   "steps": [
-    "If it's an emergency, transfer the call to dispatch.",
-    "Transfer the call to dispatch for emergencies."
+    "All emergencies should be transferred to the phone tree for dispatch."
   ]
 }
```

- **integration_constraints** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-We use ServiceTrade for job management, but we cannot create jobs automatically yet.
+ServiceTrade is used. Do not create sprinkler jobs in ServiceTrade. Automation should only capture details and hand off to humans unless explicitly enabled.
```

- **non_emergency_routing_rules** changed:
```diff
--- v1
+++ v2
@@ -1,4 +1,6 @@
 {
-  "raw": "",
-  "steps": []
+  "raw": "Non-emergency calls after hours should be collected and followed up during the next business day.",
+  "steps": [
+    "Non-emergency calls after hours should be collected and followed up during the next business day."
+  ]
 }
```

- **notes** changed:
```diff
--- v1
+++ v2
@@ -1 +1,5 @@
-[]
+[
+  "Structured form override for 'business_hours': 'raw' overridden: previous='Business hours are Monday through Friday, 8:00 AM to 5:00 PM, Pacific Time.', new='Mon–Fri 8:00 AM–5:00 PM PT'.",
+  "Structured form override for 'call_transfer_rules': 'raw' overridden: previous='If the transfer fails after 60 seconds, notify dispatch and take a message with caller name, callback number, and service address.', new='For emergencies, transfer to dispatch phone tree. If transfer does not connect within 60 seconds, return to caller, take a message (name, callback number, service address), and notify dispatch.'.",
+  "Structured form override for 'integration_constraints': previous value='Never create sprinkler jobs in ServiceTrade.', new value='ServiceTrade is used. Do not create sprinkler jobs in ServiceTrade. Automation should only capture details and hand off to humans unless explicitly enabled.'."
+]
```

- **questions_or_unknowns** changed:
```diff
--- v1
+++ v2
@@ -1,8 +1,4 @@
 [
-  "Business hours timezone missing or unclear.",
   "Missing office address (not found or unclear in transcript).",
-  "Missing services supported (not found or unclear in transcript).",
-  "Missing emergency definition (not found or unclear in transcript).",
-  "Missing non-emergency routing rules (not found or unclear in transcript).",
-  "Missing after-hours flow summary (not found or unclear in transcript)."
+  "Missing services supported (not found or unclear in transcript)."
 ]
```

### Agent Spec Changes

- **agent_name** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-Ben's Electric – Clara Answers Agent v1
+Ben's Electric – Clara Answers Agent v2
```

- **call_transfer_protocol** changed:
```diff
--- v1
+++ v2
@@ -1,6 +1,6 @@
 {
-  "raw": "transfer the call to dispatch.",
-  "timeout_seconds": null,
+  "raw": "For emergencies, transfer to dispatch phone tree. If transfer does not connect within 60 seconds, return to caller, take a message (name, callback number, service address), and notify dispatch.",
+  "timeout_seconds": 60,
   "retries": null,
   "what_to_say_if_fails": ""
 }
```

- **key_variables** changed:
```diff
--- v1
+++ v2
@@ -11,16 +11,15 @@
     ],
     "start": "08:00",
     "end": "17:00",
-    "timezone": "",
-    "raw": "We are open Monday to Friday 8am to 5pm."
+    "timezone": "PT",
+    "raw": "Mon–Fri 8:00 AM–5:00 PM PT"
   },
   "office_address": "",
-  "timezone": "",
+  "timezone": "PT",
   "emergency_routing": {
-    "raw": "If it's an emergency, transfer the call to dispatch. Transfer the call to dispatch for emergencies.",
+    "raw": "All emergencies should be transferred to the phone tree for dispatch.",
     "steps": [
-      "If it's an emergency, transfer the call to dispatch.",
-      "Transfer the call to dispatch for emergencies."
+      "All emergencies should be transferred to the phone tree for dispatch."
     ]
   }
 }
```

- **system_prompt** changed:
```diff
--- v1
+++ v2
@@ -2,7 +2,7 @@
 
 === Business Hours Call Flow ===
 Business hours description:
-We are open Monday to Friday 8am to 5pm.
+Mon–Fri 8:00 AM–5:00 PM PT
 During business hours, follow **exactly** this sequence. Do not skip steps, and do not add new ones:
 1. Greeting: Greet the caller on behalf of the business and state that you are an AI assistant.
 2. Ask purpose: Ask the caller for the reason for their call.
@@ -17,7 +17,7 @@
 
 === After-Hours Call Flow ===
 After-hours flow description:
-[UNKNOWN: after-hours flow summary – if caller asks, say you do not have this information yet and collect it for a human follow-up.]
+After hours, first confirm if this is an emergency. Non-emergency calls after hours should be collected and followed up during the next business day.
 During after-hours, follow **exactly** this sequence. Do not skip steps, and do not add new ones:
 1. Greeting: Greet the caller on behalf of the business and clarify that it is after hours.
 2. Ask purpose: Ask the caller for the reason for their call.
@@ -33,17 +33,17 @@
 
 === Emergency Handling ===
 Definition / examples of emergencies:
-[UNKNOWN: emergency definition – if caller asks, say you do not have this information yet and collect it for a human follow-up.]
+- any electrical issue that causes sparking
+- burning smell
+- loss of power to critical systems
+- immediate safety risk
 Routing rules for emergencies:
-If it's an emergency, transfer the call to dispatch. Transfer the call to dispatch for emergencies.
+All emergencies should be transferred to the phone tree for dispatch.
 Routing rules for non-emergencies:
-{
-  "raw": "",
-  "steps": []
-}
+Non-emergency calls after hours should be collected and followed up during the next business day.
 
 === Call Transfer Protocol ===
-transfer the call to dispatch.
+For emergencies, transfer to dispatch phone tree. If transfer does not connect within 60 seconds, return to caller, take a message (name, callback number, service address), and notify dispatch.
 If you initiate a transfer, clearly tell the caller who you are transferring to and why.
 
 === Transfer Failure Handling ===
@@ -64,9 +64,5 @@
 
 === Known Questions or Unknowns ===
 The following items are not yet clearly defined from the account materials. If they come up, collect information and flag for human review, and do NOT guess:
-- Business hours timezone missing or unclear.
 - Missing office address (not found or unclear in transcript).
 - Missing services supported (not found or unclear in transcript).
-- Missing emergency definition (not found or unclear in transcript).
-- Missing non-emergency routing rules (not found or unclear in transcript).
-- Missing after-hours flow summary (not found or unclear in transcript).
```

- **version** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-v1
+v2
```

# Changelog

### Account Memo Changes

- **after_hours_flow_summary** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-Right now after hours we ask callers to leave a voicemail and then the tech on call checks it. Half the time they forget to leave a callback number. We want Clara to capture the name, callback number, and what’s going on, then try to reach the on-call tech.
+After hours, Clara should immediately determine whether the situation fits that emergency definition. If it does, collect the caller name, callback number, job site address, and a short description, then attempt to transfer to the on‑call tech at the on‑call number we will provide. If the call rings for more than 60 seconds, cancel the transfer, go back to the caller, and apologize, then confirm all details so we can dispatch manually. If after hours and it is not an emergency, Clara should collect the same information but clearly tell the caller that the office will follow up during the next business day.
```

- **business_hours** changed:
```diff
--- v1
+++ v2
@@ -1,7 +1,13 @@
 {
-  "days": [],
-  "start": "",
-  "end": "",
-  "timezone": "",
-  "raw": ""
+  "days": [
+    "mon",
+    "tue",
+    "wed",
+    "thu",
+    "fri"
+  ],
+  "start": "08:00",
+  "end": "16:30",
+  "timezone": "PT",
+  "raw": "Mon–Fri 8:00 AM–4:30 PM PT"
 }
```

- **call_transfer_rules** changed:
```diff
--- v1
+++ v2
@@ -1,5 +1,5 @@
 {
-  "raw": "",
+  "raw": "During business hours transfer inspection and minor repair calls to the service coordinator at extension 102. After hours, for emergencies transfer to the on-call technician and if it rings more than 60 seconds return to the caller, apologize, and take a full message.",
   "timeout_seconds": null,
   "retries": null,
   "what_to_say_if_fails": ""
```

- **emergency_routing_rules** changed:
```diff
--- v1
+++ v2
@@ -1,7 +1,7 @@
 {
-  "raw": "Our main issue is missed after-hours calls. Right now we forward everything to a single cell phone, and if that person is on another call, emergencies get missed. If a sprinkler is actively leaking or a head has been damaged, we consider that an emergency. Same thing if the fire department has been out and they tell the customer to call us right away.",
+  "raw": "Let me confirm our exact hours. We are open Monday through Friday, 8:00 AM to 4:30 PM Pacific Time. We do not take routine calls on weekends unless they are emergencies. After hours, Clara should immediately determine whether the situation fits that emergency definition. If it does, collect the caller name, callback number, job site address, and a short description, then attempt to transfer to the on‑call tech at the on‑call number we will provide. If the call rings for more than 60 seconds, cancel the transfer, go back to the caller, and apologize, then confirm all details so we can dispatch manually.",
   "steps": [
-    "Our main issue is missed after-hours calls. Right now we forward everything to a single cell phone, and if that person is on another call, emergencies get missed.",
-    "If a sprinkler is actively leaking or a head has been damaged, we consider that an emergency. Same thing if the fire department has been out and they tell the customer to call us right away."
+    "Let me confirm our exact hours. We are open Monday through Friday, 8:00 AM to 4:30 PM Pacific Time. We do not take routine calls on weekends unless they are emergencies.",
+    "After hours, Clara should immediately determine whether the situation fits that emergency definition. If it does, collect the caller name, callback number, job site address, and a short description, then attempt to transfer to the on‑call tech at the on‑call number we will provide. If the call rings for more than 60 seconds, cancel the transfer, go back to the caller, and apologize, then confirm all details so we can dispatch manually."
   ]
 }
```

- **integration_constraints** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-We use ServiceTrade for all jobs. For now, Clara should not create jobs directly; just capture details so the office can create the job in the morning.
+ServiceTrade is used for all jobs. Clara must not create or modify jobs directly; only capture details for the office.
```

- **non_emergency_routing_rules** changed:
```diff
--- v1
+++ v2
@@ -1,4 +1,6 @@
 {
-  "raw": "",
-  "steps": []
+  "raw": "If after hours and it is not an emergency, Clara should collect the same information but clearly tell the caller that the office will follow up during the next business day.",
+  "steps": [
+    "If after hours and it is not an emergency, Clara should collect the same information but clearly tell the caller that the office will follow up during the next business day."
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
+  "Structured form override for 'business_hours': 'raw' overridden: previous='Let me confirm our exact hours. We are open Monday through Friday, 8:00 AM to 4:30 PM Pacific Time. We do not take routine calls on weekends unless they are emergencies.', new='Mon–Fri 8:00 AM–4:30 PM PT'.",
+  "Structured form override for 'call_transfer_rules': 'raw' overridden: previous='During business hours, if someone is calling about an inspection or a minor repair, Clara should collect their name, callback number, site address, and what they need, then transfer to the service coordinator at extension 102. If the coordinator does not answer, take a message rather than looping the transfer.', new='During business hours transfer inspection and minor repair calls to the service coordinator at extension 102. After hours, for emergencies transfer to the on-call technician and if it rings more than 60 seconds return to the caller, apologize, and take a full message.'.",
+  "Structured form override for 'integration_constraints': previous value='We use ServiceTrade only for scheduling and documentation. Do not let Clara promise that a job is created; just say that the office will review and schedule.', new value='ServiceTrade is used for all jobs. Clara must not create or modify jobs directly; only capture details for the office.'."
+]
```

- **office_hours_flow_summary** changed:
```diff
--- v1
+++ v2
@@ -0,0 +1 @@
+During business hours, if someone is calling about an inspection or a minor repair, Clara should collect their name, callback number, site address, and what they need, then transfer to the service coordinator at extension 102. If the coordinator does not answer, take a message rather than looping the transfer.
```

- **questions_or_unknowns** changed:
```diff
--- v1
+++ v2
@@ -1,8 +1,4 @@
 [
-  "Missing business hours (not found or unclear in transcript).",
   "Missing office address (not found or unclear in transcript).",
-  "Missing services supported (not found or unclear in transcript).",
-  "Missing non-emergency routing rules (not found or unclear in transcript).",
-  "Missing call transfer rules (not found or unclear in transcript).",
-  "Missing office-hours flow summary (not found or unclear in transcript)."
+  "Missing services supported (not found or unclear in transcript)."
 ]
```

### Agent Spec Changes

- **agent_name** changed:
```diff
--- v1
+++ v2
@@ -1 +1 @@
-FireGuard Sprinkler Services – Clara Answers Agent v1
+FireGuard Sprinkler Services – Clara Answers Agent v2
```

- **call_transfer_protocol** changed:
```diff
--- v1
+++ v2
@@ -1,5 +1,5 @@
 {
-  "raw": "",
+  "raw": "During business hours transfer inspection and minor repair calls to the service coordinator at extension 102. After hours, for emergencies transfer to the on-call technician and if it rings more than 60 seconds return to the caller, apologize, and take a full message.",
   "timeout_seconds": null,
   "retries": null,
   "what_to_say_if_fails": ""
```

- **key_variables** changed:
```diff
--- v1
+++ v2
@@ -2,19 +2,25 @@
   "account_id": "fireguard_sprinklers",
   "company_name": "FireGuard Sprinkler Services",
   "business_hours": {
-    "days": [],
-    "start": "",
-    "end": "",
-    "timezone": "",
-    "raw": ""
+    "days": [
+      "mon",
+      "tue",
+      "wed",
+      "thu",
+      "fri"
+    ],
+    "start": "08:00",
+    "end": "16:30",
+    "timezone": "PT",
+    "raw": "Mon–Fri 8:00 AM–4:30 PM PT"
   },
   "office_address": "",
-  "timezone": "",
+  "timezone": "PT",
   "emergency_routing": {
-    "raw": "Our main issue is missed after-hours calls. Right now we forward everything to a single cell phone, and if that person is on another call, emergencies get missed. If a sprinkler is actively leaking or a head has been damaged, we consider that an emergency. Same thing if the fire department has been out and they tell the customer to call us right away.",
+    "raw": "Let me confirm our exact hours. We are open Monday through Friday, 8:00 AM to 4:30 PM Pacific Time. We do not take routine calls on weekends unless they are emergencies. After hours, Clara should immediately determine whether the situation fits that emergency definition. If it does, collect the caller name, callback number, job site address, and a short description, then attempt to transfer to the on‑call tech at the on‑call number we will provide. If the call rings for more than 60 seconds, cancel the transfer, go back to the caller, and apologize, then confirm all details so we can dispatch manually.",
     "steps": [
-      "Our main issue is missed after-hours calls. Right now we forward everything to a single cell phone, and if that person is on another call, emergencies get missed.",
-      "If a sprinkler is actively leaking or a head has been damaged, we consider that an emergency. Same thing if the fire department has been out and they tell the customer to call us right away."
+      "Let me confirm our exact hours. We are open Monday through Friday, 8:00 AM to 4:30 PM Pacific Time. We do not take routine calls on weekends unless they are emergencies.",
+      "After hours, Clara should immediately determine whether the situation fits that emergency definition. If it does, collect the caller name, callback number, job site address, and a short description, then attempt to transfer to the on‑call tech at the on‑call number we will provide. If the call rings for more than 60 seconds, cancel the transfer, go back to the caller, and apologize, then confirm all details so we can dispatch manually."
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
-[UNKNOWN: business hours – if caller asks, say you do not have this information yet and collect it for a human follow-up.]
+Mon–Fri 8:00 AM–4:30 PM PT
 During business hours, follow **exactly** this sequence. Do not skip steps, and do not add new ones:
 1. Greeting: Greet the caller on behalf of the business and state that you are an AI assistant.
 2. Ask purpose: Ask the caller for the reason for their call.
 3. Collect name and number: Collect the caller's name and callback phone number early in the call.
 4. Determine routing: Based only on the rules below and the memo:
-   - Office-hours flow summary: [UNKNOWN: office hours call flow summary – if caller asks, say you do not have this information yet and collect it for a human follow-up.]
+   - Office-hours flow summary: During business hours, if someone is calling about an inspection or a minor repair, Clara should collect their name, callback number, site address, and what they need, then transfer to the service coordinator at extension 102. If the coordinator does not answer, take a message rather than looping the transfer.
    - Do not guess routes that are not specified.
 5. Transfer or route: If routing requires a live person, follow the transfer protocol section.
 6. Fallback if transfer fails: If the transfer fails, drops, or no one answers, follow the 'Transfer Failure Handling' section.
@@ -17,7 +17,7 @@
 
 === After-Hours Call Flow ===
 After-hours flow description:
-Right now after hours we ask callers to leave a voicemail and then the tech on call checks it. Half the time they forget to leave a callback number. We want Clara to capture the name, callback number, and what’s going on, then try to reach the on-call tech.
+After hours, Clara should immediately determine whether the situation fits that emergency definition. If it does, collect the caller name, callback number, job site address, and a short description, then attempt to transfer to the on‑call tech at the on‑call number we will provide. If the call rings for more than 60 seconds, cancel the transfer, go back to the caller, and apologize, then confirm all details so we can dispatch manually. If after hours and it is not an emergency, Clara should collect the same information but clearly tell the caller that the office will follow up during the next business day.
 During after-hours, follow **exactly** this sequence. Do not skip steps, and do not add new ones:
 1. Greeting: Greet the caller on behalf of the business and clarify that it is after hours.
 2. Ask purpose: Ask the caller for the reason for their call.
@@ -38,20 +38,12 @@
 - we consider that an emergency. Same thing if the fire department has been out
 - they tell the customer to call us right away
 Routing rules for emergencies:
-Our main issue is missed after-hours calls. Right now we forward everything to a single cell phone, and if that person is on another call, emergencies get missed. If a sprinkler is actively leaking or a head has been damaged, we consider that an emergency. Same thing if the fire department has been out and they tell the customer to call us right away.
+Let me confirm our exact hours. We are open Monday through Friday, 8:00 AM to 4:30 PM Pacific Time. We do not take routine calls on weekends unless they are emergencies. After hours, Clara should immediately determine whether the situation fits that emergency definition. If it does, collect the caller name, callback number, job site address, and a short description, then attempt to transfer to the on‑call tech at the on‑call number we will provide. If the call rings for more than 60 seconds, cancel the transfer, go back to the caller, and apologize, then confirm all details so we can dispatch manually.
 Routing rules for non-emergencies:
-{
-  "raw": "",
-  "steps": []
-}
+If after hours and it is not an emergency, Clara should collect the same information but clearly tell the caller that the office will follow up during the next business day.
 
 === Call Transfer Protocol ===
-{
-  "raw": "",
-  "timeout_seconds": null,
-  "retries": null,
-  "what_to_say_if_fails": ""
-}
+During business hours transfer inspection and minor repair calls to the service coordinator at extension 102. After hours, for emergencies transfer to the on-call technician and if it rings more than 60 seconds return to the caller, apologize, and take a full message.
 If you initiate a transfer, clearly tell the caller who you are transferring to and why.
 
 === Transfer Failure Handling ===
@@ -72,9 +64,5 @@
 
 === Known Questions or Unknowns ===
 The following items are not yet clearly defined from the account materials. If they come up, collect information and flag for human review, and do NOT guess:
-- Missing business hours (not found or unclear in transcript).
 - Missing office address (not found or unclear in transcript).
 - Missing services supported (not found or unclear in transcript).
-- Missing non-emergency routing rules (not found or unclear in transcript).
-- Missing call transfer rules (not found or unclear in transcript).
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

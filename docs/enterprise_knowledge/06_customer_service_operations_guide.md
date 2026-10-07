# Customer Service Operations Guide

## Document Metadata

Document Owner: Customer Operations  
Document Type: Operational Guide  
Version: 1.0  
Status: Active  
Last Reviewed: October 2026

---

## 1. Purpose

This guide defines how Customer Operations should handle common customer-service situations involving orders, cancellations, shipping, delivery, returns, refunds, and escalations.

The goal is to provide consistent customer handling while ensuring that operational decisions remain aligned with enterprise policies.

---

## 2. General Service Principles

Customer Operations should:

- verify relevant order information before making a decision,
- distinguish policy requirements from operational recommendations,
- avoid promising outcomes before eligibility is confirmed,
- explain available options clearly,
- document exceptions and escalations,
- use governed enterprise information when answering policy questions,
- avoid guessing when required information is unavailable.

When a request spans multiple business areas, the case should be evaluated using all relevant policies.

---

## 3. Order Status Review

Before advising a customer, the current order status should be verified.

Common statuses include:

- Processing
- Shipped
- Complete
- Cancelled
- Returned

Different statuses may require different workflows.

For example:

- Processing orders may still qualify for cancellation.
- Shipped orders normally follow shipping or return workflows.
- Completed orders are not eligible for standard cancellation.
- Returned orders should be handled through the return and refund process.

---

## 4. Cancellation Requests

When a customer asks to cancel an order:

1. verify the current order status,
2. determine whether shipment has occurred,
3. determine whether fulfillment has entered a non-reversible stage,
4. apply the Order Cancellation Policy.

### Processing Orders

A processing order may still be cancellable if fulfillment has not reached a locked stage.

### Shipped Orders

A shipped order should not normally be cancelled.

If the customer no longer wants the item, the customer should generally wait for delivery and follow the return process.

### Completed Orders

Completed orders should be handled under the Return and Refund Policy rather than the cancellation process.

---

## 5. Standard Return Requests

For standard return requests:

- confirm the delivery date,
- verify that the request falls within the applicable return window,
- confirm product eligibility,
- determine whether the customer or company is responsible for return shipping.

The standard return window is 30 calendar days from delivery.

A standard return request does not automatically qualify for free return shipping.

---

## 6. Damaged or Defective Product Requests

For damaged or defective products:

- confirm the delivery date,
- determine when the issue was reported,
- collect available evidence,
- determine whether damaged-product handling applies.

Damage or defect should generally be reported within 14 calendar days of delivery.

When confirmed, available resolutions may include:

- replacement,
- full refund,
- store credit.

The company covers return shipping for confirmed damaged or defective products.

---

## 7. Incorrect Item Requests

When a customer receives the wrong product:

1. verify the original order,
2. verify the item received,
3. classify the issue as a fulfillment error,
4. provide return shipping at no cost,
5. offer replacement or refund as appropriate.

Incorrect-item incidents should also be recorded for fulfillment-quality monitoring.

---

## 8. Delivery Delay Requests

When a customer reports a delayed order, Customer Operations should determine whether the issue is:

- a processing delay,
- a carrier delay,
- a delivery delay,
- a potentially lost shipment.

### Processing Delay

An order remaining in processing for more than 3 business days should be reviewed.

### Carrier Movement Delay

No carrier movement for more than 2 business days after shipment should trigger review.

### Potentially Lost Shipment

A shipment may be considered potentially lost when there has been no tracking movement for 7 consecutive calendar days after the expected movement period.

---

## 9. Refund Questions

When discussing refunds:

- verify that return or cancellation eligibility has been established,
- verify whether the refund has been approved,
- explain that processing time may differ from bank settlement time.

Approved refunds should generally begin processing after the returned product is received and validated.

Customers should normally allow 5 to 7 business days for refund processing after approval.

Additional payment-provider processing time may apply.

---

## 10. Policy Conflict Handling

If a customer request appears to involve conflicting policy rules:

- do not choose a rule arbitrarily,
- identify the applicable order stage,
- determine which policy governs the current situation,
- escalate when necessary.

Examples:

A request to cancel a shipped order should generally transition from the cancellation workflow to the return workflow.

A damaged product reported after the 14-day damaged-product reporting period may still fall within the 30-day standard return window.

---

## 11. Customer Communication

Customer-facing explanations should:

- state what is known,
- state what remains uncertain,
- avoid internal jargon where possible,
- avoid unsupported promises,
- explain the next required action.

Customer Operations should not tell a customer that a refund, replacement, or exception is guaranteed unless approval has been confirmed.

---

## 12. Escalation Rules

Cases should be escalated when:

- the customer disputes a denied return or cancellation,
- the order value exceeds applicable escalation thresholds,
- repeated fulfillment problems are present,
- fraud or abuse is suspected,
- policy interpretation is unclear,
- multiple enterprise policies appear to apply,
- a system issue prevents normal case handling.

---

## 13. High-Value Orders

High-value orders may require additional review.

Relevant thresholds include:

- Return-related escalation: order value above $500
- Fulfillment-related unresolved issue: order value above $750
- Cancellation-related escalation: order value above $750

The applicable threshold depends on the operational workflow.

These thresholds should not be treated as interchangeable.

---

## 14. Operational Analytics

Customer Operations may use analytics to identify patterns such as:

- high cancellation rates,
- high return rates,
- repeated fulfillment delays,
- frequent incorrect-item incidents,
- repeated product defects.

Aggregate analytics should support investigation but should not replace case-level verification.

For example, a high category return rate does not automatically mean that an individual customer's return should be approved.

---

## 15. AI-Assisted Customer Support

AI systems may assist Customer Operations by:

- retrieving relevant enterprise policies,
- summarizing applicable procedures,
- identifying which workflow may apply,
- highlighting missing information,
- combining operational metrics with policy guidance.

AI-generated recommendations should remain grounded in authoritative enterprise sources.

An AI system should not:

- invent company policy,
- override validated enterprise data,
- approve exceptions without authority,
- fabricate customer or order information,
- treat operational thresholds as customer eligibility rules.

---

## 16. Example Routing Scenarios

### Scenario A

Customer asks:

"Can I cancel my order?"

Required information:

- current order status,
- fulfillment stage,
- shipment status.

Primary knowledge source:

Order Cancellation Policy.

---

### Scenario B

Customer asks:

"My package arrived damaged. What are my options?"

Required information:

- delivery date,
- date damage was reported,
- evidence of damage.

Primary knowledge sources:

- Return and Refund Policy
- Shipping and Fulfillment Policy

---

### Scenario C

Customer asks:

"My order already shipped, but I don't want it anymore."

Primary workflow:

Shipping and Return workflow.

The request should not normally be handled as a standard cancellation.

---

### Scenario D

Business analyst asks:

"Our monthly cancellation rate is 15.07%. What operational action is required?"

Required capabilities:

- structured analytics,
- Order Cancellation Policy retrieval.

This is a hybrid analytics and knowledge request.

---

### Scenario E

Business analyst asks:

"Our product-category return rate is 16%. What should happen?"

Relevant policy:

A category return rate above 15% triggers priority review.

This is an operational review trigger, not a customer refund eligibility rule.

---

## 17. Important Interpretation Notes

Customer eligibility rules, operational thresholds, and escalation thresholds are different concepts.

The same numerical value may have different meaning depending on context.

Examples:

- 15% cancellation rate may trigger operational review.
- 15% category return rate may trigger priority product review.
- Neither threshold automatically determines customer eligibility.

Customer Operations should use the correct policy for the current order stage and business process.

When information is missing or policies conflict, the case should be escalated rather than resolved through assumption.
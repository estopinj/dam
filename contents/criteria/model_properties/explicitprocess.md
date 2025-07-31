---
title: "Explicit process required"
parent: "Model properties"
nav_order: 1
permalink: /explicitprocess
categories:
- criteria
- model_properties
---

# Explicit process required

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Yes` | Must encode system processes (e.g., differential equations). |
| `Optional` | The method can incorporate mechanisms but not required. |
| `Agnostic` | No process modeling needed. |


## Definition
Whether the method mandates building an explicit mechanistic or process‐based model of the underlying system. 

## Explanation
Process‐explicit methods (e.g., dynamic vegetation models) leverage domain knowledge to simulate system behavior. Agnostic methods rely on observed statistical patterns and assumptions. 

## Tools/rationale for helping assessment
1. Review whether you want to enforce mechanistic equations in your system modeling. 
2. If your expertise or data do not support that, select an Agnostic approach. 


## Example
I lack detailed dispersal/mortality rates for my species, so I opt for an `Agnostic` statistical model rather than an explicit process‐based simulator. 

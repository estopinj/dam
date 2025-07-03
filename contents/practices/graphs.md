---
title: A primer on causal graphs
parent: Good practices
nav_order: 1
---

# A primer on causal graphs

Causal graphs depict the assumed process underlying the generation of the analysed data. They explicitly represent the presence or absence of relationships between the variables, without making any assumptions about functional forms. While different types of graphs coexist (see Section XXX), the Directed Acyclic Graph (DAG), popularised by XXX, remains the cornerstone. This type of graph only allows oriented links between variables and prohibits cycles of influence. Working with graphs can support various research objectives, such as estimating unbiased causal effects and improving system comprehension by targeting efforts towards critical and unproven links. It can also enhance out-of-sample predictions and scenario projection between others.
{: .fs-4 .fw-300 }

> On this page, we briefly motivate the usage of DAGs. Sketching research assumptions using nodes and arrows is indeed not only necessary for detection and attribution methods, but can also be highly beneficial for other research objectives. In fact, we are convinced it should become a reflex prior to any modelling exercise!


<!-- ## When should we draw DAGs?

{: .note-title }
> TL;DR
>
> **Always**, i.e. before any modelling exercise.


%% Classically, for effect estimation & discovery
    %% Adjustment & bette pred.
    
    %% But beneficial to others


%% Expliciting assumptions
    %% Better communication, justification, increased confidence in results & reproducibility

    %% Enables discussion and challenges of assumptions, iterative science


%%% Note: Each task classically fine on its own, difficulty: doing everything at once
%%% Now: connections between both:  hard but active research areas

## The origin story: graphs & causal paradigms

%% SCM & PO: The workhorses of causal inference

%% Other paradigms

%% Graph types


## Triplet structures for adjustement

%% Base triplets

 Mermaid for each
 -->




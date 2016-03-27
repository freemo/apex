---
title: Routing
sidebar: protocol_sidebar
permalink: /protocol/routing/
toc: false
---

The APEX routing algorithm defines a few new routing aliases in addition to the
common ones such as "WIDE2-2", along with a few new behaviors regarding how the
paths are consumed.

The problems with the current APRS model are numerous. One problem is that
aside from the use of WIDE and GATE there isn't much flexibility on how we can
route packets when we don't know the explicit digipeaters with which to
specify; Using WIDEN-n is more of a sledgehammer when we need a scalpel. It is
also completely ineffective at being able to route a VHF message across HF
channels which may be critical during an emergency. A similar problem occurs
when we consider multiple HF nets across multiple bands; as it stands right now
there is no paradigm that defines cross-band repeating paths. The closest we
have is the GATE path which is generally used to only repeat from HF into
VHF. This has some limited usefulness at best. As such the initial release of
the APEX reference application attempts to address these problems (though
testing and feedback may change the details of the specification as described
here).


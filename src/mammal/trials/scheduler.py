"""Domain session scheduler and Latin-square block balancing for exploratory sessions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
import numpy as np
from sqlalchemy import select
from sqlalchemy.orm import Session

from mammal.models.entities import Item


@dataclass
class ScheduledBlock:
    block_index: int
    domain: str
    item_ids: list[str]
    item_count: int


@dataclass
class ScheduledSessionPlan:
    protocol_id: str
    total_trials: int
    total_blocks: int
    blocks: list[ScheduledBlock]
    ordered_items: list[Item]


class DomainSessionScheduler:
    """Manages multi-domain balance, pseudo-randomization, and block schedules for exploratory sessions."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def plan_session(
        self,
        protocol_id: str,
        domains: list[str],
        items_per_domain: int = 15,
        block_size: int = 5,
        partition: str = "engineering",
        seed: int = 42,
    ) -> ScheduledSessionPlan:
        """Create a balanced multi-block session schedule with deterministic block pseudo-randomization."""
        rng = np.random.default_rng(seed)
        domain_items_map: dict[str, list[Item]] = {}

        # 1. Fetch available items for each domain/family
        for d in domains:
            stmt = select(Item).where(
                (Item.domain == d) | (Item.family == d),
                Item.partition == partition,
            )
            items = list(self.session.scalars(stmt).all())
            if not items:
                # Fallback: query without partition filter
                stmt_fallback = select(Item).where((Item.domain == d) | (Item.family == d))
                items = list(self.session.scalars(stmt_fallback).all())

            if not items:
                # If still empty, seed items
                from mammal.items.bank import seed_qualification_items
                seed_qualification_items(self.session)
                stmt_re = select(Item).where((Item.domain == d) | (Item.family == d))
                items = list(self.session.scalars(stmt_re).all())

            # Shuffle items deterministically
            if items:
                shuffled_idx = rng.permutation(len(items))
                selected = [items[i] for i in shuffled_idx[:items_per_domain]]
            else:
                selected = []
            domain_items_map[d] = selected

        # 2. Divide each domain's items into blocks
        blocks: list[ScheduledBlock] = []
        ordered_items: list[Item] = []
        block_idx = 1

        # Interleave domains across blocks (Latin-square style rotation)
        domain_ptrs = {d: 0 for d in domains}
        has_remaining = True

        while has_remaining:
            has_remaining = False
            for d in domains:
                d_items = domain_items_map[d]
                ptr = domain_ptrs[d]
                if ptr < len(d_items):
                    block_items = d_items[ptr : ptr + block_size]
                    domain_ptrs[d] += len(block_items)
                    has_remaining = True

                    block = ScheduledBlock(
                        block_index=block_idx,
                        domain=d,
                        item_ids=[it.item_id for it in block_items],
                        item_count=len(block_items),
                    )
                    blocks.append(block)
                    ordered_items.extend(block_items)
                    block_idx += 1

        return ScheduledSessionPlan(
            protocol_id=protocol_id,
            total_trials=len(ordered_items),
            total_blocks=len(blocks),
            blocks=blocks,
            ordered_items=ordered_items,
        )

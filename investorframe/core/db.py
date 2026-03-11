"""SQLAlchemy database layer for InvestorFrame.

Provides ORM models for persisting pipeline results and a ``Database``
manager with session lifecycle helpers.
"""

from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime
from typing import Generator

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    JSON,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    pass


# ── ORM Models ───────────────────────────────────────────────


class PipelineRunRecord(Base):
    __tablename__ = "pipeline_runs"

    id = Column(String(16), primary_key=True)
    status = Column(String(20), nullable=False)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, default=0.0)
    event_count = Column(Integer, default=0)
    warnings = Column(JSON, default=list)
    errors = Column(JSON, default=list)


class EventRecord(Base):
    __tablename__ = "events"

    id = Column(String(12), primary_key=True)
    run_id = Column(String(16), nullable=False, index=True)
    event_type = Column(String(30), nullable=False)
    subtype = Column(String(30), nullable=False)
    source = Column(String(20), nullable=False)
    severity = Column(Integer, nullable=False)
    direction = Column(String(10), nullable=False)
    confidence = Column(Float, nullable=False)
    headline = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)


class RegimeRecord(Base):
    __tablename__ = "regimes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(16), nullable=False, index=True)
    state = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    contributing_factors = Column(JSON, default=list)
    indicator_values = Column(JSON, default=dict)
    timestamp = Column(DateTime, nullable=False)


class SectorScoreRecord(Base):
    __tablename__ = "sector_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(16), nullable=False, index=True)
    symbol = Column(String(10), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    score = Column(Float, nullable=False)
    direction = Column(String(10), nullable=False)
    confidence = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)
    event_count = Column(Integer, default=0)
    timestamp = Column(DateTime, nullable=False)


class StockScoreRecord(Base):
    __tablename__ = "stock_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(16), nullable=False, index=True)
    symbol = Column(String(10), nullable=False, index=True)
    sector = Column(String(10), nullable=False)
    tailwind_score = Column(Float, nullable=False)
    headwind_score = Column(Float, nullable=False)
    net_signal = Column(Float, nullable=False)
    label = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)


# ── Database Manager ─────────────────────────────────────────


class Database:
    """SQLAlchemy database manager with session lifecycle helpers."""

    def __init__(self, url: str = "sqlite:///investorframe.db") -> None:
        self.engine = create_engine(url, echo=False)
        self._session_factory = sessionmaker(bind=self.engine)

    def create_tables(self) -> None:
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_session(self) -> Session:
        return self._session_factory()

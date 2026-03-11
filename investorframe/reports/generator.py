"""Report generation: JSON, HTML, and Markdown outputs."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from investorframe.core.config import AppConfig
from investorframe.core.models import PipelineResult

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates output artifacts from pipeline results."""

    def __init__(
        self,
        config: AppConfig,
        output_dir: Path | str = "output",
    ) -> None:
        self.config = config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ── JSON ─────────────────────────────────────────────────────

    def generate_json(self, result: PipelineResult) -> dict:
        """Convert PipelineResult to a JSON-serializable dict."""
        data = {
            "run_id": result.run_id,
            "status": result.status.value,
            "started_at": self._fmt(result.started_at),
            "completed_at": self._fmt(result.completed_at) if result.completed_at else None,
            "duration_seconds": result.duration_seconds,
            "regime": None,
            "sentiment": None,
            "sector_scores": [],
            "stock_scores": [],
            "risk_assessment": None,
            "event_count": len(result.events),
            "warnings": result.warnings,
            "errors": result.errors,
            "connector_status": result.connector_status,
        }

        if result.regime:
            data["regime"] = {
                "state": result.regime.state.value,
                "confidence": result.regime.confidence,
                "contributing_factors": result.regime.contributing_factors,
                "indicator_values": result.regime.indicator_values,
            }

        if result.sentiment:
            data["sentiment"] = {
                "composite_score": result.sentiment.composite_score,
                "label": result.sentiment.label.value,
                "confidence": result.sentiment.confidence,
            }

        for s in result.sector_scores:
            data["sector_scores"].append({
                "symbol": s.symbol,
                "name": s.name,
                "score": s.score,
                "direction": s.direction.value,
                "confidence": s.confidence,
                "rank": s.rank,
                "event_count": s.event_count,
                "top_drivers": [e.headline for e in s.driving_events[:3]],
            })

        for s in result.stock_scores:
            data["stock_scores"].append({
                "symbol": s.symbol,
                "name": s.name,
                "sector": s.sector,
                "sector_name": s.sector_name,
                "tailwind_score": s.tailwind_score,
                "headwind_score": s.headwind_score,
                "net_signal": s.net_signal,
                "label": s.label.value,
                "confidence": s.confidence,
                "explanation": s.explanation,
                "rank": s.rank,
            })

        if result.risk_assessment:
            data["risk_assessment"] = {
                "passed": result.risk_assessment.passed,
                "flags": [
                    {
                        "code": f.code,
                        "severity": f.severity.value,
                        "message": f.message,
                    }
                    for f in result.risk_assessment.flags
                ],
                "disclaimers": result.risk_assessment.disclaimers,
            }

        return data

    def save_json(self, result: PipelineResult) -> Path:
        """Write JSON report to output_dir."""
        data = self.generate_json(result)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        path = self.output_dir / f"report_{ts}.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)
        logger.info("JSON report saved to %s", path)
        return path

    # ── HTML ─────────────────────────────────────────────────────

    def generate_html(self, result: PipelineResult) -> str:
        """Render a static HTML report using Jinja2 template."""
        try:
            from jinja2 import Environment, FileSystemLoader
        except ImportError:
            logger.warning("jinja2 not installed; falling back to basic HTML")
            return self._generate_basic_html(result)

        template_dir = Path(__file__).parent / "templates"
        if not (template_dir / "report.html.j2").exists():
            return self._generate_basic_html(result)

        env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=True,
        )
        template = env.get_template("report.html.j2")
        return template.render(
            result=result,
            data=self.generate_json(result),
            generated_at=self._fmt(datetime.now(timezone.utc)),
        )

    def save_html(self, result: PipelineResult) -> Path:
        """Write HTML report to output_dir."""
        html = self.generate_html(result)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        path = self.output_dir / f"report_{ts}.html"
        with open(path, "w") as f:
            f.write(html)
        logger.info("HTML report saved to %s", path)
        return path

    # ── Markdown ─────────────────────────────────────────────────

    def generate_markdown(self, result: PipelineResult) -> str:
        """Generate a Markdown summary report."""
        lines: list[str] = []
        lines.append("# InvestorFrame Market Intelligence Report")
        lines.append("")
        lines.append(f"**Run ID**: {result.run_id}")
        lines.append(f"**Status**: {result.status.value}")
        lines.append(f"**Generated**: {self._fmt(datetime.now(timezone.utc))}")
        lines.append("")

        # Regime
        if result.regime:
            lines.append("## Market Regime")
            lines.append("")
            lines.append(f"- **State**: {result.regime.state.value}")
            lines.append(f"- **Confidence**: {result.regime.confidence:.2f}")
            if result.regime.contributing_factors:
                lines.append("- **Factors**: " + ", ".join(result.regime.contributing_factors))
            lines.append("")

        # Sentiment
        if result.sentiment:
            lines.append("## Aggregate Sentiment")
            lines.append("")
            lines.append(f"- **Score**: {result.sentiment.composite_score:+.3f}")
            lines.append(f"- **Label**: {result.sentiment.label.value}")
            lines.append(f"- **Confidence**: {result.sentiment.confidence:.2f}")
            lines.append("")

        # Sectors
        if result.sector_scores:
            lines.append("## Sector Scores")
            lines.append("")
            lines.append("| Rank | Sector | Score | Direction | Confidence |")
            lines.append("|------|--------|-------|-----------|------------|")
            for s in sorted(result.sector_scores, key=lambda x: x.rank):
                lines.append(
                    f"| {s.rank} | {s.name} ({s.symbol}) | {s.score:+.1f} | "
                    f"{s.direction.value} | {s.confidence:.2f} |"
                )
            lines.append("")

        # Watchlist
        if result.stock_scores:
            lines.append("## Watchlist Scores")
            lines.append("")
            lines.append("| Rank | Stock | Signal | Label | Confidence |")
            lines.append("|------|-------|--------|-------|------------|")
            for s in sorted(result.stock_scores, key=lambda x: x.rank):
                lines.append(
                    f"| {s.rank} | {s.name} ({s.symbol}) | {s.net_signal:+.1f} | "
                    f"{s.label.value} | {s.confidence:.2f} |"
                )
            lines.append("")

        # Risk Assessment
        if result.risk_assessment:
            lines.append("## Risk Assessment")
            lines.append("")
            status = "PASSED" if result.risk_assessment.passed else "FAILED"
            lines.append(f"**Overall**: {status}")
            if result.risk_assessment.flags:
                lines.append("")
                for flag in result.risk_assessment.flags:
                    lines.append(f"- **{flag.code}** ({flag.severity.value}): {flag.message}")
            lines.append("")

        # Disclaimers
        if result.risk_assessment and result.risk_assessment.disclaimers:
            lines.append("## Disclaimers")
            lines.append("")
            for d in result.risk_assessment.disclaimers:
                lines.append(f"> {d}")
                lines.append("")

        lines.append("---")
        lines.append("*Generated by InvestorFrame v0.1.0*")
        return "\n".join(lines)

    def save_markdown(self, result: PipelineResult) -> Path:
        """Write Markdown report to output_dir."""
        md = self.generate_markdown(result)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        path = self.output_dir / f"report_{ts}.md"
        with open(path, "w") as f:
            f.write(md)
        logger.info("Markdown report saved to %s", path)
        return path

    # ── Helpers ───────────────────────────────────────────────────

    def _fmt(self, dt: datetime | None) -> str:
        if dt is None:
            return "N/A"
        return dt.strftime("%Y-%m-%d %H:%M UTC")

    def _generate_basic_html(self, result: PipelineResult) -> str:
        """Minimal HTML fallback when Jinja2 is unavailable."""
        md = self.generate_markdown(result)
        return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>InvestorFrame Report</title>
<style>body{{font-family:sans-serif;max-width:900px;margin:auto;padding:2rem;}}
table{{border-collapse:collapse;width:100%;}}
th,td{{border:1px solid #ddd;padding:8px;text-align:left;}}
th{{background:#f4f4f4;}}</style></head>
<body><pre>{md}</pre></body></html>"""

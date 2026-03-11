"""CLI entry point for InvestorFrame pipeline."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from investorframe.core.config import AppConfig
from investorframe.core.db import Database
from investorframe.core.types import PipelineStatus
from investorframe.pipeline.orchestrator import PipelineOrchestrator
from investorframe.reports.generator import ReportGenerator
from investorframe.scenarios.simulator import ScenarioSimulator
from investorframe.scenarios.templates import ScenarioTemplateLoader

logger = logging.getLogger("investorframe")


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="investorframe",
        description="InvestorFrame — Event-driven market intelligence framework",
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=Path("config"),
        help="Path to YAML config directory (default: config/)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Path to output directory for reports (default: output/)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "html", "markdown", "all"],
        default="json",
        help="Output report format (default: json)",
    )
    parser.add_argument(
        "--scenario",
        type=str,
        default=None,
        help="Run a named scenario simulation instead of live pipeline",
    )
    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="List available scenario templates and exit",
    )
    parser.add_argument(
        "--enable-llm",
        action="store_true",
        help="Enable OpenAI LLM enrichment",
    )
    parser.add_argument(
        "--db-url",
        type=str,
        default=None,
        help="Database URL (default: from env or sqlite:///investorframe.db)",
    )
    parser.add_argument(
        "--no-db",
        action="store_true",
        help="Skip database persistence",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (DEBUG) logging",
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Start the FastAPI server instead of running the pipeline",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="API server host (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="API server port (default: 8000)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    # Logging setup
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Config
    config = AppConfig(config_dir=args.config_dir)
    if args.enable_llm:
        config.pipeline.enable_llm = True
    if args.db_url:
        config.pipeline.db_url = args.db_url

    # List scenarios
    if args.list_scenarios:
        loader = ScenarioTemplateLoader(config)
        scenarios = loader.list_scenarios()
        print("Available scenario templates:")
        for name in scenarios:
            template = loader.get_template(name)
            desc = template.description if template else ""
            print(f"  - {name}: {desc}")
        return 0

    # Serve API
    if args.serve:
        return _serve(args)

    # Database
    db = None
    if not args.no_db:
        db = Database(url=config.pipeline.db_url)
        db.create_tables()

    # Run pipeline
    logger.info("Starting InvestorFrame pipeline")
    orchestrator = PipelineOrchestrator(config=config, db=db)
    result = orchestrator.run()

    # Run scenario if requested
    if args.scenario:
        loader = ScenarioTemplateLoader(config)
        template = loader.get_template(args.scenario)
        if template is None:
            logger.error("Unknown scenario: %s", args.scenario)
            print(f"Error: Unknown scenario '{args.scenario}'")
            print(f"Available: {', '.join(loader.list_scenarios())}")
            return 1

        simulator = ScenarioSimulator(config)
        scenario_result = simulator.simulate(
            template=template,
            baseline_events=result.events,
            baseline_regime=result.regime,
            baseline_sectors=result.sector_scores,
            baseline_stocks=result.stock_scores,
        )
        print(f"\nScenario: {scenario_result.scenario_name}")
        print(f"Description: {scenario_result.description}")
        print(f"Sector impacts: {len(scenario_result.sector_impacts)}")
        print(f"Watchlist impacts: {len(scenario_result.watchlist_impacts)}")

    # Generate reports
    reporter = ReportGenerator(config=config, output_dir=args.output_dir)
    fmt = args.format

    if fmt in ("json", "all"):
        path = reporter.save_json(result)
        print(f"JSON report: {path}")

    if fmt in ("html", "all"):
        path = reporter.save_html(result)
        print(f"HTML report: {path}")

    if fmt in ("markdown", "all"):
        path = reporter.save_markdown(result)
        print(f"Markdown report: {path}")

    # Summary
    print(f"\nPipeline status: {result.status.value}")
    print(f"Events processed: {len(result.events)}")
    print(f"Sectors scored: {len(result.sector_scores)}")
    print(f"Stocks scored: {len(result.stock_scores)}")
    if result.regime:
        print(f"Market regime: {result.regime.state.value} "
              f"(confidence: {result.regime.confidence:.2f})")
    if result.risk_assessment:
        status = "PASSED" if result.risk_assessment.passed else "FAILED"
        print(f"Risk assessment: {status}")
        for flag in result.risk_assessment.flags:
            print(f"  - {flag.code}: {flag.message}")

    return 0 if result.status != PipelineStatus.FAILED else 1


def _serve(args: argparse.Namespace) -> int:
    """Start the FastAPI server."""
    try:
        import uvicorn
    except ImportError:
        print("Error: uvicorn is required for --serve. Install with: pip install uvicorn")
        return 1

    logger.info("Starting InvestorFrame API server on %s:%d", args.host, args.port)
    uvicorn.run(
        "api.main:app",
        host=args.host,
        port=args.port,
        reload=False,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

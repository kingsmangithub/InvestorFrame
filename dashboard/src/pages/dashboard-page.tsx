import { PageHeader } from "@/components/shared/page-header";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ErrorState } from "@/components/shared/error-state";
import { WorldStateStrip } from "@/components/dashboard/world-state-strip";
import { MarketFramePanel } from "@/components/dashboard/market-frame-panel";
import { DominantNarrativePanel } from "@/components/dashboard/dominant-narrative-panel";
import { SectorTransmissionPanel } from "@/components/dashboard/sector-transmission-panel";
import { WatchlistSnapshotPanel } from "@/components/dashboard/watchlist-snapshot-panel";
import { RiskUncertaintyPanel } from "@/components/dashboard/risk-uncertainty-panel";
import { QuickActionsPanel } from "@/components/dashboard/quick-actions-panel";
import { useMarket, useSectors, useWatchlist } from "@/lib/api/queries";

export function DashboardPage() {
  const market = useMarket();
  const sectors = useSectors();
  const watchlist = useWatchlist();

  return (
    <div className="space-y-6">
      <PageHeader
        title="Today's Market Frame"
        subtitle="Event-driven market pulse, sector transmission, and watchlist alignment."
      />

      {/* World State Strip */}
      {market.isLoading ? (
        <LoadingSkeleton variant="card" />
      ) : market.isError ? (
        <ErrorState
          title="Failed to load the current market frame."
          message="Check your API connection or retry with demo data."
          onRetry={() => market.refetch()}
        />
      ) : market.data ? (
        <>
          <WorldStateStrip data={market.data} />

          {/* Market Frame + Dominant Narrative — side by side */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
            <div className="lg:col-span-5">
              <MarketFramePanel data={market.data} />
            </div>
            <div className="lg:col-span-7">
              <DominantNarrativePanel data={market.data} />
            </div>
          </div>
        </>
      ) : null}

      {/* Sector Transmission */}
      {sectors.isLoading ? (
        <LoadingSkeleton variant="chart" />
      ) : sectors.isError ? (
        <ErrorState
          title="Failed to load sector transmission data."
          message="This may be caused by a temporary API or parsing issue."
          onRetry={() => sectors.refetch()}
        />
      ) : sectors.data ? (
        <SectorTransmissionPanel data={sectors.data} />
      ) : null}

      {/* Watchlist Snapshot */}
      {watchlist.isLoading ? (
        <LoadingSkeleton variant="table" />
      ) : watchlist.isError ? (
        <ErrorState
          title="Failed to load watchlist insights."
          message="Try refreshing the page or checking whether watchlist data is available."
          onRetry={() => watchlist.refetch()}
        />
      ) : watchlist.data ? (
        <WatchlistSnapshotPanel data={watchlist.data} />
      ) : null}

      {/* Risk & Uncertainty + Quick Actions — side by side */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {market.data ? (
          <RiskUncertaintyPanel data={market.data} />
        ) : (
          <div />
        )}
        <QuickActionsPanel />
      </div>
    </div>
  );
}

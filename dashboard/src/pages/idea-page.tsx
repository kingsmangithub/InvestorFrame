import { useMemo } from "react";
import { Link, useParams } from "react-router-dom";
import { IdeaDetailCard } from "@/components/idea/idea-detail-card";
import { PageHeader } from "@/components/shared/page-header";
import { StatusCard } from "@/components/shared/status-card";
import { Card, CardContent } from "@/components/ui/card";
import { useStaticResource } from "@/hooks/use-static-resource";
import { loadIdeas } from "@/lib/static-data";

export function IdeaPage() {
  const { ticker } = useParams();
  const ideasState = useStaticResource(loadIdeas);

  const idea = useMemo(
    () => ideasState.data?.find((item) => item.ticker.toLowerCase() === ticker?.toLowerCase()),
    [ideasState.data, ticker],
  );

  if (ideasState.isLoading) return <StatusCard message="Loading idea card..." />;
  if (ideasState.error) return <StatusCard message={ideasState.error} />;

  if (!idea) {
    return (
      <Card>
        <CardContent className="pt-5 text-sm text-muted-foreground">
          No idea found for this ticker. Return to the <Link to="/desk" className="underline">desk</Link>.
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title={`${idea.ticker} idea card`}
        subtitle="A written thesis is the minimum entry ticket for real capital."
      />
      <IdeaDetailCard idea={idea} />
    </div>
  );
}

import { Link, useParams } from "react-router-dom";
import { PageHeader } from "@/components/shared/page-header";
import { IdeaDetailCard } from "@/components/idea/idea-detail-card";
import { Card, CardContent } from "@/components/ui/card";
import { getIdeaByTicker } from "@/content/demo-data";

export function IdeaPage() {
  const { ticker } = useParams();
  const idea = getIdeaByTicker(ticker);

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

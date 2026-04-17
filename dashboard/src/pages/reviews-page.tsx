import { ReviewLogCard } from "@/components/review/review-log-card";
import { PageHeader } from "@/components/shared/page-header";
import { StatusCard } from "@/components/shared/status-card";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useStaticResource } from "@/hooks/use-static-resource";
import { loadReviews, loadWisdom } from "@/lib/static-data";

export function ReviewsPage() {
  const reviewsState = useStaticResource(loadReviews);
  const wisdomState = useStaticResource(loadWisdom);
  const isLoading = reviewsState.isLoading || wisdomState.isLoading;
  const error = reviewsState.error ?? wisdomState.error;

  if (isLoading) return <StatusCard message="Loading review history..." />;
  if (error || !reviewsState.data || !wisdomState.data) {
    return <StatusCard message={error ?? "Review history is unavailable."} />;
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Reviews"
        subtitle="Review the quality of your thinking and behavior, not just the result on the screen."
      />
      <ReviewLogCard items={reviewsState.data} />
      <Card>
        <CardHeader>
          <CardTitle>Wisdom patterns</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-6 md:grid-cols-2">
          <div>
            <div className="text-xs uppercase tracking-wide text-muted-foreground">Mistake patterns</div>
            <ul className="mt-2 space-y-2 text-sm text-muted-foreground list-disc pl-5">
              {wisdomState.data.mistake_patterns.map((item) => <li key={item}>{item}</li>)}
            </ul>
          </div>
          <div>
            <div className="text-xs uppercase tracking-wide text-muted-foreground">Good patterns</div>
            <ul className="mt-2 space-y-2 text-sm text-muted-foreground list-disc pl-5">
              {wisdomState.data.good_patterns.map((item) => <li key={item}>{item}</li>)}
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

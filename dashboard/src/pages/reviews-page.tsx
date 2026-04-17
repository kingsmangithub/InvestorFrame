import { PageHeader } from "@/components/shared/page-header";
import { ReviewLogCard } from "@/components/review/review-log-card";
import { reviews } from "@/content/demo-data";

export function ReviewsPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Reviews"
        subtitle="Review the quality of your thinking and behavior, not just the result on the screen."
      />
      <ReviewLogCard items={reviews} />
    </div>
  );
}

import { useMemo } from "react";
import { FrameSummaryCard } from "@/components/frame/frame-summary-card";
import { IdeaListCard } from "@/components/idea/idea-list-card";
import { PageHeader } from "@/components/shared/page-header";
import { StatusCard } from "@/components/shared/status-card";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useStaticResource } from "@/hooks/use-static-resource";
import { loadBehavior, loadFrame, loadIdeas } from "@/lib/static-data";

export function DeskPage() {
  const frameState = useStaticResource(loadFrame);
  const ideasState = useStaticResource(loadIdeas);
  const behaviorState = useStaticResource(loadBehavior);

  const isLoading = frameState.isLoading || ideasState.isLoading || behaviorState.isLoading;
  const error = frameState.error ?? ideasState.error ?? behaviorState.error;

  const behaviorChecks = useMemo(() => behaviorState.data?.checks ?? [], [behaviorState.data]);

  if (isLoading) return <StatusCard message="Loading static decision data..." />;
  if (error || !frameState.data || !ideasState.data || !behaviorState.data) {
    return <StatusCard message={error ?? "Static decision data is unavailable."} />;
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Decision desk"
        subtitle="One market frame, a handful of real ideas, and a visible set of constraints."
      />

      <div className="grid lg:grid-cols-5 gap-4">
        <div className="lg:col-span-2">
          <FrameSummaryCard data={frameState.data} />
        </div>
        <div className="lg:col-span-3">
          <IdeaListCard ideas={ideasState.data} />
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Questions for today</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm text-muted-foreground list-disc pl-5">
              {frameState.data.questions.map((question) => (
                <li key={question}>{question}</li>
              ))}
            </ul>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Behavior gate</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm text-muted-foreground list-disc pl-5">
              {behaviorChecks.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

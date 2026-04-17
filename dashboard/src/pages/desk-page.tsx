import { PageHeader } from "@/components/shared/page-header";
import { FrameSummaryCard } from "@/components/frame/frame-summary-card";
import { IdeaListCard } from "@/components/idea/idea-list-card";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { frameData, ideas, rulebook } from "@/content/demo-data";

export function DeskPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Decision desk"
        subtitle="One market frame, a handful of real ideas, and a visible set of constraints."
      />

      <div className="grid lg:grid-cols-5 gap-4">
        <div className="lg:col-span-2">
          <FrameSummaryCard data={frameData} />
        </div>
        <div className="lg:col-span-3">
          <IdeaListCard ideas={ideas} />
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Questions for today</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm text-muted-foreground list-disc pl-5">
              {frameData.questions.map((question) => (
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
              {rulebook.behaviorGate.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

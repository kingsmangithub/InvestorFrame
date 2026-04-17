import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { ReviewData } from "@/lib/types";

export function ReviewLogCard({ items }: { items: ReviewData[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Review log</CardTitle>
        <CardDescription>Review decision quality, not just outcomes.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {items.map((item) => (
          <div key={`${item.date}-${item.ticker}`} className="rounded-xl border p-4 space-y-2">
            <div className="flex items-start justify-between gap-4">
              <div className="font-semibold">{item.ticker}</div>
              <div className="text-xs uppercase tracking-wide text-muted-foreground">{item.result}</div>
            </div>
            <div className="text-xs text-muted-foreground">{item.date}</div>
            <div className="grid sm:grid-cols-3 gap-2 text-sm">
              <div>Thesis quality: {item.thesis_quality}/10</div>
              <div>Process quality: {item.process_quality}/10</div>
              <div>Emotional discipline: {item.emotional_discipline}/10</div>
            </div>
            <p className="text-sm text-muted-foreground">{item.lesson}</p>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

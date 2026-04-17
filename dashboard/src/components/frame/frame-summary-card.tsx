import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { FrameData } from "@/lib/types";

export function FrameSummaryCard({ data }: { data: FrameData }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Current frame</CardTitle>
        <CardDescription>{data.date}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4 text-sm">
        <div>
          <div className="text-xs uppercase tracking-wide text-muted-foreground">Regime</div>
          <div className="mt-1 text-lg font-semibold">{data.frame.label}</div>
        </div>
        <div>
          <div className="text-xs uppercase tracking-wide text-muted-foreground">Confidence</div>
          <div className="mt-1">{Math.round(data.frame.confidence * 100)}%</div>
        </div>
        <div>
          <div className="text-xs uppercase tracking-wide text-muted-foreground">Dominant pressure</div>
          <p className="mt-1 text-muted-foreground">{data.frame.dominant_pressure}</p>
        </div>
        <div>
          <div className="text-xs uppercase tracking-wide text-muted-foreground">Caution</div>
          <p className="mt-1 text-muted-foreground">{data.frame.caution}</p>
        </div>
        <div>
          <div className="text-xs uppercase tracking-wide text-muted-foreground">Action bias</div>
          <p className="mt-1 text-muted-foreground">{data.frame.action_bias}</p>
        </div>
      </CardContent>
    </Card>
  );
}

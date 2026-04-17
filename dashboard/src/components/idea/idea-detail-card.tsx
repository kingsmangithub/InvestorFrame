import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { IdeaData } from "@/content/demo-data";

function BulletSection({ title, items }: { title: string; items: string[] }) {
  return (
    <div>
      <div className="text-xs uppercase tracking-wide text-muted-foreground">{title}</div>
      <ul className="mt-2 space-y-2 text-sm text-muted-foreground list-disc pl-5">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export function IdeaDetailCard({ idea }: { idea: IdeaData }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{idea.ticker} · {idea.company}</CardTitle>
        <CardDescription>Action now: {idea.action}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <div className="text-xs uppercase tracking-wide text-muted-foreground">Business summary</div>
          <p className="mt-2 text-sm text-muted-foreground">{idea.business_summary}</p>
        </div>
        <BulletSection title="Bull case" items={idea.bull_case} />
        <BulletSection title="Bear case" items={idea.bear_case} />
        <BulletSection title="Assumptions" items={idea.assumptions} />
        <BulletSection title="Invalidation" items={idea.invalidation} />
        <BulletSection title="Buy conditions" items={idea.buy_conditions} />
        <BulletSection title="Sell conditions" items={idea.sell_conditions} />
      </CardContent>
    </Card>
  );
}

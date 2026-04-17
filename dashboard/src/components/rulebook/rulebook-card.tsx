import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { RulebookData } from "@/lib/types";

function RuleSection({ title, items }: { title: string; items: string[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2 text-sm text-muted-foreground list-disc pl-5">
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}

export function RulebookCard({ rulebook }: { rulebook: RulebookData }) {
  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>Investment constitution</CardTitle>
          <CardDescription>A small set of rules should survive emotional swings.</CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2 text-sm text-muted-foreground list-disc pl-5">
            {rulebook.principles.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </CardContent>
      </Card>
      <RuleSection title="Behavior gate" items={rulebook.behavior_gate} />
      <RuleSection title="Sell discipline" items={rulebook.sell_rules} />
      <Card>
        <CardHeader>
          <CardTitle>Wisdom vault</CardTitle>
          <CardDescription>Patterns worth remembering.</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-6 md:grid-cols-2">
          <div>
            <div className="text-xs uppercase tracking-wide text-muted-foreground">Mistake patterns</div>
            <ul className="mt-2 space-y-2 text-sm text-muted-foreground list-disc pl-5">
              {rulebook.wisdom.mistake_patterns.map((item) => <li key={item}>{item}</li>)}
            </ul>
          </div>
          <div>
            <div className="text-xs uppercase tracking-wide text-muted-foreground">Good patterns</div>
            <ul className="mt-2 space-y-2 text-sm text-muted-foreground list-disc pl-5">
              {rulebook.wisdom.good_patterns.map((item) => <li key={item}>{item}</li>)}
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

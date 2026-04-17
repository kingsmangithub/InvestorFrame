import { Link } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { IdeaData } from "@/content/demo-data";

export function IdeaListCard({ ideas }: { ideas: IdeaData[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Active ideas</CardTitle>
        <CardDescription>Only a few ideas deserve deep attention.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {ideas.map((idea) => (
          <Link
            key={idea.ticker}
            to={`/ideas/${idea.ticker}`}
            className="block rounded-xl border p-4 hover:bg-secondary/40 transition-colors"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="font-semibold">{idea.ticker} · {idea.company}</div>
                <p className="mt-1 text-sm text-muted-foreground">{idea.business_summary}</p>
              </div>
              <div className="text-xs uppercase tracking-wide text-muted-foreground">{idea.action}</div>
            </div>
          </Link>
        ))}
      </CardContent>
    </Card>
  );
}

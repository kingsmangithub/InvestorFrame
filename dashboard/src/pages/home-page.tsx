import { Link } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export function HomePage() {
  return (
    <div className="min-h-screen px-4 sm:px-6 py-16 max-w-5xl mx-auto space-y-10">
      <div className="space-y-4 max-w-3xl">
        <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">InvestorFrame Lean</div>
        <h1 className="text-4xl sm:text-5xl font-bold tracking-tight">
          A calmer operating system for investment decisions.
        </h1>
        <p className="text-base sm:text-lg text-muted-foreground max-w-2xl">
          Frame the market simply, write a real thesis, block impulsive actions, review decision quality,
          and compound personal investing wisdom over time.
        </p>
        <div className="flex flex-wrap gap-3">
          <Link to="/desk"><Button size="lg">Open the desk</Button></Link>
          <Link to="/rulebook"><Button variant="outline" size="lg">Read the rulebook</Button></Link>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-4">
        {[
          ["Frame", "Start with the world, but keep the interpretation simple."],
          ["Idea", "Write the thesis before touching capital."],
          ["Review", "Learn from decision quality, not just P&L."],
        ].map(([title, body]) => (
          <Card key={title}>
            <CardHeader>
              <CardTitle>{title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">{body}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>What was removed on purpose</CardTitle>
          <CardDescription>This version prefers clarity over cleverness.</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-2 sm:grid-cols-2 text-sm text-muted-foreground">
          <div>• no live API</div>
          <div>• no scenario lab</div>
          <div>• no report generator</div>
          <div>• no sentiment layer</div>
          <div>• no watchlist scorer</div>
          <div>• no always-on backend</div>
        </CardContent>
      </Card>
    </div>
  );
}

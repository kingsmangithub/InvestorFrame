import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { FlaskConical, FileText, MessageCircleQuestion } from "lucide-react";

const ACTIONS = [
  {
    label: "Run Scenario",
    description: "Stress-test the current frame against a hypothetical shock.",
    icon: FlaskConical,
    to: "/scenario",
    disabled: false,
  },
  {
    label: "View Daily Report",
    description: "Full daily summary with sector and watchlist detail.",
    icon: FileText,
    to: "#",
    disabled: true,
  },
  {
    label: "Ask Why",
    description: "Query the system for reasoning behind any assessment.",
    icon: MessageCircleQuestion,
    to: "#",
    disabled: true,
  },
] as const;

export function QuickActionsPanel() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Quick Actions</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {ACTIONS.map((action) => {
          const Icon = action.icon;

          return (
            <div key={action.label}>
              {action.disabled ? (
                <Button
                  variant="outline"
                  className="w-full justify-start gap-3 h-auto py-3"
                  disabled
                >
                  <Icon className="h-4 w-4 flex-shrink-0" />
                  <span className="text-sm font-medium">{action.label}</span>
                </Button>
              ) : (
                <Link to={action.to} className="block">
                  <Button
                    variant="outline"
                    className="w-full justify-start gap-3 h-auto py-3"
                  >
                    <Icon className="h-4 w-4 flex-shrink-0" />
                    <span className="text-sm font-medium">{action.label}</span>
                  </Button>
                </Link>
              )}
              <p className="text-xs text-muted-foreground mt-1 ml-[calc(1rem+0.75rem+1rem)]">
                {action.description}
              </p>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}

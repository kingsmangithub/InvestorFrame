import { Inbox } from "lucide-react";

interface EmptyStateProps {
  title?: string;
  message?: string;
}

export function EmptyState({
  title = "No data available",
  message = "Try refreshing the page or changing the selected parameters.",
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-10 text-center">
      <Inbox className="h-8 w-8 text-muted-foreground mb-3" />
      <h3 className="text-sm font-semibold">{title}</h3>
      <p className="text-xs text-muted-foreground mt-1 max-w-sm">{message}</p>
    </div>
  );
}

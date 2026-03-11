import { cn } from "@/lib/utils";

interface MetricCardProps {
  label: string;
  value: string;
  detail?: string;
  className?: string;
}

export function MetricCard({ label, value, detail, className }: MetricCardProps) {
  return (
    <div className={cn("flex-shrink-0 rounded-lg border bg-card p-3 min-w-[140px]", className)}>
      <div className="text-xs text-muted-foreground font-medium">{label}</div>
      <div className="text-sm font-semibold mt-1">{value}</div>
      {detail && <div className="text-xs text-muted-foreground mt-1 line-clamp-2">{detail}</div>}
    </div>
  );
}

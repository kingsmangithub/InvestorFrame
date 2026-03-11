import { cn } from "@/lib/utils";

interface ConfidenceBarProps {
  value: number; // 0 to 1
  label?: string;
  className?: string;
}

export function ConfidenceBar({ value, label = "Confidence", className }: ConfidenceBarProps) {
  const percentage = Math.round(value * 100);
  const barColor =
    value >= 0.7 ? "bg-emerald-500" :
    value >= 0.5 ? "bg-amber-500" :
    "bg-rose-500";

  return (
    <div className={cn("space-y-1", className)}>
      <div className="flex items-center justify-between text-xs">
        <span className="text-muted-foreground">{label}</span>
        <span className="font-medium tabular-nums">{percentage}%</span>
      </div>
      <div className="h-1.5 w-full rounded-full bg-muted">
        <div
          className={cn("h-full rounded-full transition-all", barColor)}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

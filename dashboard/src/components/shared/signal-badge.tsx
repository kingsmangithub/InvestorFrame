import { Badge } from "@/components/ui/badge";
import { SIGNAL_CONFIG } from "@/lib/constants";
import { cn } from "@/lib/utils";

interface SignalBadgeProps {
  label: string;
}

export function SignalBadge({ label }: SignalBadgeProps) {
  const config = SIGNAL_CONFIG[label as keyof typeof SIGNAL_CONFIG] ?? {
    label,
    color: "bg-slate-500/15 text-slate-400",
  };

  return (
    <Badge className={cn(config.color, "text-xs font-medium")}>
      {config.label}
    </Badge>
  );
}

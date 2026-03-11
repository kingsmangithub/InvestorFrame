import { Badge } from "@/components/ui/badge";
import { REGIME_CONFIG } from "@/lib/constants";
import { cn } from "@/lib/utils";

interface RegimeBadgeProps {
  regime: string;
  size?: "sm" | "md" | "lg";
}

export function RegimeBadge({ regime, size = "md" }: RegimeBadgeProps) {
  const config = REGIME_CONFIG[regime as keyof typeof REGIME_CONFIG] ?? {
    label: regime,
    color: "bg-slate-500/15 text-slate-400 border-slate-500/30",
  };

  return (
    <Badge
      variant="outline"
      className={cn(
        config.color,
        size === "sm" && "text-xs px-2 py-0.5",
        size === "md" && "text-sm px-3 py-1",
        size === "lg" && "text-base px-4 py-1.5 font-semibold",
      )}
    >
      {config.label}
    </Badge>
  );
}

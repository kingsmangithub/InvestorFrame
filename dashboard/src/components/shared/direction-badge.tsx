import { DIRECTION_CONFIG } from "@/lib/constants";
import { cn } from "@/lib/utils";

interface DirectionBadgeProps {
  direction: string;
}

export function DirectionBadge({ direction }: DirectionBadgeProps) {
  const config = DIRECTION_CONFIG[direction as keyof typeof DIRECTION_CONFIG] ?? {
    label: direction,
    color: "text-slate-400",
    arrow: "·",
  };

  return (
    <span className={cn("inline-flex items-center gap-1 text-xs font-medium", config.color)}>
      <span>{config.arrow}</span>
      <span>{config.label}</span>
    </span>
  );
}

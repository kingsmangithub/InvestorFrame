import { SENTIMENT_CONFIG } from "@/lib/constants";
import { cn } from "@/lib/utils";

interface SentimentGaugeProps {
  score: number;
  label: string;
}

export function SentimentGauge({ score, label }: SentimentGaugeProps) {
  const config = SENTIMENT_CONFIG[label as keyof typeof SENTIMENT_CONFIG] ?? {
    label,
    color: "text-slate-400",
  };

  return (
    <div className="flex items-center gap-3">
      <div className="text-center">
        <div className={cn("text-3xl font-bold tabular-nums", config.color)}>
          {score.toFixed(1)}
        </div>
        <div className="text-xs text-muted-foreground mt-0.5">Sentiment Score</div>
      </div>
      <div className={cn("text-sm font-medium", config.color)}>
        {config.label}
      </div>
    </div>
  );
}

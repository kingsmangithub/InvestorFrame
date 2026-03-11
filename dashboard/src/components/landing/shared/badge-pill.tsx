import { cn } from "@/lib/utils";

interface BadgePillProps {
  children: React.ReactNode;
  className?: string;
}

export function BadgePill({ children, className }: BadgePillProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-3 py-1 text-xs font-medium",
        "bg-[#1A2540] border border-[#24314F] text-[#B7C2D9]",
        className,
      )}
    >
      {children}
    </span>
  );
}

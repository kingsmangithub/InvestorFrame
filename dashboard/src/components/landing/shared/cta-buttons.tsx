import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

interface CtaButtonsProps {
  className?: string;
  size?: "default" | "lg";
}

export function CtaButtons({ className, size = "default" }: CtaButtonsProps) {
  const isLg = size === "lg";

  return (
    <div className={cn("flex flex-wrap items-center gap-3", className)}>
      <Link
        to="/dashboard"
        className={cn(
          "inline-flex items-center justify-center rounded-md font-medium transition-colors",
          "bg-[#3ECF8E] text-[#0B1020] hover:bg-[#36b87d]",
          isLg ? "h-11 px-6 text-base" : "h-9 px-4 text-sm",
        )}
      >
        Explore the Demo
      </Link>

      <a
        href="#"
        className={cn(
          "inline-flex items-center justify-center rounded-md font-medium transition-colors",
          "border border-[#24314F] bg-transparent text-foreground hover:bg-[#151E32]",
          isLg ? "h-11 px-6 text-base" : "h-9 px-4 text-sm",
        )}
      >
        View on GitHub
      </a>

      <a
        href="#"
        className={cn(
          "inline-flex items-center justify-center rounded-md font-medium transition-colors",
          "text-muted-foreground hover:text-foreground",
          isLg ? "h-11 px-6 text-base" : "h-9 px-4 text-sm",
        )}
      >
        Read the Docs
      </a>
    </div>
  );
}

import { cn } from "@/lib/utils";

interface SectionWrapperProps {
  id?: string;
  children: React.ReactNode;
  className?: string;
}

export function SectionWrapper({ id, children, className }: SectionWrapperProps) {
  return (
    <section id={id} className={cn("max-w-6xl mx-auto px-6 py-16 md:py-20", className)}>
      {children}
    </section>
  );
}

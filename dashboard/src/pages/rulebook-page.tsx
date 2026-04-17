import { PageHeader } from "@/components/shared/page-header";
import { RulebookCard } from "@/components/rulebook/rulebook-card";

export function RulebookPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Rulebook"
        subtitle="Small rules are how principles survive when emotions rise."
      />
      <RulebookCard />
    </div>
  );
}

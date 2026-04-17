import { PageHeader } from "@/components/shared/page-header";
import { StatusCard } from "@/components/shared/status-card";
import { RulebookCard } from "@/components/rulebook/rulebook-card";
import { useStaticResource } from "@/hooks/use-static-resource";
import { loadRulebook } from "@/lib/static-data";

export function RulebookPage() {
  const rulebookState = useStaticResource(loadRulebook);

  if (rulebookState.isLoading) return <StatusCard message="Loading rulebook..." />;
  if (rulebookState.error || !rulebookState.data) {
    return <StatusCard message={rulebookState.error ?? "Rulebook is unavailable."} />;
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Rulebook"
        subtitle="Small rules are how principles survive when emotions rise."
      />
      <RulebookCard rulebook={rulebookState.data} />
    </div>
  );
}
